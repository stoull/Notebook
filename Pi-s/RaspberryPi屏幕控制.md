# RaspberryPi屏幕控制


## 关闭屏保

RaspberryPi系统使用的是LightDM显示管理。

> LightDM is the display manager running in Ubuntu up to version 16.04 LTS. [更多信息-LightDM](https://wiki.ubuntu.com/LightDM)

* 1.使用编辑器打开`LightDM`的配置文件, nano或者vim

	`sudo vi /etc/lightdm/lightdm.conf`

* 2.在`Seat:*`或者`SeatDefault`下增加如下一行：

	`xserver-command=X -s 0 -p 0 -dpms`
	> `-s 0`  表示禁用屏幕保护程序（即不让屏幕进入保护状态）。 
	> `-p 0`  确保 X 服务器在没有活动时不会进入暂停状态.

* 3.重新启动机器

## 代码控制屏屏幕开关

[How to Turn a Raspberry Pi Display Off & On Using a Python Script, + How to Disable the ScreenSaver](https://www.youtube.com/watch?v=lETqSCimcyM)