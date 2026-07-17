# OpenWrt + Tailscale 问题及要点记录

基于 NanoPi R2S（旁路由）+ OpenWrt 25.12.x + Tailscale 远程回家实践整理。  
目标：外网设备经 Tailscale 访问家里整段局域网（如 `192.168.1.0/24`）。

---

## 1. 旁路由基础（先做对）

| 项 | 推荐值 |
|----|--------|
| 接线 | 主路由 LAN → R2S **LAN**（不要接 WAN） |
| R2S IP | 如 `192.168.1.11`（勿与主路由 `192.168.1.1` 冲突） |
| 网关 | `192.168.1.1`（主路由） |
| DNS（OpenWrt 自己用） | 如 `223.5.5.5` 或 `192.168.1.1` |
| DHCP | **关闭**（LAN → DHCP Server → Ignore interface） |

直连电脑能访问、插路由器就不能：多半是 **接错 WAN/LAN**，或 IP 仍是 `192.168.1.1` 与主路由冲突。

R2S 解析外网靠 **OpenWrt 的 `network.lan.dns`**，不靠 Tailscale Global DNS。

```bash
uci set network.lan.ipaddr='192.168.1.11'
uci set network.lan.netmask='255.255.255.0'
uci set network.lan.gateway='192.168.1.1'
uci delete network.lan.dns 2>/dev/null
uci add_list network.lan.dns='223.5.5.5'
uci set dhcp.lan.ignore='1'
uci commit
/etc/init.d/network restart
```

---

## 2. Tailscale 远程回家：核心模型

```
手机/电脑 (Tailscale, 5G)
        │
        ▼
   R2S (Subnet Router, 如 192.168.1.11)
        │  需要：转发 + NAT (masq)
        ▼
   其它内网设备 (如 192.168.1.6)
```

| 能访问 | 说明 |
|--------|------|
| 仅 R2S 本机 LAN IP（如 `.11`） | 子网路由/批准/手机 Accept subnets **多半已 OK**；缺的是 **转发/NAT** |
| 其它内网 IP（如 `.6`） | 需要 `tailscale → lan` + `masq=1` + `ip_forward=1` |

**判断口诀：** 能到网关本机、到不了其它 IP = 转发/防火墙问题，不是「没连上 Tailscale」。

---

## 3. Tailscale 推荐启动参数（R2S）

本环境实际使用（旁路由 + 自管防火墙）：

```bash
tailscale up --accept-routes --advertise-routes=192.168.1.0/24 --accept-dns=false --netfilter-mode=off
```

| 参数 | 作用 |
|------|------|
| `--advertise-routes=192.168.1.0/24` | 广播家里网段 |
| `--accept-routes` | 接受其它节点路由（按需） |
| `--accept-dns=false` | R2S **不用** Tailscale DNS，继续用 OpenWrt DNS |
| `--netfilter-mode=off` | Tailscale **不自动改 iptables**，必须自己配 OpenWrt 防火墙 |

注意：

1. **命令必须一行写完**，不要拆行（中间多一个 `-` 会把参数弄坏）。
2. 若报错要求带上已有参数，按提示补齐，或用：

```bash
tailscale up --reset --accept-routes --advertise-routes=192.168.1.0/24 --accept-dns=false --netfilter-mode=off
```

3. `tailscale status` 里可能只显示 `-`，**以 prefs 为准**：

```bash
tailscale debug prefs | grep -i -A3 AdvertiseRoutes
# 应有 "192.168.1.0/24"
```

### 持久化（防重启丢失）

在 `/etc/rc.local` 的 `exit 0` **之前**：

```bash
sleep 15
tailscale up --accept-routes --advertise-routes=192.168.1.0/24 --accept-dns=false --netfilter-mode=off
```

---

## 4. 管理后台必须批准子网

在 Tailscale Admin → 设备 openwrt → Subnets：

| 项 | 期望 |
|----|------|
| Approved | `192.168.1.0/24` |
| Exit Node | 远程回家 **不必** 开 |
| Awaiting Approval | 应为空 |

未批准时：外面往往只能摸到 R2S 相关路径，整网访问不可靠。

---

## 5. 防火墙（最关键、最易漏）

因 `--netfilter-mode=off`，**必须**自配：

```bash
# tailscale 一般为 @zone[2]，以 uci show 为准
uci set firewall.@zone[2].name='tailscale'
uci set firewall.@zone[2].input='ACCEPT'
uci set firewall.@zone[2].output='ACCEPT'
uci set firewall.@zone[2].forward='ACCEPT'
uci set firewall.@zone[2].masq='1'
uci set firewall.@zone[2].mtu_fix='1'
uci -q delete firewall.@zone[2].device
uci -q delete firewall.@zone[2].network
uci add_list firewall.@zone[2].device='tailscale0'
uci add_list firewall.@zone[2].network='tailscale0'

uci add firewall forwarding
uci set firewall.@forwarding[-1].src='tailscale'
uci set firewall.@forwarding[-1].dest='lan'

uci add firewall forwarding
uci set firewall.@forwarding[-1].src='lan'
uci set firewall.@forwarding[-1].dest='tailscale'

uci commit firewall
/etc/init.d/firewall restart
echo 1 > /proc/sys/net/ipv4/ip_forward
```

### 两条转发的区别

| 规则 | 方向 | 用途 |
|------|------|------|
| **tailscale → lan** | 外面 → 家里 | 手机访问 `192.168.1.6`（**远程回家必开**） |
| **lan → tailscale** | 家里 → 外面 | 家里设备主动访问 Tailscale 节点 |

**`masq=1` 必开**：否则内网设备看到源地址是 `100.x.x.x`，回包常常回不来。

### 自检

```bash
ip link show | grep tailscale          # tailscale0 应 UP
cat /proc/sys/net/ipv4/ip_forward      # 必须为 1
ping -c 2 192.168.1.6                  # R2S 本机先要通
uci show firewall.@zone[2]             # masq=1, device=tailscale0
uci show firewall | grep forwarding
```

---

## 6. 手机客户端检查清单

```
□ Tailscale 显示 Connected（不是 offline）
□ 打开 Use Tailscale subnets（使用子网路由）
□ 测试时用 5G/4G，不要连家里 Wi‑Fi
□ 先测纯 IP：192.168.1.11 → 再测 192.168.1.6
□ 若用域名：再开 Use Tailscale DNS，并检查 Split DNS
```

---

## 7. DNS：OpenWrt / Global / Split / Override

### 分工

| 谁解析 | 靠什么 |
|--------|--------|
| **R2S 自己**（apk、ping 外网域名） | OpenWrt `network.lan.dns`；保持 `--accept-dns=false` |
| **手机/电脑**（连 Tailscale 时） | Tailscale DNS：MagicDNS / Split DNS / Global nameservers |

**不要用 Tailscale Override 来「给 R2S 解析外网」——无效。**

### Split DNS vs Override + Global

典型优先级：

```text
1. MagicDNS / 机器名
2. Split DNS（后缀匹配 → 指定内网 DNS，如 192.168.1.1）
3. Global nameservers（公共 DNS）
```

| 问题 | 答案 |
|------|------|
| Override + Global 会禁用 Split 吗？ | **按设计不会**；Split 优先，Global 兜底 |
| 什么时候像「Split 坏了」？ | Split 的 DNS IP 从手机达不到；后缀写错；客户端没用 Tailscale DNS |
| 纯 IP 不通 `.6` 是 DNS 吗？ | **不是**；是转发/NAT |

Split DNS 要生效，还要求：**Nameserver IP（如 192.168.1.1）经子网路由可达**。

客户端可用（在能跑 dig 的设备上）：

```bash
dig @100.100.100.100 你的内网域名
ping -c 2 192.168.1.1
```

---

## 8. 曾遇到的问题与结论

| 现象 | 原因 / 处理 |
|------|-------------|
| `opkg: not found`，且 `/rom/bin/opkg` 也没有 | **正常**。OpenWrt **25.12+** 已改用 **`apk`**（Alpine Package Keeper）替代 `opkg`，不是镜像损坏。用 `which apk` / `apk update` 即可 |
| 直连能管 R2S，上主路由后 ping 不通 | 接错口 / IP 冲突 / 未改旁路由 IP |
| 忘记关 DHCP | 补勾 Ignore interface，电脑 renew IP |
| `tailscale up` 报必须提及所有非默认参数 | 按提示带齐参数，或加 `--reset` |
| prefs 有子网、后台已 Approved，仍只能访问 R2S | **缺 firewall：tailscale→lan + masq**（netfilter=off） |
| 以为 Global nameservers 导致不能访问 `.6` | 纯 IP 不通与 DNS 无关；改 DNS 时可能顺带弄丢转发配置 |
| UDP GRO / netfilter=off Warning | 提示信息；后者表示必须自配防火墙 |

---

## 9. 快速验收清单

```text
□ 旁路由：IP/网关/DNS/关 DHCP/LAN 接线正确
□ R2S：AdvertiseRoutes 含 192.168.1.0/24
□ 后台：Approved 192.168.1.0/24
□ 防火墙：tailscale zone + masq=1 + tailscale→lan
□ ip_forward=1；R2S 能 ping 通目标内网 IP
□ 手机：在线 + Accept subnets + 蜂窝网络
□ 5G 下：通 192.168.1.11，再通 192.168.1.6
□ （可选）Split DNS：dig @100.100.100.100 内网域名
```

---

## 10. 软件包管理：apk（OpenWrt 25.12+）

OpenWrt **25.12** 起包管理器从 **`opkg` 切换为 `apk`**。没有 `opkg` **不等于**系统坏了。

| 旧 (opkg) | 新 (apk) |
|-----------|----------|
| `opkg update` | `apk update` |
| `opkg install <pkg>` | `apk add <pkg>` |
| `opkg remove <pkg>` | `apk del <pkg>` |
| `opkg list-installed` | `apk list --installed` |
| `opkg search <kw>` | `apk search <kw>` |

```bash
which apk
apk update
apk add wireguard-tools   # 示例
```

注意：

- 多数软件包名仍与从前相同；命令行参数与 `opkg` 不同。
- **不要随意使用 `apk upgrade` 做整机升级**（易弄乱依赖）；系统升级优先用 LuCI Attended Sysupgrade / `owut` 等官方推荐方式。
- 参考：OpenWrt Wiki「apk package manager」「opkg to apk cheatsheet」。

---

## 11. 常用命令速查

```bash
# 软件包 (25.12+)
apk update
apk add <package>

# Tailscale
tailscale status
tailscale debug prefs | grep -i -A5 AdvertiseRoutes
tailscale up --accept-routes --advertise-routes=192.168.1.0/24 --accept-dns=false --netfilter-mode=off

# 网络 / 转发
ip link show | grep tailscale
cat /proc/sys/net/ipv4/ip_forward
ping -c 2 192.168.1.1
ping -c 2 192.168.1.6

# 防火墙
uci show firewall | grep "\.name="
uci show firewall.@zone[2]
uci show firewall | grep forwarding
/etc/init.d/firewall restart

# 抓包（手机访问 .6 时）
tcpdump -ni tailscale0 host 192.168.1.6
tcpdump -ni br-lan host 192.168.1.6
```

---

## 12. 约束备忘

- 协助排查时：**不要访问 `tailscale.com` 及 `*.tailscale.com`**（避免触发网络限制）。
- Tailscale 管理页、文档链接由用户本机浏览器自行操作；信息以本机 `tailscale` 命令输出与用户描述为准。

---

## 13. 相关文档

- `NanoPi上配置VPN网关.md` — WireGuard / Tailscale 完整配置说明  

---

> 记录日期：2026-07  
> 环境：NanoPi R2S · OpenWrt 25.12.x（包管理器为 **apk**，非 opkg）· Tailscale Subnet Router · 旁路由 `192.168.1.0/24`
