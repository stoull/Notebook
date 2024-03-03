# Mac上读写NTFS


## 安装macFUSE
* 法一、 下载并安装最新的mac版FUSE [http://osxfuse.github.io. ](http://osxfuse.github.io)
这个步骤需要重启mac，安装后打开设置app, 在最底部可以找到`macFUSE`,能找到就可以
	
	也可以是在[macFUSE](https://osxfuse.github.io)网站上

* 法二、 使用HomeBrew 安装 `NTFS-3G`
>
```
brew install --cask macfuse
brew tap gromgit/homebrew-fuse
brew install ntfs-3g-mac 
```

### 查看是否安装成功


* Intel芯片电脑：`/usr/local/bin/ntfs-3g --version`
* M芯片电脑：`/opt/homebrew/Cellar/ntfs-3g-mac/2022.10.3/bin/ntfs-3g --version` 注意版本号2022.10.3

如果重新运行`brew install ntfs-3g-mac` 会看到如下的告警信息，`2022.10.3`就是对应的版本

```
Warning: gromgit/fuse/ntfs-3g-mac 2022.10.3 is already installed and up-to-date.
To reinstall 2022.10.3, run:
  brew reinstall ntfs-3g-mac
```

### 权限管理 (需要重新启动)

在首次挂载的时候，弹出权限提示，并且报错: `mount_macfuse: the file system is not available (1)`

**System Settings** -> **Privacy & Security** -> `System software rom developer "Benjamin Fleischer" was blocked from loading.` -> **Allow** -> **Restart Mac**


## 挂载NTFS

3. 手动挂载NTFS. **注意：将disk4s2更换为对应的分区**

> 1. 使用`diskutil list`查看分区信息
> 2. 如果NTFS磁盘已被系统自动挂载，先卸载对应的磁盘分区
> `sudo diskutil unmount /dev/disk4s2`	(或手动推出，如将桌面上的磁盘拉到垃圾桶)
> 3. 新建一个目录用来挂载磁盘(这个文件夹在硬盘弹出后，会被移除)
> `sudo mkdir /Volumes/NTFS`
> 4. 以读写模式挂载NTFS 磁盘
> `sudo /usr/local/bin/ntfs-3g /dev/disk2s1 /Volumes/NTFS -o local -o allow_other -o auto_xattr -o auto_cache`
> `sudo /opt/homebrew/Cellar/ntfs-3g-mac/2022.10.3/bin/ntfs-3g /dev/disk4s1 /Volumes/NTFS -o local -o allow_other -o auto_xattr -o auto_cache`
> 或者 `sudo /usr/local/sbin/mount_ntfs /dev/disk4s2 /Volumes/NTFS`
> 5. 或者：`sudo ntfs-3g /dev/disk8s1 /Volumes/NTFS -o local -o allow_other -o auto_xattr -o auto_cache`

这样就会挂载一个名为NTFS的磁盘，可进行读写操作，使用`mount`查看对应的信息为：
`/dev/disk4s2 on /Volumes/NTFS (macfuse, local, synchronous, noatime)`

4. 卸载
`sudo diskutil unmount /dev/disk4s2`

## 方案二 使用Boot Camp Assistant安装windows系统
> 用Boot Camp Assistant在mac安装一个windows系统，这样就可以读写NTFS了