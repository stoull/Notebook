# RaspberryPi安装MQTT服务

## MQTT的基础概念

**MQTT Broker** ： 即mqtt的服务器， 是负责处理客户端请求的关键组件，包括建立连接、断开连接、订阅和取消订阅等操作，同时还负责消息的转发。

**MQTT 客户端**： 任何连接mqtt的服务器的设备都是客户端。客户端可发布数据也可以订阅数据。

**MQTT 发布/订阅**： MQTT 客户端之间的不同数据，通过MQTT Broker，以发布/订阅的形式在各个设备之间进行发送和接收。

**MQTT 主题**： 客户端之间有不同的数据，主题即对某种数据进行分类，如汽车中的速度，调的温度等。这样不同的客户端可以根据对应的主题发布或订阅所需要的数据。

## 热门开源的MQTT Broker

* [emqx - EMQX](https://github.com/emqx/emqx)
* [eclipse - Mosquitto](https://github.com/eclipse/mosquitto)
* [nanomq - nanomq](https://github.com/nanomq/nanomq)
* [HiveMQ - Enterprise MQTT Platform](https://github.com/hivemq)

还有一些在线的mqtt平台

* [EMQX - 免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)
* [Adafruit Io](https://io.adafruit.com/)

## 安装使用Mosquitto

这里选择安装使用Mosquitto，因为轻量方便，使用的人也不少。安装[Mosquitto - Download](https://mosquitto.org/download/)。这里的安装包含mqtt broker及client, client可以用测试。

### 安装mqtt broker

* `sudo apt update`
* `sudo apt upgrade`
* `sudo apt-get install mosquitto`: 安装mqtt broker服务端
* `sudo apt-get install mosquitto-clients`: 安装对应的客服端（如没有需要可以不用安装, 安装了可以用来测试）

安装后`mosquitto broker`服务就直接启动了，可以使用`systemctl`来查看及控制mosquitto服务。

* `systemctl status mosquitto.service`： 查看对应的状态
	* `sudo systemctl enable mosquitto.service`： 将服务添加到开机启动，注意使用的使用账户权限，以防安全问题。
	* `sudo systemctl stop mosquitto.service`： 将服务stop
	* `sudo systemctl start mosquitto.service`： 开始服务
* `mosquitto -v`: 查看服务的详细信息，可以看到使用的是1883端口
* `netstat -nlpt|grep 1883`: 查看端口的使用情况

#### macOS上安装
如果是在macOS上，可以使用`brew install mosquitto`进行安装

```
$brew install mosquitto

==> Caveats
==> mosquitto
mosquitto has been installed with a default configuration file.
You can make changes to the configuration by editing:
    /opt/homebrew/etc/mosquitto/mosquitto.conf

To start mosquitto now and restart at login:
  brew services start mosquitto
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

### 测试

安装完`mosquitto`及`mosquitto-clients`后，可以在两个终端，一个终端订阅信息，另一个终端发布信息测试整个mqtt的功能。

* `mosquitto_sub -d -t "binary/updates"`: 订阅终端订阅`binary/updates`主题
* `mosquitto_pub -d -t "binary/updates" -m "update temperature data 23"`： 发布终端发布`binary/updates`主题的信息

这样就可以在订阅终端接收到发布终端发布的信息了。


## 远程访问mosquitto服务

设备2订阅信息，设备3发布信息，都是通过刚安装好的服务，在服务器1上面。这个时候就要给服务器1上的`mosquitto broker`配置密码等。

### mosquitto配置

`mosquitton`的配置文件在目录`/etc/mosquitto/mosquitto.conf`下，使用`mosquitto_passwd`指令生成密码，并配置到`mosquitton`的配置文件中。

1. `systemctl stop mosquitto.service`: 先停止服务
2. `sudo mosquitto_passwd -c /etc/mosquitto/pwfile leo`: 生成一个名为`leo`的账户，并存储在`/etc/mosquitto/pwfile`文件中，运行这个指令会提示设置密码。
3. `vi /etc/mosquitto/mosquitto.conf`: 将账户文件增加到配置文件中, 将下面三行加入到配置文件中
	* `allow_anonymous false`: 关才匿名登录的权限；
	* `password_file /etc/mosquitto/pwfile`： 指向mosquitto登录的账户和密码
	* `listener 1883`: 增加监听的端口，如果是监听所有的端口则为：`listener 1883 0.0.0.0`
4. `systemctl start mosquitto.service`: 重新启动mosquitto服务
5. `sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v`: 加载新的配置文件, 没有报错即加载成功


### 远程测试

例如运行broker服务器1机器的ip为`192.168.1.88`

* `mosquitto_sub -d -h 192.168.1.88 -t "binary/updates"`: 设备2终端上订阅信息
* `mosquitto_pub -d -h 192.168.1.88 -t "binary/updates" -m "update temperature data 25"`: 设备3终端上发布信息

这个时候你会发现报错：

```
Error: Connection refused
```

需要加上刚设置的用户名及密码

* `mosquitto_sub -d -h 192.168.1.88 -t "binary/updates" -u leo -P xxxxx `: 设备2终端上订阅信息
* `mosquitto_pub -d -h 192.168.1.88 -t "binary/updates" -m "update temperature data 25" -u leo -P xxxxx `: 设备3终端上发布信息

但是直接将密码放在命令里很危险，因为可能会被别查记录查到，仅测试用!!!!!!


## 在Python上使用

`publisher.py`文件的内容：

```
import paho.mqtt.publish as publish

msgs = [{'topic': "kids/yolo", 'payload': "jump"},
        {'topic': "adult/pics", 'payload': "some photo"},
        {'topic': "adult/news", 'payload': "extra extra"},
        {'topic': "adult/news", 'payload': "super extra"}]

host = "localhost"

if __name__ == '__main__':
    # publish a single message
    publish.single(topic="kids/yolo", payload="just do it", hostname=host)

    # publish multiple messages
    publish.multiple(msgs, hostname=host)
```

`subscriber.py`文件的内容：

```
import paho.mqtt.client as paho

def on_message(mosq, obj, msg):
    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    mosq.publish('pong', 'ack', 0)

def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883, 60)

    client.subscribe("kids/yolo", 0)
    client.subscribe("adult/#", 0)

    while client.loop() == 0:
        pass
```


[更详细的使用方法](https://pypi.org/project/paho-mqtt/)

[MQTT for Beginners Tutorials and Course](http://www.steves-internet-guide.com/mqtt-basics-course/)

[Python MQTT客户端 paho-mqtt](https://www.cnblogs.com/Mickey-7/p/17402095.html)

