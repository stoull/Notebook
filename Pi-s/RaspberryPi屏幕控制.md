# RaspberryPi屏幕控制

在Linux中使用[X视窗系统(X Window System) ](https://zh.wikipedia.org/zh-hans/X視窗系統).  使用[LightDM](https://en.wikipedia.org/wiki/LightDM)作为图形登录管理器
（Display Manager）. 使用[vcgencmd](https://elinux.org/RPI_vcgencmd_usage)控制RPI中的VideoCore GPU 相关指令.

[LightDM](https://en.wikipedia.org/wiki/LightDM)它负责管理用户登录和图形会话，而 [X视窗系统(X Window System) ](https://zh.wikipedia.org/zh-hans/X視窗系統) 是一个
图形显示系统，负责将图像绘制到屏幕上。当用户登录时，[LightDM](https://en.wikipedia.org/wiki/LightDM) 会启动  [X视窗系统(X Window System) ](https://zh.wikipedia.org/zh-hans/X視窗系統)，并创建一个新的图形会话。

所以涉及到屏幕控制的内容有`LightDM`, `xrandr`, `xset`, `vcgencmd `

	xset: 是一个更加广泛的工具，可以用来配置 X Window System 的许多方面
	xrandr: 是一个专门用于管理显示输出设备的工具，可以用来设置显示 Resolution、Frame Rate、启用或禁用显示设备等。

以及一些屏幕管理的工具如`tvservice`, `cec-client`

* CEC (Consumer Electronics Control) is a one-wire serial bus connected via HDMI and used to perform remote control functions across multiple devices.

## 屏幕开关控制

在做屏幕开关控制的时候,不同类型的屏幕之间可能会很大的一样. 有的可能正常开关,有的可能开不了或者显示错误的分辨率. 所以先用SSH连接测试,如果直接在机器上测试,可能会出现关了屏幕,然后屏幕回不来,找不到终端窗口了.

### 方法一 `vcgencmd`

使用这个方法是关闭HDMI端口,使用机器没有视频输出. 直正关闭显示器的显示器本身, 因为大部分显示器在一定的时间没有检测到视频输入,则会自动关闭显示器.

另一个问题是大部分显示器会自动测试视频信号的输入.如果有多个视频的输入, 在关闭或重新打开HDMI端口后,显示器可能会自动选择其它的视频输入进行显示.

主要下面两行指令, 如果测试可行的话,那太好了就用这个方法吧,记得关闭自动电源管理(Automating the power management),防止屏幕自动关闭, 具体方法见文章后面的 [关闭屏保或省电模式(Automating the power management)](#关闭屏保或省电模式(Automating the power management))

* `vcgencmd display_power 0`: 关闭屏幕
* `vcgencmd display_power 1`: 重新打开屏幕

**注意**: 在调用关闭屏幕的指令前,确保你能在机器上运行重新打开屏幕的指令,不然要重新启动Pi.

### 方法二 `tvservice`

使用这个方法在重打开屏幕的时候,可能会出屏幕分辨率不正确的问题:

* `tvservice --off`: 关闭屏幕
* `tvservice --preferred`: 重新打开屏幕

### 方法三 `cec-client`

强大的cec-utils是一组用于控制和管理HDMI设备的工具，特别是通过HDMI CEC（Consumer Electronics Control）协议。HDMI CEC 允许通过一条HDMI连接线控制多个设备，例如电视、音响和蓝光播放器等，使得用户可以使用一个遥控器来控制所有连接的设备。 

不仅可以控制显示器,还可控制其它的输入输出,如音量等.

一般系统没有自带需要手动安装:

`apt-get install libcec3 cec-utils`

强大.但使用起来相对复杂:

* `echo 'standby 0' | cec-client -s -d 1`: Turning your monitor off
* `echo 'on 0' | cec-client -s -d 1`: Turning your monitor on
* `echo 'as' | cec-client -s -d 1`: Set the Raspberry Pi as input as active (i.e. toggle the TV to switch input)
* `echo 'is' | cec-client -s -d 1`: Set the Raspberry Pi input as an inactive input
* `echo h | cec-client -s -d 1`: You can learn more about what you can do with CEC by running

You can also find more at [CEC-O-Matic](https://www.cec-o-matic.com) and in the [libcec faq](http://libcec.pulse-eight.com/faq).

### 方法四 `xset` `xrandr`

或许可以试试

`xrandr --output HDMI-0 --off`: 关闭HDMI
`xset dpms force off`: 关闭省电模式
`xset dpms force standby`
`xset dpms force suspend`


### 在Python在使用指令

```
from subprocess import run
run('vcgencmd display_power 0', shell=True)	# turn off the display
run('vcgencmd display_power 1', shell-True)	# turn on the display

```

### 设置定时开关屏幕

最简单的是使用crontab, 如下表示每天早上6点开屏幕,晚上11点关屏幕:

`0 6 * * * /usr/bin/vcgencmd display_power 1`
`0 23 * * * /usr/bin/vcgencmd display_power 0`

[How to automatically turn off and on your monitor from your Raspberry Pi](https://www.screenly.io/blog/2017/07/02/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi/)

## 关闭屏保或省电模式(Automating the power management)

RaspberryPi系统使用的是LightDM显示管理。

> LightDM is the display manager running in Ubuntu up to version 16.04 LTS. [更多信息-LightDM](https://wiki.ubuntu.com/LightDM)

* 1.使用编辑器打开`LightDM`的配置文件, nano或者vim

	`sudo vi /etc/lightdm/lightdm.conf`

* 2.在`Seat:*`或者`SeatDefault`下增加如下一行：

	`xserver-command=X -s 0 -p 0 -dpms`
	> `-s 0`  表示禁用屏幕保护程序（即不让屏幕进入保护状态）。 
	> `-p 0`  确保 X 服务器在没有活动时不会进入暂停状态.

* 3.重新启动机器


## AI概念解释

### xset

xset  是一个用于 X Window System 的命令行工具，主要用于设置和查询 X11 环境的各种参数。它可以在 Linux 系统中使用，包括 Raspberry Pi OS。以下是  xset  的一些常见功能： 
 
1. **查询设置**： 
   -  xset q ：查询当前的 X 设置，包括键盘、鼠标和屏幕保护程序的状态。 
 
2. **键盘设置**： 
   -  xset r rate [delay] [rate] ：设置键盘的重复延迟和重复速率。 
   -  xset r [keycode] ：启用某个键的重复功能。 
   -  xset -r [keycode] ：禁用某个键的重复功能。 
 
3. **屏幕保护程序**： 
   -  xset s [timeout] ：设置屏幕保护程序的超时时间。 
   -  xset s activate ：立即激活屏幕保护程序。 
   -  xset s reset ：重置屏幕保护程序的计时。 
 
4. **显示器设置**： 
   -  xset dpms [standby] [suspend] [off] ：设置显示器的节能模式时间。 
   -  xset +dpms ：启用 DPMS（显示电源管理信号）。 
 
5. **鼠标设置**： 
   -  xset m [accel] [threshold] ：设置鼠标的加速和阈值。 
 
通过  xset ，用户可以根据自己的需求调整图形界面的行为和性能。要获取更详细的信息，可以在终端中输入  man xset  查看手册页。


### cec-utils

cec-utils是一组用于控制和管理HDMI设备的工具，特别是通过HDMI CEC（Consumer Electronics Control）协议。HDMI CEC 允许通过一条HDMI连接线控制多个设备，例如电视、音响和蓝光播放器等，使得用户可以使用一个遥控器来控制所有连接的设备。 
 
 cec-utils  包含几个命令行工具，最常用的包括： 
 
1. **cec-client**：用于与 CEC 设备进行交互的客户端，可以发送和接收 CEC 命令。它可以用于调试和控制连接的 HDMI 设备。 
 
2. **cec-ctl**：用于控制 CEC 设备的工具，可以用来发送特定的 CEC 命令。 
 
3. **cec-standby**：用于将连接的 HDMI 设备置于待机状态。 
 
通过  cec-utils ，用户可以实现许多功能，例如开关设备、调整音量、选择输入源等，所有这些都可以通过 HDMI 连接的设备之间的相互控制来完成。 
 
如果你想要使用  cec-utils ，可以通过你的 Linux 发行版的包管理器进行安装，例如在 Raspberry Pi OS 上可以使用以下命令：
bash


sudo apt-get install cec-utils
安装后，你可以使用  cec-client  等工具来进行设备控制和调试。

### LightDM

在 Linux 中，LightDM 是一个图形登录管理器（Display Manager），它提供了一种简单、灵活和高效的方式来管理用户登录和图形会话。 LightDM 是一个轻量级的解决方案，可以运行于多个 Linux 发行版中。

LightDM 的主要特性包括：

1. **简单易用**：LightDM 使用了简洁的界面设计，易于使用和配置。
2. **高效**：LightDM 可以在短时间内启动，提高用户登录速度。
3. **灵活**：LightDM 支持多种图形桌面环境（DE），例如 GNOME、KDE 和 XFCE。
4. **安全**：LightDM 提供了强大的安全功能，例如加密登录和访问控制。

LightDM 可以与多种 Linux 发行版集成，包括 Ubuntu、Debian、Fedora 和 
openSUSE 等。它也可以与多种图形桌面环境结合使用，例如 GNOME Shell、KDE 
Plasma 和 XFCE 等。

总的来说，LightDM 是一个功能强大且易于使用的图形登录管理器，可以帮助 Linux 
发行版提供一种更好的用户体验。