# WireGuard VPN 安装与使用手册

本手册说明如何在外网服务器上搭建 WireGuard VPN，并用手机连接，使全部或部分流量经该服务器转发。

---

## 目录

1. [适用场景与前提](#1-适用场景与前提)
2. [架构说明](#2-架构说明)
3. [服务器端安装](#3-服务器端安装)
4. [手机端配置](#4-手机端配置)
5. [分流：特定流量走 VPN](#5-分流特定流量走-vpn)
6. [日常运维](#6-日常运维)
7. [增删客户端](#7-增删客户端)
8. [故障排查](#8-故障排查)
9. [安全建议](#9-安全建议)
10. [附录](#10-附录)

---

## 1. 适用场景与前提

### 1.1 适用场景

- 手机在外网，希望流量经自有服务器出口
- 仅访问服务器内网或指定网段
- 按 IP/网段做分流（特定目的地走 VPN）

### 1.2 环境前提

| 项目 | 要求 |
|------|------|
| 服务器 | 具备公网 IP（或可端口映射）的 Linux，推荐 Ubuntu 22.04 / Debian 12 |
| 权限 | 服务器 root 或 sudo |
| 网络 | 云厂商安全组 / 防火墙放行 **UDP 51820**（可自定义端口） |
| 手机 | iOS 或 Android，可安装官方 WireGuard App |

### 1.3 本文约定

| 名称 | 示例值 | 说明 |
|------|--------|------|
| 服务器公网 IP | `YOUR_SERVER_IP` | 替换为真实公网 IP 或域名 |
| VPN 网段 | `10.8.0.0/24` | 隧道内虚拟网段，可按需修改 |
| 服务端地址 | `10.8.0.1/24` | 服务器在 VPN 内的地址 |
| 手机地址 | `10.8.0.2/32` | 第一台手机客户端地址 |
| 监听端口 | `51820` | WireGuard UDP 端口 |
| 网卡名 | `eth0` | 服务器出网网卡，需按实际修改 |

查看服务器出网网卡：

```bash
ip -o -4 route show to default
# 示例输出中的 dev 后面即为网卡名，如 eth0、ens3、ens5
```

---

## 2. 架构说明

```
手机 App ──(UDP 51820)──► 公网服务器 WireGuard (10.8.0.1)
                              │
                              ├─ AllowedIPs = 0.0.0.0/0  → 全部流量经服务器 NAT 出网
                              └─ AllowedIPs = 指定网段     → 仅这些目的地走隧道
```

- **服务端 Peer 的 AllowedIPs**：该客户端在隧道内可使用的地址（通常是客户端单个 IP）
- **客户端 Peer 的 AllowedIPs**：决定「哪些目的地走隧道」（分流关键配置）

---

## 3. 服务器端安装

以下以 Ubuntu / Debian 为例。CentOS / Rocky 见 [附录 A](#附录-a-centosrocky-安装)。

### 3.1 安装 WireGuard

```bash
sudo apt update
sudo apt install -y wireguard wireguard-tools iptables
```

确认版本：

```bash
wg --version
```

### 3.2 生成密钥

```bash
sudo mkdir -p /etc/wireguard
sudo chmod 700 /etc/wireguard
cd /etc/wireguard

# 服务端密钥
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key

# 手机客户端密钥（也可在手机 App 内生成，再把公钥填到服务器）
wg genkey | tee phone_private.key | wg pubkey > phone_public.key

# 查看公钥（后续配置要用）
echo "=== Server Public ===" && cat server_public.key
echo "=== Phone Public  ===" && cat phone_public.key
```

> **安全**：私钥勿外传、勿提交到 Git。权限保持 `600`。

### 3.3 编写服务端配置

```bash
sudo nano /etc/wireguard/wg0.conf
```

内容模板（替换尖括号内内容，并把 `eth0` 换成真实网卡）：

```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <server_private.key 的内容>

# 允许转发 + NAT（手机流量经服务器出网）
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# 手机
PublicKey = <phone_public.key 的内容>
AllowedIPs = 10.8.0.2/32
```

可用命令自动写入（仍需确认网卡名）：

```bash
SERVER_PRIV=$(sudo cat /etc/wireguard/server_private.key)
PHONE_PUB=$(sudo cat /etc/wireguard/phone_public.key)
IFACE=$(ip -o -4 route show to default | awk '{print $5}')

sudo tee /etc/wireguard/wg0.conf >/dev/null <<EOF
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = ${SERVER_PRIV}
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ${IFACE} -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o ${IFACE} -j MASQUERADE

[Peer]
PublicKey = ${PHONE_PUB}
AllowedIPs = 10.8.0.2/32
EOF

sudo chmod 600 /etc/wireguard/wg0.conf
```

### 3.4 开启 IP 转发

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wireguard-forward.conf
sudo sysctl --system
# 确认
sysctl net.ipv4.ip_forward
# 应输出: net.ipv4.ip_forward = 1
```

### 3.5 防火墙与安全组

**本机 ufw（若启用）：**

```bash
sudo ufw allow 51820/udp comment 'WireGuard'
sudo ufw allow OpenSSH
sudo ufw status
# 若 ufw 未开启且你打算启用：
# sudo ufw enable
```

**云厂商安全组 / 防火墙：**

- 入站：UDP `51820`（来源可先放开 `0.0.0.0/0`，稳定后再收紧）
- 出站：默认允许即可

### 3.6 启动服务

```bash
sudo systemctl enable --now wg-quick@wg0
sudo systemctl status wg-quick@wg0 --no-pager
sudo wg show
```

正常时 `wg show` 会显示 interface、public key、listening port，以及 peer（尚未连接时可能无 handshake）。

### 3.7 停止 / 重启 / 卸载接口

```bash
# 停止
sudo systemctl stop wg-quick@wg0

# 重启（改配置后常用）
sudo systemctl restart wg-quick@wg0

# 开机禁用
sudo systemctl disable wg-quick@wg0
```

---

## 4. 手机端配置

### 4.1 安装 App

- iOS：App Store 搜索 **WireGuard**
- Android：Google Play / F-Droid 搜索 **WireGuard**（官方客户端）

### 4.2 配置内容

在手机新建隧道，可「从文件创建」或「手动创建」。完整配置示例：

```ini
[Interface]
PrivateKey = <phone_private.key 的内容>
Address = 10.8.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server_public.key 的内容>
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

说明：

| 字段 | 含义 |
|------|------|
| `PrivateKey` | 手机私钥，与服务器 Peer 公钥成对 |
| `Address` | 手机在 VPN 内的 IP，须与服务器 `AllowedIPs` 一致 |
| `DNS` | 连接 VPN 后使用的 DNS；分流时可按需调整 |
| `Endpoint` | 服务器公网 IP（或域名）+ 端口 |
| `AllowedIPs` | 走隧道的目的地；见第 5 章 |
| `PersistentKeepalive` | 建议 `25`，利于穿越 NAT / 保持心跳 |

从服务器拷贝手机私钥与服务端公钥（在服务器上执行）：

```bash
echo "Phone PrivateKey:" && sudo cat /etc/wireguard/phone_private.key
echo "Server PublicKey:" && sudo cat /etc/wireguard/server_public.key
```

也可在服务器生成二维码（需安装 `qrencode`），用手机扫码导入：

```bash
sudo apt install -y qrencode

SERVER_PUB=$(sudo cat /etc/wireguard/server_public.key)
PHONE_PRIV=$(sudo cat /etc/wireguard/phone_private.key)

qrencode -t ansiutf8 <<EOF
[Interface]
PrivateKey = ${PHONE_PRIV}
Address = 10.8.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF
```

把 `YOUR_SERVER_IP` 换成真实地址后再生成。

### 4.3 连接与验证

1. 在 App 中打开隧道开关  
2. 服务器执行：`sudo wg show`，应出现 `latest handshake` 与双向 transfer  
3. 手机浏览器访问 [https://ifconfig.me](https://ifconfig.me)（全流量模式），应显示服务器公网 IP  

---

## 5. 分流：特定流量走 VPN

分流只改 **手机端** 配置里 Peer 的 `AllowedIPs`，改完后保存并重连。

### 5.1 常见策略

| 策略 | 手机端 `AllowedIPs` | 效果 |
|------|---------------------|------|
| 全局代理 | `0.0.0.0/0, ::/0` | 几乎全部 IPv4/IPv6 流量走服务器 |
| 仅 VPN 内互通 | `10.8.0.0/24` | 只能访问隧道内主机（如 `10.8.0.1`） |
| 指定内网 | `192.168.1.0/24` | 仅该局域网网段走 VPN |
| 多个网段 | `10.0.0.0/8, 172.16.0.0/12` | 多个 CIDR 用逗号分隔 |
| 单个 IP | `203.0.113.10/32` | 仅访问该 IP 时走 VPN |

示例（仅国内某内网 + VPN 网关）：

```ini
AllowedIPs = 10.8.0.0/24, 192.168.10.0/24
```

### 5.2 注意点

1. **域名无法直接写在 AllowedIPs**，需写成解析后的 IP/CIDR。域名经常变化时，更适合用 Clash / Surge 等规则客户端。  
2. 全局模式下手机流量都会经服务器，注意服务器带宽与流量费用。  
3. 部分系统在分流时仍可能改 DNS；若解析异常，可暂时去掉客户端 `DNS=` 行，或改为分流友好的 DNS 方案。  
4. 服务端 Peer 的 `AllowedIPs` 仍应是客户端地址（如 `10.8.0.2/32`），不要改成 `0.0.0.0/0`。

### 5.3 按 App / 域名精细分流

WireGuard 原生只按 IP 路由。若需要「某 App、某域名走代理」，可：

1. 继续用本手册搭建的 WireGuard 作为底层通道；或  
2. 在手机使用支持规则的客户端（Clash Meta、Surge、Shadowrocket 等），以 WireGuard / 其他协议为节点，用规则分流。

本手册以原生 WireGuard 分流为主。

---

## 6. 日常运维

### 6.1 查看连接状态

```bash
sudo wg show
sudo wg show wg0 dump
```

关注：

- `latest handshake`：近期有握手表示客户端在线或刚活跃过  
- `transfer`：收发流量  
- `endpoint`：客户端当前公网地址

### 6.2 查看服务日志

```bash
sudo journalctl -u wg-quick@wg0 -n 50 --no-pager
sudo journalctl -u wg-quick@wg0 -f
```

### 6.3 修改配置后生效

```bash
sudo nano /etc/wireguard/wg0.conf
sudo systemctl restart wg-quick@wg0
sudo wg show
```

仅增删 Peer、且希望不停主接口时，可用：

```bash
# 热添加 Peer 示例
sudo wg set wg0 peer <CLIENT_PUBLIC_KEY> allowed-ips 10.8.0.3/32
# 持久化：仍须写入 wg0.conf，否则重启丢失
```

### 6.4 备份

建议定期备份：

```bash
sudo tar czf ~/wireguard-backup-$(date +%F).tar.gz -C /etc wireguard
```

备份文件含私钥，妥善保管，勿上传公开仓库。

### 6.5 更换端口

1. 修改 `wg0.conf` 中 `ListenPort`  
2. 同步改安全组 / ufw  
3. 同步改手机 `Endpoint` 端口  
4. `sudo systemctl restart wg-quick@wg0`

---

## 7. 增删客户端

### 7.1 新增一台手机 / 电脑

1. 生成新密钥对：

```bash
cd /etc/wireguard
umask 077
wg genkey | tee client2_private.key | wg pubkey > client2_public.key
```

2. 在 `wg0.conf` 增加 Peer（IP 勿冲突，例如 `10.8.0.3`）：

```ini
[Peer]
# client2
PublicKey = <client2_public.key>
AllowedIPs = 10.8.0.3/32
```

3. 重启服务：

```bash
sudo systemctl restart wg-quick@wg0
```

4. 新设备配置：

```ini
[Interface]
PrivateKey = <client2_private.key>
Address = 10.8.0.3/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server_public.key>
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

### 7.2 删除 / 吊销客户端

1. 从 `wg0.conf` 删除对应 `[Peer]` 段  
2. `sudo systemctl restart wg-quick@wg0`  
3. 可选：删除对应私钥文件  

即时踢下线（未改 conf 则重启后若 conf 仍在会恢复）：

```bash
sudo wg set wg0 peer <CLIENT_PUBLIC_KEY> remove
```

---

## 8. 故障排查

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| 无 handshake | UDP 被拦、Endpoint 错误、密钥不匹配 | 查安全组/ufw、核对 IP:端口、核对公私钥配对 |
| 有握手但不能上网 | 未开转发、NAT 网卡名错误、iptables 失败 | 查 `ip_forward`、PostUp 中网卡名、`iptables -t nat -L -n` |
| 能 ping 10.8.0.1 不能上网 | 仅内网 AllowedIPs，或运营商拦截 | 检查客户端 AllowedIPs；换端口试一次 |
| 握手很快过期 | 蜂窝 NAT 回收 | 保持 `PersistentKeepalive = 25` |
| DNS 异常 | VPN DNS 不可达 | 改 `DNS = 8.8.8.8` 或去掉 DNS 行试验 |
| iOS 提示权限 | 未授权 VPN | 系统设置中允许 WireGuard 添加 VPN 配置 |

服务器侧快速检查清单：

```bash
sudo systemctl is-active wg-quick@wg0
sudo wg show
sysctl net.ipv4.ip_forward
ip -4 addr show wg0
sudo iptables -t nat -L POSTROUTING -n -v
sudo ss -ulnp | grep 51820
```

手机侧：

- 飞行模式开关一次后重连  
- 换 Wi‑Fi / 蜂窝试一次  
- 确认 `Endpoint` 无多余空格、端口正确  

---

## 9. 安全建议

1. **保护私钥**：`/etc/wireguard` 权限 `700`，密钥与 `wg0.conf` 为 `600`。  
2. **最小分流**：不需要全局时，用精确 `AllowedIPs`，减少经服务器的流量与暴露面。  
3. **安全组收紧**：若手机出口 IP 相对固定，可将 UDP 51820 来源限制到常用网段（注意：蜂窝 IP 常变，收紧可能导致连不上）。  
4. **及时吊销**：设备丢失后立即删除对应 Peer。  
5. **系统更新**：定期 `apt update && apt upgrade`。  
6. **勿用 HTTP 明文传密钥**；用 SSH、二维码当面导入即可。  
7. 服务器若仅作个人 VPN，可关闭不必要的对外端口，仅保留 SSH + WireGuard。

---

## 10. 附录

### 附录 A. CentOS / Rocky 安装

```bash
sudo dnf install -y epel-release
sudo dnf install -y wireguard-tools iptables

# 若内核模块未就绪，按发行版文档安装 wireguard 内核支持
sudo mkdir -p /etc/wireguard
# 后续密钥与 wg0.conf 步骤与本文第 3 章相同

# firewalld 示例
sudo firewall-cmd --permanent --add-port=51820/udp
sudo firewall-cmd --permanent --add-masquerade
sudo firewall-cmd --reload
```

### 附录 B. 配置字段速查

**服务端 `[Interface]`**

| 字段 | 说明 |
|------|------|
| Address | 本机隧道 IP |
| ListenPort | UDP 监听端口 |
| PrivateKey | 服务端私钥 |
| PostUp / PostDown | 启动/停止时执行的防火墙与 NAT 命令 |

**服务端 `[Peer]`**

| 字段 | 说明 |
|------|------|
| PublicKey | 客户端公钥 |
| AllowedIPs | 该客户端隧道 IP（路由到该 Peer） |

**客户端 `[Interface]` / `[Peer]`**

| 字段 | 说明 |
|------|------|
| Address | 本机隧道 IP |
| DNS | 可选 |
| Endpoint | 服务器 `IP:端口` |
| AllowedIPs | **分流表**：哪些目的地走隧道 |
| PersistentKeepalive | 建议 25 秒 |

### 附录 C. 地址规划建议

| 设备 | 地址 |
|------|------|
| 服务器 | `10.8.0.1/24` |
| 手机 1 | `10.8.0.2/32` |
| 手机 2 | `10.8.0.3/32` |
| 笔记本 | `10.8.0.10/32` |
| 预留 | `10.8.0.20+` |

同一 `10.8.0.0/24` 内不要分配重复地址。

### 附录 D. 一键检查脚本（可选）

在服务器保存为 `~/check-wg.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "== service =="
systemctl is-active wg-quick@wg0 || true
echo "== forward =="
sysctl net.ipv4.ip_forward
echo "== iface =="
ip -4 addr show wg0 2>/dev/null || echo "wg0 down"
echo "== wg =="
sudo wg show || true
echo "== listen =="
sudo ss -ulnp | grep -E '51820|wireguard' || true
echo "== nat =="
sudo iptables -t nat -L POSTROUTING -n -v | head -n 20
```

```bash
chmod +x ~/check-wg.sh
~/check-wg.sh
```

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-08-12 | 初版：安装、手机连接、分流、运维与排障 |

---

**使用提示**：全文将 `YOUR_SERVER_IP`、密钥占位符、网卡名替换为实际值后，按第 3 → 4 → 5 章顺序操作即可完成搭建与分流。
