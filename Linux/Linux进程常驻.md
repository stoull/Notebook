
# Linux进程常驻

在使用ssh远程Linux的时候经常会遇到一些需要在终端运行长时间，或者要一直运行的服务，这个时候如果关闭终端将会终止正在运行的任务。

如果想在关闭终端之后，还想继续运之前的任务和服务，则需要用到一些像`nohup`和`screen`


## `nohup`

`nohup` 英文全称 no hang up（不挂起）, 命令用于运行程序或者命令，并忽略所有中断信号SIGHUP。SIGHUP是当前控制终端关闭时发送到进程的信号。

#### nohup启动后台进程
实例:
`nohup python3 -m http.server &`

命令将在后台运行Python的HTTP服务器，并在终端上打印作业ID和进程ID，并将标准输出定向到nohup.out

`nohup python3 -m http.server > access.log 2> error.log &`

#### 结束nohup进程

使用`ps -aux | grep " http.server" `或 `ps -def | grep "runoob.sh"` 命令来查找nohup启动的后台进程

使用`kill -9  进程号PID`来结束进程。

## `screen`

screen可以通过单个ssh终端窗口，创建多个screen（背后的技术是不是虚拟出多个屏幕？！）。这些screen可用于运行各种任务，并且在我们关闭ssh终端后不会关闭，还可以可恢复和管理。这样运行在screen中的任务就可以不被ssh终端窗口关闭而被中断了。

### 安装screen

`sudo apt install screen`
`screen --version`

### 使用screen

* 列出已创建的Screen: `screen -ls`
* 恢复连接Screen:	`screen -r name`
* 断开Screen:	使用组合键：`Control+a d` 或者使用命令：`screen -d 12555`
* 结束Screen:	在已Attached的screen内运行`exit`
未Attached的screen: `screen -S 12555 -X quit`

#### 常用组合键

|组合键|使用说明|
|---|---|
|ctrl+a c|即Ctrl键+a键，之后再按下c键, 新建一个screen，并切换|
|ctrl+a '|列出当前已创建的screen|
|ctrl+a 0|按序号选择screen, 这里是切换到0号screen|
|ctrl+a A|重命名当前screen|
|ctrl+a tab |切换screen|
|ctrl+a x|关闭screen|
|ctrl+a ctrl+a|与之前的screen进行切换|
|ctrl+a S|横屏左右分屏|
|ctrl+a I|竖屏上下分屏|

## `disown`
从当前的shell中移除或标记作业。

`disown [-h] [-ar] [jobspec ... | pid ...]`

选项：

* -h    标记每个作业标识符，这些作业将不会在shell接收到sighup信号时接收到sighup信号。
* -a    移除所有的作业。
* -r    移除运行的作业。

jobspec（可选）：要移除的作业标识符，可以是一到多个。

参数:

* jobspec（可选）：要移除的作业标识符，可以是一到多个。
* pid（可选）：要移除的作业对应的进程ID，可以是一到多个。

### 示例
`jobs -l`: 列出当前终端作业。
`disown %2`: 删除指定的作业 ，2为jobs编号。
`disown %2`: 删除指定的作业 ，2为jobs编号。
`disown -a`: 删除全部作业
`disown -h %1`: 标记1号作业在终端退出时也不停止。

> 此时前一个终端已经关闭，现在打开新终端查找该作业。
[user2@pc] pgrep -a -u user2 -f 'http.server'

**注意disown只是移除作业，并没有停止。**