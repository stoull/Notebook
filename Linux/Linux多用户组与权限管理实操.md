# Linux多用户组与权限管理实操


##  用户

* `whoami`: 列出当前的用户名uername
* `cat /etc/passwd`: 查看所有用户
* `passwd username`: 设置修改用户密码

### 用户切换及权限提升

su 和 sudo 用户切换及权限提升

* `su username`: 切换用户, 在不登出当前用户的情况下登录为另外一个用户
*  `su` 和 `su -`(即 su -l --login)，都为切换到 root用户。`su`：保持原用户环境，`su -`：创建一个新的环境（由 root 用户 ~/.bashrc 文件所设置的环境），相当于使用 root 用户正常登录。
	- `su`可用于登录目标用户以便重现以及调试问题。
* sudo 命令需要输入当前用户的密码，su 命令需要输入 root 用户的密码。
* sudo 命令只允许使用提升的权限运行单个命令，而 su 命令会启动一个新的 shell，同时允许使用 root 权限运行尽可能多的命令，直到明确退出登录。
* `sudo su -` 使用当前用户密码登录root用户

### 用户操作

#### 创建用户

要在root权限下

* 创建服务用户

	`useradd username`: 不带任何选项
	* 不会创建用户主目录
	* 密码必须单独设置：`passwd username`
	* 用户的默认shell是sh，可使用`su username` 切换登录用户
	* 同时创建组，组与用户同名
	
* 创建标准用户

	`useradd -m username`: 创建标准用户
	* 会创建用户主目录`/home/username`及同名组
	* 可使用`-d`更改主目录位置, `useradd -m username -d /home/topath`
	* 可使用`-s`更改默认 shell，如`useradd -m -s usr/bin/zsh username`
	
* 创建安全服务用户

	`useradd -r username` : 创建系统用户
	* `-r` 为创建系统用户，无home目录无密码，不能登录，只有root可以登录。
	
	`useradd -s /sbin/nologin username` (Debian systems) 
	
	* -s指定用户登录后使用的shell, 这里指定的为无nologin或false。任何人不可登录，显示：
	
	> This account is currently not available.


#### 删除用户
1. `pkill -u username`: 删除前终结用户的所有进程
2. `userdel -r username `: 删除用户，`-r`表示删除用户的同时，将其用户目录和系统内与其相关的内容删除。



## 用户组

### 查看用户组 三种方法
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

### 用户组操作


## 文件

### 查看文件详情
```
ls -l /var/log/nginx/error.log
-rw-r--r--. 1 root root 7769 Oct 31 02:22 /var/log/nginx/error.log
```
|-rw-r--r--. |  1 |  root |  root |  7769 | Oct 31 02:22 | /var/log/nginx/error.log |
| ------- | --- | --- | --- | --- | ------ | --------- |
| 类型及权限 | 连结数 | 所属用户| 所属用户组 | 文档大小 | 最后修改时间 | 文档名称 |

### 文件用户及组操作

* `chown -R user1 folder1` : 递归修改文件夹的所属用户，不修改组
* `chown -R user1: folder1` : 递归修改文件为用户及用户所属的组
* `chown -R user1:usergroup folder1` : 递归修改用户及用户组
* `chown -R :usergroup folder1` : 仅修改用户组，不修改用户
* `chgrp -R usergroup folder1` : 仅修改用户组，不修改用户

### 文件权限操作

