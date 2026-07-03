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


###针对 Linux 中 **wpa_supplicant.conf** 配置文件的**简洁字段说明**，涵盖全局配置和最常见的网络连接字段：

---

### 1. 全局配置（写在所有 `network` 块之前）

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| `ctrl_interface` | 指定控制套接字的目录，用于外部程序（如 `wpa_cli`）与进程通信。 | `ctrl_interface=/run/wpa_supplicant` |
| `update_config` | 设为 `1` 时，允许通过 `wpa_cli` 或 GUI 工具**保存**修改到该文件中。 | `update_config=1` |
| `country` | 设置国家代码，以遵守当地的 Wi-Fi 信道法规（影响可扫描的频段）。 | `country=CN`（中国）或 `US`（美国） |

---

### 2. 网络连接块（`network={ ... }`）核心字段

| 字段 | 必填？ | 含义 | 示例 |
| :--- | :--- | :--- | :--- |
| **`ssid`** | **是** | Wi-Fi 名称（服务集标识符）。**区分大小写**。 | `ssid="MyHome"` |
| **`psk`** | **视情况** | **预共享密钥**（即密码）。<br>• 可写明文（如 `"12345678"`）<br>• 也可写通过 `wpa_passphrase` 生成的 64 位哈希值（更安全）。<br>• **注意**：如果网络是**开放式**（无密码），此项留空，但要设置 `key_mgmt=NONE`。 | `psk="password123"`<br>或<br>`psk=5e4e...`（哈希串） |
| **`key_mgmt`** | 否（默认 WPA-PSK） | 认证密钥管理协议。<br>• `WPA-PSK`（个人级，最常见）<br>• `WPA-EAP`（企业级）<br>• `NONE`（开放或无加密网络） | `key_mgmt=WPA-PSK` |
| **`priority`** | 否（默认为 0） | **连接优先级**。数值越大，优先级越高。当多个配置的网络都在范围内时，优先连数值最大的。<br>⚠️ **必须全小写**（`priority`）。 | `priority=10` |
| **`proto`** | 否 | 允许的 WPA 协议版本。通常默认包含 RSN（WPA2）和 WPA（WPA1）。 | `proto=RSN WPA` |
| **`pairwise`** | 否 | 单播加密算法。常用 `CCMP`（AES）和 `TKIP`。 | `pairwise=CCMP TKIP` |
| **`group`** | 否 | 组播加密算法。 | `group=CCMP TKIP` |
| **`id_str`** | 否 | 自定义标识符（字符串），用于辅助脚本或 `wpa_cli` 区分不同的网络配置。 | `id_str="office"` |

---

### 3. 完整的简单配置示例（适用于家庭 WPA2 网络）

```conf
# 全局设置
ctrl_interface=/run/wpa_supplicant
update_config=1
country=CN

# 第一个网络（主要使用）
network={
    ssid="Home_WiFi"
    psk="my_secure_password"
    priority=10
    key_mgmt=WPA-PSK
}

# 第二个网络（备用，信号差时自动切换）
network={
    ssid="Guest_WiFi"
    psk="guest_pass"
    priority=5
    key_mgmt=WPA-PSK
}
```

---

### 4. 特别注意（避坑指南）

1. **大小写敏感**：`ssid` 和密码均区分大小写；字段名如 `priority` 必须小写（`Priority` 会被忽略）。
2. **引号使用**：如果密码或 SSID 包含空格或特殊符号（如 `#`、`!`、`$`），**务必用双引号**括起来。
3. **密码生成（推荐）**：避免在文件中明文保存密码，可以使用命令生成哈希值：
   ```bash
   wpa_passphrase "你的SSID" "你的密码" >> /etc/wpa_supplicant/wpa_supplicant.conf
   ```
   这会自动生成带哈希 `psk` 的 `network` 块（明文不会写入）。
4. **多网卡场景**：如果有多块无线网卡，可以通过 `-i` 参数指定网卡，配置文件可以通用。