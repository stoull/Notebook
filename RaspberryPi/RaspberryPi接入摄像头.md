# RaspberryPi接入摄像头

### raspberrypi-guide.github.io

[Working with USB webcams on your Raspberry Pi](https://raspberrypi-guide.github.io/electronics/using-usb-webcams)

[Secure Webcam streaming with MJPG-Streamer on a Raspberry Pi](https://www.sigmdel.ca/michel/ha/rpi/streaming_en.html)

`fswebcam -r 1280x720 --no-banner /home/pi/Shared/image2023-0928-1.jpg`


`ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 mage2023-0928-2.jpg`



## 数字摄影机-Cameras

digital interfaces, power, and software

Additional factors such as bandwidth capacity, cable lengths, and additional hardware support will also be covered for each interface, as well as some examples of current camera models that are available today with these interfaces. T


图像传感器如CMOS,CCD

工商业或者科学用摄像机一般需要

System on a chip - 单片系统
### Digital Camera Interfaces

###  Industrial Digital Camera Interface 

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

[Cameras-Cameras基础介绍 by Edmund](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/camera-types-and-interfaces-for-machine-vision-applications/)

[An overview of machine vision interfaces](https://www.jai.com/machine-vision-interfaces#embedded-vision)

[Industrial Camera Interface Guide](https://www.lumenera.com/media/wysiwyg/documents/casestudies/Guide_to_Camera_Interfaces.pdf)
## USB摄像头

免驱？

USB摄像头，720P 20帧都会出问题

## CSI接口摄像头


CSI(Camera Serial Interface)是由MIPI联盟下Camera工作组指定的接口标准。CSI-2是MIPI CSI第二版，是目前广泛使用的版本。

> MIPI (Mobile Industry Processor Interface)联盟是一个开放的会员制组织。2003年7月，由美国德州仪器(TI)、意法半导体(ST）、英国ARM和芬兰诺基亚 (Nokia) 4
家公司共同成立。MIPl联盟旨在推进移动应用处理器接口的标淮化。MIPI联盟下面有不同的WorkGroup，分别定义了一系列的手机内部接口标淮，比如摄像头接口CSl显示接口DSI、射频Q接口DigRF、麦克风/喇叭接口SLIMbus等。

[MIPI - Mobile Industry Processor Interface](https://www.mipi.org)

> MIPI - Developing interface specifications for mobile and mobile-influenced products

[MIPI CSI-2®](https://www.mipi.org/specifications/csi-2)

[MIPI CSI2学习（一）：说一说MIPI CSI2](https://blog.csdn.net/u011652362/article/details/81741134)

`raspivid` 命令