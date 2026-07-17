# WireGuard / Tailscale / Cloudflare Tunnel 功能对比

三者都能解决「外网访问家里/内网服务」的问题，但定位不同：

| | **WireGuard** | **Tailscale** | **Cloudflare Tunnel** |
|---|---|---|---|
| 本质 | VPN 协议（底层加密隧道） | 基于 WireGuard 的零配置组网产品 | 把内网 HTTP(S) 服务安全暴露到公网域名 |
| 主要目标 | 组虚拟私有网络 | 设备互联、像局域网一样互通 | 对外发布网站/API，无需开端口 |
| 你得到的是 | 一层二/三层网络（IP 可达） | 一张私有 Mesh 网（IP + 可选子网路由） | 一个公网 HTTPS 入口（按应用转发） |

一句话区分：

- **WireGuard**：自己造「加密局域网」
- **Tailscale**：别人帮你造好、管好的 WireGuard 网
- **Cloudflare Tunnel**：不给你整网，只把指定服务「挂」到 Cloudflare 边缘

---

## 1. 功能对比总表

| 维度 | WireGuard | Tailscale | Cloudflare Tunnel (`cloudflared`) |
|------|-----------|-----------|-----------------------------------|
| **网络模型** | 点对点 / 星型 VPN，三层 IP | Mesh VPN（DERP 中继兜底） | 出站隧道 → Cloudflare 边缘 → 公网 |
| **访问方式** | 连上后用私网 IP（如 `10.66.66.2`） | 连上后用 Tailscale IP / MagicDNS 名 | 用公网域名（如 `frigate.example.com`） |
| **是否像「进内网」** | 是（整机/网段可通） | 是（设备级；可开子网路由） | 否（只暴露你配置的服务） |
| **暴露面** | 不对外开业务端口；需开 WG UDP 或经中转 | 默认不暴露公网端口 | 业务对公网可见（经 CF 防护） |
| **公网 IP / 端口转发** | 常需公网 VPS 做枢纽（家宽无公网时） | 不需要；NAT 穿透 + 中继 | 不需要；内网主动出站连 CF |
| **配置复杂度** | 高：密钥、Peer、路由、防火墙手写 | 低：登录账号即可组网 | 中：装 agent + 配 Hostname/路由 |
| **身份与鉴权** | 主要靠密钥 + 可选上层应用鉴权 | SSO、ACL、设备审批、Mullvad 等 | Cloudflare Access（SSO/OTP）、WAF |
| **协议支持** | 任意 IP 流量（TCP/UDP/ICMP 等） | 任意 IP 流量 | 以 HTTP/HTTPS 为主；也支持 TCP/SSH/RDP 等经隧道 |
| **性能** | 极高（内核实现，开销小） | 很高（底层 WG；穿不透时走中继会降） | 取决于 CF 路径与协议；非全量 VPN |
| **自建依赖** | 可完全自建 | 控制面依赖 Tailscale（开源有 Headscale） | 依赖 Cloudflare 边缘与账号 |
| **费用** | 开源免费；VPS 自付 | 个人免费档够用；团队/ACL 等付费 | 免费档可用；高级 Access/带宽等付费 |
| **典型「产品感」** | 基础设施组件 | 零信任组网 / 远程办公网 | 零信任应用发布 / 反向代理即服务 |

---

## 2. 各自擅长什么

### WireGuard

- 协议简单、加密现代、性能优秀
- 适合：你要**完整私网连通**（SSH、RTSP、数据库、任意端口），且愿意自己维护
- 代价：密钥轮换、Peer 增删、多端路由、NAT 穿透要自己设计（常见做法：公网 VPS 枢纽，见 [WireGuard访问内网.md](./WireGuard访问内网.md)）

### Tailscale

- 在 WireGuard 之上加了：密钥分发、NAT 穿透、DERP 中继、ACL、DNS、客户端体验
- 适合：多设备（手机/笔记本/Pi/NAS）**长期互访**，不想维护 VPS 与配置文件
- 代价：默认依赖 Tailscale 协调服务；企业级策略与部分能力需付费；极致「完全离线自建」需 Headscale 等替代控制面

### Cloudflare Tunnel

- 内网机器主动连 Cloudflare，**不用**公网 IP、**不用**路由器端口映射
- 适合：把 Frigate Web、Home Assistant、内部 API **以 HTTPS 域名**安全公开（或仅限 Access 登录后访问）
- 代价：默认不是「整机进内网」；摄像头 RTSP、任意 UDP、复杂内网浏览往往不适合直接用 Tunnel；流量与策略受 Cloudflare 产品边界约束

---

## 3. 拓扑直觉

### WireGuard（自建枢纽）

```
[手机] ──WG──► [公网 VPS] ◄──WG── [家里 Pi]
                    │
              私网 IP 互通（如 10.66.66.0/24）
```

### Tailscale

```
[手机] ←── Mesh / DERP ──► [Pi]
[笔记本] ──────────────────┘
        （控制面：Tailscale 协调密钥与路由）
```

### Cloudflare Tunnel

```
[浏览器] ──HTTPS──► [Cloudflare 边缘] ◄──出站隧道── [家里 cloudflared]
                              │
                    只转发你映射的 hostname → 本地端口
```

---

## 4. 应用场景

### 场景 A：外网访问家里监控（Frigate / go2rtc）

| 方案 | 怎么用 | 是否推荐 |
|------|--------|----------|
| WireGuard | 连 VPN 后访问 `http://10.x.x.x:8971`；RTSP 也可走隧道 | **很适合**（完整协议，隐私好） |
| Tailscale | 装客户端，用 Tailscale IP / MagicDNS 打开 Frigate | **很适合**（比自建 WG 省事） |
| Cloudflare Tunnel | 只把 Frigate Web UI 挂到域名；RTSP/webrtc 往往另议 | **仅 Web 面板**时可用；完整监控栈优先前两者 |

**建议**：要看实时流、调 RTSP、整机管理 → WireGuard / Tailscale；只要偶尔打开网页看一眼且想用域名 + Access 登录 → Cloudflare Tunnel。

### 场景 B：远程 SSH / 运维树莓派、NAS

| 方案 | 说明 |
|------|------|
| WireGuard | 经典做法；连上后 `ssh user@10.66.66.2` |
| Tailscale | 同样自然；还可配合 Tailscale SSH、ACL 限制谁能登哪台 |
| Cloudflare Tunnel | 可用 TCP/SSH 接入或浏览器内终端类能力，但不如「进私网再 SSH」直观 |

**建议**：运维类优先 Tailscale 或 WireGuard。

### 场景 C：给家人/客户提供一个「网址就能打开」的服务

例如：演示用的内部仪表盘、个人博客在家宽后面、Webhook 接收端。

| 方案 | 说明 |
|------|------|
| Cloudflare Tunnel | **最对口**：公网域名 + HTTPS + 可选 Access |
| Tailscale | 对方也要装 Tailscale（或你用 Funnel 等能力，能力与套餐有关） |
| WireGuard | 对方要装客户端并导入配置，不适合「随便发个链接」 |

**建议**：对外分享链接 → Cloudflare Tunnel；仅自己人设备 → Tailscale。

### 场景 D：出差时访问公司/家里整段局域网（打印机、NAS 网盘、IoT）

| 方案 | 说明 |
|------|------|
| WireGuard | 配好 AllowedIPs / 站点到站点即可 |
| Tailscale | 开 **Subnet Router**，把 `192.168.1.0/24` 宣告进尾网 |
| Cloudflare Tunnel | 不擅长「整网穿越」；要逐个服务映射 |

**建议**：整网互通 → WireGuard / Tailscale。

### 场景 E：开发联调（本地服务给公网 Webhook / 手机真机访问）

| 方案 | 说明 |
|------|------|
| Cloudflare Tunnel | 快速把 `localhost:3000` 暴露为 HTTPS 域名，适合 GitHub Webhook、OAuth 回调 |
| Tailscale | 真机与电脑同尾网即可访问，不必上公网 |
| WireGuard | 可以，但为临时联调偏重 |

**建议**：要公网回调 → Cloudflare Tunnel；只要自己设备互访 → Tailscale。

### 场景 F：对安全与「不暴露任何公网业务端口」要求极高

| 方案 | 说明 |
|------|------|
| WireGuard / Tailscale | 业务端口不监听公网；只有 VPN 成员能到 |
| Cloudflare Tunnel | 业务经 CF 对外；靠 Access / WAF / 隐身 IP 降低风险，但仍是「应用层公开入口」 |

**建议**：监控、SSH、管理面优先放进 VPN；必须给外人用的 Web 再用 Tunnel + Access。

### 场景 G：完全自建、数据与控制面都要自己掌控

| 方案 | 说明 |
|------|------|
| WireGuard | **最干净** |
| Tailscale | 官方控制面第三方；可用 Headscale 自建协调 |
| Cloudflare Tunnel | 强依赖 Cloudflare |

---

## 5. 怎么选（决策简表）

| 你的需求 | 更合适的选择 |
|----------|----------------|
| 自己有 VPS，要极致可控与性能 | **WireGuard** |
| 多设备互访，不想维护配置与 VPS | **Tailscale** |
| 只要把某个 Web 服务挂到域名，给浏览器用 | **Cloudflare Tunnel** |
| 要 RTSP / 任意端口 / 整机进内网 | **WireGuard** 或 **Tailscale** |
| 要给外人一个 https:// 链接，且可 SSO 登录 | **Cloudflare Tunnel**（+ Access） |
| 家庭监控（本仓库 Frigate 场景） | 优先 **WireGuard**（已有实践文档）或 **Tailscale** |

也可以组合：

- **Tailscale / WireGuard** 管「自己人进内网」
- **Cloudflare Tunnel** 管「必须对公网或访客开放的单个 Web 应用」

---

## 6. 与本仓库相关的实践

- 自建 WireGuard 枢纽访问家里 Frigate：见 [WireGuard访问内网.md](./WireGuard访问内网.md)
- 若改为 Tailscale：Pi 与手机都加入同一 Tailnet 后，用 Tailscale IP 访问 Frigate 端口即可，一般无需 VPS
- 若只用 Cloudflare Tunnel：建议仅映射 Frigate 带鉴权的 Web 端口，并开启 Cloudflare Access；实时视频链路需单独验证是否可用

---

## 7. 小结

| | 一句话 |
|---|--------|
| **WireGuard** | 最快、最干净的「加密局域网」原材料，灵活但要自己运维 |
| **Tailscale** | 把 WireGuard 做成开箱即用的设备互联网，适合长期个人/小团队远程访问 |
| **Cloudflare Tunnel** | 不做整网 VPN，专门把内网服务安全发布到公网域名 |

按「要整网」还是「要一个网址」来选，大多不会选错。
