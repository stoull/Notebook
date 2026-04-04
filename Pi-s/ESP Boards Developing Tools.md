## ESP Boards Developing Tools


### CircuitPython

[CircuitPython](https://circuitpython.org)

[Welcome to CircuitPython!](https://cdn-learn.adafruit.com/downloads/pdf/welcome-to-circuitpython.pdf)

#### Dev tools - CircuitPython

[Mu Editor](https://codewith.mu)

### MicroPython

[MicroPython](https://micropython.org)

[MicroPython downloads](https://micropython.org/download/)

#### Dev tools - CircuitPython

1. [Thonny, Python IDE for beginners](https://thonny.org)
2. VS Code with the Pymakr Extension
3. PyCharm


## 问题记录

#### 串无打印
Ardunion时，串口一直无打印

LOLIN C3 Mini
Adafruit QT Py ESP32-C3
SparkFun Pro Micro - ESP32C3
uPesy ESP32C3 Mini
MakerGO ESP32 C3 SuperMini

* 1. 确认所选的board固件能匹配上你真实的板子的型号。eg: 在tools -> board -> esp32,下有各种板子的类型

	> 教训：买了一个 ESP32 C3 Supermini 如果选择 ESP32C3 Dev Module 的板子类型，烧录后则串口没有输出。选择MakerGO ESP32 C3 SuperMini，则串口有输出。