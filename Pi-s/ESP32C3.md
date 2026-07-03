

可选择的板子：

```
LOLIN C3 Mini
Adafruit QT Py ESP32-C3
SparkFun Pro Micro - ESP32C3
uPesy ESP32C3 Mini
MakerGO ESP32 C3 SuperMini
```


### Esp2 C3 SuperMini


它上面有两个灯一个蓝灯，为可编程LED，另一个红灯为电源指示灯
上面也有两个按键，一个RST键，一个BOOT键。


* 蓝灯- 用户指示灯，可在代码中自由控制，用于调试或状态指示。红灯不行。
* BOOT键 - 可以作为交互按钮。RST键 不行 

蓝牙打开 - 蓝灯慢闪
蓝牙关闭 - 蓝灯长亮

WIFI已连接 - 蓝灯熄灭



[ESP - sleep functions documentation](https://docs.espressif.com/projects/esp-idf/en/v5.0/esp32c3/api-reference/system/sleep_modes.html)

[Getting Started with the ESP32-C3 Super Mini](https://randomnerdtutorials.com/getting-started-esp32-c3-super-mini/)