# RaspberryPi数据库MariaDB的使用

## 一、MariaDB的安装

[mariadb.org](https://mariadb.org). [MariaDB 官网](https://mariadb.com)

### 1.保持系统最新状态:

`sudo apt update`
`sudo apt upgrade`

### 2.安装mariadb-server:

`sudo apt install mariadb-server`

### 3.初始化数据库设置:

`sudo mysql_secure_installation`

	建议设置如下:
	* Change the default root password (from no password) Y
	* Remove anonymous users
	* Disallow remote root login
	* Remove the test database
	* Reload the privilege tables

### 4.连接服务:

`mariadb -u root -p`

见下面的问题记录详见[六、问题记录](#六、问题记录)

### 5.Maria数据库的其它操作

重装,重装前注意备份数据:

`sudo apt reinstall mariadb-server`

如果数库为空的,只是想清空安装:

```
$ sudo apt purge mariadb-server
$ sudo rm -rf /var/lib/mysql/
$ sudo apt install mariadb-server
```

全部移除
`$ sudo apt-get purge mariadb-*`

Maria服务控制:

| Operation | Command | --- |
| --- | --- | --- |
| Start | sudo systemctl start mariadb |
| Stop | sudo systemctl stop mariadb |
| Restart | sudo systemctl restart mariadb |
| Enable during startup | sudo systemctl enable mariadb |
| Disable during startup | sudo systemctl disable mariadb |
| Status | sudo systemctl status mariadb |
| View systemd journal | sudo journalctl -u mariadb |

## 二、MariaDB的使用

数据库的文件一般存储于目录`/var/lib/mysql/`

在使用`mariadb -u root -p`后,就进入了MariaDB数据库, 可以使用数据库的指令了. 使用`control+d`或者使用`exit`指令退出MariaDB.

* `SELECT VERSION();` : 查看当前版本
* `SELECT USER();`
* `create database testdb;` : 创建库
* `use testdb;`: 使用库
* `create table users(name varchar(50), create_date date);`: 创建表
* `SHOW TABLES;` : 列出所有的表
* `DESC users;` : 查看表的详情
* `SHOW DATABASES;` : 列出所有的库
* `SHOW CREATE TABLE users \G` : 查看表更详细的信息
* `drop databse testdb;` : 删库

[Application Programming Interfaces](https://mariadb.com/kb/en/connectors/)

[Building a Portable Database Server](https://mariadb.com/resources/blog/building-a-portable-database-server/)

## 三、用户管理

### 创建用户

`CREATE USER 'username'@'hostname' IDENTIFIED BY 'password';`

`username`即为想要的用户名, `hostname`为用户所在的ip或主机名, `password` 为密码.

示例: 

`CREATE USER 'matthew'@'%' IDENTIFIED BY 'supersecretpassword';` 创建一个名为matthew,可以在任何地方连接上这个服务的用户.

### 权限管理

创建好用户之后,需要管理对应的用户的权限:

`GRANT priv_type ON priv_level TO 'username'@'hostname';`

> 
`priv_type`: 为权限类型, 如`SELECT`, `INSERT`, `UPDATE`, etc
`priv_level`: 为权限等级, 如特定的库或者表

示例:

`GRANT ALL PRIVILEGES ON * . * TO 'matthew'@'%';` 为给matthew所有的权限.

### `FLUSH PRIVILEGES;`

## 四、远程访问(如果需要)

MariaDB因为安全的原因, 默认是监听localhost, 及3306端口, 不允许远程访问. 如需要远程可按如下步骤检查配置信息:

* 1.确认MariaDB运行

	`ps -ef | grep -i mysql`, 输出应该如下:
	
	```
	$ ps -ef | grep -i mysql
mysql      22302       1  0 16:58 ?        00:00:00 /usr/sbin/mariadbd
pi         23894    2836  0 17:11 pts/0    00:00:00 grep --color=auto -i mysql
	```

* 2.查看MariaDB绑定的的ip及端口

	MariaDB因为安全的原因, 默认监听的是localhost, 及3306端口, 可以使用下面的命令查看监听的内容:

	```
	$ netstat -ant | grep 3306
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
	```

* 2.更改MariaDB绑定的的ip及端口

	在文件`/etc/mysql/my.cnf`或在`/etc/mysql/mariadb.conf.d/50-server.cnf`配置文件中找到`bind-address`字段,更改为:
	`bind-address = 0.0.0.0`

* 3.重启mariadb

	`sudo systemctl restart mariadb`
	
	这个时间查看监听的信息应该如下:
	
	```
	$ netstat -ant | grep 3306
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN
	```
* 4.检查防火墙,是否屏蔽了3306端口

* 5.命令行的远程连接和访问
	`mariadb -h 166.78.144.191 -u username -p database_name`
	-h: host, -P: port, -p: password一般留空,连接时输入才安全: 如
	`mariadb -h 43.138.214.x -u ubuntu -p test_db`

[Configuring MariaDB for Remote Client Access](https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/) 

[MariaDB/MySQL Remote Access Guides](https://webdock.io/en/docs/how-guides/database-guides/how-enable-remote-access-your-mariadbmysql-database?srsltid=AfmBOoqSs04WgcVQTVThhaxITU_FvOhODFNheQVPVS8EyXswsr3vd6DP)



## 五、Python中使用MariaDB



## 六、问题记录

* 报错误: `ERROR 1698 (28000): Access denied for user 'root'@'localhost'`

	参考解决方法1: [ERROR 1698 (28000): Access denied for user 'root'@'localhost'](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost)
	
	产生这个问题是因为在一些系统中,像Ubuntu Debain 使用的是[Unix auth_socket plugin](https://dev.mysql.com/doc/mysql-security-excerpt/5.5/en/socket-pluggable-authentication.html)系统授权, 如你当前使用的不是root用户登录系统,就不能授权登录数据库. 处理的方法有二种:

	* 设置root用户不使用系统授权系统登录数据库,而使用原生的`mysql_native_password`验证方式
	* 新增加与系统用户匹配的数据库用户进行访问(推荐)

	
	```
	sudo mysql -u root
	MariaDB [(none)]> USE mysql;
	.... Database changed
	MariaDB [mysql]> SELECT User, Host, plugin FROM mysql.user;
	+------+-----------+-------------+
	| User | Host      | plugin      |
	+------+-----------+-------------+
	| root | localhost | unix_socket |
	+------+-----------+-------------+
	1 row in set (0.000 sec)
	```
	可以看到root用户使用的是`unix_socket`进行用户授权验证.有的系统为`auth_socket`
	
	* 方法一

	```
	sudo mysql -u root # I had to use "sudo" since it was a new installation

	mysql> USE mysql;
	mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
	mysql> FLUSH PRIVILEGES;
	mysql> exit;
	
	sudo service mysql restart
	```
	
	
	* 方法二 (其中的`YOUR_SYSTEM_USER`要替换为当前登录的用户名,可使用`$whoami`查看)

	```
	sudo mysql -u root # I had to use "sudo" since it was a new installation

	mysql> USE mysql;
	mysql> CREATE USER 'YOUR_SYSTEM_USER'@'localhost' IDENTIFIED BY 'YOUR_PASSWD';
	mysql> GRANT ALL PRIVILEGES ON *.* TO 'YOUR_SYSTEM_USER'@'localhost';
	mysql> UPDATE user SET plugin='unix_socket' WHERE User='YOUR_SYSTEM_USER';
	mysql> FLUSH PRIVILEGES;
	mysql> exit;
	
	sudo service mysql restart
	```
	
* 报错误: `ERROR 1130 (HY000): Host 'x.x.x.x' is not allowed to connect to this MariaDB server`

	这个是通过远程连接数据库时出现的错误,原因是默认创建用户的时候只允许本地访问, 形如: 'root'@'localhost', `localhost`即只能本地访问.
	
	查看用户
	```
	$mysql -u root
	mysql> USE mysql;
	mysql> SELECT User, Host, plugin FROM mysql.user;
	```
	
	设置对应用户设置可连接的ip:
	
	* `GRANT ALL ON *.* to root@'123.123.123.123' IDENTIFIED BY 'put-your-password';`: 特定ip可以访问
	* `GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' WITH GRANT OPTION;` 所有ip可以访问
	* `GRANT ALL ON database_name.* to 'database_username'@'156.236.9.%' IDENTIFIED BY ‘database_password’;`: 156.236.9.*段ip可以访问

	如果需要多个ip,则运行多次:
	
	```
	mysql> GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'1.2.3.4' IDENTIFIED BY 'PASSWORD' WITH GRANT OPTION;
	mysql> GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'5.6.7.8' IDENTIFIED BY 'PASSWORD' WITH GRANT OPTION;
	```


[How to connect Python programs to MariaDB](https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/)

[Using SQLAlchemy with MariaDB Connector/Python: Part 1](https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/)

[Using SQLAlchemy with MariaDB Connector/Python: Part 2](https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-2/)

[dev-example-blog-samples](https://github.com/mariadb-corporation/dev-example-blog-samples/blob/main/mariadb_python_sqlalchemy/part_1/employees.py)









