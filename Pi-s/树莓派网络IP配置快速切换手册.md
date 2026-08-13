好的，我为你整理了一份完整的操作手册。手册名称定为 **`RaspberryPi_Static_Dynamic_IP_Switch_Guide.md`**，以下是其完整内容，你可以直接复制并保存为 `.md` 文件。

---

```markdown
# 树莓派网络IP配置快速切换手册
## —— 在家用静态IP，在公司用动态IP

本手册适用于需要在不同网络环境（如家庭固定IP、公司自动获取IP）间快速切换的树莓派用户。根据你的树莓派操作系统版本，提供了两种主流配置方案。

---

## 1. 前置准备

- 树莓派已安装并连接好Wi-Fi。
- 拥有树莓派的SSH访问权限（或直接连接显示器和键盘）。
- 知道以下信息（用于静态IP配置）：
  - 家庭网络的**网关IP**（通常为 `192.168.1.1` 或 `192.168.0.1`）。
  - 一个**未被占用**的静态IP地址（建议在DHCP地址池范围之外，例如DHCP池为 `100-200`，则可选 `50` 或 `201`）。
  - 首选DNS（可填网关IP或公共DNS如 `114.114.114.114`）。

---

## 2. 确认系统版本

打开终端，执行以下命令查看操作系统版本：

```bash
cat /etc/os-release | grep VERSION=
```

- 如果版本包含 **`12`**（Bookworm）或更高 → 使用 **方案A（NetworkManager）**。
- 如果版本包含 **`11`**（Bullseye）或更早 → 使用 **方案B（dhcpcd）**。

---

## 方案A：使用 NetworkManager 自动切换（适用于 Bookworm 及更新）

NetworkManager 支持为同一个Wi-Fi接口创建多个“连接配置”，并根据信号自动切换，无需手动干预。

### A.1 查看当前活动的Wi-Fi连接

```bash
nmcli con show --active
```

记下输出中 `NAME` 一栏的名称，例如 `MyHomeWiFi`。

### A.2 为家庭网络设置静态IP

假设家庭Wi-Fi的SSID为 `MyHomeWiFi`，设定的静态IP为 `192.168.1.100/24`，网关为 `192.168.1.1`。

```bash
sudo nmcli con mod "MyHomeWiFi" ipv4.method manual \
  ipv4.addresses 192.168.1.100/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns 192.168.1.1
```

### A.3 为公司网络创建动态IP配置

假设公司Wi-Fi的SSID为 `OfficeWiFi`，密码为 `your_office_password`。

```bash
# 创建新连接（自动获取IP）
sudo nmcli con add con-name "OfficeWiFi" ifname wlan0 type wifi ssid "OfficeWiFi"

# 设置Wi-Fi密码（若无需密码可跳过）
sudo nmcli con modify "OfficeWiFi" wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify "OfficeWiFi" wifi-sec.psk "your_office_password"

# 确保IP获取方式为自动（DHCP）
sudo nmcli con mod "OfficeWiFi" ipv4.method auto
```

### A.4 （可选）设置连接优先级

让树莓派优先连接家庭网络（数值越大优先级越高）。

```bash
sudo nmcli con mod "MyHomeWiFi" connection.autoconnect-priority 100
sudo nmcli con mod "OfficeWiFi" connection.autoconnect-priority 50
```

### A.5 重启网络服务或重启树莓派

```bash
sudo nmcli networking off && sudo nmcli networking on
# 或直接重启
sudo reboot
```

**切换效果**：此后，当树莓派检测到 `MyHomeWiFi` 时自动使用静态IP；检测到 `OfficeWiFi` 时自动使用DHCP。

---

## 方案B：手动切换 dhcpcd 配置文件（适用于 Bullseye 及更早）

旧版系统使用 `dhcpcd` 管理网络，我们可以准备两套配置文件，通过脚本快速切换。

### B.1 创建静态IP配置文件

编辑 `/etc/dhcpcd.static.conf`：

```bash
sudo nano /etc/dhcpcd.static.conf
```

填入以下内容（根据实际情况修改IP、网关、DNS）：

```
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
```

保存退出（`Ctrl+X`，`Y`，`Enter`）。

### B.2 创建动态IP配置文件

编辑 `/etc/dhcpcd.dynamic.conf`：

```bash
sudo nano /etc/dhcpcd.dynamic.conf
```

填入以下内容（只需指定接口，dhcpcd将自动使用DHCP）：

```
interface wlan0
```

保存退出。

### B.3 编写快速切换脚本（可选）

创建脚本 `/usr/local/bin/switch_network.sh`：

```bash
sudo nano /usr/local/bin/switch_network.sh
```

写入以下内容：

```bash
#!/bin/bash
case "$1" in
  static)
    sudo cp /etc/dhcpcd.static.conf /etc/dhcpcd.conf
    echo "切换到静态IP（家庭网络）"
    ;;
  dynamic)
    sudo cp /etc/dhcpcd.dynamic.conf /etc/dhcpcd.conf
    echo "切换到动态IP（公司网络）"
    ;;
  *)
    echo "用法: $0 {static|dynamic}"
    exit 1
    ;;
esac
sudo systemctl restart dhcpcd
echo "配置已应用，IP地址已更新"
```

赋予执行权限：

```bash
sudo chmod +x /usr/local/bin/switch_network.sh
```

### B.4 手动切换

- **切换到静态IP（在家）**：
  ```bash
  sudo switch_network.sh static
  ```
- **切换到动态IP（在公司）**：
  ```bash
  sudo switch_network.sh dynamic
  ```

> **注意**：切换后，树莓派的IP地址会改变，SSH连接可能断开，请使用新的IP重新连接。

---

## 3. 验证配置

无论使用哪种方案，都可以通过以下命令检查当前IP地址：

```bash
ip addr show wlan0
```

或查看路由和DNS：

```bash
ip route show
cat /etc/resolv.conf
```

---

## 4. 常见问题与注意事项

| 问题 | 解决方法 |
|------|----------|
| 设置的静态IP无法上网 | 检查IP是否与网关在同一网段，且未被其他设备占用。 |
| NetworkManager 找不到Wi-Fi | 确保Wi-Fi已启用：`nmcli radio wifi on`。 |
| 切换后SSH连不上 | 使用树莓派屏幕或串口查看新IP，或使用 `ping` 扫描局域网。 |
| 公司Wi-Fi有认证页面（Portal） | 需额外处理，本手册不涵盖，建议先连接后再配置。 |
| 想要更自动化的切换 | 可使用 `iwlib` 或 `NetworkManager` 的 `dispatcher` 脚本，但本手册暂不展开。 |

---

## 5. 总结

- **Bookworm 及以上**：推荐使用 **NetworkManager 多配置文件**，实现无感自动切换。
- **Bullseye 及以下**：使用 **dhcpcd 双配置文件 + 脚本**，一键手动切换。

请根据你的系统版本选择相应方案，并确保静态IP地址不与DHCP池冲突。切换后请验证网络连通性，如有问题可重启树莓派或重置网络管理器。
```

---

你可以将上述内容保存为 `RaspberryPi_Static_Dynamic_IP_Switch_Guide.md` 文件，方便随时查阅。如果有任何细节需要调整，也可以告诉我。