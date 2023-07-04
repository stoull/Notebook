# 高级包装工具(APT)-Advanced Packaging

Debian Linux uses [dpkg packaging system](https://wiki.debian.org/DebianPackageManagement). A packaging system is a way to provide programs and applications for installation. 

[APT](https://wiki.debian.org/Apt) (Advanced Package Tool) is the command line tool to interact with the packaging system in Debian, and Debian-based Linux Distributions.

There is already dpkg commands to manage it. But APT is a more friendly way to handle packaging. You can use it to find and install new packages, upgrade packages, remove the packages etc.

## `APT` VS `apt-get`

Debin系统使用高级包装工具(APT)系统即Advanced Packaging Tool--与命令行apt不是同一个概念--来管理系统软件的功能，且可以从软件源获取并解析软件包依赖。

可以使用Debin包管理系统工具有很多，常用的有：

* Aptitude是一个命令行工具，它同时提供一个基于文本的用户界面。该程序提供了一些改进功能，例如对软件包元信息的增强搜索。
* apt-get和apt-cache等命令是标准apt软件包中的命令行工具。apt-get用于安装和删除软件包，apt-cache用于搜索软件包及显示软件包信息。
* 新版apt软件包提供了apt命令作为面向用户使用的工具。与传统apt-get和aptitude相比，它提供了进度条显示、彩色字符支持等用户友好的新功能。


`apt`第一个稳定版本是在2014年发布的，但在2016 随着Ubuntu 16.04的发布，大众才慢慢关注到这个工具。从之前的`apt-get install package`慢慢变成了`apt install package`

`apt`包含了部分 `apt-get`及`apt-cache`的用于包管理的指令，并且对于用户更友好。

[From StackExchange：](https://askubuntu.com/questions/445384/what-is-the-difference-between-apt-and-apt-get)

apt-get may be considered as lower-level and "back-end", and support other APT-based tools. apt is designed for end-users (human) and its output may be changed between versions.

>The `apt` command is meant to be pleasant for end users and does not need to be backward compatible like apt-get(8).
>
This is the correct answer (for Debian and Ubuntu as well as other derivatives like Mint). In particular, running sudo apt upgrade will perform the same operations as sudo apt-get upgrade --with-new-pkgs. It will install new packages but, unlike sudo apt-get dist-upgrade, it will not remove old ones (except when installing a new version of the same package, of course--which sudo apt-get upgrade will also do). man apt further corroborates that this answer is correct. – Eliah Kagan

## Install `apt`

### On Debian based systems
从这里[apt Source-Debian](http://ftp.us.debian.org/debian/pool/main/a/apt/)找到`apt`的资源及其版本。

1. 使用`wget`下载

`wget http://ftp.us.debian.org/debian/pool/main/a/apt/apt_2.4.2_amd64.deb -O apt.deb -O apt.deb`

2. 使用`dpkg`安装apt

`sudo dpkg -i apt.deb` or without sudo `pkexec dpkg -i apt.deb`

### On Ubuntu based system
[apt Source-Ubuntu](http://security.ubuntu.com/ubuntu/pool/main/a/apt/?C=M;O=D)



## `apt` Commands

#### 包数据库及更新

`sudo apt update`	// 只更新package数据库。如果有新版本，会知道有新版本，但不会安装

##### 更改包数据库源
更改文件`/etc/apt/sources.list`中的url为想设置的源url。

如：

```
$ cat /etc/apt/sources.list
deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi

所有deb后的url更改为 archive.ubuntu.com/ubuntu
deb http://archive.ubuntu.com/ubuntu/ buster main contrib non-free rpi
```


#### 更新已安装的包

`sudo apt upgrade` // 根package数据库，来更新安装所需要的包。如果package数据库没有更新，可能会安装不到最新的版本

`sudo apt full-upgrade` // 会移除更新需要移除的已经安装了的旧包

所以最方便更新包及包库的命令为：

`sudo apt update && sudo apt upgrade -y`

#### 搜索安装包
`apt search <search item>`

#### 显示安装包信息
`apt list <search item>`


#### 安装-包
`sudo apt install <pack_name>`

`sudo apt install <package_1> <package_2> <package_3>` // 同时安装多个包
`sudo apt install <package_name> --no-upgrade`	// 只安装，不更新
`sudo apt install <package_name> --only-upgrade`	// 只更新，不安装
`sudo apt install <package_name>=<version_number>`	// 安装特别版本的包

#### 移除安装包
`sudo apt remove <package_name>` // 称除可执行行文件，保留配置文件，下次安装后会有相同的配置

或者：

`sudo apt purge <package_name>` // 移除所有包括配置文件

可以在`remove`之后运行`purge`，通常来说`apt remove`对卸载一个包来说足够了。

#### 查看安装包
`apt list` 列出所有可用包
`apt list --upgradable` // 列出可更新的包
`apt list --installed`		// 列出已安装的包
`apt list --all-versions` // 列出当前系统所有可用包


#### 管理
`sudo apt autoremove`

或者

`sudo apt-get autoremove`

当安装一些有依赖的包时，对应的依赖包也会安装，但当`remove`有依赖的包的包时，这些依赖包并不会移除掉，会保存在系统中。 这个命令会移除这些‘失主’的依赖包。

##### apt cache 文件

apt 包管理系统会缓存DEB包于`/var/cache/apt/archives`，会缓存一些你卸载了的包，时间长了可能会占很大的存储空间。使用下面的命令查看文件大小：

`sudo du -sh /var/cache/apt`

如果文件大，有两种方式管理这个缓存文件

`sudo apt-get autoclean` // 删除过期的或停用的版本缓存

`sudo apt-get clean` // 删除缓存整个


**参考资料：**

[维基百科-Debian](https://zh.wikipedia.org/zh-cn/Debian)

[维基百科-APT](https://en.wikipedia.org/wiki/APT_(software))

[Using apt Commands in Linux](https://itsfoss.com/apt-command-guide/)
