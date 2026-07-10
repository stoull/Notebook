# NanoPi + OpenWrt 配置 VPN 网关

本文档介绍如何在 **NanoPi（运行 OpenWrt）** 上配置 VPN 网关，涵盖 **WireGuard** 和 **Tailscale** 两种方案。

适用场景：

- **远程回家**：在外面安全访问家里 NAS、摄像头、打印机等内网设备
- **VPN 网关**：让局域网内指定设备通过 VPN 访问外网（策略分流）

---

## 目录

1. [准备工作](#1-准备工作)
2. [方案选择](#2-方案选择)
3. [方案一：WireGuard（推荐有公网 IP）](#3-方案一wireguard推荐有公网-ip)
4. [方案二：Tailscale（推荐无公网 IP）](#4-方案二tailscale推荐无公网-ip)
5. [策略路由：部分设备走 VPN](#5-策略路由部分设备走-vpn)
6. [安全建议](#6-安全建议)
7. [常见问题排查](#7-常见问题排查)
8. [附录：配置文件速查](#8-附录配置文件速查)

---

## 1. 准备工作

### 1.1 硬件与系统

| 项目 | 要求 |
|------|------|
| 设备 | NanoPi R2S / R4S / R5S / R6S 等 |
| 系统 | OpenWrt 23.05 或 24.x（建议官方或可靠第三方固件） |
| 内存 | ≥ 512MB（WireGuard / Tailscale 均可流畅运行） |
| 存储 | ≥ 128MB 可用空间 |

### 1.2 网络信息（先记录下来）

在配置前，先确认以下信息：

```bash
# SSH 登录 OpenWrt 后执行
uci show network.lan
ip route show
```

记录：

| 信息 | 示例 | 你的值 |
|------|------|--------|
| LAN 网段 | `192.168.1.0/24` | |
| OpenWrt LAN IP | `192.168.1.1` | |
| WAN IP | 光猫/上级路由分配 | |
| 是否有公网 IP | 是 / 否 | |
| 能否做端口转发 | 是 / 否 | |

> **如何判断有无公网 IP**：在 OpenWrt 上查看 WAN 口 IP，与 [ip.sb](https://ip.sb) 显示的 IP 对比。若一致，通常有公网 IP（或可达的公网地址）。

### 1.3 访问 OpenWrt 的方式

- **Web 界面（LuCI）**：浏览器访问 `http://192.168.1.1`
- **SSH**：`ssh root@192.168.1.1`

后续命令若无特别说明，均在 SSH 中执行。

### 1.4 更新软件包

```bash
opkg update
```

---

## 2. 方案选择

```
你的目标是什么？
│
├── 远程回家（访问家里内网）
│   ├── 有公网 IP 或能做端口转发 → WireGuard 服务端 ✅
│   └── 无公网 IP / 不想折腾端口转发 → Tailscale Subnet Router ✅
│
└── VPN 网关（让部分 LAN 设备走 VPN 上网）
    └── WireGuard 客户端 + 策略路由（PBR）✅
```

| 方案 | 适用场景 | 需要公网 IP | 难度 |
|------|----------|-------------|------|
| WireGuard 服务端 | 远程回家 | 是（或端口转发） | ★★★ |
| Tailscale | 远程回家 | 否 | ★★ |
| WireGuard 客户端 + PBR | 部分设备走 VPN | 取决于 VPN 服务商 | ★★★★ |

---

## 3. 方案一：WireGuard（推荐有公网 IP）

WireGuard 是内核级 VPN 协议，性能高、配置简洁，适合作为 **远程回家** 的 VPN 服务端。

### 3.1 整体架构

```
┌─────────────┐         UDP 51820          ┌──────────────────┐
│  手机/笔记本  │ ────────────────────────► │  NanoPi OpenWrt  │
│ WG 客户端    │         公网 IP/DDNS        │  WireGuard 服务端  │
└─────────────┘                             └────────┬─────────┘
                                                     │ LAN
                                            ┌────────▼─────────┐
                                            │ 192.168.1.0/24   │
                                            │ NAS / 摄像头 / PC │
                                            └──────────────────┘
```

### 3.2 安装 WireGuard

**方法一：命令行**

```bash
opkg update
opkg install wireguard-tools kmod-wireguard luci-proto-wireguard
# 可选：Web 管理界面
opkg install luci-app-wireguard
```

**方法二：LuCI 界面**

1. 登录 LuCI → **System → Software**
2. 搜索并安装 `wireguard-tools`、`kmod-wireguard`、`luci-proto-wireguard`
3. 可选安装 `luci-app-wireguard`

安装完成后重启网络（可选）：

```bash
/etc/init.d/network restart
```

### 3.3 生成密钥

WireGuard 使用公私钥对认证。需要生成：

- **服务端**（OpenWrt）一对密钥
- **每个客户端**（手机、笔记本）各一对密钥

```bash
# 创建配置目录
mkdir -p /etc/wireguard
cd /etc/wireguard

# 生成服务端密钥
wg genkey | tee server_private.key | wg pubkey > server_public.key
chmod 600 server_private.key

# 生成客户端密钥（示例：手机）
wg genkey | tee phone_private.key | wg pubkey > phone_public.key
chmod 600 phone_private.key

# 查看密钥（后面配置要用）
echo "=== 服务端 ==="
echo "私钥: $(cat server_private.key)"
echo "公钥: $(cat server_public.key)"
echo ""
echo "=== 手机客户端 ==="
echo "私钥: $(cat phone_private.key)"
echo "公钥: $(cat phone_public.key)"
```

> **重要**：私钥绝不能泄露。建议把客户端私钥通过安全方式传到手机，不要发到公开渠道。

### 3.4 规划 IP 地址

| 角色 | 接口 / 地址 |
|------|-------------|
| WireGuard 网段 | `10.0.0.0/24` |
| OpenWrt 服务端 | `10.0.0.1` |
| 手机客户端 | `10.0.0.2` |
| 笔记本客户端 | `10.0.0.3` |
| 家里 LAN 网段 | `192.168.1.0/24`（按你的实际网段修改） |

### 3.5 配置 OpenWrt 服务端

#### 3.5.1 方法一：LuCI 图形界面（推荐新手）

1. 登录 LuCI → **Network → Interfaces → Add new interface**
2. 填写：
   - **Name**：`wg0`
   - **Protocol**：`WireGuard VPN`
3. 点击 **Create**，进入配置页：

**General Settings（常规）**

| 字段 | 值 |
|------|-----|
| Private Key | 粘贴 `server_private.key` 的内容 |
| Listen Port | `51820` |
| IP Addresses | `10.0.0.1/24` |

**Peers（对端 / 客户端）** → 点击 **Add peer**

以手机为例：

| 字段 | 值 |
|------|-----|
| Public Key | 手机的公钥（`phone_public.key`） |
| Allowed IPs | `10.0.0.2/32` |
| Persistent Keep Alive | `25` |

每增加一个客户端，就添加一个 Peer，Allowed IPs 设为该客户端的 `/32` 地址。

4. 点击 **Save**，再 **Save & Apply**

#### 3.5.2 方法二：直接编辑配置文件

编辑 `/etc/config/network`，追加：

```bash
vi /etc/config/network
```

追加内容（**替换其中的密钥和 IP**）：

```
config interface 'wg0'
    option proto 'wireguard'
    option private_key '<服务端私钥>'
    option listen_port '51820'
    list addresses '10.0.0.1/24'

config wireguard_wg0
    option description 'Phone'
    option public_key '<手机公钥>'
    list allowed_ips '10.0.0.2/32'
    option persistent_keepalive '25'

config wireguard_wg0
    option description 'Laptop'
    option public_key '<笔记本公钥>'
    list allowed_ips '10.0.0.3/32'
    option persistent_keepalive '25'
```

保存后重启网络：

```bash
/etc/init.d/network restart
```

验证接口是否起来：

```bash
wg show
# 应看到 wg0 接口和 listen port 51820
```

### 3.6 配置防火墙

WireGuard 接口需要加入防火墙，并允许 VPN 客户端访问 LAN。

#### 3.6.1 LuCI 操作

1. **Network → Firewall → Zones**
2. 点击 **Add**，新建 zone：
   - Name：`vpn`
   - Input：`accept`
   - Output：`accept`
   - Forward：`accept`
   - Masquerading（NAT）：**勾选**
   - Covered networks：勾选 `wg0`
3. 在 **Forwardings** 区域添加：
   - `lan` → `vpn`：允许
   - `vpn` → `lan`：允许
4. **Save & Apply**

#### 3.6.2 命令行配置

编辑 `/etc/config/firewall`：

```
config zone
    option name 'vpn'
    option input 'ACCEPT'
    option output 'ACCEPT'
    option forward 'ACCEPT'
    list network 'wg0'
    option masq '1'
    option mtu_fix '1'

config forwarding
    option src 'lan'
    option dest 'vpn'

config forwarding
    option src 'vpn'
    option dest 'lan'
```

应用：

```bash
/etc/init.d/firewall restart
```

### 3.7 端口转发（若无公网 IP 或在上级路由后）

若 NanoPi 不是拨号主路由，需要在 **上级路由（光猫/主路由）** 做端口转发：

| 外部端口 | 内部 IP | 内部端口 | 协议 |
|----------|---------|----------|------|
| 51820 | NanoPi LAN IP（如 192.168.1.1） | 51820 | UDP |

### 3.8 配置 DDNS（动态公网 IP 时）

家庭宽带 IP 常会变化，建议配置 DDNS，客户端用域名连接。

**LuCI 路径**：**Services → Dynamic DNS**

常用服务：Cloudflare、No-IP、DuckDNS 等。按你的 DNS 服务商填写 API 信息，域名例如 `home.example.com`。

### 3.9 配置客户端

#### 3.9.1 手机 / 笔记本通用配置

创建客户端配置文件 `phone.conf`（内容示例）：

```ini
[Interface]
PrivateKey = <手机私钥>
Address = 10.0.0.2/32
DNS = 192.168.1.1

[Peer]
PublicKey = <服务端公钥>
Endpoint = home.example.com:51820
AllowedIPs = 192.168.1.0/24, 10.0.0.0/24
PersistentKeepalive = 25
```

字段说明：

| 字段 | 说明 |
|------|------|
| `Address` | 客户端在 VPN 网段中的地址 |
| `DNS` | 连上 VPN 后使用的 DNS，填 OpenWrt LAN IP 即可 |
| `Endpoint` | 家里的公网 IP 或 DDNS 域名 + 端口 |
| `AllowedIPs` | 哪些流量走 VPN。远程回家填 `192.168.1.0/24, 10.0.0.0/24` |
| `PersistentKeepalive` | 保持 NAT 映射，移动网络建议 `25` |

#### 3.9.2 导入客户端

| 平台 | 操作 |
|------|------|
| iOS / Android | 安装 WireGuard App → 扫描二维码或导入 `.conf` |
| Windows / macOS | 安装 WireGuard 客户端 → Import tunnel |
| Linux | `sudo wg-quick up phone.conf` |

**生成二维码**（在 OpenWrt 上，需安装 qrencode）：

```bash
opkg install qrencode
qrencode -t ansiutf8 < phone.conf
```

用手机 WireGuard App 扫描终端显示的二维码即可。

### 3.10 验证 WireGuard 远程回家

1. **断开手机 Wi-Fi**，改用 4G/5G（确保不在家里局域网）
2. 打开 WireGuard，连接刚配置的隧道
3. 验证：

```bash
# 应能 ping 通 OpenWrt
ping 192.168.1.1

# 应能 ping 通内网设备
ping 192.168.1.100

# 访问 NAS Web 界面
# 浏览器打开 http://192.168.1.100:5000
```

4. 在 OpenWrt 上查看连接状态：

```bash
wg show
# 应看到 phone 的 latest handshake 时间
```

---

## 4. 方案二：Tailscale（推荐无公网 IP）

Tailscale 基于 WireGuard，但自动处理 NAT 穿透和密钥管理，**无需公网 IP 和端口转发**，适合国内常见家庭宽带。

### 4.1 整体架构

```
┌─────────────┐                              ┌──────────────────┐
│  手机/笔记本  │ ◄──── Tailscale 云 ────► │  NanoPi OpenWrt  │
│ Tailscale   │      （自动 NAT 穿透）        │  Subnet Router   │
└─────────────┘                              └────────┬─────────┘
                                                      │ LAN
                                             ┌────────▼─────────┐
                                             │ 192.168.1.0/24   │
                                             │ NAS / 摄像头 / PC │
                                             └──────────────────┘
```

### 4.2 注册 Tailscale 账号

1. 访问 [https://tailscale.com](https://tailscale.com) 注册（可用 Google / GitHub / 邮箱）
2. 免费版支持最多 100 台设备，个人远程回家完全够用

### 4.3 在 OpenWrt 上安装 Tailscale

```bash
opkg update
opkg install tailscale
```

若 `opkg` 找不到包，可手动安装（以 aarch64 为例，按你的架构调整）：

```bash
# 查看架构
opkg print-architecture

# 从 Tailscale 官方 GitHub Release 下载对应架构的 ipk
# 或使用第三方仓库，参考 OpenWrt 论坛 Tailscale 安装帖
```

### 4.4 启动并登录 Tailscale

```bash
# 启动 tailscale
/etc/init.d/tailscale start
/etc/init.d/tailscale enable   # 开机自启

# 登录（会输出一个 URL，复制到浏览器完成授权）
tailscale up
```

浏览器打开输出的链接，用 Tailscale 账号登录并授权此设备。

登录成功后，在 OpenWrt 上验证：

```bash
tailscale status
# 应看到本机和一个 100.x.x.x 的 Tailscale IP
```

### 4.5 配置 Subnet Router（关键步骤）

Subnet Router 让外部 Tailscale 设备能访问家里整个 LAN 网段。

```bash
# 将 192.168.1.0/24 替换为你的实际 LAN 网段
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
```

然后在 **Tailscale 管理后台** 批准路由：

1. 打开 [https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines)
2. 找到 NanoPi 设备，点击 **...** → **Edit route settings**
3. 勾选 `192.168.1.0/24` → **Save**

### 4.6 配置 OpenWrt 防火墙

Tailscale 接口（通常为 `tailscale0`）需要能转发到 LAN：

```bash
# 查看 tailscale 接口名
ip link show | grep tailscale
```

**LuCI 操作**：

1. **Network → Firewall → Zones → Add**
   - Name：`tailscale`
   - Input / Output / Forward：`accept`
   - Masquerading：**勾选**
   - Covered networks：勾选 `tailscale0`（或实际接口名）
2. 添加 Forwarding：
   - `tailscale` → `lan`：允许
   - `lan` → `tailscale`：允许
3. **Save & Apply**

**命令行**（编辑 `/etc/config/firewall`）：

```
config zone
    option name 'tailscale'
    option input 'ACCEPT'
    option output 'ACCEPT'
    option forward 'ACCEPT'
    list network 'tailscale0'
    option masq '1'
    option mtu_fix '1'

config forwarding
    option src 'tailscale'
    option dest 'lan'

config forwarding
    option src 'lan'
    option dest 'tailscale'
```

```bash
/etc/init.d/firewall restart
```

### 4.7 启用 IP 转发

确保 OpenWrt 允许转发：

```bash
# 临时启用
echo 1 > /proc/sys/net/ipv4/ip_forward

# 永久启用
uci set network.globals.forwarding='1'
uci commit network
/etc/init.d/network restart
```

### 4.8 在其他设备安装 Tailscale

| 平台 | 操作 |
|------|------|
| iOS / Android | App Store / 应用商店搜索 Tailscale，登录同一账号 |
| Windows / macOS | [https://tailscale.com/download](https://tailscale.com/download) |
| Linux | `curl -fsSL https://tailscale.com/install.sh \| sh && tailscale up` |

### 4.9 验证 Tailscale 远程回家

1. 手机 **断开家里 Wi-Fi**，改用移动数据
2. 确认 Tailscale 已连接（App 显示 Connected）
3. 测试：

```bash
ping 192.168.1.1      # OpenWrt
ping 192.168.1.100    # 内网 NAS
```

4. 浏览器访问内网服务，例如 `http://192.168.1.100:5000`

### 4.10 Tailscale 常用管理命令

```bash
# 查看状态
tailscale status

# 查看本机 Tailscale IP
tailscale ip -4

# 重新连接
tailscale down && tailscale up --advertise-routes=192.168.1.0/24

# 退出登录
tailscale logout
```

### 4.11 使 Subnet Router 配置持久化

`tailscale up` 的参数重启后可能丢失，写入启动脚本：

```bash
vi /etc/rc.local
```

在 `exit 0` 之前添加：

```bash
sleep 10
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
```

```bash
chmod +x /etc/rc.local
```

---

## 5. 策略路由：部分设备走 VPN

若目标不是远程回家，而是让 **局域网内部分设备** 通过 WireGuard 访问外网（VPN 网关 / 分流），使用 **WireGuard 客户端 + PBR（策略路由）**。

> Tailscale 不适合做「翻墙网关」，此节仅针对 WireGuard 客户端场景。

### 5.1 架构

```
┌──────────┐                    ┌──────────────┐
│ 电脑 A    │ ── 走 VPN ──────► │              │
│ 192.168.1.100              │  NanoPi      │ ── wg0 ──► VPN 服务器
├──────────┤                    │  OpenWrt     │
│ 电脑 B    │ ── 直连 WAN ────► │  + PBR 分流   │ ── wan ──► 互联网
│ 192.168.1.101              │              │
└──────────┘                    └──────────────┘
```

### 5.2 安装 PBR

```bash
opkg update
opkg install pbr luci-app-pbr
/etc/init.d/pbr enable
/etc/init.d/pbr start
```

### 5.3 配置 WireGuard 客户端接口

假设你有一个外部 WireGuard VPN 服务（如自建 VPS 或订阅服务）。

LuCI → **Network → Interfaces → Add**：

| 字段 | 值 |
|------|-----|
| Name | `wg0` |
| Protocol | WireGuard VPN |
| Private Key | 客户端私钥 |
| IP Addresses | `10.0.0.2/32`（按服务商分配） |

Peer 配置：

| 字段 | 值 |
|------|-----|
| Public Key | 服务端公钥 |
| Endpoint | `vpn.example.com:51820` |
| Allowed IPs | `0.0.0.0/0`（全局）或仅特定网段 |
| Persistent Keep Alive | `25` |

> **注意**：做分流时，`Allowed IPs` 建议 **不要** 填 `0.0.0.0/0`，只填 VPN 服务端网段。由 PBR 决定哪些设备走 wg0。

### 5.4 配置 PBR 策略

LuCI → **Services → Policy Routing**：

1. 启用 PBR
2. 添加规则：
   - **Source IP**：`192.168.1.100`（要走 VPN 的设备）
   - **Interface**：`wg0`
3. 其他设备不添加规则，默认走 WAN

或使用 IP 集合 / MAC 地址指定设备。

```bash
/etc/init.d/pbr restart
```

### 5.5 验证分流

在指定设备（192.168.1.100）上：

```bash
curl ifconfig.me
# 应显示 VPN 服务器的 IP
```

在其他设备上：

```bash
curl ifconfig.me
# 应显示家庭宽带的 IP
```

---

## 6. 安全建议

### 6.1 通用

- [ ] **不要把 SSH、LuCI 管理端口暴露到公网**，远程管理走 VPN 即可
- [ ] **定期更新** OpenWrt 和 VPN 组件：`opkg update && opkg upgrade`
- [ ] WireGuard 私钥妥善保管，不要提交到 Git 或发到公开渠道
- [ ] 为 VPN 客户端使用独立网段（如 `10.0.0.0/24`），与 LAN 隔离

### 6.2 WireGuard 专属

- [ ] 每个客户端独立密钥，方便单独吊销
- [ ] 客户端 `AllowedIPs` 只填需要的网段，避免过度路由
- [ ] 使用 DDNS + 域名连接，避免 IP 变化导致连不上

### 6.3 Tailscale 专属

- [ ] 在管理后台启用 **ACL**，限制哪些设备能访问 Subnet Route
- [ ] 定期检查已授权设备列表，移除不用的设备
- [ ] 敏感环境可考虑自建 **Headscale** 替代 Tailscale 官方控制面

### 6.4 Kill Switch（防泄漏）

VPN 断线时，防止流量从 WAN 直连泄露：

- PBR 中启用 **Strict** 模式
- 或在防火墙中限制：指定设备只能走 VPN 接口，VPN 断开则阻断

---

## 7. 常见问题排查

### 7.1 WireGuard 连不上

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| 握手超时 | 端口未通 | 检查上级路由是否转发 UDP 51820 |
| 握手超时 | 防火墙拦截 | `iptables -L -n` 检查，确认 wan 允许 51820/udp |
| 能握手但 ping 不通 LAN | 防火墙 zone 未配置 | 检查 vpn → lan forwarding 和 masq |
| 能 ping OpenWrt 但不通其他设备 | 目标设备防火墙 | 检查 NAS/PC 是否允许来自 10.0.0.0/24 的访问 |
| 之前能用现在不行 | 公网 IP 变了 | 更新 DDNS 或客户端 Endpoint |

**调试命令**：

```bash
# OpenWrt 上
wg show                          # 查看 WireGuard 状态
logread | grep wireguard         # 查看日志
tcpdump -i wan port 51820 -n     # 抓包看是否有 UDP 51820 流量

# 客户端上
ping 10.0.0.1                    # 先 ping VPN 网关
ping 192.168.1.1                 # 再 ping LAN 网关
```

### 7.2 Tailscale 连不上或访问不了内网

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| 设备显示 Offline | 未登录或网络问题 | `tailscale up` 重新登录 |
| 能连 Tailscale IP 但不通 LAN | Subnet Route 未批准 | 管理后台 Edit route settings 勾选网段 |
| 能连 Tailscale IP 但不通 LAN | 防火墙未放行 | 检查 tailscale zone 和 forwarding |
| 重启后 Subnet Route 失效 | 启动参数未持久化 | 写入 `/etc/rc.local` |
| 速度慢 | 走了 DERP 中继 | `tailscale netcheck` 检查是否能直连 |

**调试命令**：

```bash
tailscale status                 # 查看所有节点状态
tailscale netcheck               # 检测 NAT 穿透能力
tailscale ping <设备名>           # 测试连通性
ip route show table 52           # 查看 Tailscale 路由表
```

### 7.3 性能问题

| 现象 | 解决方法 |
|------|----------|
| VPN 速度慢 | 检查 MTU，WireGuard 建议 `1420` 或 `1280` |
| 延迟高 | Tailscale 尝试直连；WireGuard 选近的 VPS |
| CPU 占用高 | 确认使用内核 WireGuard（`kmod-wireguard`），而非用户态实现 |

**MTU 调整**（WireGuard 接口）：

LuCI → wg0 接口 → Advanced Settings → Override MTU → `1420`

### 7.4 DNS 问题

| 现象 | 解决方法 |
|------|----------|
| 域名无法解析 | 客户端 DNS 设为 `192.168.1.1` 或指定 DNS |
| 解析结果不对 | 检查 OpenWrt DNS 设置（LuCI → Network → DHCP and DNS） |

---

## 8. 附录：配置文件速查

### 8.1 WireGuard 服务端 `/etc/config/network` 完整示例

```
config interface 'wg0'
    option proto 'wireguard'
    option private_key 'SERVER_PRIVATE_KEY_HERE'
    option listen_port '51820'
    list addresses '10.0.0.1/24'

config wireguard_wg0
    option description 'Phone'
    option public_key 'PHONE_PUBLIC_KEY_HERE'
    list allowed_ips '10.0.0.2/32'
    option persistent_keepalive '25'

config wireguard_wg0
    option description 'Laptop'
    option public_key 'LAPTOP_PUBLIC_KEY_HERE'
    list allowed_ips '10.0.0.3/32'
    option persistent_keepalive '25'
```

### 8.2 WireGuard 客户端 `.conf` 完整示例

```ini
[Interface]
PrivateKey = PHONE_PRIVATE_KEY_HERE
Address = 10.0.0.2/32
DNS = 192.168.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
Endpoint = home.example.com:51820
AllowedIPs = 192.168.1.0/24, 10.0.0.0/24
PersistentKeepalive = 25
```

### 8.3 防火墙 zone 完整示例

```
config zone
    option name 'vpn'
    option input 'ACCEPT'
    option output 'ACCEPT'
    option forward 'ACCEPT'
    list network 'wg0'
    option masq '1'
    option mtu_fix '1'

config forwarding
    option src 'lan'
    option dest 'vpn'

config forwarding
    option src 'vpn'
    option dest 'lan'
```

### 8.4 Tailscale 一键启动脚本

`/etc/rc.local` 内容：

```bash
#!/bin/sh
sleep 10
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
exit 0
```

### 8.5 常用命令速查

| 操作 | 命令 |
|------|------|
| 查看 WireGuard 状态 | `wg show` |
| 重启 WireGuard | `/etc/init.d/network restart` |
| 查看 Tailscale 状态 | `tailscale status` |
| 重启 Tailscale | `/etc/init.d/tailscale restart` |
| 查看防火墙规则 | `iptables -L -n -v` |
| 查看路由表 | `ip route show` |
| 查看系统日志 | `logread -e vpn\|wireguard\|tailscale` |
| 测试端口连通 | `nc -zvu <公网IP> 51820` |

---

## 快速决策卡

```
┌─────────────────────────────────────────────────────┐
│              NanoPi VPN 网关配置决策                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  远程回家 + 有公网 IP                                │
│  → 第 3 章 WireGuard 服务端                          │
│                                                     │
│  远程回家 + 无公网 IP                                │
│  → 第 4 章 Tailscale Subnet Router                  │
│                                                     │
│  部分设备走 VPN 上网                                 │
│  → 第 3 章（客户端模式）+ 第 5 章 PBR                │
│                                                     │
│  两种都要                                           │
│  → WireGuard 服务端（远程回家）                       │
│    + WireGuard 客户端 + PBR（分流）                   │
│    或 Tailscale（远程回家）+ WireGuard 客户端（分流）  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

> 文档版本：2026-07  
> 适用：NanoPi + OpenWrt 23.05 / 24.x  
> 如有问题，可先查看 [第 7 章 常见问题排查](#7-常见问题排查)
