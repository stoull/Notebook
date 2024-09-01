# RaspberryPi接入CSI摄像头


## 摄像头购买及安装

### 购买官方的摄像头
RsPI的摄像头模组已经出了好几个版本了, Camera Module 1 2013, Camera Module 2 2016, Camera Module 3 2023

* **Camera Module 1**  5-megapixel (停产) 发布于 2013年
* **Camera Module 2** 8-megapixel , with or without an infrared filter 发布于 2016年 
* **Camera Module 3** 12-megapixel , with both standard and wide lenses, with or without an infrared filter发布于 2023年
*  the 12-megapixel **High Quality Camera** with CS and M12 mount variants for use with external lenses
*  the 1.6-megapixel **Global Shutter Camera** for fast motion photography

具体硬件详情可参考：[Camera - 硬件信息](https://www.raspberrypi.com/documentation/accessories/camera.html)

### 其它三方的摄像头

购买三方摄像头的时候，需要确认Pi是否支持对应摄像头的芯片。  检查软件`libcamera`支持的摄像头，是否支持对应的购买的摄像头。可见如下`软件`->`libcamera`。

## 安装

可以先看[Camera - Connect the Camera](https://www.raspberrypi.com/documentation/accessories/camera.html#about-the-camera-modules)这里有Connect the Camera的章节里面有安装视频。

在RaspberryPi OS中，不像使用BIOS为初始化系统， 而是通过配置`config.txt`文件，系统在启动的时候读取`config.txt`文件中的信息来初始化系统的一些能力,像加载不同硬件的驱动。

`config.txt`文件中有一个dtoverlay的配置项,用于加载不同的摄像头硬件。

>
dtoverlay是树莓派（Raspberry Pi）配置中的一个参数，用于动态覆盖设备树（Device Tree）。设备树是描述硬件配置的数据结构，在Linux内核启动过程中被加载，用于初始化硬件设备。dtoverlay允许用户在不需要修改内核的情况下，通过加载额外的设备树覆盖层来扩展或修改硬件配置。
>	
在树莓派中，dtoverlay参数通常用于启用或配置特定的硬件设备，例如摄像头、显示屏、音频接口等。通过在配置文件中添加dtoverlay行，并指定要加载的设备树覆盖层的名称，可以告诉内核在启动过程中加载相应的设备树覆盖层，从而实现对硬件设备的支持和配置。
>	
例如，dtoverlay=vc4-kms-v3d表示加载名为vc4-kms-v3d的设备树覆盖层，该覆盖层用于启用VC4显卡的DRM（Direct Rendering Manager）驱动，以充分利用树莓派上的图形硬件资源。

如果是官方的摄像头设置如下即可：

```
# Automatically load overlays for detected cameras
start_x=1
...
[pi4]
camera_auto_detect=1
dtoverlay=vc4-fkms-v3d
# Run as fast as firmware / board allows
arm_boost=1
```

如果是非官方的摄像头，如`IMX290`, 则应设置如下：

```
# Automatically load overlays for detected cameras
start_x=1
...
[pi4]
camera_auto_detect=0
dtoverlay=vc4-fkms-v3d
dtoverlay=imx290,clock-frequency=37125000
# Run as fast as firmware / board allows
arm_boost=1
```

`camera_auto_detect=1`是表示系统会自动加载任何连接着的摄像头。
`dtoverlay=vc4-fkms-v3d` fake KMS

`config.txt`更改完需要重启才生效。目录位置`/boot/config.txt`

摄像头型号与设备树对照表：

| 型号 | dtoverlay语句 | 
| --- | --- |
| OV9281 | dtoverlay=ov9281 |
| IMX290/IMX327 | dtoverlay=imx290,clock-frequency=37125000 |
| IMX378 | dtoverlay=imx378 |
| IMX219 | dtoverlay=imx219 |
| IMX477 | dtoverlay=imx477 |
| IMX462 | dtoverlay=imx462 |

### 开启系统的Legacy Camera接口

如果使用的是旧款摄像头模块，需要开启这个接口，方法如下：

`sudo raspi-config` 通过上下左右键控制选择项

`Interface Options` -> `Legacy Camera Eable/disable`


#### Modern vs Legacy camera interface:

The legacy camera interface, still used/needed for some camera software, requires `start_x=1` to be set and does not work if KMS is enabled, but only with the legacy framebuffer graphics stack (no `dtoverlay=vc4-kms-v3d`).

The modern camera stack only works with KMS (`dtoverlay=vc4-kms-v3d`) enabled. `camera_auto_detect=1` enables modern camera support in a generic way, so the camera model is automatically detected and no dedicated overlay needs to be enabled explicitly.

资料： *[What is config.txt?](https://www.raspberrypi.com/documentation/computers/config_txt.html)	*[Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)	*[Connect to the Raspberry Pi](https://docs.arducam.com/Raspberry-Pi-Camera/Low-Light/quick-start/)

## 软件

### libcamera

>
新系统的摄像头系统已经切换成Modern camera - `libcamera `. Legacy camera 已经从64-bit的系统中移除，32-bit的系统还在用
>
新的摄像头应用程序`libcamera-still`和`libcamera-vid`取代了`raspistill`和`raspivid`

`libcamera`支持的摄像头(芯片型号)：

	官方摄像头:
		· OV5647 (V1)
		· IMX219 (V2)
		· IMX477 (HQ)
		· IMX296 (GS)
		· IMX708 (V3)

	第三方摄像头:
		· IMX290
		· IMX327
		· IMX378
		· IMX519
		· OV9281

`OV5647`是OmniVision公司生产的一款高分辨率、高性能的CMOS图像传感器，常见于各种智能手机、平板电脑以及物联网设备的摄像头模块中。[OV5647 datasheet 翻译文档](https://www.zybuluo.com/SiberiaBear/note/52744)

IMX序列是索尼公司制造的图像传感器，`IMX219`是一款由索尼公司制造的高性能CMOS图像传感器，主要用于彩色摄像头，特别是应用于手机和平板电脑。[IMX219](https://developer.sony.com/vision-sensing-processor/hardware-overview/sensors/cmos/imx219)

### rpicam-apps

> 在新的RaspberryPi OS系统Debian version: 12 (bookworm)中将`libcamera-*` 更名为 `rpicam-*`， 而在以前的系统如Debian version: 11 (bullseye)， 中仍使用`libcamera-*`

[Operating system images](https://www.raspberrypi.com/software/operating-systems/)

#### `rpicam-apps`基于`libcamera`进行开发的工具，包含以下功能：

* `rpicam-hello`: A "hello world"-equivalent for cameras, which starts a camera preview stream and displays it on the screen.
* `rpicam-jpeg`: Runs a preview window, then captures high-resolution still images.
* `rpicam-still`: Emulates many of the features of the original raspistill application.
* `rpicam-vid`: Captures video.
* `rpicam-raw`: Captures raw (unprocessed Bayer) frames directly from the sensor.
* `rpicam-detec`t: Not built by default, but users can build it if they have TensorFlow Lite installed on their Raspberry Pi. Captures JPEG images when certain objects are detected.


### 检测及测试摄像头

**注意在新版本中`libcamera`更名为`rpicam`。**

如没有安装`libcamera`， 使用命令： `sudo apt install libcamera-apps`进行安装。

**常用测试指令：**

* `vcgencmd get_camera`: 检测当时连接的摄像头信息
* `libcamera-hello --list-cameras`: 检测当时连接的摄像头信息
* `libcamera-still -o ./libcamera-still-test.jpg`: 测试拍摄一张libcamera-still-test.jpng照片,存到当前目录下。
*  `libcamera-vid -t 10000 -o ~/Shared/video.h264`: 测试录制一个10s的视频，PI5中`rpicam`可直接输出为mp4, `rpicam-vid  -t 10s -o test.mp4`

使用 `vcgencmd get_camera`，如果如下信息，则表示成功识别到摄像头：

```
$ vcgencmd get_camera
supported=1 detected=1, libcamera interfaces=1
or 
supported=1 detected=0, libcamera interfaces=1
```

```
$ libcamera-hello --list-cameras
Available cameras
-----------------
0 : ov5647 [2592x1944] (/base/soc/i2c0mux/i2c@1/ov5647@36)
    Modes: 'SGBRG10_CSI2P' : 640x480 [58.92 fps - (16, 0)/2560x1920 crop]
                             1296x972 [43.25 fps - (0, 0)/2592x1944 crop]
                             1920x1080 [30.62 fps - (348, 434)/1928x1080 crop]
                             2592x1944 [15.63 fps - (0, 0)/2592x1944 crop]
```

#### 问题记录

```
:~ $ vcgencmd get_camera
supported=1 detected=0, libcamera interfaces=1
:~ $ libcamera-hello --list-cameras
No cameras available!
```

解决方法：

检查摄像头有没有连接好


## 参考资料


[Camera Software](https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started)

[Building libcamera and rpicam-apps](https://www.raspberrypi.com/documentation/computers/camera_software.html#building-libcamera-and-rpicam-apps)

[Getting started with the Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)

[Working with USB webcams on your Raspberry Pi](https://raspberrypi-guide.github.io/electronics/using-usb-webcams)

[Secure Webcam streaming with MJPG-Streamer on a Raspberry Pi](https://www.sigmdel.ca/michel/ha/rpi/streaming_en.html)

`fswebcam -r 1280x720 --no-banner /home/pi/Shared/image2023-0928-1.jpg`


`ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 mage2023-0928-2.jpg`



[参考 - raspistill: command not found 树莓派4B无法使用raspistill命令](https://blog.csdn.net/weixin_51245887/article/details/124692953?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-5-124692953-blog-130135257.235^v43^pc_blog_bottom_relevance_base7&spm=1001.2101.3001.4242.4&utm_relevant_index=8)



这里这里：[Pi camera module 3 - libcamera cant detect camera](https://dietpi.com/forum/t/pi-camera-module-3-libcamera-cant-detect-camera/17009/10)

```
dtoverlay=vc4-kms-v3d
camera_auto_detect=1
```
or

```
dtoverlay=vc4-kms-v3d
dtoverlay=imx708
```