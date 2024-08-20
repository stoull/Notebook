# MySQL使用


## 安装

### Mac
* 方法一 HomeBrew

* 方法二 MySQL官网下载：
[MySQL Community Downloads](https://dev.mysql.com/downloads/)

##### 如出现`zsh: command not found: mysql` 错误

>
在文件`~/.zsh_profile`（如没有则创建）,增加一行：`export PATH=$PATH:/usr/local/mysql/bin`
>
运行更新：`source ~/.zsh_profile`

### CentOS

##### Amazon Linux 2023上安装

* 1.安装命令：

`sudo dnf update`
`wget https://dev.mysql.com/get/mysql80-community-release-el9-3.noarch.rpm`
`sudo dnf install mysql-community-server`

* 2.mysql 服务控制：

* `sudo systemctl start mysqld`
* `sudo systemctl enable mysqld`
* `sudo systemctl status mysqld`

* 3.设置密码：

查找初始密码：
`sudo grep 'temporary password' /var/log/mysqld.log`

设置密码, 需要使用初始密码：
`sudo mysql_secure_installation -p`

### Debian

##### Raspberrypi 上安装

#### 1.保持系统最新状态:

`sudo apt update`
`sudo apt upgrade`

#### 2.安装mariadb-server:

`sudo apt install mariadb-server`

#### 3.初始化数据库设置:

`sudo mysql_secure_installation`

	建议设置如下:
	* Change the default root password (from no password) Y
	* Remove anonymous users
	* Disallow remote root login
	* Remove the test database
	* Reload the privilege tables

#### 4.连接服务:

`mariadb -u root -p`

#### 5.Maria数据库的其它操作

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

## mysql使用

登录：`mysql -u root -p` 密码不要写，不安全，见如下提示：

> mysql: [Warning] Using a password on the command line interface can be insecure.

```
If you haven’t set a password for your MySQL user you can omit the -p switch.
```

导入数据:
```mysql -u root -p 123456 < /Users/kevin/Documents/xxxxx.sql```

mysql -u root -p < /home/ec2-user/Documents/TestProjects/meal_ordering_system/deploy/apsfc_20150727_2133.sql



显示所有的database:`SHOW DATABASES;`

`SHOW SCHEMAS;`

切换database:`USE database_name;`

显示所有的表:`SHOW TABLES;`



[To Install Apache Maven and Java 8 on your EC2 instance](https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth-connect-prerq.html)

[How to Install MySQL on Amazon Linux 2023](https://muleif.medium.com/how-to-install-mysql-on-amazon-linux-2023-5d39afa5bf11)