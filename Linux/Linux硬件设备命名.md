
## EVerythins is a file

[Everything is a file](https://en.wikipedia.org/wiki/Everything_is_a_file)

[Device file](https://en.wikipedia.org/wiki/Device_file)

[Everything is a file?](https://unix.stackexchange.com/questions/225537/everything-is-a-file)
>The "Everything is a file" phrase defines the architecture of the operating system. It means that everything in the system from processes, files, directories, sockets, pipes, ... is represented by a file descriptor abstracted over the virtual filesystem layer in the kernel. The virtual filesytem is an interface provided by the kernel. Hence the phrase was corrected to say "Everything is a file descriptor". Linus Torvalds himself corrected it again a bit more precisely: "Everything is a stream of bytes".
>
>	-- by chaos



### 设备硬件命名

几乎所有的硬件设备文件（硬盘及分区，打印机，蓝牙耳机）都存放在/dev目录内。常见设备的命名：

|  设备   | 在Linux内的文件名  |
|  ----  | ----  |
| SCSI/SATA/USB硬盘机  | /dev/sd[a-p] |
| VirtI/O界面  | /dev/vd[a-p] （用于虚拟机内） |
| 软盘机 | /dev/fd[0-7] | 
| 打印机 | /dev/lp[0-2] （25针打印机） /dev/usb/lp[0-15] （USB 接口） | 
| 鼠标 | /dev/input/mouse[0-15] （通用） /dev/psaux （PS/2界面） /dev/mouse （当前鼠标） | 
| CDROM/DVDROM | /dev/scd[0-1] （通用） /dev/sr[0-1] （通用，CentOS 较常见） /dev/cdrom （当前 CDROM） | 
| 磁带机 | /dev/ht0 （IDE 界面） /dev/st0 （SATA/SCSI界面） /dev/tape （当前磁带） | 
| IDE硬盘机 | /dev/hd[a-d] （旧式系统才有） | 
| 控制终端 | tty(teletype) | 