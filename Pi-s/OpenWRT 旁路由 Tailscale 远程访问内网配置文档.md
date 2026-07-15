# OpenWRT 旁路由 Tailscale 远程访问内网配置文档

本文档适用于将 OpenWRT 作为旁路由，通过 Tailscale 组建 VPN，实现从外网安全访问家庭内网设备（如 `192.168.1.9`）的完整配置流程。

---

## 1. 前提条件

- OpenWRT 已正确接入家庭局域网，并获得固定 IP（例如 `192.168.1.2`）。
- OpenWRT 能够正常访问互联网（用于下载软件包和连接 Tailscale 服务）。
- 已拥有 Tailscale 账号，并可在 [Tailscale 管理后台](https://login.tailscale.com/admin) 登录。
- 有 SSH 访问 OpenWRT 的权限。

---

## 2. 安装 Tailscale

通过 SSH 登录 OpenWRT，执行以下命令安装 Tailscale 及其依赖：

```bash
# 更新软件源
opkg update

# 安装 Tailscale 和必要内核模块
opkg install tailscale kmod-tun
```

> **说明**：`kmod-tun` 是虚拟网卡所必需的内核模块，如未安装会导致 `tailscale0` 接口无法创建。

---

## 3. 启动 Tailscale 并完成认证

### 3.1 启动服务
```bash
# 启动 Tailscale 守护进程
/etc/init.d/tailscale start

# 设置开机自启
/etc/init.d/tailscale enable
```

### 3.2 登录认证
执行以下命令，并按提示访问生成的链接完成登录：
```bash
tailscale up
```
登录成功后，Tailscale 会自动创建虚拟网卡 `tailscale0` 并分配一个 `100.x.x.x` 的 IP。

### 3.3 验证虚拟网卡
```bash
ip addr show tailscale0
```
应看到类似 `inet 100.x.x.x/32` 的输出，表示网卡已正常创建。

---

## 4. 防火墙配置（推荐方案：独立区域）

为了精细控制 Tailscale 流量，我们为 `tailscale0` 创建一个独立的防火墙区域 `vpn`，并与 `lan` 区域建立双向转发。

### 4.1 创建接口
Tailscale 默认只生成了设备 `tailscale0`，需先在 OpenWRT 中为其建立一个网络接口。

**通过 LuCI 界面：**
- 进入 **网络 (Network) -> 接口 (Interfaces)**。
- 点击 **添加新接口**，名称填 `tailscale`，协议选 **“不配置协议”**，设备选择 **`tailscale0`**，点击创建。

**或通过 SSH 命令行：**
```bash
uci set network.tailscale=interface
uci set network.tailscale.proto='none'
uci set network.tailscale.device='tailscale0'
uci commit network
```

### 4.2 创建防火墙区域
**通过 LuCI：**
- 进入 **网络 (Network) -> 防火墙 (Firewall)**。
- 在 **区域 (Zones)** 选项卡，点击 **添加**：
  - 名称：`vpn`
  - 入站、出站、转发：均设为 **“接受”**
  - 已涵盖的网络：勾选 `tailscale`（即上一步创建的接口）
  - 勾选 **“IP 动态伪装”** 和 **“MSS 锁定”**

**或通过 SSH 命令行：**
```bash
uci add firewall zone
uci set firewall.@zone[-1].name='vpn'
uci set firewall.@zone[-1].input='ACCEPT'
uci set firewall.@zone[-1].output='ACCEPT'
uci set firewall.@zone[-1].forward='ACCEPT'
uci set firewall.@zone[-1].masq='1'
uci set firewall.@zone[-1].mtu_fix='1'
uci set firewall.@zone[-1].network='tailscale'
uci commit firewall
```

### 4.3 设置区域间转发
在防火墙 **区域间转发** 中添加两条规则：
- 允许从 `lan` 到 `vpn` 的转发。
- 允许从 `vpn` 到 `lan` 的转发。

**命令行操作：**
```bash
uci add firewall forwarding
uci set firewall.@forwarding[-1].src='vpn'
uci set firewall.@forwarding[-1].dest='lan'
uci commit firewall

uci add firewall forwarding
uci set firewall.@forwarding[-1].src='lan'
uci set firewall.@forwarding[-1].dest='vpn'
uci commit firewall
```

### 4.4 重启防火墙
```bash
service firewall restart
```

> **备选方案（更简单）**：如果不需要独立区域，可直接将 `tailscale0` 设备加入 `lan` 区域：
> ```bash
> uci add_list firewall.@zone[0].device='tailscale0'   # 假设 @zone[0] 是 lan
> uci commit firewall
> service firewall restart
> ```
> 此方案不需要创建接口和独立区域，但无法进行精细控制。

---

## 5. 开启子网路由（关键）

为了让 Tailscale 网络中的设备能够访问你的家庭内网（如 `192.168.1.0/24`），必须在 OpenWRT 上通告并批准子网路由。

### 5.1 在 OpenWRT 上通告路由
执行以下命令（假设你的内网网段是 `192.168.1.0/24`）：
```bash
tailscale up --advertise-routes=192.168.1.0/24 --reset
```

> 如果有多个网段，可用逗号分隔，例如 `--advertise-routes=192.168.1.0/24,10.0.0.0/24`。

### 5.2 在 Tailscale 管理后台批准路由
1. 登录 [Tailscale Admin Console](https://login.tailscale.com/admin/machines)。
2. 找到你的 OpenWRT 设备，点击右侧的 **“...”** 并选择 **“Edit route settings”**。
3. 在 **“Subnet routes”** 下，你会看到 `192.168.1.0/24`，将其 **启用（Approve）**。
4. 保存设置。稍等片刻，路由生效。

---

## 6. 验证连通性

在 Tailscale 网络中的任意设备（如手机、笔记本电脑）上执行：

1. **测试 OpenWRT 旁路由可达性**：
   ```bash
   ping 192.168.1.2   # 替换为你的 OpenWRT 实际 IP
   ```

2. **测试内网设备可达性**：
   ```bash
   ping 192.168.1.9   # 你家里的目标设备
   ```

如果两个 ping 都成功，则配置完全正确。

---

## 7. 故障排查指南

| 问题现象 | 可能原因 | 解决方法 |
|--------|---------|---------|
| `tailscale0` 接口不存在 | Tailscale 服务未启动或未认证 | 执行 `tailscale up` 完成登录，并用 `ip addr show tailscale0` 确认 |
| LuCI 物理设置中看不到 `tailscale0` | 未创建接口或服务未运行 | 参照第4.1节创建 `tailscale` 接口，并确保服务已启动 |
| 无法 ping 通内网设备 | 子网路由未批准 | 登录 Tailscale 控制台，批准广告的路由 |
| 无法 ping 通 OpenWRT | 防火墙区域转发未设置 | 检查 `lan` 到 `vpn` 的双向转发规则是否添加 |
| IP 转发未开启 | 系统内核未允许转发 | 执行 `echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf && sysctl -p` |
| 目标内网设备防火墙拦截 | 设备自身防火墙阻止 ICMP | 临时关闭防火墙测试，或放行相关端口/协议 |

---

## 8. 附加建议

- **持久化配置**：将 `/etc/config/tailscale` 和 `/var/lib/tailscale/` 目录添加到 `/etc/sysupgrade.conf`，以便系统升级后保留状态。
- **日志查看**：如需调试，可查看日志 `logread | grep tailscale`。
- **更新 Tailscale**：定期执行 `opkg update && opkg upgrade tailscale` 获取最新版本。

---

## 9. 结语

按照以上步骤，你的 OpenWRT 旁路由即可成为 Tailscale 的网关，实现安全、便捷的远程家庭网络访问。若仍有疑问，欢迎参考 [Tailscale 官方文档](https://tailscale.com/kb/) 或 OpenWRT 社区。