import numpy as np

A = np.arange(2,14).reshape((3,4))
print(A)
print(A.T)
print(np.transpose(A))

print(np.mean(A))
print(A.mean())
print(np.average(A))
print(np.argmin(A))
print(np.argmax(A))
print(np.median(A))
print(np.cumsum(A))
print(np.diff(A))
print(np.nonzero(A))
print('sort', np.sort(A))
print('sort reverse', A[::-1])
print((A.T).dot(A))
print(np.clip(A, 5, 9))
