# realVNC使用方法

# 开启nvc

`vncserver :7` 指定端口为7

```
Log file is /home/pi/.vnc/raspberrypi:1.log
New desktop is raspberrypi:1 (192.168.1.2:1)
```
# 关闭
`vncserver -kill :7`

## 查看开启的
`ps aux | grep vnc*`

`ps aux | grep vnc* | grep <username>`