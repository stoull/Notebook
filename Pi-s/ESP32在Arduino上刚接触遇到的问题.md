# ESP32在Arduino上刚接触遇到的问题

#### 1. 开发工具及框架的选择

Arduino 框架和Espressif 官方的 esp-idf 框架有什么区别？

Arduino 框架 和 Espressif 官方的 esp-idf 框架 是运行在 ESP32（如 ESP32-C3）系列芯片上的两种常见软件开发框架。

---

|              | Arduino 框架                  | esp-idf 框架                 |
|--------------|------------------------------|------------------------------|
| **开发体验**     | 简单、API抽象、高度封装           | 复杂、底层控制更强              |
| **学习曲线**     | 低（好上手）                      | 高（需理解底层原理和架构）         |
| **生态库支持**   | 丰富，很多“即插即用”库             | 官方库为主，移植第三方库难度略高      |
| **功能/性能**    | 对硬件控制简化，部分特性受限         | 性能最好，底层全部可控，官方持续更新   |
| **移植性**       | 代码易在不同平台（如Arduino Uno/MEGA）移植 | 多用于 ESP 平台                  |
| **开发工具**     | Arduino IDE/PlatformIO/ESPHome等    | ESP-IDF CLI/VSCode 插件          |

---

各开发工具对比：

---

| 工具               | 主要语言      | 学习门槛 | 灵活性 | 自动化/集成 | 适用项目         |
|------------------|------------|------|------|---------|----------------|
| **Thonny**           | Python     | 低   | 中   | 较弱     | 入门、教学、原型 |
| **Arduino IDE**      | 类 C/C++   | 低   | 中   | 一般     | DIY、初学者     |
| **ESPHome**          | YAML       | 很低 | 一般  | 极强      | 智能家居配置     |
| **esp-idf+VSCode**   | C/C++      | 高   | 极高 | 强       | 专业产品、复杂项目|

---

#### 2. 串口无打印

在Arduino中，安装好espressif的arduino-esp32开发模块后，使用Tools->Board->esp32->ESP32C3 Dev Module的开发模块，发现串口无打印，代码，波特率都正常，但无打印信息。

最后看我的板子上有：

```
HW 466AB 
ESP32-C3
Super Mini
```

的字样，最后选择其它的开发板模块,如下的开发板模块正常：

```
LOLIN C3 Mini
Adafruit QT Py ESP32-C3
SparkFun Pro Micro - ESP32C3
uPesy ESP32C3 Mini
MakerGO ESP32 C3 SuperMini
```
说明板子（HW 466AB ESP32-C3 Super Mini）与 上面的开发板的的默认串口配置（如 UART TX/RX、晶振频率、Flash size）是兼容的。

**确保板子与Arduino中所选的Arduino模块中的开发板子模块兼容**


#### 3. wifi连接不上或者不稳定

使用ESP32 C3 SuperMini中的wifi模块，经常连接不上，但使用手指头触碰天线模块就能正常连接上。

[ESP32-C3 Super Mini WiFi connection problem](https://community.home-assistant.io/t/esp32-c3-super-mini-wifi-connection-problem/785228)

**使用天线或者增加WiFi信号强度**

#### 4. 这里
























