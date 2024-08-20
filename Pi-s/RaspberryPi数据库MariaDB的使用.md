# RaspberryPi数据库MariaDB的使用

## 一、MariaDB的安装

[MariaDB 官网](https://mariadb.com)

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

## 四、远程访问

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

[Configuring MariaDB for Remote Client Access](https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/) 

[MariaDB/MySQL Remote Access Guides](https://webdock.io/en/docs/how-guides/database-guides/how-enable-remote-access-your-mariadbmysql-database?srsltid=AfmBOoqSs04WgcVQTVThhaxITU_FvOhODFNheQVPVS8EyXswsr3vd6DP)















