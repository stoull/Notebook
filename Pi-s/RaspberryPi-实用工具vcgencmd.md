# RPI实用工具-vcgencmd


The vcgencmd tool is used to output information from the VideoCore GPU on the Raspberry Pi.

`vcgencmd` 是由树莓派基金会（Raspberry Pi Foundation）开发的工具，旨在提供与树莓派的 VideoCore GPU 相关的系统信息和控制功能。它是树莓派操作系统（如 Raspberry Pi OS）的一部分，允许用户通过命令行访问和管理硬件参数。这个工具的设计目的是方便开发者和用户监控和调试树莓派的性能。

`vcgencmd` 是一个命令行工具，用于与树莓派的 VideoCore GPU 进行交互。它可以用来访问和控制各种系统参数和状态信息，包括 CPU 温度、GPU 温度、内存使用情况、时钟频率等。这个工具通常用于性能监控和调试，尤其是在运行需要 GPU 加速的应用程序时。 


## 常用指令

* `vcgencmd get_camera`: 获取连接的摄像头信息
* `vcgencmd vcos version`: 显示VideoCore的打包及硬件版本信息
* `vcgencmd vcos log status`: 打印VideoCore各个模块的错误信息
* `vcgencmd  measure_temp`: 获取CPU内部温度
* `vcgencmd measure_temp pmic`: 获取电源管理芯片温度
* `vcgencmd measure_clock`: 获取各模块的时钟频率
	* `vcgencmd measure_clock arm`:  arm核心频率
	* `vcgencmd measure_clock core`: gpu核心频率
	* `vcgencmd measure_clock hdmi`: HDMI模块频率
* `vcgencmd get_config [configuration item|int|str]`: 获取系统配置信息
	* `vcgencmd get_config total_mem`: 获取总内存信息
* `vcgencmd display_power 0`: 关闭视频输出
* `vcgencmd display_power 1`: 打开视频输出
* `vcgencmd hdmi_status_show`: 显示 HDMI 接口的状态信息


[RPI - vcgencmd](https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd)

[eLinux - RPI vcgencmd usage](https://elinux.org/RPI_vcgencmd_usage)

[VideoCore Tools](https://github.com/nezticle/RaspberryPi-BuildRoot/wiki/VideoCore-Tools)

[vcgencmd - code](https://github.com/raspberrypi/utils/tree/master/vcgencmd)