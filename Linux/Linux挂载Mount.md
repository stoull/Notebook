# Linux 挂载(Mount)

## 挂载的意义
在Linux中所有的数据都被当成文件，管理这些文件使用的是[目录树架构](https://www.pathname.com/fhs/pub/fhs-2.3.html#MNTMOUNTPOINTFORATEMPORARILYMOUNT)。目录树可以接入很多Linux系统可识别的设备，比如键盘、鼠标、蓝牙耳机、打印机、手机、磁盘等等，这些接入的设备都可以在目录`/dev`下以文件的形式找到。但对应的文件都只是设备的描述，只是一个文件。

>
磁盘设备硬件命名:
>
* /dev/sd[a-p][1-128]：为实体磁盘的磁盘文件名；
* /dev/vd[a-d][1-128]：为虚拟磁盘的磁盘文件名；

* 如果对应的设备为你的一个磁盘，你是不能从`/dev/sda1`这个文件中进入你的磁盘的。挂载是将磁盘中的文件系统接入到Linux系统目录树下的一个目录里，实现对磁盘的读写。

* 对于Linux系统，根文件系统“/”之外的其他文件要想能够被访问，都必须通过“关联“至根文件系统上的某个目录来实现，此关联操作即为“挂载”，此目录即为“挂载点”，解除此关联关系的过程称之为“卸载”。

* 鼠标、耳机等不提供数据存储的设备的接入不是叫挂载，挂载只针对提供数据存储的设备接入到Linux系统。

* Linux系统文件管理使用的是目录树架构，遵循FHS标准。
* 存储设备的文件管理系统不在这个目录树架构中。
* 将存储设备的文件管理系统按目录树的架构接入Linux系统文件管理树，就为挂载。


<details>
  <summary>更多关于'挂载'的不厌其烦</summary>
  
  在Linux中所有的数据都被当成文件(Everything Is A File)，管理这些文件使用的是目录树架构(tree-like hierarchical structure)，遵循[FHS](https://www.pathname.com/fhs/)标准([Wiki](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard))。在磁盘安装系统之前是不会有`/, /tec, /dev, /bin`这些目录的，所以FHS标准是写在系统代码里的。当你在安装系统的时候，系统会在内存里生成对应的目录树。但生成之后需要将这些数据保存在磁盘里，怎么存？

在安装系统的时候，一般要指定安装的磁盘，系统安装的时候会将磁盘进行分区和格式化，将磁盘上的物理空间与系统按FHS标准生成的根目录对应起来的东西，就叫挂载。当系统完成安装的时候，我们就可以在磁盘上找到`/, /tec, /dev, /bin.....`这些目录。系统启动之后，只要在系统的目录树里新建或修改文件，就可以同步到磁盘里的文件系统中。

磁盘设备在目录树中也是一个文件，但磁盘是作为一个设备存在于`/dev`文件夹下。存储设备都有一个文件系统，需要通过这个文件系统才能在物理磁盘进行数据的存储操作。将磁盘的文件系统接入Linux遵循FHS标准的文件系统中，就是挂载。挂载完之后才能对磁盘数据进操作。

* 根目录一般会单独挂载到一个分区，主要是为了保证安全。
* 用户的home目录会挂载到单独的一个分区。
  </details>

## 挂载的注意事项

* 单一文件系统不应该重复挂载在不同的挂载点（目录）中；
* 单一目录不应该重复挂载多个文件系统；
* 要作为挂载点的目录，理论上应该都是空目录。

所有磁盘设备及分区都以文件的形式存储在/dev/,但是这些文件不能直接使用，如果要往这些分区内写入数据就需要挂载分区。
所谓的挂载点就是文件系统中存在的一个目录，通常情况下，创建在/mnt目录下，挂载成功后，访问挂载点就是访问新的存储设备。

## 如何挂载一个磁盘

### 查看系统中的磁盘信息

* 使用命令`sudo fdisk -l `列出系统下磁盘及分区信息

>`sudo fdisk -l | grep NTFS` 只列出特定文件的文件系统

* 或者使用`sudo diskutil list` 列出磁盘信息

* 使用命令`lsblk`可查看系统中所有磁盘的信息，如：

>
`lsblk`: 列出本系统下的所有磁盘与磁盘内的分区信息
`lsblk -ip /dev/device_name`: 设备内的所有数据的完整文件名

* 使用命令`blkid `可列出设备的 UUID 等参数

* 使用命令`mount`可列出系统已挂载的文件系统

>
```
如：
pi@raspberrypi:/home $ mount
/dev/mmcblk0p2 on / type ext4 (rw,noatime)
devtmpfs on /dev type devtmpfs (rw,relatime,size=1827468k,nr_inodes=97607,mode=755)
/dev/mmcblk0p1 on /boot type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
第一行：/dev/mmcblk0p2 为挂载的设备，挂载点为 / 文件系统为 ext4. rw表示可读写。
第二行：设备名称为devtmpfs，挂载在目录/dev .....
```


### 磁盘分区

磁盘分区使用 `gdisk`/`fdisk`工具

### 磁盘格式化（创建文件系统）

磁盘格式化使用`mkfs`工具
如：
`mkfs -t ext4 /dev/sdb1` 将设备sdb1格式化为ext4文件系统

### 磁盘挂载与卸载 mount

磁盘挂载与卸载使用`mount `工具：

```
[root@study ~]# mount -a
[root@study ~]# mount [-l]
[root@study ~]# mount [-t 文件系统] LABEL=''  挂载点
[root@study ~]# mount [-t 文件系统] UUID=''   挂载点  # 鸟哥近期建议用这种方式喔！
[root@study ~]# mount [-t 文件系统] 设备文件名  挂载点
选项与参数：
-a  ：依照配置文件 [/etc/fstab](../Text/index.html#fstab) 的数据将所有未挂载的磁盘都挂载上来
-l  ：单纯的输入 mount 会显示目前挂载的信息。加上 -l 可增列 Label 名称！
-t  ：可以加上文件系统种类来指定欲挂载的类型。常见的 Linux 支持类型有：xfs, ext3, ext4,
      reiserfs, vfat, iso9660（光盘格式）, nfs, cifs, smbfs （后三种为网络文件系统类型）
-n  ：在默认的情况下，系统会将实际挂载的情况实时写入 /etc/mtab 中，以利其他程序的运行。
      但在某些情况下（例如单人维护模式）为了避免问题会刻意不写入。此时就得要使用 -n 选项。
-o  ：后面可以接一些挂载时额外加上的参数！比方说帐号、密码、读写权限等：
      async, sync:   此文件系统是否使用同步写入 （sync） 或非同步 （async） 的
                     内存机制，请参考[文件系统运行方式](../Text/index.html#harddisk-filerun)。默认为 async。
      atime,noatime: 是否修订文件的读取时间（atime）。为了性能，某些时刻可使用 noatime
      ro, rw:        挂载文件系统成为只读（ro） 或可读写（rw）
      auto, noauto:  允许此 filesystem 被以 mount -a 自动挂载（auto）
      dev, nodev:    是否允许此 filesystem 上，可创建设备文件？ dev 为可允许
      suid, nosuid:  是否允许此 filesystem 含有 suid/sgid 的文件格式？
      exec, noexec:  是否允许此 filesystem 上拥有可执行 binary 文件？
      user, nouser:  是否允许此 filesystem 让任何使用者执行 mount ？一般来说，
                     mount 仅有 root 可以进行，但下达 user 参数，则可让
                     一般 user 也能够对此 partition 进行 mount 。
      defaults:      默认值为：rw, suid, dev, exec, auto, nouser, and async
      remount:       重新挂载，这在系统出错，或重新更新参数时，很有用！
```
[以上mount说明粘贴自鸟哥的文章](https://wizardforcel.gitbooks.io/vbird-linux-basic-4e/content/61.html)

与mount命令相关的文件：

`/etc/fstab`：为自动挂载的配置文件，当运行 mount -a时，会将根据`/etc/fstab` 中配置的所有挂载点都挂上(一般是在系统启动时的脚本中调用，自己最好别用！)。

`/etc/mtab`，`/etc/mounts`：mount 和 umount 命令会在 `/etc/mtab` 文件中维护当前挂载的文件系统的列表。


#### 查看当系统支持的文件类型
当挂载一个当前系统不支持的文件系统类型时，它是没有办法工作的。常见的 Linux 支持类型有：xfs, ext3, ext4,
      reiserfs, vfat, iso9660（光盘格式）, nfs, cifs, smbfs

* 查看Linux支持的文件系统： `ls -l /lib/modules/$(uname -r)/kernel/fs`

* 查看Linux已载入到内存中的支持的文件系统：

 `cat /proc/filesystems`
 
 > 此命令打印的第一列说明文件系统是否需要挂载在一个块设备上， nodev 表明后面的文件系统不需要挂接在设备上。 第二列是内核支持的文件系统。
 
 * Linux支持的文件系统驱动文件都放在：`/lib/modules/$(uname -r)/kernel/fs/`目录下


#### 开始挂载

>可先用`sudo fdisk -l`查看磁盘是否已经挂载，如已挂载先卸载`sudo umount /media/ntfs`

确保磁盘的文件系统格式是系统支持的然后开始挂载。根据[Filesystem Hierarchy Standard](https://www.pathname.com/fhs/pub/fhs-2.3.html#MNTMOUNTPOINTFORATEMPORARILYMOUNT) 标准, 挂载一般挂载在`/media`及`/mnt`目录下。

* `/media`: 用来挂载可移动设备的
>
>/media : Mount point for removeable media 
>
Purpose This directory contains subdirectories which are used as mount points for removeable media such as floppy disks, cdroms and zip disks.

* `/mnt`: 临时挂载点，给管理员临时手动挂载用
>
/mnt : Mount point for a temporarily mounted filesystem 
>
Purpose This directory is provided so that the system administrator may temporarily mount a filesystem as needed. The content of this directory is a local issue and should not affect the manner in which any program is run. This directory must not be used by installation programs: a suitable temporary directory not in use by the system must be used instead.


1. 新建一个用于挂载的空目录
>
`mkdir -p /media/Transfer`
>
> 使用`-p`让创建者对挂载点有权限

2. 将设备名将sda1挂载到`/media/Transfer`目录下：
>
`sudo mount /dev/sda1 /media/Transfer`
>
>这里不使用`-t`去指定对应设备的文件系统，是系统会使用`/etc/filesystems`中系统指定的尝试挂载文件系统类型，按优先顺序进行尝试，匹配成功的文件系统就进挂载。
>
>`/proc/filesystems`中的是系统已载入的文件系统。

3. 除了使用设备名还可以使用设备的UUID(比设备名更具唯一性)，进行挂载：
>
```
使用blkid找出设备或分区的UUID
pi@raspberrypi:/home $ sudo blkid /dev/sda1
/dev/sda1: LABEL="Transfer" UUID="7170-2B5B" TYPE="exfat" PARTLABEL="Basic data partition" PARTUUID="43726c47-de96-4e14-a274-97d5798293fb"
>
使用UUID进行挂载
pi@raspberrypi:/home $ sudo mount UUID="7170-2B5B" /media/Transfer
>
pi@raspberrypi:/home $ df /media/Transfer/
Filesystem     1K-blocks  Used Available Use% Mounted on
/dev/sda1       52429824 12160  52417664   1% /media/Transfer
确认挂载成功
```

4. 其它常用的命令 
>以只读的方式挂载
>
>`sudo mount -o ro /dev/sda1 /media/Transfer`
>
>把只读的挂载重新挂载为读写模式
>
>`sudo mount /media/Transfer -o rw,remount`


#### 挂载NTFS

NTFS是微软开发的文件系。但微软提供了一个非商用版本的 `ntfs-3g`可读写NTFS文件系统。LInux上实现对NTFS文凭系统主要依赖`ntfs-3g`及`fuse`工具，这两个工具很有可以linux系统默认是已经安装了的

1. 安装`ntfs-3`及`fuse `
> `sudo apt install ntfs-3g`
> 
> `sudo apt install fuse `

2. 将设备`/dev/sda2`挂载到目录`/media/ntfs`下
>
pi@raspberrypi:~ $ sudo mkdir -p /media/ntfs
>
pi@raspberrypi:~ $ sudo blkid /dev/sda2
>
/dev/sda2: LABEL="Data" UUID="4F35CAF7CAA10FF7" TYPE="ntfs" PARTLABEL="Basic data partition" PARTUUID="1181fbd8-3209-4e7a-be4a-0888462da65c"
>
>pi@raspberrypi:~ $ sudo mount -t ntfs UUID="4F35CAF7CAA10FF7" /media/ntfs
>
>pi@raspberrypi:~ $ mount | grep ntfs
/dev/sda2 on /media/ntfs type ntfs (rw,relatime,uid=0,gid=0,fmask=0177,dmask=077,nls=utf8,errors=continue,mft_zone_multiplier=1)

#### 解除挂载

`sudo umount /media/ntfs`

#### 开机自动挂载

`/etc/fstab`：为自动挂载的配置文件，当运行 `mount -a`时，会将根据`/etc/fstab` 中配置的所有挂载点都挂上。平常不要使用`mount -a`, 但可以更改`/etc/fstab`中的配置信息，实现自动挂载。

如果要将设备`/dev/sda2`中的NTFS文件系统，在开机时自动挂载到目录`/media/ntfs`下，可在`/etc/fstab`文件中增加如下的一行配置信息：

`/dev/sda2 /media/ntfs ntfs defaults 0 0`

详解：
>第一列：`/dev/sda2` 为实际的分区名称，也可以是卷标（Label）
>
>第二列：`/media/ntfs` 为挂载点
>
>第三列：`ntfs` 为此分区中的文件类型
>
>第四列：`defaults` 挂载的选项，用于设备挂载参数 
>
	auto: 系统自动挂载，fstab默认就是这个选项
	defaults: rw, suid, dev, exec, auto, nouser, and async.
	noauto 开机不自动挂载
	nouser 只有超级用户可以挂载
	ro 按只读权限挂载
	rw 按可读可写权限挂载
	user 任何用户都可以挂载
	
>第五列：`0` 当其值设置为1时，将允许dump备份程序备份；设置为0时，忽略备份操作；
>
>第六列：`0` fsck磁盘检查设置。其值是一个顺序。当其值为0时，永远不检查；而 / 根目录分区永远都为1。其它分区从2开始，数字越小越先检查，如果两个分区的数字相同，则同时检查。


[Linux mount 命令](https://www.cnblogs.com/sparkdev/p/9015312.html)

[7.3 磁盘的分区、格式化、检验与挂载](https://wizardforcel.gitbooks.io/vbird-linux-basic-4e/content/61.html)