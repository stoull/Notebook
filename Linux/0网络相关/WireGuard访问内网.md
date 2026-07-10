# WireGuard 外网访问家里 Frigate

通过**公网 VPS 做 WireGuard 枢纽**，让手机/笔记本在外网像在内网一样访问树莓派上的 Frigate、go2rtc，**无需**把监控端口直接暴露到公网。

**前置**：Pi 上已按 [RaspberryPi监控系统.md](./RaspberryPi监控系统.md) 配好 go2rtc + Frigate，内网可访问（如 `http://192.168.1.193:5000`）。

---

## 1. 拓扑与原理

```
                    公网 UDP 51820
  [手机/笔记本] ─────────────► [公网 VPS] ◄───────────── [家里 Pi + Frigate]
   WG: 10.66.66.3              WG: 10.66.66.1            WG: 10.66.66.2
                                      │
                               转发 WG 网段流量
                               （Pi 在家用 NAT 后主动连 VPS）
```

| 角色 | 设备 | WireGuard IP | 说明 |
|------|------|--------------|------|
| 枢纽 | 公网 VPS | `10.66.66.1` | 固定公网 IP，监听 `51820/udp` |
| 服务端 | 树莓派 Pi | `10.66.66.2` | 在家，无公网 IP，`PersistentKeepalive` 保活 |
| 客户端 | 手机/笔记本 | `10.66.66.3` … | 外网任意网络，连 VPS 后进 WG 网段 |

外网连上 WireGuard 后，访问 Frigate：

| 服务 | 外网地址（连 WG 后） |
|------|----------------------|
| Frigate（推荐，带鉴权） | `http://10.66.66.2:8971` |
| Frigate（无鉴权，仅内网调试） | `http://10.66.66.2:5000` |
| go2rtc 预览 | `http://10.66.66.2:1984` |
| RTSP（VLC） | `rtsp://10.66.66.2:8554/picam` |

> 使用 **Pi 的 WireGuard IP**（`10.66.66.2`），不要用家里局域网 IP（`192.168.x.x`），外网手机默认到不了家里路由。

---

## 2. 前置条件

- [ ] 一台有**固定公网 IP** 的 Linux VPS（Ubuntu 22.04 / Debian 12 均可）
- [ ] VPS 能 SSH 登录（`root` 或 `sudo` 用户）
- [ ] 树莓派已联网，内网 Frigate 正常
- [ ] 记下 VPS 公网 IP，下文记为 `<VPS公网IP>`（例：`203.0.113.10`）
- [ ] 确认 VPS 出口网卡名（下文记为 `<VPS网卡>`，常见 `eth0`、`ens3`）：

```bash
# 在 VPS 上执行
ip route | grep default
# 示例输出：default via ... dev eth0 → 网卡就是 eth0
```

---

## 3. IP 与端口规划

| 项目 | 值 |
|------|-----|
| WireGuard 网段 | `10.66.66.0/24` |
| VPS | `10.66.66.1` |
| Pi | `10.66.66.2` |
| 手机 | `10.66.66.3` |
| 笔记本（可选） | `10.66.66.4` |
| WireGuard 端口 | `51820/udp` |

选用 `10.66.66.0/24` 是为避免与常见家用网段（`192.168.x.x`、`10.0.0.x`）冲突。

---

## 4. 公网 VPS 配置

以下在 **VPS** 上执行（SSH 登录后）。

### 4.1 安装 WireGuard

```bash
sudo apt update
sudo apt install -y wireguard qrencode
```

### 4.2 生成 VPS 密钥

```bash
sudo mkdir -p /etc/wireguard
cd /etc/wireguard
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
cat server_public.key   # 记下，下文 <VPS公钥>
```

### 4.3 预生成 Pi 与手机密钥（在 VPS 上生成，再拷到对应设备）

**Pi：**

```bash
wg genkey | tee pi_private.key | wg pubkey > pi_public.key
echo "Pi 私钥（拷到 Pi，保密）："; cat pi_private.key
echo "Pi 公钥（填进 VPS server.conf）："; cat pi_public.key
```

**手机：**

```bash
wg genkey | tee phone_private.key | wg pubkey > phone_public.key
echo "手机 私钥："; cat phone_private.key
echo "手机 公钥："; cat phone_public.key
```

密钥文件留在 VPS 仅作备份亦可；**私钥切勿提交到 Git 或发给他人**。

### 4.4 创建 VPS 服务端配置

将 `<VPS网卡>`、`<Pi公钥>`、`<手机公钥>` 替换为实际值：

```bash
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
Address = 10.66.66.1/24
ListenPort = 51820
PrivateKey = <粘贴 server_private.key 内容>

# 开启转发：让手机(10.66.66.3) 能访问 Pi(10.66.66.2)
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o <VPS网卡> -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o <VPS网卡> -j MASQUERADE

# ---------- 树莓派 Pi ----------
[Peer]
# Pi
PublicKey = <Pi公钥>
AllowedIPs = 10.66.66.2/32

# ---------- 手机 ----------
[Peer]
# Phone
PublicKey = <手机公钥>
AllowedIPs = 10.66.66.3/32
```

持久化 IP 转发：

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

### 4.5 防火墙

**ufw 示例：**

```bash
sudo ufw allow 51820/udp
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

**云厂商安全组**：在控制台放行入站 **UDP 51820**（来源 `0.0.0.0/0` 或你的常用 IP）。

### 4.6 启动并设置自启

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
sudo wg show
```

正常应看到 Pi、手机两个 `peer`，此时 Pi 尚未配置，可能无 `latest handshake`。

---

## 5. 树莓派（Pi）配置

以下在 **Pi** 上执行（SSH：`ssh pi@hutpi.local` 或 `ssh pi@192.168.1.193`）。

### 5.1 安装 WireGuard

```bash
sudo apt update
sudo apt install -y wireguard
```

### 5.2 创建 Pi 客户端配置

将 `<Pi私钥>`、`<VPS公钥>`、`<VPS公网IP>` 替换为实际值：

```bash
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
Address = 10.66.66.2/24
PrivateKey = <Pi私钥>

[Peer]
# VPS 枢纽
PublicKey = <VPS公钥>
Endpoint = <VPS公网IP>:51820
# 只走 WG 隧道访问枢纽网段（不把所有上网流量绕到 VPS）
AllowedIPs = 10.66.66.0/24
PersistentKeepalive = 25
```

> `PersistentKeepalive = 25`：Pi 在家用 NAT 后，定期向 VPS 发包，保证外网手机能经 VPS 转发到 Pi。

### 5.3 启动并设置自启

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
sudo wg show
```

### 5.4 在 VPS 上确认 Pi 已连通

回到 **VPS**：

```bash
sudo wg show
```

`peer`（Pi）一行应出现 **latest handshake** 在数秒～数分钟内。在 VPS 上 ping Pi：

```bash
ping -c 3 10.66.66.2
```

在 **Pi** 上 ping VPS：

```bash
ping -c 3 10.66.66.1
```

---

## 6. 手机 / 笔记本客户端

### 6.1 安装 App

| 平台 | 应用 |
|------|------|
| iOS | App Store → **WireGuard** |
| Android | Google Play / F-Droid → **WireGuard** |
| macOS | App Store 或 `brew install wireguard-tools` + App |
| Windows | https://www.wireguard.com/install/ |

### 6.2 配置文件

新建 `phone.conf`（内容如下，替换 `<手机私钥>`、`<VPS公钥>`、`<VPS公网IP>`）：

```ini
[Interface]
Address = 10.66.66.3/24
PrivateKey = <手机私钥>
DNS = 1.1.1.1

[Peer]
PublicKey = <VPS公钥>
Endpoint = <VPS公网IP>:51820
AllowedIPs = 10.66.66.0/24
PersistentKeepalive = 25
```

> `AllowedIPs = 10.66.66.0/24`：仅 WG 网段走隧道，**不影响**手机正常 4G/5G 上网。若填 `0.0.0.0/0` 则全流量走 VPS（一般不需要）。

**导入方式：**

- **手机**：VPS 上 `qrencode -t ansiutf8 < phone.conf` 生成二维码，App 扫码；或 AirDrop/微信发 `.conf` 文件导入
- **macOS**：WireGuard App → Import from file

### 6.3 在 VPS 添加笔记本（可选）

若再增加一台笔记本，在 VPS 生成新密钥对，在 `wg0.conf` 增加：

```ini
[Peer]
# Laptop
PublicKey = <笔记本公钥>
AllowedIPs = 10.66.66.4/32
```

笔记本 `Address = 10.66.66.4/24`，其余同手机。改完 VPS 配置后：

```bash
sudo systemctl restart wg-quick@wg0
```

---

## 7. 外网访问 Frigate 视频

### 7.1 连接 WireGuard

1. 手机关闭 Wi‑Fi，用 **4G/5G**（模拟外网）
2. 打开 WireGuard App，**开启隧道**
3. 状态应显示「已连接」

### 7.2 打开 Frigate

浏览器访问（推荐带鉴权端口）：

```
http://10.66.66.2:8971
```

低延迟预览（go2rtc）：

```
http://10.66.66.2:1984
```

VLC 拉 RTSP：

```
rtsp://10.66.66.2:8554/picam
```

### 7.3 开启 Frigate 8971 鉴权（强烈建议）

外网能连上 WG 后，相当于进入「虚拟内网」，仍建议启用 Frigate 登录。

编辑 Pi 上 `frigate/config/config.yml`，增加或确认：

```yaml
auth:
  enabled: true
```

重启 Frigate：

```bash
cd ~/frigate   # 你的 docker-compose 目录
docker compose restart frigate
```

首次打开 `http://10.66.66.2:8971` 按页面提示设置用户名、密码。

> **不要**把无鉴权的 `:5000` 当作外网入口；8971 才是对外安全界面。

### 7.4 验证清单

按顺序打勾：

| # | 检查项 | 命令 / 操作 | 预期 |
|---|--------|-------------|------|
| 1 | VPS WG 运行 | `sudo wg show` | 有 `interface: wg0` |
| 2 | Pi WG 运行 | `sudo wg show` | 有 handshake |
| 3 | VPS → Pi | VPS 上 `ping 10.66.66.2` | 通 |
| 4 | 手机 WG 连接 | App 显示已连接 | 已连接 |
| 5 | 手机 → Pi | 手机浏览器 `http://10.66.66.2:8971` | Frigate 页面 |
| 6 | 视频 | Frigate 里点 picam 直播 | 有画面 |

手机连通性测试（iOS/Android 可用 Termius 或 ping 工具，或直接浏览器测 Frigate）：

```bash
# 若手机可执行 ping
ping 10.66.66.2
```

---

## 8. 故障排查

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| Pi `wg show` 无 handshake | VPS 51820 未放行；Endpoint IP/端口错 | 查云安全组 + `ufw`；核对 `Endpoint` |
| VPS 能 ping Pi，手机不能 | 手机 WG 未连；AllowedIPs 不对 | 确认 App 已开启；手机 AllowedIPs 含 `10.66.66.0/24` |
| 能 ping 通，Frigate 打不开 | Frigate 未运行；防火墙拦端口 | `docker ps`；Pi 上 `ss -tlnp \| grep -E '5000\|8971'` |
| 仅 5000 能开、8971 不能 | 未配置 auth 或端口未监听 | 查 `config.yml` 的 `auth`；Frigate 0.12+ 默认 8971 |
| 连上 WG 后整机断网 | AllowedIPs 设成 `0.0.0.0/0` | 改回 `10.66.66.0/24` |
| handshake 偶尔断 | 家用 NAT 超时 | Pi 确认 `PersistentKeepalive = 25` |
| 视频卡顿 | 上行带宽不足 | 降低 go2rtc 分辨率/帧率；用 4G 高峰时更明显 |

**常用诊断命令：**

```bash
# Pi 上
sudo wg show
sudo systemctl status wg-quick@wg0
docker ps | grep frigate
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8971

# VPS 上
sudo wg show
sudo iptables -L FORWARD -n -v
ping -c 3 10.66.66.2
```

**改 VPS `wg0.conf` 后务必重启：**

```bash
sudo systemctl restart wg-quick@wg0
```

---

## 9. 安全建议

1. **私钥保密**：`/etc/wireguard/*.key`、`*.conf` 权限应为 `600`，不要上传 Git
2. **仅暴露 UDP 51820**：不要对公网映射 Frigate 5000/1984/8554
3. **Frigate 用 8971 + auth**：强密码，必要时仅给手机 WG 配置固定 IP
4. **VPS 定期更新**：`sudo apt update && sudo apt upgrade`
5. **可选加固**：VPS `wg0.conf` 的 Peer 用 `iptables` 限制仅允许 `10.66.66.3 → 10.66.66.2:8971`（进阶，一般家庭可省略）

---

## 10. 可选：外网访问整个家里局域网

若希望连上 WG 后访问 `192.168.1.193` 等家里所有设备，需把 Pi 做成「子网路由」：

**Pi** `wg0.conf` 的 `[Peer]` 改为：

```ini
AllowedIPs = 10.66.66.0/24, 192.168.1.0/24
```

并在 Pi 上开启转发（若尚未）：

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

**手机** `AllowedIPs` 增加家里网段：

```ini
AllowedIPs = 10.66.66.0/24, 192.168.1.0/24
```

**VPS** Pi 的 `[Peer]` 改为：

```ini
AllowedIPs = 10.66.66.2/32, 192.168.1.0/24
```

> 仅看 Frigate 时**不必**做本节；用 `10.66.66.2:8971` 即可。

---

## 11. 快速参考卡片

```
VPS 公网 IP    : <VPS公网IP>
WG 端口        : UDP 51820
Pi WG IP       : 10.66.66.2
外网看 Frigate : http://10.66.66.2:8971  （先开手机 WireGuard）
外网看 go2rtc  : http://10.66.66.2:1984
```

**systemd 管理：**

```bash
sudo systemctl status wg-quick@wg0
sudo systemctl restart wg-quick@wg0
sudo wg show
```

---

## 12. 与监控系统文档的关系

| 文档 | 内容 |
|------|------|
| [RaspberryPi监控系统.md](./RaspberryPi监控系统.md) | Pi 摄像头、go2rtc、Frigate 内网搭建 |
| 本文 | 外网经 WireGuard 安全访问已搭好的 Frigate |

内网先通，再做 WireGuard；WireGuard 只解决「外网如何连到 Pi」，不替代 go2rtc/Frigate 本身配置。
