# Linux用户组与权限管理实操



### 文件

#### 查看文件详情
```
ll /var/log/nginx/error.log
-rw-r--r--. 1 root root 7769 Oct 31 02:22 /var/log/nginx/error.log
```
|-rw-r--r--. |  1 |  root |  root |  7769 | Oct 31 02:22 | /var/log/nginx/error.log |
| --- | --- | --- | --- | --- | --- | --- |
| 类型及权限 | 连结数 | 所属用户| 所属用户组 | 文档大小 | 最后修改时间 | 文档名称 |

###  用户

* `whoami`: 列出当前的用户名uername
* `cat /etc/passwd`: 查看所有用户
* `passwd username`: 修改用户密码

#### su 和 sudo 用户切换及权限提升

* `su username`: 切换用户, 在不登出当前用户的情况下登录为另外一个用户
*  `su` 和 `su -`(即 su -l --login)，都为切换到 root用户。`su`：保持原用户环境，`su -`：创建一个新的环境（由 root 用户 ~/.bashrc 文件所设置的环境），相当于使用 root 用户正常登录。
	- `su`可用于登录目标用户以便重现以及调试问题。
* sudo 命令需要输入当前用户的密码，su 命令需要输入 root 用户的密码。
* sudo 命令只允许使用提升的权限运行单个命令，而 su 命令会启动一个新的 shell，同时允许使用 root 权限运行尽可能多的命令，直到明确退出登录。
* `sudo su -` 使用当前用户密码登录root用户

### 用户组

#### 用户组查看
1. `groups`
>
```
当前用户所在组:
$ groups
ec2-user adm wheel systemd-journal
```
> 
```
列出root组成员:
$ groups root
root : root
```

2. `id`
>
```
当前用户所在组:
$ id
uid=1000(ec2-user) gid=1000(ec2-user) groups=1000(ec2-user),4(adm),10(wheel),190(systemd-journal) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

3. `/etc/group`文件， 配合使用`grep`
>
```
当前用户所在组:
$ cat /etc/group | grep ec2-user
adm:x:4:ec2-user
wheel:x:10:ec2-user
systemd-journal:x:190:ec2-user
ec2-user:x:1000:
```


