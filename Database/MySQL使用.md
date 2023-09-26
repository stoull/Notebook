# MySQL使用


## 安装

* 方法一 HomeBrew

* 方法二 MySQL官网下载：
[MySQL Community Downloads](https://dev.mysql.com/downloads/)

##### 如出现`zsh: command not found: mysql` 错误

>
在文件`~/.zsh_profile`（如没有则创建）,增加一行：`export PATH=$PATH:/usr/local/mysql/bin`
>
运行更新：`source ~/.zsh_profile`

* 方法三 Amazon Linux 2023安装：

1. 安装命令：

`sudo dnf update`
`wget https://dev.mysql.com/get/mysql80-community-release-el9-3.noarch.rpm`
`sudo dnf install mysql-community-server`

2. mysql 服务控制：

`sudo systemctl start mysqld`
`sudo systemctl enable mysqld`
`sudo systemctl status mysqld`

3. 设置密码：

查找初始密码：
`sudo grep 'temporary password' /var/log/mysqld.log`

设置密码, 需要使用初始密码：
`sudo mysql_secure_installation -p`


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