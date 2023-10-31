# Linux命令_YUM_DNF_包管理

## yum 

yum命令 是在Fedora和RedHat以及SUSE中基于rpm的软件包管理器，它可以使系统管理人员交互和自动化地更新与管理RPM软件包，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软体包，无须繁琐地一次次下载、安装。

yum提供了查找、安装、删除某一个、一组甚至全部软件包的命令，而且命令简洁而又好记。

### 语法

```
yum(选项)(参数)
```

### 选项

```
-h：显示帮助信息；
-y：对所有的提问都回答“yes”；
-c：指定配置文件；
-q：安静模式；
-v：详细模式；
-d：设置调试等级（0-10）；
-e：设置错误等级（0-10）；
-R：设置yum处理一个命令的最大等待时间；
-C：完全从缓存中运行，而不去下载或者更新任何头文件。
```

### 参数

```
install：安装rpm软件包；
update：更新rpm软件包；
check-update：检查是否有可用的更新rpm软件包；
remove：删除指定的rpm软件包；
list：显示软件包的信息；
search：检查软件包的信息；
info：显示指定的rpm软件包的描述信息和概要信息；
clean：清理yum过期的缓存；
shell：进入yum的shell提示符；
resolvedep：显示rpm软件包的依赖关系；
localinstall：安装本地的rpm软件包；
localupdate：显示本地rpm软件包进行更新；
deplist：显示rpm软件包的所有依赖关系；
provides：查询某个程序所在安装包。
```

### 实例

```
部分常用的命令包括：

自动搜索最快镜像插件：yum install yum-fastestmirror
安装yum图形窗口插件：yum install yumex
查看可能批量安装的列表：yum grouplist
```

### 安装

```
yum install              #全部安装
yum install package1     #安装指定的安装包package1
yum groupinsall group1   #安装程序组group1
```

### 更新和升级

```
yum update               #全部更新
yum update package1      #更新指定程序包package1
yum check-update         #检查可更新的程序
yum upgrade package1     #升级指定程序包package1
yum groupupdate group1   #升级程序组group1
```

### 查找和显示
```
# 检查 MySQL 是否已安装
yum list installed | grep mysql
yum list installed mysql*

yum info package1      #显示安装包信息package1
yum list               #显示所有已经安装和可以安装的程序包
yum list package1      #显示指定程序包安装情况package1
yum groupinfo group1   #显示程序组group1信息yum search string 根据关键字string查找安装包
```

### 删除程序

```
yum remove &#124; erase package1   #删除程序包package1
yum groupremove group1             #删除程序组group1
yum deplist package1               #查看程序package1依赖情况
```

### 清除缓存

```
yum clean packages       # 清除缓存目录下的软件包
yum clean headers        # 清除缓存目录下的 headers
yum clean oldheaders     # 清除缓存目录下旧的 headers
```

### 更多实例

```
# yum
/etc/yum.repos.d/       # yum 源配置文件
vi /etc/yum.repos.d/nginx.repo # 举个栗子: nginx yum源
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/6/$basearch/
gpgcheck=0
enabled=1

# yum mirror
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
wget https://mirror.tuna.tsinghua.edu.cn/help/centos/
yum makecache

# 添加中文语言支持
LANG=C # 原始语言
LANG=zh_CN.utf8 # 切换到中文
yum groupinstall "Chinese Support" # 添加中文语言支持
```

[Linux-Command](https://wangchujiang.com/linux-command/c/yum.html)

## DNF

DNF是新一代的RPM软件包管理器。他首先出现在 Fedora 18 这个发行版中，最近取代了YUM正式成为包管理器，克服了YUM包管理器的一些瓶颈，提升了包括用户体验，内存占用，依赖分析，运行速度等多方面的内容。

DNF 常用命令 

```
dnf list                                         # DNF列表 

dnf list installed                           # 列出所有安装的RPM包

dnf help                                       # DNF命令帮助
dnf history                                   # 查看DNF命令执行历史
dnf repolist                                  # 查看系统中可使用的DNF软件库
dnf info <package>                     # 查看软件包详细信息

dnf  clean all
dnf makecache

dnf install <package>                  # 安装软件包及其所需的所有依赖

dnf download $package              # 只下载软件包，不安装

dnf update <package>                # 升级软件包
dnf remove <package>               # 删除软件包
dnf reinstall <package>              # 重新安装特定软件包
dnf distro-sync                            # 更新软件包到最新的稳定发行版
```