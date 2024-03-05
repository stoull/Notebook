# RaspberryPi_WiFi设置

[使用wpa_cli](https://wiki.archlinux.org/title/Wpa_supplicant_(简体中文))

[Raspberry Pi Documentation - Configuration](https://www.raspberrypi.com/documentation/computers/configuration.html)

[FreeBSD Manual Pages wpa_supplicant.conf](https://man.freebsd.org/cgi/man.cgi?wpa_supplicant.conf(5))

因为学习的原因，我的pi要在我的工作地点和家里频繁移动，这样我希望我的pi当我到家的时候能自动接家的wifi，到办公室的时候能够自动的接入到公室的wifi。
我将`/etc/wpa_supplicant/wpa_supplicant.conf`文件中的内容更改为下面注释中的内容，就满足了我的需求。

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CN

network={
	ssid="Tenda_DA8BB0_5G"
	psk="wifi_password"
	priority=3
	id_str="work1"
}

network={
	ssid="Tenda_DA8BB0"
	psk="wifi_password"
	key_mgmt=WPA-PSK
	priority=2
	id_str="work2"
}

network={
	ssid="CMCC-Hut"
	psk="wifi_password"
	key_mgmt=WPA-PSK
	priority=3
	id_str="home"
}

network={
	ssid="ChangChun_iPhone"
	psk="wifi_password"
	priority=1
	id_str="phone_hotspot"
}

network={
	ssid="Tenda"
	psk="wifi_password"
	key_mgmt=WPA-PSK
	priority=1
	id_str="work3"
}
```

问题1: 系统会自动写入 disabled=1 。 导致在下次开机的时候不能自动连接网络。

参考资料：
[Changing Wifi networks from the command line interface](https://forums.raspberrypi.com/viewtopic.php?t=179387)