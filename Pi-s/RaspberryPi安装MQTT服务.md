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

这里选择安装使用Mosquitto，因为轻量方便，开源，社区友好。安装[Mosquitto - Download](https://mosquitto.org/download/)。这里的安装包含mqtt broker及client, client可以用测试。

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

可见在macOS上`mosquitto.conf `的目录为`/opt/homebrew/etc/mosquitto/mosquitto.conf`

### 测试

安装完`mosquitto`及`mosquitto-clients`后，可以在两个终端，一个终端订阅信息，另一个终端发布信息测试整个mqtt的功能。

* `mosquitto_sub -d -t "binary/updates"`: 订阅终端订阅`binary/updates`主题
* `mosquitto_pub -d -t "binary/updates" -m "update temperature data 23"`： 发布终端发布`binary/updates`主题的信息
* `mosquitto_sub -d -h macmini.local -t "#" -u admin -P 123456`: 订阅所有的主题

这样就可以在订阅终端接收到发布终端发布的信息了。


## 远程访问mosquitto服务

设备2订阅信息，设备3发布信息，都是通过刚安装好的服务，在服务器1上面。这个时候就要给服务器1上的`mosquitto broker`配置密码等。

### mosquitto配置

`mosquitton`的配置文件在目录`/etc/mosquitto/mosquitto.conf`下，使用`mosquitto_passwd`指令生成密码，并配置到`mosquitton`的配置文件中。

1. `systemctl stop mosquitto.service`: 先停止服务
2. `sudo mosquitto_passwd -c /etc/mosquitto/pwfile leo`: 生成一个名为`leo`的账户，并存储在`/etc/mosquitto/pwfile`文件中，运行这个指令会提示设置密码。
3. `vi /etc/mosquitto/mosquitto.conf`: 将账户文件增加到配置文件中, 将下面三行加入到配置文件中
	* `allow_anonymous false`: 关闭匿名登录的权限；
	* `password_file /etc/mosquitto/pwfile`： 指向mosquitto登录的账户和密码
	* `listener 1883`: 增加监听的端口，如果是监听所有的端口则为：`listener 1883 0.0.0.0`
4. `systemctl start mosquitto.service`: 重新启动mosquitto服务
5. `sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v`: 加载新的配置文件, 没有报错即加载成功

`sudo mosquitto_passwd /etc/mosquitto/passwd john`: 进行修改密码，john为你想要更改用户的用户名
系统会提示你输入两次新密码。

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




Mosquitto Broker 配置指南

Mosquitto的配置相对简单但功能强大，下面是完整的配置指南：

## 1. 基础配置文件位置

```
# Linux
/etc/mosquitto/mosquitto.conf

# macOS (Homebrew)
/usr/local/etc/mosquitto/mosquitto.conf
/opt/homebrew/etc/mosquitto/mosquitto.conf

# Windows
C:\Program Files\mosquitto\mosquitto.conf

# Docker
/mosquitto/config/mosquitto.conf

```

## 2. 基础配置示例

最简单配置 (开发环境)

```
# /etc/mosquitto/mosquitto.conf

# 监听端口
listener 1883

# 允许匿名访问（仅用于测试）
allow_anonymous true

# 日志配置
log_dest stdout
log_type all

# 持久化配置
persistence true
persistence_location /var/lib/mosquitto/
```

生产环境推荐配置

```
# ============================================
# 基本配置
# ============================================

# 进程ID文件
pid_file /var/run/mosquitto. pid

# 持久化存储
persistence true
persistence_location /var/lib/mosquitto/
# 自动保存间隔（秒）
autosave_interval 1800

# 系统状态发布
sys_interval 10

# ============================================
# 网络监听配置
# ============================================

# MQTT 监听器
listener 1883
protocol mqtt

# WebSocket 监听器（可选）
listener 9001
protocol websockets

# 绑定地址（0.0.0.0 允许所有，或指定IP）
bind_address 0.0.0. 0

# 最大连接数
max_connections -1

# ============================================
# 安全配置
# ============================================

# 禁用匿名访问
allow_anonymous false

# 密码文件
password_file /etc/mosquitto/passwd

# ACL访问控制文件
acl_file /etc/mosquitto/acl.conf

# ============================================
# 日志配置
# ============================================

# 日志输出位置
log_dest file /var/log/mosquitto/mosquitto.log
log_dest stdout

# 日志类型
log_type error
log_type warning
log_type notice
log_type information

# 时间戳格式
log_timestamp true
log_timestamp_format %Y-%m-%d %H:%M:%S

# ============================================
# 消息和队列配置
# ============================================

# 消息大小限制（字节）
message_size_limit 10485760

# QoS队列消息数限制
max_queued_messages 1000

# 飞行中消息数（QoS>0）
max_inflight_messages 20

# ============================================
# Keep Alive 配置
# ============================================

# 最大keep alive时间
max_keepalive 65535

# ============================================
# TLS/SSL 配置（可选）
# ============================================

# listener 8883
# cafile /etc/mosquitto/certs/ca.crt
# certfile /etc/mosquitto/certs/server. crt
# keyfile /etc/mosquitto/certs/server.key
# require_certificate false

```

## 3. 用户认证配置

创建密码文件

```
# 创建第一个用户（会创建新文件）
sudo mosquitto_passwd -c /etc/mosquitto/passwd username1

# 添加更多用户（不使用 -c 参数）
sudo mosquitto_passwd /etc/mosquitto/passwd username2

# 删除用户
sudo mosquitto_passwd -D /etc/mosquitto/passwd username1

# 设置文件权限
sudo chmod 600 /etc/mosquitto/passwd
```

修改主配置文件

```
conf
allow_anonymous false
password_file /etc/mosquitto/passwd

```

## 4. ACL访问控制配置

创建ACL文件

```
# /etc/mosquitto/acl.conf

# 匿名用户（如果允许）
# user anonymous
# topic read sensors/#

# 管理员用户 - 完全访问
user admin
topic readwrite #

# IoT设备用户 - 只能发布到自己的topic
user device001
topic write devices/device001/#
topic read devices/device001/commands/#

# 数据收集服务 - 只能订阅
user data_collector
topic read devices/#
topic read sensors/#

# 模式匹配示例
pattern write devices/%u/#
pattern read devices/%u/status
ACL规则说明
```

```
# 格式：topic [read|write|readwrite] <topic>

# %u - 替换为用户名
# %c - 替换为客户端ID
# # - 多级通配符
# + - 单级通配符

# 示例：
# user sensor_client
# topic write sensors/%u/data      # 只能写自己的数据
# topic read sensors/%u/commands   # 只能读自己的命令
```

## 5. Docker 配置

docker-compose.yml

```
YAML
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    # 如果需要自定义用户ID
    # user: "1883:1883"
```

目录结构

```
mosquitto/
├── config/
│   ├── mosquitto.conf
│   ├── passwd
│   └── acl. conf
├── data/           # 持久化数据
└── log/            # 日志文件
```

Docker版mosquitto.conf

```
# Docker容器内配置
listener 1883
listener 9001
protocol websockets

allow_anonymous false
password_file /mosquitto/config/passwd
acl_file /mosquitto/config/acl. conf

persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto. log
log_dest stdout
log_type all

```

## 6. TLS/SSL 加密配置


生成自签名证书


```
# 创建证书目录
sudo mkdir -p /etc/mosquitto/certs
cd /etc/mosquitto/certs

# 生成CA证书
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt

# 生成服务器证书
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 3650

# 设置权限
sudo chmod 600 /etc/mosquitto/certs/*
配置TLS

conf
# MQTT over TLS
listener 8883
protocol mqtt
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

# 是否要求客户端证书
require_certificate false

# TLS版本
tls_version tlsv1.2
```

## 7. 启动和管理命令

```
# 测试配置文件
mosquitto -c /etc/mosquitto/mosquitto.conf -v

# 启动服务
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# 重启服务
sudo systemctl restart mosquitto

# 查看状态
sudo systemctl status mosquitto

# 查看日志
sudo tail -f /var/log/mosquitto/mosquitto.log
journalctl -u mosquitto -f

# Docker启动
docker-compose up -d

# Docker查看日志
docker logs -f mosquitto

## 8. 测试连接

```

使用mosquitto客户端测试

```
# 订阅（终端1）
mosquitto_sub -h localhost -p 1883 -t "test/topic" -u username -P password

# 发布（终端2）
mosquitto_pub -h localhost -p 1883 -t "test/topic" -m "Hello" -u username -P password

# 测试TLS连接
mosquitto_pub -h localhost -p 8883 \
  --cafile /etc/mosquitto/certs/ca.crt \
  -t "test/topic" -m "Secure Hello" \
  -u username -P password

```

Python测试脚本

```
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client. username_pw_set("username", "password")
client. on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client. loop_forever()
```

## 9. 性能优化配置

```
# 高并发场景
max_connections 10000
max_queued_messages 10000
max_inflight_messages 100

# 禁用不需要的日志
log_type error
log_type warning

# 调整持久化
persistence true
autosave_interval 600  # 10分钟保存一次

# 内存限制
memory_limit 1073741824  # 1GB

## 10. 常见配置场景

```
场景1：开发测试（无认证）

```
conf
listener 1883
allow_anonymous true
persistence false
log_dest stdout
场景2：生产环境（认证+ACL）

conf
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl.conf
persistence true
场景3：高安全（TLS+双向认证）

conf
listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
require_certificate true
allow_anonymous false
password_file /etc/mosquitto/passwd
重启服务应用配置：

bash
sudo systemctl restart mosquitto

```