# Raspberrypi使用DHT22测温湿度.md



    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 9)


在“Raspberry Pi HATs & pHATs”中，HAT代表“硬件附加顶部”（Hardware Attached on Top），是一种标准化的扩展板设计，具有特定的功能和接口，能够与Raspberry Pi主板进行更好的兼容和连接。pHAT则是“小型硬件附加顶部”（Partial HAT），是HAT的简化版本，通常用于更小的扩展板，功能上类似但在某些方面有所限制。两者都是为Raspberry Pi提供扩展功能的模块。

[Pinout! - The Raspberry Pi GPIO pinout guide.](https://pinout.xyz)

[Raspberry Pi HATs, pHATs & Add-ons](https://pinout.xyz/boards/)

[GPIO的使用](https://www.yahboom.com/public/upload/upload-html/1639362579/5.1%20GPIO的使用.html)

[Python库-Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)

[在树莓派3/4上读取DHT11温湿度传感器-Python代码实现及常见问题梳理](https://www.cnblogs.com/hilary0614/p/dht11.html)