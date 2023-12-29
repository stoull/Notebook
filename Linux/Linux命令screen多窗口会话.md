## Linux命令screen多窗口会话

在使用ssh远程Linux的时候经常会遇到一些需要在终端运行长时间，或者要一直运行的服务，这个时候如果关闭终端将会终止正在运行的任务。

screen可以通过单个ssh终端窗口，创建多个screen（背后的技术是不是虚拟出多个屏幕？！）。这些screen可用于运行各种任务，并且在我们关闭ssh终端后不会关闭，还可以可恢复和管理。这样运行在screen中的任务就可以不被ssh终端窗口关闭而被中断了。

### 安装screen

`sudo apt install screen`

`screen --version`

### 基本使用

screen 有两种管理方法，一种是在终端输入命令如创建screen：`screen -S name`，另一种是使用组合键`Control+a` + 功能键，像使用组合键`Control+a d`可退出连接的screen，这个在screen正运行任务，而不能输入指令时可用。

#### 创建Screen

`screen`: 会显示screen说明，后创建一个Screen，默认名称为设备名
`screen -S name`: 使用name创建新的Screen, name便于记录和使用恢复

#### 连接及断开Screen

- 列出已创建的Screen

使用命令`screen -ls` 或才 `screen -list`:

```
15573.jupyterNotebook	(05/07/23 04:25:53)	(Attached)
	14027.test	(05/07/23 04:06:36)	(Detached)
2 Sockets in /run/screen/S-pi.
```

- 恢复连接Screen

	使用 `screen -r ` 命令, 如：
	>
	`screen -r 15573 `
	`screen -r jupyterNotebook`

- 断开Screen:

	使用组合键：`Control+a d` 或者使用命令：`screen -d 12555`
	`[detached from 12555.pts-1.raspberrypi]`
	
- 锁定Screen及创建密码

	使用组合键control+a x锁定Screen，后面重新进入session, 将需要要输入密码：
	`Screen used by <pi> on raspberrypi.`
	使用 `password your_password` 设置密码

- 个性化Screen
	系统个性化配置文件为`/etc/screenrc` 用户个性化配置文件为：`~/.screenrc`

#### 结束Screen
- 已Attached的screen
在已Attached的screen内运行`exit`, 会终止当前screen，即`[screen is terminating]`

> 输出版本信息如： `Screen version 4.08.00 (GNU) 05-Feb-20`即安装完成

- 未Attached的screen
> `screen -S 12555 -X quit`

`-X`: means send the specified command to a running screen session.

#### 常用组合键

|组合键|使用说明|
|---|---|
|ctrl+a c|即Ctrl键+a键，之后再按下c键, 新建一个screen，并切换|
|ctrl+a '|列出当前已创建的screen|
|ctrl+a 0|按序号选择screen, 这里是切换到0号screen|
|ctrl+a A|重命名当前screen|
|ctrl+a ctrl+a|与之前的screen进行切换|
|ctrl+a S|水平分屏|
|ctrl+a I|竖屏分屏|
|ctrl+a tab |切换screen分屏|
|ctrl+a x|关闭screen分屏-closes only active window|
|ctrl+a q|to close all splits|