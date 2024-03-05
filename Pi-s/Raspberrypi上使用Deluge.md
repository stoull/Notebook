# 在Raspberrypi上使用BitTorrent客户端


BitTorrent is a peer-to-peer (P2P) file-sharing protocol

[Install deluge on debain](https://dev.deluge-torrent.org/wiki/Installing/Linux/Debian/Jessie)

[How-to guides](https://deluge.readthedocs.io/en/latest/how-to/index.html)

[Deluge as a service](https://deluge.readthedocs.io/en/latest/how-to/systemd-service.html)

## Transmission

1. transmission-qt 可添加磁力连接
`sudo apt install transmission-qt`

2. Use vnc to connect a remote screen, then run transmission-gtk will open the GUI application 

sudo apt install transmission-qt

4. 停止transmission服务
`sudo systemctl stop transmission-daemon`

5. 设置transmission服务
transmission 的设置项都存在：`/etc/transmission-daemon/settings.json`中，对应的说明可看
`transmission-daemon -h`

6. 添加新任务
`transmission-daemon -a 'magnet:?xt=urn:btih:D60E3E013FE1E8F603B196C728B534F9DF6F25D6'`

7. 查看正在进行的任务
`transmission-remote -l`
如果出现授权的问题，则设置`rpc-authentication-required`, `rpc-username`及`rpc-password`, 如果设置为要授权则使用`transmission-remote --auth username:password -l`

8. 查看web界面
`http://192.168.1.7:9091/transmission/web/#upload`

>`sudo service transmission-daemon stop`
>`sudo service transmission-daemon start`
>`transmission-daemon --no-auth`


### 问题1: 下载时无法写入外接硬盘

* Step 1: Stop transmission daemon
`sudo service transmission-daemon stop`

* Step 2: Add pi to debian-transmission group
`sudo usermod -a -G debian-transmission pi`

* Step 3: changing the daemon-user
`sudo nano /etc/init.d/transmission-daemon`
Change USER to pi.

* Step 4 Change the rights of the configuration files folder
`sudo chown -R pi /var/lib/transmission-daemon/info/`
`sudo chmod 755 /var/lib/transmission-daemon/info/settings.json`

* Step 5: Set the correct permissions for the download / incomplete folders
`sudo chown -R pi /somewhere/downloads`
`sudo chown -R pi /somewhere/incomplete`

* Step 6: Start transmission daemon
`sudo service transmission-daemon start`

### 问题2: Error: Unable to save resume file: Permission denied
`sudo chmod 775 /var/lib/transmission-daemon/.config/transmission-daemon/resume`

[Transmission: permission denied on USB disk](https://raspberrypi.stackexchange.com/questions/4378/transmission-permission-denied-on-usb-disk)

[How to set up transmission-daemon on a Raspberry Pi and control it via web interface](https://linuxconfig.org/how-to-set-up-transmission-daemon-on-a-raspberry-pi-and-control-it-via-web-interface)

[transmissionbt.com](https://transmissionbt.com)
[transmission Github](https://github.com/transmission/transmission)

Transmission is a set of lightweight BitTorrent clients (in GUI, CLI and daemon form). All its incarnations feature a very simple, intuitive interface on top on an efficient, cross-platform back-end.

[transmission wiki](https://github.com/transmission/transmission/wiki)

[TransmissionHowTo](https://help.ubuntu.com/community/TransmissionHowTo)

## Deluge
[deluge-torrent.org](https://deluge-torrent.org)
### 安装
#### 安装GUI
设备为默认的程序[How to set Deluge as default torrent application](https://deluge.readthedocs.io/en/latest/how-to/set-mime-type.html)

#### 安装deluge服务
以服务的形式运行deluge，可设置随机器开关开启或停止服务，而且当deluge因错误crash停止服务后，还可以自动重启。

使用命令安装：
`sudo apt install deluged deluge-web` 或者 `apt-get install deluged deluge-web`

#### 使用 Deluge Ubuntu Launchpad PPA安装
`add-apt-repository 'deb http://ppa.launchpad.net/deluge-team/ppa/ubuntu trusty main'`

### 使用
[How to create systemd services for Linux](https://deluge.readthedocs.io/en/latest/how-to/systemd-service.html)