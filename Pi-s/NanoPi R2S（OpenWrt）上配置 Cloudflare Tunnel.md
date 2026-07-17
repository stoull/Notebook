# NanoPi R2S（OpenWrt）上配置 Cloudflare Tunnel

在旁路网关 **NanoPi R2S** 上运行 `cloudflared`，把家里部分 **HTTP/HTTPS 服务** 以公网域名安全暴露出去。R2S 上已有 **Tailscale** 时，两者可以并存：

| | Tailscale | Cloudflare Tunnel |
|---|-----------|-------------------|
| 用途 | 自己人整机/整网互访 | 给浏览器一个 `https://子域.域名` |
| 客户端 | 需装 Tailscale | 普通浏览器即可 |
| 适合 | SSH、RTSP、运维、内网穿透 | Web 面板、Webhook、给外人看的页面 |

**建议**：管理面、监控完整能力走 Tailscale；确需「发个链接就能打开」的 Web 服务再走 Tunnel，并加 **Cloudflare Access**。

相关对比见 [WireGuard-Tailscale-CloudflareTunnel对比.md](./WireGuard-Tailscale-CloudflareTunnel对比.md)。

---

## 1. 拓扑

```
[浏览器] ──HTTPS──► [Cloudflare 边缘]
                         ▲
                         │ 出站隧道（无需公网 IP / 端口映射）
                         │
                   [NanoPi R2S OpenWrt]
                    ├─ Tailscale（已有）
                    └─ cloudflared ──LAN──► 家里各服务
                                              ├─ Frigate  192.168.1.193:8971
                                              ├─ 其他 Web  …
                                              └─ （可选）本机 LuCI
```

旁路网关只要能上网、能访问目标局域网 IP，即可跑 Tunnel，**不必**做主路由。

---

## 2. 前置条件

- [ ] NanoPi R2S 已刷 OpenWrt，能 SSH / LuCI 登录
- [ ] R2S 能访问要暴露的内网服务（例：`curl -I http://192.168.1.193:8971`）
- [ ] Cloudflare 账号；域名已接入 Cloudflare（Nameservers 已切到 CF）
- [ ] 记下内网服务地址（下文用占位符，按需替换）

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `<域名>` | 接入 CF 的主域名 | `example.com` |
| `<Frigate内网>` | Frigate 鉴权 Web | `http://192.168.1.193:8971` |
| `<HA内网>` | Home Assistant（若有） | `http://192.168.1.50:8123` |
| `<隧道名>` | Zero Trust 里的 Tunnel 名称 | `home-r2s` |

> Frigate 请优先暴露 **8971（带鉴权）**，不要暴露无鉴权的 `5000`。

---

## 3. 在 Cloudflare 创建 Tunnel（推荐：远程管理 + Token）

远程管理（Dashboard 配路由）最适合 OpenWrt：路由器上只保留 **Token**，改 hostname 不用改本地 YAML。

### 3.1 创建隧道

1. 打开 [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. **Networks** → **Tunnels** → **Create a tunnel**
3. 类型选 **Cloudflared**
4. 名称填 `<隧道名>`（如 `home-r2s`）→ **Save**
5. 安装方式里选 **Docker** 或 **Debian** 均可，重点是复制形如：

```text
eyJhIjoi...很长一串...
```

的 **Tunnel token**（整段保存，后文记为 `<TUNNEL_TOKEN>`）

也可在隧道详情页：**Configure** → 查看/复制 token。

### 3.2 先配 Public Hostname（可装好 cloudflared 后再改）

仍在该 Tunnel → **Public Hostname** → **Add**：

| 子域示例 | 类型 | URL（Service） | 说明 |
|----------|------|----------------|------|
| `frigate.<域名>` | HTTP | `http://192.168.1.193:8971` | 家里 Pi 上的 Frigate |
| `ha.<域名>` | HTTP | `http://192.168.1.50:8123` | 若有 HA |
| `nas.<域名>` | HTTP | `http://192.168.1.x:端口` | 按实际改 |

要点：

- Service 填 **R2S 能访问到的局域网地址**，不要填 `localhost`（除非服务就在 R2S 本机）
- 内网是 HTTP 就选 HTTP；不要在这边强行写 HTTPS，除非后端真是 HTTPS
- 保存后 Cloudflare 会自动为该主机名创建 DNS（通常是 CNAME 到 `*.cfargotunnel.com`）

---

## 4. 在 OpenWrt（R2S）安装 cloudflared

NanoPi R2S 为 **aarch64**（RK3328）。先 SSH 进 R2S：

```bash
ssh root@<R2S局域网IP>
uname -m    # 应为 aarch64
```

### 4.1 方式 A：官方软件源（OpenWrt 24.10+ 优先试）

```bash
opkg update
opkg install cloudflared
# 若有 LuCI 插件可一并装：
# opkg install luci-app-cloudflared
```

若提示找不到包，用方式 B。

### 4.2 方式 B：官方二进制（兼容性最好）

```bash
cd /tmp
# 下载 Cloudflare 官方 linux arm64 包
wget -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
chmod +x cloudflared
mv cloudflared /usr/bin/cloudflared
cloudflared --version
```

> 升级 OpenWrt / Attended Sysupgrade 后，手动放入的二进制可能丢失，需重新下载或改回用 `opkg` 包装。

### 4.3 确认出网

```bash
cloudflared --version
ping -c 2 1.1.1.1
# 可选：测到 Cloudflare
nslookup region1.v2.argotunnel.com
```

---

## 5. 用 Token 启动隧道（推荐）

### 5.1 写入 UCI / 配置（有 luci-app-cloudflared 时）

LuCI：**Services** → **Cloudflared**（名称因版本而异）

- 启用服务
- Token 粘贴 `<TUNNEL_TOKEN>`
- 保存并应用

或命令行（包提供 UCI 时大致如下，以你机上 `/etc/config/cloudflared` 为准）：

```bash
uci set cloudflared.@cloudflared[0].enabled='1'
uci set cloudflared.@cloudflared[0].token='<TUNNEL_TOKEN>'
uci commit cloudflared
/etc/init.d/cloudflared enable
/etc/init.d/cloudflared restart
```

若 UCI 字段名不同，直接 `cat /etc/config/cloudflared` 对照修改。

### 5.2 无官方 init：自建启动脚本

```bash
mkdir -p /etc/cloudflared
# 仅保存 token，勿提交到公开仓库
cat > /etc/cloudflared/token << 'EOF'
<TUNNEL_TOKEN>
EOF
chmod 600 /etc/cloudflared/token
```

创建 `/etc/init.d/cloudflared`：

```bash
cat > /etc/init.d/cloudflared << 'EOF'
#!/bin/sh /etc/rc.common
START=99
STOP=10
USE_PROCD=1

start_service() {
        procd_open_instance
        procd_set_param command /usr/bin/cloudflared tunnel run --token "$(cat /etc/cloudflared/token)"
        procd_set_param respawn 3600 5 5
        procd_set_param stdout 1
        procd_set_param stderr 1
        procd_close_instance
}
EOF
chmod +x /etc/init.d/cloudflared
/etc/init.d/cloudflared enable
/etc/init.d/cloudflared start
```

### 5.3 验证

```bash
ps | grep cloudflared
logread -e cloudflared | tail -n 50
```

Zero Trust → **Tunnels** 中该隧道状态应为 **Healthy**。

本机测（在任意能上网的机器）：

```bash
curl -I https://frigate.<域名>
```

应返回 HTTP 响应（401/302/200 都说明隧道通了；401 可能是 Frigate 要登录）。

---

## 6. 可选：本地 config.yml（不用 Dashboard 管路由时）

一般**不必**用；只有想完全本地声明路由时才需要。

```bash
mkdir -p /etc/cloudflared
```

`/etc/cloudflared/config.yml` 示例：

```yaml
tunnel: <隧道UUID>
credentials-file: /etc/cloudflared/<隧道UUID>.json

ingress:
  - hostname: frigate.example.com
    service: http://192.168.1.193:8971
  - hostname: ha.example.com
    service: http://192.168.1.50:8123
  # 可选：把 OpenWrt LuCI 暴露出去（务必加 Access，见第 7 节）
  # - hostname: openwrt.example.com
  #   service: http://127.0.0.1:80
  - service: http_status:404
```

凭证 JSON 需在创建隧道时下载，放到 `credentials-file` 路径。启动：

```bash
cloudflared tunnel --config /etc/cloudflared/config.yml run
```

DNS 需自行把 `frigate.example.com` CNAME 到 `<隧道UUID>.cfargotunnel.com`（或在 Dashboard 里 Add hostname）。

**与 Token 模式不要混用两套同时跑同一隧道。**

---

## 7. 安全：Cloudflare Access（强烈建议）

Tunnel 只解决「连通」，**不替代登录**。Frigate/HA 有自带密码仍建议再套一层 Access。

1. Zero Trust → **Access** → **Applications** → **Add an application** → **Self-hosted**
2. Application domain：`frigate.<域名>`
3. Policy：例如允许你的邮箱 OTP / Google / GitHub 登录
4. 保存

效果：打开 `https://frigate.<域名>` 先过 Cloudflare 登录，再进 Frigate。

**不要**在无 Access、无强密码的情况下暴露：

- OpenWrt LuCI
- 路由器管理页
- 无鉴权的 Frigate `:5000`
- 内网 NAS 管理页

---

## 8. 与 Tailscale 并存时的用法建议

| 服务 | 推荐入口 |
|------|----------|
| Frigate 看监控、调 go2rtc/RTSP | **Tailscale**（或现有 WireGuard） |
| 偶尔用手机浏览器看一眼 Frigate Web | Tunnel + Access |
| SSH 进 Pi / R2S | **Tailscale** |
| 给朋友临时看某个 Web 面板 | Tunnel + Access（可设短期限策略） |
| GitHub Webhook / OAuth 回调到家里 | Tunnel |

同一台 R2S 上 Tailscale 与 cloudflared **可以同时运行**，一般无需改防火墙出站；若你对 `wan`/`lan` 做了严格出站限制，需放行 cloudflared 访问 `443`（及 Cloudflare 隧道相关地址）。

---

## 9. 常见服务 Ingress 对照

按你家实际 IP/端口改 Dashboard 里的 Service URL：

| 服务 | Service URL 示例 | 备注 |
|------|------------------|------|
| Frigate（鉴权） | `http://192.168.1.193:8971` | 推荐 |
| Frigate（无鉴权） | 不建议暴露 | 仅内网调试 |
| go2rtc Web | `http://192.168.1.193:1984` | 功能有限，视频协议可能不完整 |
| Home Assistant | `http://192.168.1.x:8123` | 建议 Access + HA 自带认证 |
| 群晖 DSM | `http://192.168.1.x:5000` | 务必 Access |
| R2S LuCI | `http://127.0.0.1:80` | 高风险，仅 Access + 强策略时考虑 |

WebRTC / RTSP / 任意 UDP **不要指望** Tunnel 完整替代 VPN。

---

## 10. 运维命令

```bash
# 状态
/etc/init.d/cloudflared status
ps | grep '[c]loudflared'

# 日志
logread -e cloudflared
# 或前台调试（先停服务）
/etc/init.d/cloudflared stop
cloudflared tunnel run --token "$(cat /etc/cloudflared/token)"

# 重启
/etc/init.d/cloudflared restart

# 升级官方二进制后
cloudflared update   # 若该版本支持；否则重新 wget arm64 包
```

Dashboard 里隧道变 **Down**：先查 R2S 上网、token 是否整段正确、系统时间是否准确（`date`）。

---

## 11. 排障清单

| 现象 | 排查 |
|------|------|
| Tunnel 一直 Not Healthy | R2S 无外网；token 截断；进程未起来；时钟错误 |
| 域名 502 / 1033 | Ingress URL 写错；R2S `curl` 不到目标 IP:端口；目标服务挂了 |
| 能打开但一直转圈 / 视频黑屏 | 正常：Tunnel 对实时流支持差，改用 Tailscale |
| 仅部分设备能开 | 本机 DNS 未走 CF；清 DNS 缓存；等 CNAME 生效 |
| 与 Tailscale 无关冲突 | 一般可并存；若异常，确认未把 cloudflared 流量误导入错误出口策略 |

在 **R2S 上**先验证后端：

```bash
curl -sI http://192.168.1.193:8971 | head
```

这里不通，Tunnel 也一定不通。

---

## 12. 最小落地步骤（checklist）

1. CF Zero Trust 创建 Tunnel，复制 `<TUNNEL_TOKEN>`
2. 添加 Public Hostname：`frigate.<域名>` → `http://192.168.1.193:8971`
3. R2S 安装 `cloudflared`，用 token 启动并 `enable`
4. Dashboard 显示 Healthy；浏览器打开 `https://frigate.<域名>`
5. 为该主机名加 **Access** 策略
6. 日常运维、SSH、看流继续用 **Tailscale**

---

## 13. 小结

- Tunnel 装在 **R2S**，用局域网 IP 反代家里各 Web 服务，与现有 Tailscale 分工清晰。
- 优先 **Token + Dashboard 管路由**，OpenWrt 上只跑 daemon。
- 暴露面保持最小，**Access + 应用自带鉴权** 双层防护。
- 需要整机/流媒体能力时，不要用 Tunnel 替代 Tailscale。
