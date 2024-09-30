# Raspberry Pi Pico W

[Pico-series Microcontrollers](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)

[micropython.org - RPI_PICO_W](https://micropython.org/download/RPI_PICO_W/)

[Getting started with Raspberry Pi Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)

[Getting started with your Raspberry Pi Pico W](https://projects.raspberrypi.org/en/projects/get-started-pico-w)


[Raspberry Pi Pico-series Python SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf?_gl=1*12zm6yn*_ga*MTQyMzQwNzg1NC4xNzI3NTg2Njg2*_ga_22FD70LWDS*MTcyNzY2MTM3Mi40LjEuMTcyNzY2MzMwOC4wLjAuMA..)

## 使用MircoPython


## 使用MircoPython

[MicroPython documentation](https://docs.micropython.org/en/latest/index.html)

## 使用PyCharm


## 读取温湿度

```
import machine
import time
from machine import Pin
import dht

import time

led_pin = machine.Pin("LED", machine.Pin.OUT)  # GPIO pin 25 controls the onboard LED
dSensor = dht.DHT22(Pin(2))
def readDHT():
    led_pin.toggle()  # Toggle the LED state
    try:
        dSensor.measure()
        temp = dSensor.temperature()
        temp_f = (temp * (9 / 5)) + 32.0
        hum = dSensor.humidity()
        print('Temperature= {} C, {} F'.format(temp, temp_f))
        print('Humidity= {} '.format(hum))
    except OSError as e:
        print('Failed to read data from DHT sensor')


while True:
    print("Running")
    readDHT()
    time.sleep(10)
```

### 使用REPL


[Raspberry Pi Pico-series Python SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf?_gl=1*12zm6yn*_ga*MTQyMzQwNzg1NC4xNzI3NTg2Njg2*_ga_22FD70LWDS*MTcyNzY2MTM3Mi40LjEuMTcyNzY2MzMwOC4wLjAuMA..)


[Raspberry Pi Pico Pinout](https://pico.pinout.xyz)

[Raspberry Pi Pico W Pinout](https://picow.pinout.xyz)