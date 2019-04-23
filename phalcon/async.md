# async 源码剖析

## 模块初始化时 HOOK `zend_execute_ex`

```c
PHP_MINIT_FUNCTION(async)
{

	orig_execute_ex = zend_execute_ex;
	zend_execute_ex = async_execute_ex;

	return SUCCESS;
}
```

解释器引擎最终执行 `op` 的函数是 `zend_execute_ex`，它是一个函数指针，在引擎初始化（zend_startup）的时候默认指向了`execute_ex`,这个execute定义在`zend_vm_execute.h`。

>> 用户自定义的函数执行使用 `zend_execute_ex`，内部函数调用 zend_execute_internal

```c
ZEND_API void execute_ex(zend_execute_data *ex)
{
	LOAD_OPLINE();
	ZEND_VM_LOOP_INTERRUPT_CHECK();

	while (1) {
#if (ZEND_VM_KIND == ZEND_VM_KIND_HYBRID)
		HYBRID_SWITCH() {
#else
#if defined(ZEND_VM_FP_GLOBAL_REG) && defined(ZEND_VM_IP_GLOBAL_REG)
		((opcode_handler_t)OPLINE->handler)(ZEND_OPCODE_HANDLER_ARGS_PASSTHRU);
		if (UNEXPECTED(!OPLINE)) {
#else
		if (UNEXPECTED((ret = ((opcode_handler_t)OPLINE->handler)(ZEND_OPCODE_HANDLER_ARGS_PASSTHRU)) != 0)) {
#endif
#endif

	}
}
```

这里的 `handler` 每个`opcode`的`op`对应一个`handler`，比如`DO_FCALL`这个`opcode`对应的处理函数：
```c
ZEND_VM_HOT ZEND_OPCODE_HANDLER_RET ZEND_FASTCALL ZEND_DO_FCALL_SPEC_RETVAL_USED_HANDLER(ZEND_OPCODE_HANDLER_ARGS)
{
     ...
     if (EXPECTED(fbc->type == ZEND_USER_FUNCTION)) {
        zend_execute_ex(call);
     } else if (EXPECTED(fbc->type < ZEND_USER_FUNCTION)) {
          if (!zend_execute_internal) {
               fbc->internal_function.handler(call, ret);  // 执行这个 internal_function 所定义的handler函数，这个就是实际的调用方法了，命名为：zim_[class]_function_[function]
          } else {
               zend_execute_internal(call, ret);
          }

     } else { /* ZEND_OVERLOADED_FUNCTION */
          if (UNEXPECTED(!zend_do_fcall_overloaded(fbc, call, ret))) {
               HANDLE_EXCEPTION();
          }
     }

fcall_end:
     ZEND_VM_SET_OPCODE(opline + 1);
     ZEND_VM_CONTINUE(); // 下一条 op
}
```

## 请求时初始化上下文 `async_context_init` 和任务调度器 `async_task_scheduler_init`

```c
void async_context_init()
{
	async_context *context;
	
	context = async_context_object_create(NULL, NULL);
	
	context->output.context = context;
	context->output.handler = emalloc(sizeof(zend_output_globals));
	
	ASYNC_G(context) = context;
	ASYNC_G(foreground) = context;
	
	context = async_context_object_create(NULL, NULL);
	context->flags |= ASYNC_CONTEXT_FLAG_BACKGROUND;
	
	context->output.context = ASYNC_G(foreground);
	
	ASYNC_G(background) = context;
}

void async_task_scheduler_init()
{
	async_task_scheduler *scheduler;
	async_fiber *fiber;
	
	scheduler = async_task_scheduler_object_create();
	
	ASYNC_G(executor) = scheduler;
	ASYNC_G(scheduler) = scheduler;
	
	fiber = async_fiber_create_root();
	
	ASYNC_G(root) = fiber;
	ASYNC_G(fiber) = fiber;
}

PHP_RINIT_FUNCTION(async)
{
	async_context_init();
	async_task_scheduler_init();

	return SUCCESS;
}
```

## 请求结束时关闭

```c
void async_context_shutdown()
{
	async_context *context;

	context = ASYNC_G(foreground);
	
	if (context != NULL) {
		ASYNC_DELREF(&context->std);
	}
	
	context = ASYNC_G(background);

	if (context != NULL) {
		ASYNC_DELREF(&context->std);
	}
}

void async_task_scheduler_shutdown()
{
	async_task_scheduler *scheduler;

	scheduler = ASYNC_G(executor);
	
	if (scheduler != NULL && !ASYNC_G(exit)) {
		ASYNC_G(executor) = NULL;

		async_task_scheduler_dispose(scheduler);
		async_task_scheduler_unref(scheduler);
	}
	
	async_fiber_destroy(ASYNC_G(root));
}

PHP_RSHUTDOWN_FUNCTION(async)
{
	async_task_scheduler_shutdown();
	async_context_shutdown();
	
	return SUCCESS;
}
```

## 代码运行时执行 async_execute_ex & execute_root

上一次执行环境数据与当前任务为 NULL 调用 `execute_root` 启动异步任务调度器 `async_task_scheduler_run`。

```c
static void async_execute_ex(zend_execute_data *exec)
{
	if (UNEXPECTED(exec->prev_execute_data == NULL && ASYNC_G(task) == NULL)) {
		execute_root(exec);
	} else {
		orig_execute_ex(exec);
	}
}

static void execute_root(zend_execute_data *exec)
{
	zend_object *error;
	
	error = NULL;

	zend_try {
		orig_execute_ex(exec);
	} zend_catch {
		ASYNC_G(exit) = 1;
	} zend_end_try();
	
	error = EG(exception);
	
	if (UNEXPECTED(error != NULL)) {
		ASYNC_ADDREF(error);
		zend_clear_exception();
	}
	
	async_task_scheduler_run();
	
	EG(exception) = error;
}
```

## async_task_scheduler_run

当任务调度器不为 NULL 是执行 `async_task_scheduler_dispose` 安排任务。
```c
void async_task_scheduler_run()
{
	async_task_scheduler *scheduler;

	scheduler = ASYNC_G(executor);

	if (scheduler != NULL) {
		async_task_scheduler_dispose(scheduler);
	}
}
```

## async_task_scheduler_dispose

```c
void async_fiber_suspend(async_task_scheduler *scheduler)
{
	async_fiber *current;
	async_fiber *next;
	
	async_fiber_ucontext *from;
	async_fiber_ucontext *to;
	
	current = ASYNC_G(fiber); // async_task_scheduler_init
	
	ZEND_ASSERT(scheduler != NULL);
	ZEND_ASSERT(current != NULL);
	
	// 判断协程信息队列是否为空
	if (scheduler->fibers.first == NULL) {
		next = scheduler->runner; // 创建任务对象的时候的时候创建和初始化（async_task_scheduler_object_create & async_fiber_init）
	} else {
		ASYNC_LIST_EXTRACT_FIRST(&scheduler->fibers, next);
		// 去除标记 ASYNC_FIBER_FLAG_QUEUED
		next->flags &= ~ASYNC_FIBER_FLAG_QUEUED;
	}
	
	if (UNEXPECTED(current == next)) {
		return;
	}
	
	from = (async_fiber_ucontext *) current;
	to = (async_fiber_ucontext *) next;
	
	ZEND_ASSERT(next != NULL);
	ZEND_ASSERT(from->initialized);
	ZEND_ASSERT(to->initialized);
	
	// ASYNC_DEBUG_LOG("SUSPEND: %d -> %d\n", from->id, to->id);
	
	async_fiber_capture_state(current);	
	ASYNC_G(fiber) = next;
	
	ASYNC_CHECK_FATAL(-1 == swapcontext(&from->ctx, &to->ctx), "Failed to switch fiber context");
	
	async_fiber_restore_state(current);
}

static zend_always_inline void async_task_scheduler_run_loop(async_task_scheduler *scheduler)
{
	if (UNEXPECTED(ASYNC_G(exit))) {
		return;
	}

	ASYNC_CHECK_FATAL(scheduler->flags & ASYNC_TASK_SCHEDULER_FLAG_RUNNING, "Duplicate scheduler loop run detected");
	
	scheduler->caller = ASYNC_G(fiber);
	scheduler->flags |= ASYNC_TASK_SCHEDULER_FLAG_RUNNING;
	
	async_fiber_suspend(scheduler);
	
	scheduler->flags &= ~ASYNC_TASK_SCHEDULER_FLAG_RUNNING;
	scheduler->caller = NULL;
}

static void async_task_scheduler_dispose(async_task_scheduler *scheduler)
{
	async_cancel_cb *cancel;
	async_op *op;
	
	zval error;
	// 已经布置了直接返回
	if (UNEXPECTED(scheduler->flags & ASYNC_TASK_SCHEDULER_FLAG_DISPOSED || ASYNC_G(exit))) {
		return;
	}
	// execute_root &&run_task_fiber 无异常退出，则
	if (EXPECTED(!ASYNC_G(exit))) {
		async_task_scheduler_run_loop(scheduler);
	}

	scheduler->flags |= ASYNC_TASK_SCHEDULER_FLAG_DISPOSED;

	ASYNC_PREPARE_ERROR(&error, "Task scheduler has been disposed");
	
	do {
		if (scheduler->operations.first != NULL) {
			do {
				ASYNC_NEXT_OP(&scheduler->operations, op);
				ASYNC_FAIL_OP(op, &error);
			} while (scheduler->operations.first != NULL);
		}
	
		if (scheduler->shutdown.first != NULL) {
			do {
				ASYNC_LIST_EXTRACT_FIRST(&scheduler->shutdown, cancel);
	
				cancel->func(cancel->object, &error);
			} while (scheduler->shutdown.first != NULL);
		}
		
		async_task_scheduler_run_loop(scheduler);
		
		uv_walk(&scheduler->loop, dispose_walk_cb, scheduler);
		
		async_task_scheduler_run_loop(scheduler);
	} while (uv_loop_alive(&scheduler->loop));
	
	zval_ptr_dtor(&error);
}
```