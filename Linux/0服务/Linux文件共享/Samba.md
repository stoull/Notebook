
# Samba

## 分布式文件系统

[分布式文件系统](https://zh.wikipedia.org/zh-cn/分散式檔案系統)

[网络文件系统](https://zh.wikipedia.org/zh-cn/网络文件系统)

## Samba 是什么

Samba 是**SMB**/*CIFS* 协议（*[及其它支持协议](https://zh.wikipedia.org/zh-cn/Samba)*）在Unix系列系统上的实现，目的是实现不同系统(Unix系列系统及Windows)间的文件共享，是开源软件。

**出现背景：**

Samba出现前，Windows实现的是**SMB**/*CIFS*协议在Windows间进行文件共享，Unix及类Unix系统间用的是NFS进行进行文件共享。但Windows与Unix系列系统之间是没有对应的协议实现，所以不能进行网络文件共享。Samba的出现就是在Linux上的实现SMB协议，这样不同系统间就可以进行文件共享了。



### Samba主要协议**SMB**/*CIFS*

**SMB**

服务器消息块（Server Message Block，缩写为SMB)[Wiki](https://en.wikipedia.org/wiki/Server_Message_Block)协议，最初由IBM设计，后来由微软对其进行开发和更新，使用于windows系统中。主要功能是使网络上的机器能通过授权控制共享计算机文件、打印机等资源。
[SMB 协议微软的描述：](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh831795(v=ws.11))
>The Server Message Block (SMB) protocol is a network file sharing protocol that allows applications on a computer to read and write to files and to request services from server programs in a computer network. The SMB protocol can be used on top of its TCP/IP protocol or other network protocols. Using the SMB protocol, an application (or the user of an application) can access files or other resources at a remote server. This allows applications to read, create, and update files on the remote server. It can also communicate with any server program that is set up to receive an SMB client request. Windows Server 2012 introduces the new 3.0 version of the SMB protocol.
>

SMB2.0 也被其它非Windows系统支持，如Xenix, OS/2和VMS (Pathworks)， X/Open也部分支持。Apple 从 OS X 10.8 开始也支持SMB2.0，具体的实现叫`SMBX`。[Is SMBX on 10.8.2 ready for primetime?](https://discussions.apple.com/thread/4771281)

#### CIFS

网络文件共享系统(Common Internet File System, 缩写为CIFS)，是由微软开发的协议，SMB1.0 的升级版本。但现在都不使用这个协议了，现在都使用SMB3。相对于CIFS来说，SMB3或SMB2都是很大的升级。
> 1996年，约于升阳推出WebNFS的同时，微软提出将SMB改称为Common Internet File System。此外微软还加入了许多新的功能，比如符号链接、硬链接、提高文件的大小.....不过这些提案现在均已过期。[Wiki_服务器消息块](https://zh.wikipedia.org/zh-cn/伺服器訊息區塊)

>Samba 4.0 支持SMB3.0 [Samba 4.0 support for SMB 3.0](https://wiki.samba.org/index.php/Samba_4.0_Whitepaper#New_Features)

SMB在Windows系统上的实现就是‘网络共享’，‘网上邻居’？等功能，比如你能访问家庭网络中其它电脑共享的文件夹[文件服务和SMB](https://docs.microsoft.com/zh-cn/windows-server/storage/file-server/file-server-smb-overview)。

SMB与CIFS可通用: [CIFS vs SMB: What’s the Difference?](https://www.varonis.com/blog/cifs-vs-smb/)

SMB与NFS是[NAS](https://zh.wikipedia.org/zh-cn/网络附接存储)系统的主要两个协议

### Samba 能用来做什么

Samba主要的两个程序为`smbd`和`nmbd`，这个程序主要实现了SMB协议的四个主要服务：

* 文件共享服务：smbd
* 授权与验证：smbd
* 名称解析：nmbd NetBIOS
* 服务发现及广播：nmbd NetBIOS
* Primary Domain Controller for NT (Samba 3)
* Active Directory Domain Controller (from Samba 4)

### Samba共享文件实例

设置samba文件共享的主要步骤为

#### 1.安装samba

samba一般包含以下程序：

* **samba**: Provides an SMB/Common Internet File System (CIFS) server that can be used to provide network services to SMB/CIFS clients
* **samba-client**: Provides some SMB/CIFS clients to complement the built-in SMB/CIFS file system in Linux. These clients allow access to SMB/CIFS shares and printing to SMB/CIFS printers.
* **samba-common**: Provides files necessary for both the server and client Samba packages
* **samba-winbind**: Provides the winbind daemon and client tools. winbind enables Linux membership in Windows domains and the use of Windows user and group accounts
* **samba-winbind-clients**: Provides the Network Security Services (NSS) library and Pluggable Authentication Modules (PAM) needed to communicate with winbind

开始安装：
>`sudo apt update`
>
>`sudo apt install samba samba-common smbclient` // `smbclient`可以不用安装，用来测试用
>
> 或者：`sudo apt install samba samba-common-bin`
>
>`sudo service smbd status` 查看运行状态

#### 2.配置samba
Samba的配置文件为：`/etc/samba/smb.conf`

一般是基于生成的初始配置文件进行更改配置, 初始配置文件里也有大量的配置参数据信息，可以阅读，所以开始更改配置文件前，可先复制一份初始的配置文件方便日后需要:

>`sudo mv /etc/samba/smb.conf /etc/samba/smb.conf_original`

编辑配置文件：
>`sudo vi  /etc/samba/smb.conf`

可编辑为如下配置, 可适配大多数的服务需求：

>
```
[global]
workgroup = WORKGROUP
security = user
encrypt passwords = yes
```

`[global]` 表示为将下面的设置应用到之后的所有设置之中。

`workgroup = WORKGROUP` workgroup表示网络名称，之前windows网络邻居的特别命名为`WORKGROUP`, 但现在已经不用了，所以没有特别的要求，现设置为`WORKGROUP`可兼容之前的windows设备。workgroup真正的含义为[NetBIOS group names](https://www.samba.org/samba/docs/using_samba/ch06.html), samba服务会向这个网络广播信息。在文件夹管理器‘网络’中可查找到对应的网络的所有设备。
`security = user` 表示能访问samba共享文件夹的用户，是系统配置过的用户
`encrypt passwords = yes` 表示在授权的时候，将密码加密传输

先了解：
**Samba服务控制**: samba主要由`smbd`及`nmbd`两个服务，主要控制为`start`、`stop`、`restart`、`reload`，如：
>
`sudo service smbd restart`
>
`sudo service nmbd restart`
>
`sudo service smbd stop`
>
>`sudo service smbd status` 查看运行状态

#### 3.设置共享的文件夹
Samba是以文件夹的方式进行文件共享的，所以需要创建一个用来共享文件的文件夹。位置没有要求，一般放在/home目下。
`sudo mkdir /home/shares`

根据目的给文件夹设置权限,下面新建三个文件夹对应的权限为分别为给所有人，系统用户，当前用户。

所有人可访问的共享文件夹：

```
sudo mkdir /home/shares/everyone
sudo chown root: root/home/shares/everyone/
sudo chmod 777 /home/shares/everyone/
```
系统用户可访问的共享文件夹：

```
sudo mkdir /home/shares/users
sudo chown root: root/home/shares/users/
sudo chmod 770 /home/shares/users/
```
当前pi用户可访问的共享文件夹：

```
sudo mkdir /home/shares/pi
sudo chown root: root/home/shares/pi/
sudo chmod 700 /home/shares/pi/
```

将上面三个共享文件夹配置到配置文件:

`sudo vi /etc/samba/smb.conf`

将下面的配置信息写入到`smb.conf`配置文件：

```
[Samba Test]
comment = Samba share file with everyone
path = /home/shares/everyone
writeable = yes
browseable = yes
read only = no
public = no

[Samba Users]
comment = Samba Users Share
path = /home/shares/users
writeable = yes
browseable = yes
read only = no

[SambaPi]
comment = Samba Pi release
path = /home/shares/pi
writeable = yes
browseable = yes
read only = no
```

说明：`Samba Test`, `Samba Users`及`SambaPi`分别是Samba三个共享文件夹的名称，文件夹的配置信息也可自定

当配置文件写入后，可用`$ testparm`命令测试是否合法, 作用`testparm -v`查看默认的配置。然后重启samba服务：

```
sudo service smbd restart
sudo service nmbd restart
```

**上面步骤可按需要选择共享并配置一个文件夹**

#### 4.设置给用户设置访问密码
Samba的授权使用是系统的用户及对应的文件夹及文件的权限。并且每个用户想访问共享文件（public除外），都需要为Samba服务设置一个单独的密码。

给用户`pi`设置密码：`sudo smbpasswd -a pi`
取消`pi`的访问权限：`sudo smbpasswd -d pi`
重新让`pi`有访问权限：`sudo smbpasswd -e pi`


##### 未完成

```
建议在系统中新建一个专门的共享用户`shareuser`(可自定)，并设置共享文件中的所有文件所有者为shareuser。

```
adduser --system shareuser
chown -R shareuser /path/to/share
``

[How to create a Samba share that is writable from Windows without 777 permissions?](https://unix.stackexchange.com/questions/206309/how-to-create-a-samba-share-that-is-writable-from-windows-without-777-permission)
```

#### 5. 连接 A Samba Share

现在将需要共享的文件放入到对应的文件夹中，应该是可以在网络上查找到对应的共享文件夹。

也可以将需要共享的硬盘mount到对应的共享文件夹中，也可使用`fstab`自动mount。

使用如下命令连接服务(可以输入浏览器)：

`smb://User@Server`

`smb://<servername>/<sharename>`

如：
>
smb://192.168.0.200/
smb://192.168.0.200/pi
smb://192.168.0.200/everyone

在连接上Samba Server 之后，在Mac Finder上显示图标为?, 不是很好看，针对mac系统显示可增加如下配置：


```
[Global]
min protocol = SMB2
vfs objects = fruit streams_xattr  
fruit:metadata = stream
fruit:model = MacSamba
fruit:posix_rename = yes 
fruit:veto_appledouble = no
fruit:wipe_intentionally_left_blank_rfork = yes 
fruit:delete_empty_adfiles = yes 
[TimeMachineBackup]
vfs objects = fruit streams_xattr
fruit:time machine = yes
#fruit:time machine max size = SIZE
```

6. 开机自启动

一般Samba在开机时会自动启动，但一些通过USB挂载的磁盘不会自动挂载，这个时候需要通过编辑`/etc/fstab`文件, 设置开机自动挂载。



[Configure Samba to Work Better with Mac OS X](https://wiki.samba.org/index.php/Configure_Samba_to_Work_Better_with_Mac_OS_X)

[vfs_fruit — Enhanced OS X and Netatalk interoperability](https://www.samba.org/samba/docs/current/man-html/vfs_fruit.8.html)



[参考资料]:

[Samba: An Introduction](https://www.samba.org/samba/docs/SambaIntro.html)

[Samba: www.samba.org](https://www.samba.org)

[Samba Basics](http://www.novell.com/documentation/open-enterprise-server-2018/file_samba_cifs_lx/data/baxvv81.html)

[Samba: An Introduction](https://www.samba.org/samba/docs/SambaIntro.html)

[Install and Configure Samba](https://ubuntu.com/tutorials/install-and-configure-samba#2-installing-samba)

[Connect to the NAS server](https://howtoraspberrypi.com/create-a-nas-with-your-raspberry-pi-and-samba/)

[Samba on Raspberry Pi Guide – A To Z](https://kalitut.com/samba-on-raspberry-pi/)

[How to Build a Raspberry Pi NAS Using Samba](https://howchoo.com/pi/how-to-make-a-raspberry-pi-nas-device-with-samba)