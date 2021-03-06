# 使用 PPA 安装

```shell
sudo apt install software-properties-common
#sudo apt-get install python-software-properties
# 添加 PHP 软件源
sudo add-apt-repository ppa:ondrej/php
#sudo add-apt-repository ppa:ondrej/php-zts

# 更新软件源信息
sudo apt-get update
# 卸载老版本 PHP
sudo apt-get purge php5-fpm
sudo apt-get install php7.1-cli php7.1-dev php7.1-dev php7.1-curl php7.1-pgsql php7.1-mcrypt
```

```shell
# 开启模块
sudo phpenmod xxx

# 关闭模块
sudo phpdismod xxx
```

# 使用源码编译安装 PHP7

```shell
# sudo apt-get install libpcre3 libpcre3-dev
# sudo apt-get install libxml2-dev
# sudo apt-get install libicu-dev
# sudo apt-get install libmcrypt-dev
# sudo apt-get install libpostgresql-ocaml-dev
# wget http://launchpadlibrarian.net/140087283/libbison-dev_2.7.1.dfsg-1_amd64.deb
# wget http://launchpadlibrarian.net/140087282/bison_2.7.1.dfsg-1_amd64.deb
# dpkg -i libbison-dev_2.7.1.dfsg-1_amd64.deb
# dpkg -i bison_2.7.1.dfsg-1_amd64.deb

./buildconf --force

./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --with-fpm-user=www-data --with-fpm-group=www-data --with-pdo-pgsql --with-pdo-mysql --with-pdo-sqlite  --with-iconv-dir --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib --with-libxml-dir=/usr --enable-xml --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --with-curl --enable-mbregex --enable-mbstring --with-mcrypt --enable-ftp --with-gd --enable-gd-native-ttf --with-openssl --with-mhash --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --disable-fileinfo --enable-maintainer-zts --enable-phpdbg-debug --enable-debug

# 简易配置
./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --with-pdo-pgsql --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --with-curl --enable-mbregex --enable-mbstring --with-mcrypt --with-mhash --without-pear --with-gettext --disable-fileinfo --enable-maintainer-zts --enable-phpdbg-debug --enable-debug

# PHP 5.6 配置
./configure --prefix=/usr --with-config-file-path=/etc/php5/fpm --enable-fpm --with-fpm-user=www-data --with-fpm-group=www-data --with-config-file-scan-dir=/etc/php5/fpm/conf.d --sysconfdir=/etc --localstatedir=/var --mandir=/usr/share/man --disable-debug --with-regex=php --disable-rpath --disable-static --with-pic --with-layout=GNU --with-pear=/usr/share/php --enable-calendar --enable-sysvsem --enable-sysvshm --enable-sysvmsg --enable-bcmath --with-bz2 --enable-ctype --with-iconv --enable-exif --enable-ftp --with-gettext --enable-mbstring --enable-shmop --enable-sockets --enable-wddx --with-libxml-dir=/usr --with-zlib --with-openssl --enable-soap --enable-zip --with-mhash=yes --with-mysql-sock=/var/run/mysqld/mysqld.sock --without-mm --with-curl=shared,/usr --with-zlib-dir=/usr --with-gd=shared --enable-gd-native-ttf --with-kerberos=/usr --with-imap-ssl --with-jpeg-dir=shared,/usr --with-xpm-dir=shared,/usr/X11R6 --with-png-dir=shared,/usr --with-freetype-dir=shared,/usr --with-imap=shared,/usr --enable-intl=shared --with-mcrypt=shared,/usr --with-mysql=shared,/usr --with-mysqli=shared,/usr/bin/mysql_config --with-pgsql=shared,/usr --with-pdo-pgsql  --with-pdo-mysql --with-pdo-sqlite

make -j4

sudo make install
```

# Fedora/RHEL/CentOS

## Fedora 23

```shell
wget http://rpms.remirepo.net/fedora/remi-release-23.rpm
dnf install remi-release-23.rpm
dnf config-manager --set-enabled remi-php70
yum install php70
# or
yum update
```

## RHEL version 7.2

```shell
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
wget http://rpms.remirepo.net/enterprise/remi-release-7.rpm
rpm -Uvh remi-release-7.rpm epel-release-latest-7.noarch.rpm
subscription-manager repos --enable=rhel-7-server-optional-rpms
yum-config-manager --enable remi-php70
yum install php70
# or
yum update
```

## RHEL version 6.7

```shell
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
wget http://rpms.remirepo.net/enterprise/remi-release-6.rpm
rpm -Uvh remi-release-6.rpm epel-release-latest-6.noarch.rpm
rhn-channel --add --channel=rhel-$(uname -i)-server-optional-6
yum install php70
# or
yum update
```

## CentOS version 7.2

```shell
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
wget http://rpms.remirepo.net/enterprise/remi-release-7.rpm
rpm -Uvh remi-release-7.rpm epel-release-latest-7.noarch.rpm
yum-config-manager --enable remi-php70
yum install php70
# or
yum update
```

## CentOS version 6.7

```shell
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
wget http://rpms.remirepo.net/enterprise/remi-release-6.rpm
rpm -Uvh remi-release-6.rpm epel-release-latest-6.noarch.rpm
yum-config-manager --enable remi-php70
yum install php70
# or
yum update
```

## 安装扩展

```shell
phpize
./configure
make && sudo make install

# 如果是源码编译安装的，带上安装路径
/usr/local/php/bin/phpize
./configure CFLAGS="-g3 -O0 -std=gnu90 -Wall -Werror -Wno-error=uninitialized" --with-php-config=/usr/local/php/bin/php-config
make && sudo make install
```

## apache
```conf
LoadModule php7_module modules/libphp7.so

<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

<FilesMatch "\.ph(p[2-7]?|tml)$">
    SetHandler application/x-httpd-php
</FilesMatch>

<FilesMatch "\.phps$">
    SetHandler application/x-httpd-php-source
</FilesMatch>

RewriteEngine On
RewriteRule (.*\.php)s$ $1 [H=application/x-httpd-php-source]
```

# 解压文件乱码
------------

在 Ubuntu 下，当PHP的执行用户为 www-data 时，调用 shell 命令进行解压时，有可能乱码，因为 www-data 用户语言环境没有设置。正确的方法如下：
```shell
putenv('LANG=en_US.UTF-8');
exec('7za x test.7z -r -y -o ./test');
# or
exec('LANG=en_US.UTF-8 7za x test.7z -r -y -o ./test');
```

Valgrind 内存泄漏检查

```shell
export USE_ZEND_ALLOC=0 # setenv USE_ZEND_ALLOC 0
export ZEND_DONT_UNLOAD_MODULES=1

valgrind --tool=memcheck --num-callers=30 --log-file=memcache.log /usr/local/php/bin/php test.php
# or
valgrind --leak-check=full /usr/local/php/bin/php test.php
 ```


# 覆盖安装

查看原有 PHP 配置的信息
```shell
php-config
```

```shell
./configure --prefix=/usr --with-apxs2=/usr/bin/apxs2 --with-config-file-path=/etc/php5/apache2 --with-config-file-scan-dir=/etc/php5/apache2/conf.d --build=x86_64-linux-gnu --host=x86_64-linux-gnu --sysconfdir=/etc --localstatedir=/var --mandir=/usr/share/man --disable-debug --with-regex=php --disable-rpath --disable-static --with-pic --with-layout=GNU --without-pear --enable-calendar --enable-sysvsem --enable-sysvshm --enable-sysvmsg --enable-bcmath --with-bz2 --enable-ctype --with-db4 --with-qdbm=/usr --without-gdbm --with-iconv --enable-exif --enable-ftp --with-gettext --enable-mbstring --with-onig=/usr --with-pcre-regex=/usr --enable-shmop --enable-sockets --enable-wddx --with-libxml-dir=/usr --with-zlib --with-kerberos=/usr --with-openssl=/usr --enable-soap --enable-zip --with-mhash=yes --with-system-tzdata --with-mysql-sock=/var/run/mysqld/mysqld.sock --enable-dtrace --without-mm --with-curl=shared,/usr --with-enchant=shared,/usr --with-zlib-dir=/usr --with-gd=shared,/usr --enable-gd-native-ttf --with-gmp=shared,/usr --with-jpeg-dir=shared,/usr --with-xpm-dir=shared,/usr/X11R6 --with-png-dir=shared,/usr --with-freetype-dir=shared,/usr --with-vpx-dir=shared,/usr --with-imap=shared,/usr --with-imap-ssl --enable-intl=shared --without-t1lib --with-ldap=shared,/usr --with-ldap-sasl=/usr --with-mcrypt=shared,/usr --with-mysql=shared,/usr --with-mysqli=shared,/usr/bin/mysql_config --with-pspell=shared,/usr --with-unixODBC=shared,/usr --with-recode=shared,/usr --with-xsl=shared,/usr --with-snmp=shared,/usr --with-sqlite3=shared,/usr --with-mssql=shared,/usr --with-tidy=shared,/usr --with-xmlrpc=shared --with-pgsql=shared,/usr PGSQL_INCLUDE=/usr/include/postgresql --enable-pdo=shared --without-pdo-dblib --with-pdo-mysql=shared,/usr --with-pdo-odbc=shared,unixODBC,/usr --with-pdo-pgsql=shared,/usr/bin/pg_config --with-pdo-sqlite=shared,/usr --with-pdo-dblib=shared,/usr --with-interbase=shared,/usr --with-pdo-firebird=shared,/usr build_alias=x86_64-linux-gnu host_alias=x86_64-linux-gnu 


./configure --enable-fpm --prefix=/usr --with-config-file-path=/etc/php5/fpm --with-config-file-scan-dir=/etc/php5/fpm/conf.d --with-fpm-user=www-data --with-fpm-group=www-data --with-pdo-pgsql --with-pdo-mysql --with-pdo-sqlite  --with-iconv-dir --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib --with-libxml-dir=/usr --enable-xml --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --with-curl --enable-mbregex --enable-mbstring --with-mcrypt --enable-ftp --with-gd --enable-gd-native-ttf --with-openssl --with-mhash --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --disable-fileinfo --enable-maintainer-zts --enable-phpdbg-debug
--enable-debug

./configure --enable-fpm --prefix=/usr --with-config-file-path=/etc/php5/fpm --with-config-file-scan-dir=/etc/php5/fpm/conf.d --with-fpm-user=www-data --with-fpm-group=www-data  --build=x86_64-linux-gnu --host=x86_64-linux-gnu --sysconfdir=/etc --localstatedir=/var --mandir=/usr/share/man --disable-debug --with-regex=php --disable-rpath --disable-static --with-pic --with-layout=GNU --with-pear=/usr/share/php --without-gdbm --with-iconv --enable-exif --enable-ftp --with-gettext --enable-mbstring --with-pcre-regex=/usr --enable-shmop --enable-sockets --with-libxml-dir=/usr --with-zlib --enable-zip --without-mm --with-curl=shared,/usr --with-zlib-dir=/usr --enable-gd-native-ttf --with-jpeg-dir=shared,/usr --with-png-dir=shared,/usr --enable-intl=shared --without-t1lib --with-libdir=/lib/x86_64-linux-gnu --enable-maintainer-zts --enable-pdo --with-pdo-mysql --with-pdo-pgsql --with-pdo-sqlite --with-pgsql --disable-dom --disable-xml --without-pear --disable-simplexml


./configure --prefix=/usr --with-apxs2=/usr/bin/apxs2 --with-config-file-path=/etc/php5/apache2 --with-config-file-scan-dir=/etc/php5/apache2/conf.d --build=x86_64-linux-gnu --host=x86_64-linux-gnu --sysconfdir=/etc --localstatedir=/var --mandir=/usr/share/man --disable-debug --with-regex=php --disable-rpath --disable-static --with-pic --with-layout=GNU --with-pear=/usr/share/php --without-gdbm --with-iconv --enable-exif --enable-ftp --with-gettext --enable-mbstring --with-pcre-regex=/usr --enable-shmop --enable-sockets --with-libxml-dir=/usr --with-zlib --enable-zip --without-mm --with-curl=shared,/usr --with-zlib-dir=/usr --enable-gd-native-ttf --with-jpeg-dir=shared,/usr --with-png-dir=shared,/usr --enable-intl=shared --without-t1lib --with-libdir=/lib/x86_64-linux-gnu --enable-maintainer-zts --enable-pdo --with-pdo-mysql --with-pdo-pgsql --with-pdo-sqlite --with-pgsql --disable-dom --disable-xml --without-pear --disable-simplexml

sudo apt-get install apache2-prefork-dev

./configure --prefix=/usr --with-apxs2=/usr/bin/apxs2 --with-config-file-path=/etc/php5/apache2 --with-config-file-scan-dir=/etc/php5/apache2/conf.d  --sysconfdir=/etc --localstatedir=/var --mandir=/usr/share/man --disable-debug --with-regex=php --disable-rpath --disable-static --with-pic --with-layout=GNU --with-pear=/usr/share/php --without-gdbm --with-iconv --enable-exif --enable-ftp --with-gettext --enable-mbstring --enable-shmop --enable-sockets --with-zlib --enable-zip --without-mm --with-curl --enable-gd-native-ttf --with-jpeg-dir=shared,/usr --with-png-dir=shared,/usr --enable-intl=shared --enable-maintainer-zts --enable-pdo --with-pdo-mysql --with-pdo-pgsql --with-pdo-sqlite --with-pgsql --disable-dom --disable-xml --without-pear --disable-simplexml --disable-xmlreader
```


```shell
sudo apt-get purge php5-common -y
sudo apt-get --purge autoremove -y
```

## PHP CLI与CGI 和 PHP日志

PHP错误跟踪，错误提示有助于，定位错误的位置，从而进行调试。与错误显示有关的命令有如下：

1、直接显示
```conf
# 错误显示级别设置
error_reporting=ALL
# 是否显示错误
display_errors=On|Of
```

2、把错误存入日志文件里
```conf
# 开启日志显示
log_errors=On
# 错误日志存放地址
error_log=/var/log/php-error.log
```

## PHP FPM 多实例

```shell
cp /etc/init.d/php7.1-fpm /etc/init.d/php7.1-fpm2
```
修改为：
```conf
#!/bin/sh
### BEGIN INIT INFO
# Provides:          php7.1-fpm2
# Required-Start:    $remote_fs $network
# Required-Stop:     $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts php7.1-fpm
# Description:       Starts The PHP FastCGI Process Manager Daemon
### END INIT INFO

# Author: Ondrej Sury <ondrej@debian.org>

PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="PHP 7.1 FastCGI Process Manager"
NAME=php-fpm7.1
CONFFILE=/etc/php/7.1/fpm/php-fpm2.conf
DAEMON=/usr/sbin/$NAME
DAEMON_ARGS="--daemonize --fpm-config $CONFFILE"
CONF_PIDFILE=$(sed -n 's/^pid[ =]*//p' $CONFFILE)
PIDFILE=${CONF_PIDFILE:-/run/php/php7.1-fpm2.pid}
TIMEOUT=30
SCRIPTNAME=/etc/init.d/$NAME
```
加入 service：
```shell
sudo update-rc.d php7.1-fpm2 defaults
```
