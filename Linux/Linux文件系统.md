
# Linux 文件系统

## 什么是文件系统

想想数据在磁盘（硬盘、U盘、光盘）是怎么存储的。文件系统就在物理磁盘上存储及管理数据的系统。

### 特性：

* 物理磁盘分区后，需要格式化为对应的一种文件系统，之后才能在这个磁盘中进行数据的存储等操作。

	> 安装操作系统之前为什么要格式化，因为每种操作系统所设置的文件属性/权限并不相同
	
* 每种计算机操作系统能够使用的文件系统并不相同
	* Linux 的标准文件系统: ext2， ext3, ext4, XFS
	* Microsoft operating system: FAT, FAT16, FAT32, NTFS, ExFAT
	* Mac OS: Mac OS Extended(HFS+), Apple File System (APFS)

### 具体运作:

#### 索引式文件系统（indexed allocation）

实际的将文件存到磁盘，通常会有三个部分的数据存储下来：

1. 文件的属性数据， 比如文件的权限，拥有者，文件的大小，创建时间等等。
2. 文件的实际数据，比如电影每一帧的数据。
3. 文件系统自身的整体信息数据。比如文件系统的格式啊，用了多少还剩多少

文件系统用inode来存储文件的属性, data block来存储文件的实际数据，用superblock来记录filesystem的整体信息，具体信息如下：

* superblock：记录此 filesystem 的整体信息，包括inode/block的总量、使用量、剩余量， 以及文件系统的格式与相关信息等；
* inode：记录文件的属性，一个文件占用一个inode，同时记录此文件的数据所在的 block 号码；
* block：实际记录文件的内容，若文件太大时，会占用多个 block 。

磁盘在格式化的时候，会将磁盘分区分出几个区域，有一个区域用来专门存放superblock， 有一个区域专门用来存放 inode，还有一个区域专门用来存放data block。

每一个data block和data block都有编号，每一个文件都会占用一个inode，并且inode内存有实际文件数据存放的 block号码。这样找到文件的inode就能找到对应的实际文件数据位置。

> 
* inode的大小一般为128 Bytes，新的ext4或xfs可设置256 Bytes。
* 对于目录，文件系统会分配一个 inode 与至少一块 block 给该目录。其中，inode 记录该目录的相关权限与属性，并可记录分配到的那块 block 号码； 而 block 则是记录在这个目录下的文件名与该文件名占用的 inode 号码数据。
* superblock 中用block bitmap及inode bitmap存放有所有已用的及未用的 block 及 inode信息。

磁盘在格式化的时候就会把inode和data block规划好，在使用的时候是固定不变的。除非格式化的时候会重新规划。

>
* 磁盘容量大，为了方便管理，在格式化的时候基本上是区分为多个区块群组 （block group） 的，每个区块群组都有独立的 inode/block/superblock 系统
* 如果磁盘大的话，规划inode及block就需要很长的时间，格式化动作慢。XFS 文件系统的inode与 block 是系统需要用到时才动态产生，格式化动作快。
* data block 的大小，可在格式化的时候指定1K, 2K 及 4K，可根据需求选择。格式化大block考虑磁盘容量浪费，格式化小block考虑磁盘的读写性能。
* 可能会出现inode先用完，而data block没有用完的情况。

#### 查看文件系统信息

```
[root@study ~]# dumpe2fs [-bh] 设备文件名
选项与参数：
-b ：列出保留为坏轨的部分（一般用不到吧！？）
-h ：仅列出 superblock 的数据，不会列出其他的区段内容！
```

`blkid &lt;==` 这个指令可以叫出目前系统有被格式化的设备

`fdisk -lu` 查看当前盘的每个分区情况

`dumpe2fs /dev/sda2` 可列出文件系统信息

#### 非索引式文件系统（indexed allocation）
Windows中的FAT文件系统就不是索引式文件系统,像是一个链式系统，每一个数据块都存放下一个数据块的索引
闪存文件系统：JFFS2与YAFFS

 `磁盘碎片整理`，`磁盘重组` 这些概念就是因为非索引式文件系统的数据块太过离散，需要将block进行整理，提高读性性能。索引式文件系统就较少需要进行碎片整理。

### 文件的写入过程

假设我们想要新增一个文件，此时文件系统的行为是：

1. 先确定使用者对于欲新增文件的目录是否具有 w 与 x 的权限，若有的话才能新增；
2. 根据 inode bitmap 找到没有使用的 inode 号码，并将新文件的权限/属性写入；
3. 根据 block bitmap 找到没有使用中的 block 号码，并将实际的数据写入 block 中，且更新 inode 的 block 指向数据；
4. 将刚刚写入的 inode 与 block 数据同步更新 inode bitmap 与 block bitmap，并更新 superblock 的内容。

#### 日志式文件系统 （Journaling filesystem）
如果系统在上述文件的写入过程中遇到断电，完成了第三步而没有完成第四步，就会产生superblock中的记录与实际的数据不一致。操作系统在开机的时候就会进行数据检查。全盘检查很费时，日志式文件系统的出现用来简化一致性检查的步骤。日志式文件系统会规划出一个区域，用来记录文件写入或修改时的步骤。如下：
>
1. 预备：当系统要写入一个文件时，会先在日志记录区块中纪录某个文件准备要写入的信息；
2. 实际写入：开始写入文件的权限与数据；开始更新 metadata 的数据；
3. 结束：完成数据与 metadata 的更新后，在日志记录区块当中完成该文件的纪录。

如果出现不一致的问题，只要查日志记录区块就可以了，需不要全盘检查。

## 文件系统的类型
* 传统文件系统：ext2 / minix / MS-DOS / FAT （用 vfat 模块） / iso9660 （光盘）等等；
* 日志式文件系统：ext3 /ext4 / ReiserFS / Windows' NTFS / IBM's JFS / SGI's XFS / ZFS / APFS
* 网络文件系统：NFS, SMBFS, SMB, CIFS, WebDAV, AFP

## 不同的操作系统支持不同的文件系统

### Linux 系统 VFS

很多硬盘插上就能用，而不用我们指定用什么文件系统去读取。这是VFS(Virtual Filesystem Switch)核心功能在帮忙做文件系统的读取工作。整个 Linux 认识的 filesystem 都是 VFS 在进行管理，VFS自动检测分区上的文件系统类型。

查看Linux支持的文件系统： `ls -l /lib/modules/$(uname -r)/kernel/fs`

查看Linux已载入到内存中的支持的文件系统： `cat /proc/filesystems`


**主要是下面的学习资料记录：**

[鸟哥私房菜 - 7.1 认识 Linux 文件系统](https://wizardforcel.gitbooks.io/vbird-linux-basic-4e/content/59.html)

[漫谈Linux标准的文件系统(Ext2/Ext3/Ext4)](https://www.cnblogs.com/justmine/p/9128730.html)

[一口气搞懂「文件系统」，就靠这 25 张图了](https://segmentfault.com/a/1190000023615225)