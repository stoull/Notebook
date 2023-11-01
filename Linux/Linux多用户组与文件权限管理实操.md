# Linux多用户组与文件权限管理实操


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
* `sudo su -u USERNAME /bin/bash` 切换到nologin用户, 或者`sudo -u USERNAME /bin/bash`

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

* 切换到nologin用户，使用 `su -s /bin/bash username` 或者 `sudo su -s /bin/bash username` 或  `sudo -u USERNAME /bin/bash`

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

* 创建和删除组

```
# 创建组
groupadd group_name
# 删除组
groupdel group_name
```

* 把用户与组的操作

```
将用户 hut 添加（追加 append）到组 group_name 中：
usermod -a -G group_name hut
追加到两个组中
usermod -a -G group_name,group_name2 hut

修改用户主要组, 每个用户仅有一个主要组，零个或多个次要组。
usermod -g admin hut	将hut的主要组更改为admin组
```

* 把用户从某个组中删除

```
把hut从admin组中删除
gpasswd -d hut admin
```
> 注意：当用户只属于一个组的时候，是无法删除组的。因为所有用户必须属于一个组

```
# 只保留用户 hut 到组 admin
usermod -G admin hut
# 保留用户 hut 到组 admin 和 mysql
usermod -G admin,mysql hut
```

## 文件

### 查看文件详情
```
ls -l /var/log/nginx/error.log
-rw-r--r--. 1 root root 7769 Oct 31 02:22 /var/log/nginx/error.log
```
|-rw-r--r--. |  1 |  root |  root |  7769 | Oct 31 02:22 | /var/log/nginx/error.log |
| ------- | --- | --- | --- | --- | ------ | --------- |
| 类型及权限 | 连结数 | 所属用户| 所属用户组 | 文档大小 | 最后修改时间 | 文档名称 |

>
文件类型详情：
>
* `d` 目录
* `-` 文件；
* `l` 链接文档(link file)；
* `b` 装置文件里面的可供储存的接口设备(可随机存取装置)；
* `c` 装置文件里面的串行端口设备，例如键盘、鼠标(一次性读取装置)。

### 文件所属用户及组操作

* `chown -R user1 folder1` : 递归修改文件夹的所属用户，不修改组
* `chown -R user1: folder1` : 递归修改文件为用户及用户所属的组
* `chown -R user1:usergroup folder1` : 递归修改用户及用户组
* `chown -R :usergroup folder1` : 仅修改用户组，不修改用户
* `chgrp -R usergroup folder1` : 仅修改用户组，不修改用户

### 文件权限操作

权限：`r`: 读read `w`: 写write `x`: 执行权限execute `X`: 特殊执行权限

#### 使用符号

* `u` - user 用户, 文件所有者Owner
* `g` - group 组, 与该文件的拥有者属于同一个群体
* `o` - others 其它用户 Other Users
* `a` - all 所有用户

操作operator符号：

* `+` : 增加权限
* `-` : 移除权限
* `=` : 指定权限

示例：

```
chmod ugo+r file1.txt		所有人可读
chmod a+r file1.txt		所有人可读
chmod u=r,g+r,o-r filename.txt
chmod g=r,o=r file.txt 
chmod ug+r,o-r file1.txt file2.txt
chmod -R a+r *	// 遍历所有的文件
```

#### 使用数字(八进制语法)
`r: 4 w:2 x:1`

示例：

```
chmod 664 filename
chmod 400 filename
chmod 777 filename
```

八进制语法:

| # | 权限 | rwx | 二进制 |
| --- | --- | --- | --- |
| 7 | 读 + 写 + 执行 |rwx |111 |
| 6 | 读 + 写 |rw- |110 |
| 5 | 读 + 执行 |r-x |101 |
| 4 | 只读 |r-- |100 |
| 3 | 写 + 执行 |-wx |011 |
| 2 | 只写 |-w- | 010 |
| 1 | 只执行 |--x |001 |
| 0 | 无 |--- |000 |

### 特殊权限

#### setuid、setgid (SET位权限)

`/usr/bin/passwd` 与 `/etc/passwd` 文件的权限 与 普通文件不一样：

```
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 Apr 16  2020 /usr/bin/passwd
```

`setuid` ：让普通用户拥有可以执行“只有 root 权限才能执行”的特殊权限，setgid 同理指'组'

#### stick bit (粘滞位权限)

`/tmp` 目录的权限与普通文件也不一样：

```
ls -dl /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 Apr 16  2020 /usr/bin/passwd
```

特殊权限设置：

```
setuid：chmod u+s xxx
setgid: chmod g-s xxx
stick bit : chmod o+t xxx
```
