# Linux启动磁盘配置文件表(File System Table)-fstab

### 系统启动时配置的文件`/etc/fstab` :

* 英文名称是 Linux File System Table。
* `/etc/fstab` 是启动时的配置文件 ,可以自动挂载各种文件系统格式的硬盘、分区、可移动设备和远程设备等。
* 记录在系统启动时需要自动挂载的文件系统，被`mount`命令执行，时需要自动配置的Swap分区, 被`swapon`命令执行。所以实际文件系统是挂载到`/etc/mtab`,`/proc/mounts`
* 文件路径为`/etc/fstab`，它是一个文本文件，文件的权限需要为644,即所有的用户只读，root权限可读写。
* 系统因为缺失fstab文件不能正常启动，只能先进入单用户模式，创建修复fstab文件。

> Linux中Swap（即：交换分区），类似于Windows的虚拟内存，就是当内存不足的时候，把一部分硬盘空间虚拟成内存使用,从而解决内存容量不足的情况
> 
> 根目录/是一定在要系统启动时挂载的，如果挂载失败，系统会启动失败。根目录的挂载和其它的`mount`有区别。
 
### `/etc/fstab`文件中字段解释

```
# <Device>   <Mount Point>    <File System Type>      <Options>      <Backup Operation/File System Check Order>
proc            /proc           proc    defaults          0       0
PARTUUID=8c0cb233-01  /boot           vfat    defaults          0       2
PARTUUID=8c0cb233-02  /               ext4    defaults,noatime  0       1
# a swapfile is not a swap partition, no line here
#   use  dphys-swapfile swap[on|off]  for that
```

- `Device`: 挂载设备, 一般使用设备名或者UUID,像名称：`/dev/disk2s1/etc` UUID: `2aa5eb08-26a7-434c-a9f9-6ab89ea0f362`。
	> 因设备名并非总是不变的，所以建议使用设备的UUID, 能过`blkid`命令可获得UUID。UUID为系统中的存储设备提供唯一的标识字符串，可避免启动的时候因为找不到设备而失败。
	> 使用`sudo fdisk -l`列出可挂载的设备，在mac下使用`sudo diskutil list`

- `Mount Point`: 挂载点，必须是目录
- `File System Type`: Linux支持许多文件系统。 要得到一个完整的支持名单查找mount man-page。典型 的名字包括这些：ext2, ext3, reiserfs, xfs, jfs,iso9660, vfat, ntfs, swap和auto, 'auto' 不是一个文件系统，而是让mount命令自动判断文件类型，特别对于可移动设备，软盘，DVD驱动器，这样做是很有必要的，因为可能每次挂载的文件类型不一致。
- `Options`: 文件系统参数：这部分是最有用的设置！！！ 它能使你所挂载的设备在开机时自动加载、使中文显示不出现乱码、限制对挂载分区读写权限。它是与mount命令的用法相关的，要想得到一个完整的列表，参考mount manpage. 如果使用多个值，须用逗号隔开','
- `Backup Operation`: 备份命令：dump utility用来决定是否做备份的. dump会检查entry并用数字来决定是否对这个文件系统进行备份。允许的数字是0和1。如果是0，dump就会忽略这个文件系统，如果是1，dump就会作一个备份。大部分的用户是没有安装dump的，所以对他们而言<dump>这个entry应该写为0。
- `File System Check Order`:  是否以fsck检验扇区：启动的过程中，系统默认会以fsck检验我们的 filesystem 是否完整 (clean)。 不过，某些 filesystem 是不需要检验的，例如内存置换空间 (swap) ，或者是特殊文件系统例如 /proc 与 /sys 等等。fsck会检查这个头目下的数字来决定检查文件系统的顺序，允许的数字是0, 1, 和2。0 是不要检验， 1 表示最早检验(一般只有根目录会配置为 1)， 2 也是要检验，不过1会比较早被检验啦！一般来说,根目录配置为1,其他的要检验的filesystem都配置为 2 就好了。

#### Options常用参数

* `noatime` 关闭atime特性，提高性能，这是一个很老的特性，放心关闭，还能减少loadcycle
* `defaults` 使用默认设置。等于rw,suid,dev,exec,auto,nouser,async，具体含义看下面的解释。
* 自动与手动挂载:
`auto` 在启动或在终端中输入mount -a时自动挂载
`noauto` 设备（分区）只能手动挂载
* 读写权限:
	> `ro` 挂载为只读权限
	> 
	> `rw` 挂载为读写权限

* 可执行:
	> `exec` 是一个默认设置项，它使在那个分区中的可执行的二进制文件能够执行
	>  `noexec` 二进制文件不允许执行。千万不要在你的root分区中用这个选项
 
* I/O同步:
	> `sync` 所有的I/O将以同步方式进行
	> `async` 所有的I/O将以非同步方式进行
* 户挂载权限:
	> `user` 允许任何用户挂载设备。 Implies noexec,nosuid,nodev unless overridden.
	> `nouser` 只允许root用户挂载。这是默认设置。
* 临时文件执行权限：
	> `suid` Permit the operation of suid, and sgid bits. They are mostly used to allow users on a computer system to execute binary executables with temporarily elevated privileges in order to perform a specific task.（允许suid和sgid位的操作。它们主要用于允许计算机系统上的用户执行具有临时提升权限的二进制可执行文件，以执行特定任务。）
* `nosuid` Blocks the operation of suid, and sgid bits.（阻止suid和sgid位的操作。）

### `/etc/fstab` 示例

* `/media`: 用来挂载可移动设备的
* `/mnt`: 临时挂载点，给管理员临时手动挂载用

`/dev/disk2s1	/dev/sda1	vfat	defaults	0	0`

使用UUID自动挂载NTFS硬盘：
`2aa5eb08-26a7-434c-a9f9-6ab89ea0f362	/media/Movie	ntfs3	defaults	0	0`


### `/etc/fstab`文件生效
* 重启系统
* `mount -a`, 如果文件中的option配置的是自动挂载，此命令会自动执行

### Linux启动时根文件系统的初始化
内核代码启动完之后，linux进入加载根文件系统的阶段：

根文件系统首先本身是个普通又特殊的文件系统，普通是指，具有普通文件系统的存储数据文件的功能，里面存储着许多目录和文件

特殊是指，它是linux启动后第一个挂载的文件系统：

> 根文件系统之所以在前面加一个”根“，说明它是加载其它文件系统的”根“，既然是根的话，那么如果没有这个根，其它的文件系统也就没有办法进行加载的。它包含系统引导和使其他文件系统得以挂载（mount）所必要的文件。根文件系统包括Linux启动时所必须的目录和关键性的文件，例如Linux启动时都需要有init目录下的相关文件，在 Linux挂载分区时Linux一定会找/etc/fstab这个挂载文件等，根文件系统中还包括了许多的应用程序bin目录等，任何包括这些Linux 系统启动所必须的文件都可以成为根文件系统。Linux启动时，第一个必须挂载的是根文件系统；若系统不能从指定设备上挂载根文件系统，则系统会出错而退出启动。成功之后可以自动或手动挂载其他的文件系统。因此，一个系统中可以同时存在不同的文件系统。在 Linux 中将一个文件系统与一个存储设备关联起来的过程称为挂载（mount）。使用 mount 命令将一个文件系统附着到当前文件系统层次结构中（根）。在执行挂装时，要提供文件系统类型、文件系统和一个挂装点。根文件系统被挂载到根目录下“/”上后，在根目录下就有根文件系统的各个目录，文件：/bin /sbin /mnt等，再将其他分区挂接到/mnt目录上，/mnt目录下就有这个分区的各个目录，文件

若系统不能从指定设备上挂载根文件系统，则系统会出错而退出启动。如果正常挂载根文件系统，就可以执行用户态的指令了，比如最经典的，我们就会进入shell, 就可以操作各个文件和目录了。至此，欢迎来到linux的世界。

> 文件系统是kernel的一部分。文件系统实现了系统上存储介质和其他资源的交互。kernel tree中的fs目录都是关于文件系统的，可以说它是kernel的一个大子系统。

> 嵌入式系统在flash中分配了存放内核、根文件系统的区域。bootloader加载了内核，内核启动，加载文件系统，进入Linux系统。

> 整个嵌入式系统而言，可以分为三个部分1.uboot 2.kernel 3.文件系统。其中kernel中以VFS去支持各种文件系统，如yaffs，ext3，cramfs等等。yaffs/yaffs2是专为嵌入式系统使用NAND型闪存而设计的一种日志型文件系统。在内核中以VFS来屏蔽各种文件系统的接口不同，以VFS向kernel提供一个统一的接口。如打开一个文件时统一使用open，写时采用write，而不用去考虑是那种文件系统，也不用去考虑文件系统是如何将数据写入物理介质的。其中 kernel中的配置，只是让VFS支持这种接口。

Linux启动时根文件系统的初始化 来自 [疾速瓜牛
 - 系统启动知识 (三) linux的启动之根文件系统的初始化](https://www.cnblogs.com/Arnold-Zhang/p/15808400.html)

[Linux 磁盘配置文件 /etc/fstab 详解](https://juejin.cn/post/7110032451472195620)

[An introduction to the Linux /etc/fstab file](https://www.redhat.com/sysadmin/etc-fstab)

[配置启动挂载：fstab文件详解](https://www.cnblogs.com/augusite/p/10930793.html)