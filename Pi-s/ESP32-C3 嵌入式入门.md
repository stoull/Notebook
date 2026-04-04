# ESP32-C3 Get Started



[ESP32-C3 SuperMini 嵌入式入门](https://www.cnblogs.com/wuqiyang/p/18932737)

[Getting Started With ESP32-C3 Super Mini](https://www.youtube.com/watch?v=V9I9koQ0AeA)

[ESP-IDF Programming Guide - Wi-Fi Driver]()


```

esptool -p /dev/cu.usbmodem101 flash-id

esptool --chip esp32c3 --port /dev/cu.usbmodem101 erase_flash

esptool.py --port /dev/ttyUSB0 erase_flash

esptool --chip esp32c3 --port COM4 --baud 460800 write_flash -z 0x0 D:\\路径\\固件名.bin


esptool --chip esp32c3 --port /dev/cu.usbmodem101 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC_C3-20251209-v1.27.0.bin

esptool --port /dev/cu.usbmodem101 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC_C3-20251209-v1.27.0.bin


```