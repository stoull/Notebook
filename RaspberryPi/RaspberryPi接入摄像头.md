# RaspberryPi接入摄像头

## 数字摄影机-Digital Cameras


数字摄影机就是将光学信号转化成数字图片的设备。设备包含光学组件-镜头（也可能无线电接收机？），光感器，图像处理芯片及软件及接口等。
数字摄影机从发明以来，发展出各个领域，各种用途的类型。从航天科研到工业，家用，到手机及嵌入式，有各种各样的电子摄像机。但主要可以从光学组件，传感器，接口，供电，软件等几个方面去区分。

* 光学组件: 主要看功能，镜头类型，长焦短焦，红外，单色，运动....
* 传感器: CMOS,CCD，一般传感器的尺寸越大，能获取到越多的光信号，图像越清晰
	- CCD（Charge Coupled Device）即电荷耦合器件的缩写
	- CMOS（Complementary Metal-Oxide Semiconductor）互补金属氧化物半导体
	- CCD传感器，电荷信号先传送，后放大，再A/D，成像质量灵敏度高、分辨率好、噪声小；处理速度慢；造价高，工艺复杂。
	- CMOS传感器，电荷信号先放大，后A/D，再传送；成像质量灵敏度低、噪声明显；处理速度快；造价低，工艺简单。
* 接口: 主要考虑带宽，线缆长度，供电，硬件适配等
	- 工业用接口有：USB (Universal Serial Bus), GigE (Gigabit Ethernet),Camera Link®..., 可见下图
	- 常用接口有：
		1. USB: 常用的电脑摄像头接口
		2. DVP: DVP(Digital Video Port)摄像头数据并口传输协议
		3. MIPI(CSI): 移动产业处理器接口(Mobile Industry Processor Interface，MIPI) CSI为(MIPI Camera Serial Interface)
* 供电: 
	- 电源适配器AC/DC adapter
	- USB,
	- 通用型之输入输出缆线(General-Purpose Input/Output (GPIO) Power Cable)
	- Power over Ethernet (PoE) Injector
	- Power over Ethernet Network Interface Card (PoE NIC)
* 软件: camera-specific Software Development Kits (SDKs), NI LabVIEW™, MATLAB®, and OpenCV.)

**History of Digital Camera:**
>
- The first digital photo camera was created in 1975 by an engineer working for the Eastman Kodak company in New York
- The Sony Mavica went on the market in 1981, but was technically not a fully digital camera and image resolution was low
- The Fujix DS-1P, developed in 1988, is often considered to be the first true digital camera. 
- In answer to the key question, When did digital cameras come out? It was in 1991 that Kodak introduced a fully digital camera, the DCS-100, a version of the Nikon F3, that produced high-quality images.
- One of the first cameras to be marketable to average citizens was the Apple QuickTake 100 in 1994.
- The LCD screen was added to digital cameras in the 1990s.
- The first cell phones with built-in digital cameras were produced in 2000 by Sharp and Samsung.
- The first interchangeable-lens fully digital camera that had a live view capacity was the Fujifilm FinePix S3 Pro. It went on the market in 2004. 

###  工业摄像机接口-Industrial Digital Camera Interface 

Digital Interface Comparison:

|DIGITAL SIGNAL OPTIONS | USB 3.1 | GigE (PoE) | 5 GigE (PoE) | 10 GigE (PoE) | CoaXPress | Camera Link|
| ----------- | -------- | -------- | -------- | -------- | -------- | -------- |
| <div> <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-1a.svg" alt="USB 3" width="60"/> <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-1b.svg" alt="USB 3" width="60"/> </div> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-2-3-4.svg" alt="GigE" width="60"/> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-2-3-4.svg" alt="GigE" width="60"/> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-2-3-4.svg" alt="GigE" width="60"/> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-2-3-4.svg" alt="GigE" width="60"/> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-5.svg" alt="CoaXPress" width="60"/> | <img src="../images/RaspberryPi/RaspberryPi接入摄像头/cameras-tb1-6.svg" alt="CoaXPress" width="60"/> |
||  USB 3.1 | GigE (PoE) | 5 GigE (PoE) | 10 GigE (PoE) | CoaXPress | Camera Link®|
|Data Transfer Rate: | 5Gb/s | 1000 Mb/s | 5Gb/s | 10Gb/s | up to 12.5Gb/s | up to 6.8Gb/s|
|Max Cable Length: | 3m (recommended) | 100m | 100m | 100m | >100m at 3.125Gb/s | 10m|
|# Devices: | up to 127 | Unlimited | Unlimited | Unlimited | Unlimited | 1|
|Connector: | USB 3.1 Micro B/USB-C | RJ45 / Cat5e or 6 | RJ45 / Cat5e or 6 | Cat7 or Optical Cabling | RG59 / RG6 / RG11 | 26pin|
|Capture Board: | Optional | Not Required | Not Required | Not Required | Optional | Required|

> -- 图表 by: edmundoptics.com

参考资料：

[IMAGING OPTICS RESOURCE GUIDE](https://www.edmundoptics.com/knowledge-center/industry-expertise/imaging-optics/imaging-resource-guide/)

[Cameras-Cameras基础介绍 by Edmund](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/camera-types-and-interfaces-for-machine-vision-applications/)

[An overview of machine vision interfaces](https://www.jai.com/machine-vision-interfaces#embedded-vision)

[Industrial Camera Interface Guide](https://www.lumenera.com/media/wysiwyg/documents/casestudies/Guide_to_Camera_Interfaces.pdf)


## RaspberryPi可用的摄像头

### USB摄像头

免驱？

USB摄像头，720P 20帧都会出问题

### CSI接口摄像头


CSI(Camera Serial Interface)是由MIPI联盟下Camera工作组指定的接口标准。CSI-2是MIPI CSI第二版，是目前广泛使用的版本。

> MIPI (Mobile Industry Processor Interface)联盟是一个开放的会员制组织。2003年7月，由美国德州仪器(TI)、意法半导体(ST）、英国ARM和芬兰诺基亚 (Nokia) 4
家公司共同成立。MIPl联盟旨在推进移动应用处理器接口的标淮化。MIPI联盟下面有不同的WorkGroup，分别定义了一系列的手机内部接口标淮，比如摄像头接口CSl显示接口DSI、射频Q接口DigRF、麦克风/喇叭接口SLIMbus等。

[MIPI - Mobile Industry Processor Interface](https://www.mipi.org)

> MIPI - Developing interface specifications for mobile and mobile-influenced products

[MIPI CSI-2®](https://www.mipi.org/specifications/csi-2)

[MIPI CSI2学习（一）：说一说MIPI CSI2](https://blog.csdn.net/u011652362/article/details/81741134)

`raspivid` 命令


### 安装摄像头

```
$ vcgencmd get_camera
supported=1 detected=1, libcamera interfaces=0
```


[Introducing the Raspberry Pi Cameras](https://www.raspberrypi.com/documentation/computers/camera_software.html#introducing-the-raspberry-pi-cameras)

`sudo apt install libcamera-apps`


### raspberrypi-guide.github.io


## RaspberryPi 上开启

`sudo raspi-config` 通过上下左右键控制选择项

`Interface Options` -> `Legacy Camera Eable/disable`

https://forums.raspberrypi.com/viewtopic.php?t=336065

`vcgencmd get_camera`
 
`raspistill`

[Building libcamera and rpicam-apps](https://www.raspberrypi.com/documentation/computers/camera_software.html#building-libcamera-and-rpicam-apps)

[Getting started with the Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)

[Working with USB webcams on your Raspberry Pi](https://raspberrypi-guide.github.io/electronics/using-usb-webcams)

[Secure Webcam streaming with MJPG-Streamer on a Raspberry Pi](https://www.sigmdel.ca/michel/ha/rpi/streaming_en.html)

`fswebcam -r 1280x720 --no-banner /home/pi/Shared/image2023-0928-1.jpg`


`ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 mage2023-0928-2.jpg`

