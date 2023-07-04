# Linux查看磁盘及文件信息

## `lsblk` 列出所有的可用块设备列表

`lsblk`可所有的可用块设备列表，并且显示它们的关系。块设备包含硬盘，闪存盘，U盘, CD-ROM等

```
$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
mmcblk0     179:0    0 29.7G  0 disk 
|-mmcblk0p1 179:1    0  256M  0 part /boot
`-mmcblk0p2 179:2    0 29.5G  0 part /
```
字段说明：

* NAME: 块设备的名称
* MAJ:MIN: 主要和次要设备号
* RM: 是否是可移动(removable)设备，上面是0表示，不可移动，如果为1则表示可移动
* SIZE: 设备的容量大小信息
* RO：表示是否为只读，如果为1则表示只读
* TYPE: 表示该块设备是磁盘，或是磁盘上的一个分区。上面本例中mmcblk0为磁盘，下面两个为分区。
* MOUNTPOINT: 设备的挂载点。

#### 列出指定设备的信息:
`$lsblk -b /dev/sda`

##  `df`命令检查磁盘空间占用情况

检查磁盘空间占用情况 (并不能查看某个目录占用的磁盘大小)

命令格式：
df [option]

* -h 以容易理解的格式(给人看的格式)输出文件系统分区使用情况，例如 10kB、10MB、10GB 等。
* -k 以 kB 为单位输出文件系统分区使用情况。
* -m 以 mB 为单位输出文件系统分区使用情况。
* -a 列出所有的文件系统分区，包含大小为 0 的文件系统分区。
* -i 列出文件系统分区的 inodes 信息。
* -T 显示磁盘分区的文件系统类型。

> `df -hT`: 查看系统的分区使用情况，并显示文件系统的类型
> 
> `df -h path/to`: 查看某个目录所在分区的磁盘使用情况

##  `du`命令

显示文件或目录所占的磁盘空间

命令格式：
du [option] 文件/目录

* -h 以容易理解的格式(给人看的格式)输出文件系统分区使用情况，例如 10kB、10MB、10GB 等。
* -s 显示文件或整个目录的大小，默认单位为 kB。

> `du -hs`: 显示当前目录的大小
> 
> `du -hs path/to/file`: 显示某个目录或文件的大小
> 
> `du –hs xxxx`: 显示目录总大小，不会列出目录中的每一个文件
> 
> `du –hs xxxx/*`: 列出 xxxx下每个目录和文件所占容量

## `fdisk`命令

> `sudo fdisk -l` 列出系统下磁盘及分区信息
 >`sudo fdisk -l | grep NTFS` 只列出特定文件的文件系统

## `blkid `命令

blkid命令可以打印块设备的信息, 包含UUID等

```
/dev/mmcblk0p1: LABEL_FATBOOT="bootfs" LABEL="bootfs" UUID="35DE-9C73" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="8c0cb233-01"
/dev/mmcblk0p2: LABEL="rootfs" UUID="2aa5eb08-26a7-434c-a9f9-6ab89ea0f362" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="8c0cb233-02"
```

## `mount`命令

使用命令`mount`可列出系统已挂载的文件系统

```
如：
pi@raspberrypi:/home $ mount
/dev/mmcblk0p2 on / type ext4 (rw,noatime)
devtmpfs on /dev type devtmpfs (rw,relatime,size=1827468k,nr_inodes=97607,mode=755)
/dev/mmcblk0p1 on /boot type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
第一行：/dev/mmcblk0p2 为挂载的设备，挂载点为 / 文件系统为 ext4. rw表示可读写。
第二行：设备名称为devtmpfs，挂载在目录/dev .....
```
