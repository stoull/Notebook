# DTH22及SHT3x的接线方法

接线方法

### DTH22 单总线 - SuperMini


| 模块 | SuperMini | other |
| --- | --- | ---- |
| VCC | 5V | - |
| GND | GND | - |
| Out | GPIO4 -单总线数据引脚 | - |

### SHT3x I2C - SuperMini


| 模块 | SuperMini | other |
| --- | --- | ---- |
| VCC | 3.3V | - |
| GND | GND | - |
| SDA | GPIO5（推荐）或 GPIO8（若你确认无 LED/BOOT 问题） | - |
| SCL | GPIO6（推荐）或 GPIO9（不推荐，易踩 BOOT | - |

