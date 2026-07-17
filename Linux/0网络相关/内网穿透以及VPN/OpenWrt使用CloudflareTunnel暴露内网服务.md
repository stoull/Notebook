# OpenWrt 使用 Cloudflare Tunnel 暴露内网服务

基于 NanoPi R2S（旁路由）+ OpenWrt + Cloudflare Tunnel 实践整理。  
目标：把家里内网的 HTTP/HTTPS 服务（NAS、Home Assistant、LuCI、Docker 应用等）安全暴露到公网域名，**无需在主路由开端口、无需公网 IP**。

---

## 1. 这是什么、适合什么场景

```
外网用户
   │  HTTPS（访问你的域名）
   ▼
Cloudflare 边缘节点
   │  已建立的出站隧道（cloudflared 主动连出去）
   ▼
R2S 上的 cloudflared
   │  转发到内网 IP:端口
   ▼
家里设备（如 192.168.1.50:8123）
```

| 对比 | Cloudflare Tunnel | Tailscale / WireGuard |
|------|-------------------|------------------------|
| 典型用途 | 给别人 / 自己用浏览器访问某个 Web 服务 | 把整段局域网当「回家专线」 |
| 需要公网 IP | 否 | 否 |
| 要开端口 | 否 | 否 |
| 访问方式 | 域名（如 `ha.example.com`） | 客户端 VPN / 内网 IP |
| 适合 | Home Assistant、图床、博客、NAS Web UI | SSH、SMB、整网穿透 |

本教程只讲 **Public Hostname（公网域名 → 内网服务）**。若你要的是「手机连上后访问整个 `192.168.1.0/24`」，见同目录的 Tailscale / WireGuard 文档。

---

## 2. 前置条件

| 项 | 要求 |
|----|------|
| 域名 | 已添加到 Cloudflare（DNS 由 CF 托管，状态 Active） |
| 账号 | Cloudflare 免费套餐即可；需进入 **Zero Trust** |
| 路由 | R2S 已装好 `cloudflared`，能稳定访问外网 |
| 内网服务 | 目标服务在局域网可访问（如 `http://192.168.1.50:8123`） |

旁路由常见拓扑（与本仓库其它文档一致）：

| 项 | 推荐值 |
|----|--------|
| 接线 | 主路由 LAN → R2S **LAN** |
| R2S IP | 如 `192.168.1.11` |
| 网关 | 主路由，如 `192.168.1.1` |

确认本机能出网：

```bash
ping -c 2 1.1.1.1
cloudflared --version
```

---

## 3. 推荐方式：仪表盘远程管理（Token）

适合大多数人：**在 Cloudflare 网页上创建隧道、添加域名与内网地址**，路由器只负责跑 Token，以后加服务不用改 OpenWrt 配置文件。

### 3.1 在 Zero Trust 里创建隧道

1. 打开 [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. 左侧 **Networks** → **Tunnels** → **Create a tunnel**
3. 类型选 **Cloudflared**
4. 起个名字，例如 `r2s-home`
5. 安装界面会给出类似命令：

```bash
cloudflared service install eyJhIjoiXXXX....很长一串....
```

真正有用的是 **`eyJ...` 这一段 Token**（整段复制）。

### 3.2 把 Token 写进 OpenWrt

SSH 登录 R2S：

```bash
uci set cloudflared.config.token='这里粘贴完整Token'
uci set cloudflared.config.enabled='1'
uci commit cloudflared
/etc/init.d/cloudflared enable
/etc/init.d/cloudflared restart
```

查看是否连上：

```bash
logread -e cloudflared | tail -n 50
```

仪表盘里该隧道应显示 **Healthy / Connected**。首次可能要等 1～3 分钟。

> **注意：** 使用 Token（远程管理）时，请把 `/etc/cloudflared/config.yml` 里示例内容全部注释掉或清空有效配置，避免本地 YAML 与远程配置冲突。本地只保留 Token 即可。

```bash
# 可先备份再清空有效项
cp /etc/cloudflared/config.yml /etc/cloudflared/config.yml.bak
# 编辑：把未注释的 url / tunnel / ingress 等全部注释掉
vi /etc/cloudflared/config.yml
```

查看当前 UCI：

```bash
uci show cloudflared
cat /etc/config/cloudflared
```

典型内容类似：

```
config cloudflared 'config'
	option enabled '1'
	option token 'eyJhIjoi....'
```

---

## 4. 暴露第一个内网服务（核心步骤）

隧道 Healthy 之后，**加服务全部在 Cloudflare 网页完成**，不必再动路由器。

### 4.1 添加 Public Hostname

在隧道详情页 → **Public Hostname** → **Add a public hostname**：

| 字段 | 示例 | 说明 |
|------|------|------|
| Subdomain | `ha` | 子域名前缀 |
| Domain | `example.com` | 你在 CF 上的域名 |
| Type | `HTTP` | 内网多数是明文 HTTP |
| URL | `http://192.168.1.50:8123` | 内网 IP + 端口（Home Assistant 示例） |

保存后，Cloudflare 会自动加一条 **CNAME**（指向隧道）。稍等 DNS 生效，浏览器访问：

```
https://ha.example.com
```

流量路径：浏览器 → Cloudflare → 隧道 → R2S 的 cloudflared → `192.168.1.50:8123`。

### 4.2 常见内网服务对照

| 服务 | Public Hostname 示例 | Type | URL |
|------|----------------------|------|-----|
| Home Assistant | `ha.example.com` | HTTP | `http://192.168.1.50:8123` |
| OpenWrt LuCI | `router.example.com` | HTTP | `http://192.168.1.11` |
| NAS（群晖 DSM） | `nas.example.com` | HTTPS | `https://192.168.1.20:5001`（常需关证书校验，见下） |
| Jellyfin | `media.example.com` | HTTP | `http://192.168.1.30:8096` |
| Docker 某 Web | `app.example.com` | HTTP | `http://192.168.1.40:8080` |
| 本机已跑的 Web | `local.example.com` | HTTP | `http://127.0.0.1:80` |

要点：

1. **URL 填的是 R2S 能访问到的地址**，不是公网地址。旁路由下直接写内网 IP 即可。
2. 内网是 HTTPS 且自签证书时，在 Public Hostname 的 **Additional application settings → TLS** 里勾选 **No TLS Verify**（或本地 config 里 `noTLSVerify: true`）。
3. 一条隧道可以挂很多个 Hostname，不必为每个服务再建隧道。

### 4.3 在路由器上自测连通（可选）

在 R2S 上确认目标服务通：

```bash
wget -qO- --timeout=3 http://192.168.1.50:8123 | head
# 或
curl -I --connect-timeout 3 http://192.168.1.50:8123
```

若这里都超时，先修内网连通，再查隧道。

---

## 5. 给敏感服务加门禁（强烈建议）

暴露 LuCI、NAS、HA 等管理界面时，仅靠「没人知道域名」不够。用 **Cloudflare Access** 加一层登录：

1. Zero Trust → **Access** → **Applications** → **Add an application** → **Self-hosted**
2. Application domain 填你的公网主机名，如 `ha.example.com`
3. Policy：例如只允许你的邮箱登录（One-time PIN / Google / GitHub 等）

之后访问该域名会先过 Cloudflare 登录页，通过后才到内网服务。

---

## 6. 可选：本地 YAML 管理（不推荐新手）

适合想把配置全部放在路由器、用 Git 管理的人。步骤概要：

```bash
cd /etc/cloudflared
cloudflared tunnel login          # 浏览器授权，生成 cert.pem
cloudflared tunnel create r2s-home
cp /root/.cloudflared/*.json /etc/cloudflared/
cp /root/.cloudflared/cert.pem /etc/cloudflared/
```

编辑 `/etc/cloudflared/config.yml`：

```yaml
tunnel: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
credentials-file: /etc/cloudflared/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.json

ingress:
  - hostname: ha.example.com
    service: http://192.168.1.50:8123
  - hostname: nas.example.com
    service: https://192.168.1.20:5001
    originRequest:
      noTLSVerify: true
  - hostname: router.example.com
    service: http://192.168.1.11
  # 必须有且放在最后
  - service: http_status:404
```

DNS 记录：

```bash
cloudflared tunnel route dns r2s-home ha.example.com
cloudflared tunnel route dns r2s-home nas.example.com
cloudflared tunnel route dns r2s-home router.example.com
```

启用服务（本地模式一般**不要**再填 Token，或按包文档二选一）：

```bash
uci set cloudflared.config.enabled='1'
uci commit cloudflared
/etc/init.d/cloudflared enable
/etc/init.d/cloudflared restart
```

若出现 QUIC / 缓冲区相关告警，可按 OpenWrt Wiki 增加：

```bash
cat > /etc/sysctl.d/30-cloudflared.conf << 'EOF'
net.ipv4.ping_group_range=0 2147483647
net.core.rmem_max=2500000
EOF
sysctl -p /etc/sysctl.d/30-cloudflared.conf
```

---

## 7. 日常运维

### 启停与状态

```bash
/etc/init.d/cloudflared status
/etc/init.d/cloudflared restart
logread -e cloudflared | tail -n 80
```

仪表盘 **Tunnels** 里应始终为 Healthy。

### 新增 / 修改服务（Token 模式）

只需在 Zero Trust → 该隧道 → **Public Hostname** 增删改，几分钟内生效，**不用重启** OpenWrt（配置由 Cloudflare 下发）。

### 换 Token / 重建隧道

```bash
uci set cloudflared.config.token='新Token'
uci commit cloudflared
/etc/init.d/cloudflared restart
```

旧隧道在仪表盘里删除即可。

---

## 8. 排障清单

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| 隧道一直 Not connected | Token 错、config.yml 冲突、出网失败 | 核对 Token；注释本地 YAML；`ping 1.1.1.1` |
| 域名 530 / Error 1033 | 隧道未连接 | 先恢复 Healthy |
| 502 Bad Gateway | URL 写错或内网服务挂了 | 在 R2S 上 `curl` 内网 URL |
| 能开页但证书告警 | 浏览器侧一般由 CF 提供 HTTPS；若异常检查域名是否走 CF 代理（橙云） | DNS 记录应为 Proxied |
| `failed to dial to edge with quic` | 部分环境下 QUIC/UDP 不稳 | 已知问题；多数仍可走其它协议；检查防火墙是否拦 UDP |
| 空间不够装不上包 | R2S overlay 太小 | 见同目录《OpenWrt扩展SD卡overlay空间》 |
| 想暴露 SSH/非 HTTP | Public Hostname 的 HTTP 不够用 | 用 Cloudflare 的 private network + WARP，或改用 Tailscale |

快速自检脚本思路：

```bash
echo "=== cloudflared ==="
cloudflared --version
uci get cloudflared.config.enabled
/etc/init.d/cloudflared status
echo "=== recent log ==="
logread -e cloudflared | tail -n 30
echo "=== can reach origin? ==="
# 换成你的内网服务
curl -sI --connect-timeout 3 http://192.168.1.50:8123 | head -n 5
```

---

## 9. 安全建议（务必看）

1. **管理类服务（LuCI、NAS、路由器）务必开 Cloudflare Access**，不要裸奔到公网。
2. 能不开的就别开：纯内网用的东西继续用 Tailscale，不必上域名。
3. 源站保持内网 HTTP 即可；公网侧由 Cloudflare 提供 HTTPS，不必在家里另开 443 端口。
4. Token / `*.json` 凭据等同 root 密码，不要提交到 Git、不要发到群里。
5. 主路由 **不要** 为这些服务做端口转发；隧道是出站连接，开端口反而扩大攻击面。

---

## 10. 最小操作复盘（你已装好 cloudflared 时）

若软件已经装好，按这个最短路径做即可：

1. Zero Trust → 创建 Tunnel → 复制 Token  
2. `uci set cloudflared.config.token='...'` + `enabled=1` → `commit` → `restart`  
3. 仪表盘确认 Healthy  
4. Public Hostname：`子域名` + `http://内网IP:端口`  
5. 浏览器访问 `https://子域名.你的域名`  
6. 敏感服务再套一层 Access  

---

## 参考

- [OpenWrt Wiki: Cloudflare tunnel](https://openwrt.org/docs/guide-user/services/vpn/cloudfare_tunnel)
- [Cloudflare Tunnel 文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [config.yml 参考](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/configure-tunnels/local-management/configuration-file/)
- 官方包：`opkg install cloudflared`（可选 GUI：`luci-app-cloudflared`）
