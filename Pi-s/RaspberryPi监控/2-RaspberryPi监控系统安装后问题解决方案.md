
RaspberryPi监控系统安装后问题解决方案

## 外网访问

### 使用 WireGuard 访问内网

通过**公网 VPS 做 WireGuard 枢纽**，让手机/笔记本在外网像在内网一样访问 Pi 上的 Frigate、go2rtc，**无需**把监控端口直接暴露到公网。

**前置**：Pi 上已按 [RaspberryPi监控系统.md](./RaspberryPi监控系统.md) 配好 go2rtc + Frigate，内网可访问（如 `http://192.168.1.193:5000`）。完整分步配置见 [WireGuard访问内网.md](./WireGuard访问内网.md)。

**拓扑**：

```
[手机/笔记本] ──UDP 51820──► [公网 VPS] ◄── [家里 Pi + Frigate]
  10.66.66.3                  10.66.66.1       10.66.66.2
                                    │
                             转发 WG 网段（Pi 在 NAT 后主动连 VPS）
```

| 角色 | WireGuard IP | 说明 |
|------|--------------|------|
| VPS 枢纽 | `10.66.66.1` | 固定公网 IP，监听 `51820/udp` |
| 树莓派 | `10.66.66.2` | 在家，`PersistentKeepalive` 保活 |
| 手机/笔记本 | `10.66.66.3` … | 外网连 VPS 后进 WG 网段 |

**IP 规划**：网段 `10.66.66.0/24`（避免与家用 `192.168.x.x` 冲突）；端口 `51820/udp`。

#### 三端配置要点

**1. VPS**（Ubuntu/Debian）：安装 `wireguard`，生成服务端 + 各 Peer 密钥，创建 `/etc/wireguard/wg0.conf`：

```ini
[Interface]
Address = 10.66.66.1/24
ListenPort = 51820
PrivateKey = <VPS私钥>
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o <VPS网卡> -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o <VPS网卡> -j MASQUERADE

[Peer]  # Pi
PublicKey = <Pi公钥>
AllowedIPs = 10.66.66.2/32

[Peer]  # 手机
PublicKey = <手机公钥>
AllowedIPs = 10.66.66.3/32
```

放行 `51820/udp`（ufw + 云安全组），`systemctl enable --now wg-quick@wg0`。

**2. Pi** `/etc/wireguard/wg0.conf`：

```ini
[Interface]
Address = 10.66.66.2/24
PrivateKey = <Pi私钥>

[Peer]
PublicKey = <VPS公钥>
Endpoint = <VPS公网IP>:51820
AllowedIPs = 10.66.66.0/24
PersistentKeepalive = 25
```

`systemctl enable --now wg-quick@wg0`。VPS 上 `ping 10.66.66.2` 应有 handshake。

**3. 手机/笔记本**：WireGuard App 导入配置（VPS 上 `qrencode -t ansiutf8 < phone.conf` 可生成二维码）：

```ini
[Interface]
Address = 10.66.66.3/24
PrivateKey = <手机私钥>

[Peer]
PublicKey = <VPS公钥>
Endpoint = <VPS公网IP>:51820
AllowedIPs = 10.66.66.0/24
PersistentKeepalive = 25
```

> `AllowedIPs = 10.66.66.0/24`：仅 WG 网段走隧道，不影响正常 4G/5G 上网。勿填 `0.0.0.0/0`（否则全流量绕 VPS）。

#### 外网访问地址

连上 WireGuard 后，用 **Pi 的 WG IP**（`10.66.66.2`），不要用家里 `192.168.x.x`：

| 服务 | 地址 |
|------|------|
| Frigate（推荐，带鉴权） | `http://10.66.66.2:8971` |
| Frigate（无鉴权，仅调试） | `http://10.66.66.2:5000` |
| go2rtc 预览 | `http://10.66.66.2:1984` |
| RTSP（VLC） | `rtsp://10.66.66.2:8554/picam` |

**外网鉴权**：Pi 上 `frigate/config/config.yml` 启用 `auth: enabled: true`，重启 Frigate 后用 `:8971` 登录。**不要**把无鉴权的 `:5000` 当作外网入口。

#### 验证清单

| 步骤 | 操作 | 预期 |
|------|------|------|
| 1 | VPS / Pi 上 `sudo wg show` | 有 handshake |
| 2 | VPS `ping 10.66.66.2` | 通 |
| 3 | 手机开 WG（4G/5G） | App 显示已连接 |
| 4 | 手机浏览器 `http://10.66.66.2:8971` | Frigate 页面 + 直播有画面 |

#### 常见问题

| 现象 | 处理 |
|------|------|
| Pi 无 handshake | 查 VPS 安全组 / ufw 是否放行 UDP 51820；核对 `Endpoint` |
| VPS 能 ping Pi，手机不能 | 确认手机 WG 已开；`AllowedIPs` 含 `10.66.66.0/24` |
| 能 ping，Frigate 打不开 | `docker ps`；Pi 上 `ss -tlnp \| grep -E '5000\|8971'` |
| 连 WG 后手机断网 | 手机 `AllowedIPs` 改回 `10.66.66.0/24`，勿用 `0.0.0.0/0` |
| 视频卡顿 | 降低 go2rtc 分辨率/帧率；检查 Pi 上行带宽 |

改 VPS `wg0.conf` 后须 `sudo systemctl restart wg-quick@wg0`。

#### 安全要点

1. 私钥勿提交 Git；`/etc/wireguard/` 权限 `600`
2. **仅暴露 UDP 51820**，不对公网映射 Frigate 5000/1984/8554
3. 外网用 **8971 + auth** 强密码
4. 仅看 Frigate 时不必做「整网段路由」；需要访问全部 `192.168.x.x` 设备时再改 `AllowedIPs`（见 [WireGuard访问内网.md](./WireGuard访问内网.md) 第 10 节）

**快速参考**：

```
Pi WG IP       : 10.66.66.2
外网看 Frigate : http://10.66.66.2:8971  （先开手机 WireGuard）
外网看 go2rtc  : http://10.66.66.2:1984
```

### 使用 Cloudflare Tunnel

在 Pi 上运行 **cloudflared**，由树莓派**主动出站**连到 Cloudflare，把内网的 Frigate / go2rtc 以 HTTPS 域名暴露出去。**无需公网 IP、无需 VPS、无需路由器端口映射**（与上一节 WireGuard 互补）。

**前置**：Pi 上已按 [1-RaspberryPi监控系统安装.md](./1-RaspberryPi监控系统安装.md) 配好 go2rtc + Frigate，内网可访问（如 `http://192.168.1.193:8971`）。

**拓扑**：

```
[手机/笔记本] ──HTTPS──► [Cloudflare 边缘] ◄──出站隧道── [家里 Pi + cloudflared]
  frigate.example.com                              127.0.0.1:8971 / :1984
```

| 对比项 | WireGuard（上一节） | Cloudflare Tunnel（本节） |
|--------|---------------------|---------------------------|
| 需要 VPS | 是 | 否 |
| 路由器端口映射 | UDP 51820 | 不需要 |
| 域名 / HTTPS | 可选 | 需要（域名接入 Cloudflare） |
| 外网直播（WebRTC） | 进隧道后直连 Pi `:8555` | **8555 不经隧道**；直播多降级为 MSE |
| 适合场景 | 完整内网体验、RTSP | 无公网 IP、不想维护 VPS、只看 Web UI |

| 角色 | 说明 |
|------|------|
| Cloudflare 账号 | 免费即可；域名 NS 指向 Cloudflare |
| Pi | 安装 `cloudflared`，维持出站连接 |
| 访问端 | 浏览器打开 `https://<子域名>`，无需装客户端 |

#### 1. Pi 上安装 cloudflared

树莓派为 **arm64**，任选其一：

**方式 A：apt（Raspberry Pi OS Bookworm 推荐）**

```bash
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared bookworm main' | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install -y cloudflared
cloudflared -v
```

> 非 Bookworm 可把 `bookworm` 换成 `bullseye` 等；或直接用手动二进制。

**方式 B：手动二进制**

```bash
curl -L -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
sudo install -m 755 cloudflared /usr/local/bin/cloudflared
cloudflared -v
```

#### 2. 在 Cloudflare 创建 Tunnel

1. 登录 [Cloudflare Zero Trust](https://one.dash.cloudflare.com/) → **Networking** → **Tunnels** → **Create a tunnel**
2. 类型选 **Cloudflared**，命名如 `hutpi-frigate`
3. 在 **Install connector** 页复制 **Token**（形如 `eyJhIjoi...`）
4. 在 Pi 上安装为系统服务：

```bash
sudo cloudflared service install <粘贴Token>
sudo systemctl enable --now cloudflared
sudo systemctl status cloudflared
```

5. 回到控制台 **Public Hostname**，添加路由（Pi 上 Frigate 为 `network_mode: host` 时用 `127.0.0.1`）：

| 子域名（示例） | 服务类型 | URL |
|----------------|----------|-----|
| `frigate.example.com` | HTTP | `http://127.0.0.1:8971` |
| `go2rtc.example.com` | HTTP | `http://127.0.0.1:1984` |

> **只映射 `:8971`（带鉴权）**，不要把无鉴权的 `:5000` 暴露到公网。

6. 保存后等 1～2 分钟，外网访问 `https://frigate.example.com`。

#### 3. 配置文件方式（多服务 / 可版本管理）

若不用 Token、改用手写配置，典型 `/etc/cloudflared/config.yml`：

```yaml
tunnel: <tunnel-uuid>
credentials-file: /home/pi/.cloudflared/<tunnel-uuid>.json

ingress:
  - hostname: frigate.example.com
    service: http://127.0.0.1:8971
  - hostname: go2rtc.example.com
    service: http://127.0.0.1:1984
  - service: http_status:404
```

```bash
# 首次创建命名隧道（按提示登录 Cloudflare）
cloudflared tunnel login
cloudflared tunnel create hutpi-frigate
cloudflared tunnel route dns hutpi-frigate frigate.example.com

sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cloudflared service install
sudo systemctl restart cloudflared
```

凭证与 `config.yml` 权限建议 `600`，勿提交 Git。

#### 4. Frigate 鉴权（必须）

外网入口务必启用 Frigate 登录（与 WireGuard 节相同），`frigate/config/config.yml`：

```yaml
auth:
  enabled: true
```

```bash
docker compose restart frigate
```

首次打开 `https://frigate.example.com` 按页面设置用户名、密码。

**可选加固**：Zero Trust → **Access** → 为 `frigate.example.com` 加一层 Cloudflare 登录（邮箱 OTP / Google 等），再进入 Frigate 二次鉴权。

#### 5. 外网访问地址

| 服务 | 地址 |
|------|------|
| Frigate（推荐） | `https://frigate.example.com` |
| go2rtc 预览 | `https://go2rtc.example.com` |
| RTSP（VLC） | **不适合**经 Tunnel 使用；外网请走 Frigate / go2rtc 的 HTTP 页面 |

#### 6. WebRTC 限制（重要）

Cloudflare Tunnel **只代理 HTTP/HTTPS（及 WebSocket）**。Frigate / go2rtc 的 **WebRTC 媒体流走 TCP/UDP `:8555`**，**不会**从隧道出去。

| 能力 | 经 Tunnel 外网 |
|------|----------------|
| Frigate UI、事件列表、录像回放 | 通常正常 |
| 直播 MSE（浏览器降级模式） | 通常可用，延迟略高 |
| 直播 WebRTC（低延迟） | **需额外方案**（见下） |
| RTSP `8554` | 不支持 |

若外网直播只有 UI、无画面或一直转圈：

1. 在 Frigate 直播窗口看是否已自动降级为 **MSE**（非 WebRTC）
2. 若必须 WebRTC：需能访问 Pi 的 `8555`（例如 **WireGuard 进内网**、或路由器映射 `8555` 并在 go2rtc 配 `webrtc.candidates`）——纯 Tunnel **无法**替代
3. CGNAT、完全无端口映射时：以 **MSE + 录像回放** 为主，或改用上节 WireGuard

#### 验证清单

| 步骤 | 操作 | 预期 |
|------|------|------|
| 1 | Pi `sudo systemctl status cloudflared` | `active (running)` |
| 2 | Pi `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8971` | `200` 或 `401` |
| 3 | 手机关 Wi‑Fi，4G 打开 `https://frigate.example.com` | 登录页 / Frigate UI |
| 4 | 点开直播 | 有画面（MSE）或知悉 WebRTC 限制 |
| 5 | `https://go2rtc.example.com` | go2rtc 管理页可开流 |

#### 常见问题

| 现象 | 处理 |
|------|------|
| Tunnel 显示 Down | Pi 上 `journalctl -u cloudflared -f`；检查 Token / `config.yml` 路径 |
| 502 Bad Gateway | Frigate 未运行；`ingress` 端口写错（应用 `8971` 非 `5000`） |
| 能开 UI、直播黑屏 | WebRTC 限制；确认 MSE 或配合 WireGuard / 8555 转发 |
| 证书错误 | 确认域名 NS 在 Cloudflare；Hostname 在 Tunnel 里已绑定 |
| 与 WireGuard 并存 | 可以；Tunnel 管 HTTPS 外网入口，WG 管完整内网 |

#### 安全要点

1. **仅暴露 `8971`**，禁用公网 `:5000`
2. Frigate `auth.enabled: true` + 强密码；建议再加 Cloudflare Access
3. `credentials-file`、Tunnel Token 勿泄露、勿进 Git
4. 录像经 Tunnel 外传占用 Cloudflare 带宽；大量回放注意用量与 ToS

**快速参考**：

```
内网 Frigate : http://127.0.0.1:8971
外网 Frigate : https://frigate.example.com  （无需 VPN 客户端）
外网 go2rtc  : https://go2rtc.example.com
直播注意     : WebRTC/8555 不经 Tunnel；外网多为 MSE
```

与 WireGuard 选型：**要完整内网 + RTSP + WebRTC** → WireGuard；**无 VPS、零端口映射、主要看 Web** → Cloudflare Tunnel。

## 图像旋转

Camera Module 3 等 CSI 摄像头若因安装空间只能**倒着装（180°）**，可通过软件校正，使预览、录像、AI 检测框均为正向。本节基于上文 **go2rtc + Frigate** 架构，旋转应在**最上游采集端**完成，下游无需各自处理。

**链路（与「接入 NVR」一致，旋转加在 exec 采集命令上）**：

```
CSI 摄像头（物理倒装 180°）
    │
    ▼
libcamera-vid / rpicam-vid（--rotation 180，ISP 内校正后再 H.264 编码）
    │
    ▼
go2rtc（:1984 Web / :8554 RTSP / :8555 WebRTC）
    ├→ Frigate Docker（detect + record，画面已正向）
    ├→ 浏览器（WebRTC / MSE）
    ├→ VLC / ffplay（RTSP）
    └→ Home Assistant
```

#### 推荐方案：采集端 `--rotation 180`

树莓派官方采集工具支持在 **ISP 阶段** 做 180° 旋转（编码前完成），**几乎不增加 CPU**；go2rtc 扇出的所有消费者（Frigate 录像/检测、直播、VLC）均为正向。

只需修改 `/var/lib/go2rtc/go2rtc.yaml` 中 `exec:` 行，增加 `--rotation 180`（等效：`--hflip --vflip`）。

**Pi 4**（`libcamera-vid`）：

```yaml
streams:
  picam:
    - exec:/usr/bin/libcamera-vid -t 0 --width 1920 --height 1080 --framerate 15 --nopreview --inline --codec h264 --rotation 180 -o -
```

**Pi 5**（`rpicam-vid`）：

```yaml
streams:
  picam:
    - exec:/usr/bin/rpicam-vid --camera 0 --mode 1920:1080 --framerate 15 --timeout 0 --nopreview --codec h264 --libav-video-codec h264 --libav-format h264 --inline --rotation 180 -o -
```

改完后重启并验证：

```bash
sudo systemctl restart go2rtc
curl -s http://127.0.0.1:1984/api/streams | python3 -m json.tool
```

- 管理页：`http://<Pi-IP>:1984/` → 流 `picam` 预览应为正向
- Frigate **无需改配置**，仍拉 `rtsp://127.0.0.1:8554/picam`

本地可先单独测方向（5 秒试录）：

```bash
rpicam-vid --timeout 5000 --nopreview --rotation 180 -o /tmp/test.h264
# Pi 4 将 rpicam-vid 换为 libcamera-vid
```

#### 备选：go2rtc FFmpeg 旋转

若无法在采集命令上加 `--rotation`（例如流来自外部 RTSP 而非本机 exec），可在 go2rtc 内用 FFmpeg **重编码并旋转**。此路 **CPU 开销明显更高**，Pi 上仅作备选。

**两路流**：一路原始 exec，一路 FFmpeg 引用并旋转；Frigate 改拉旋转后的流名：

```yaml
streams:
  picam_raw:
    - exec:/usr/bin/rpicam-vid --camera 0 --mode 1920:1080 --framerate 15 --timeout 0 --nopreview --codec h264 --libav-video-codec h264 --libav-format h264 --inline -o -
  picam:
    - "ffmpeg:picam_raw#video=h264#rotate=180"
```

Frigate `config.yml` 中 `path` 仍指向 `rtsp://127.0.0.1:8554/picam`（与流名 `picam` 一致）。Pi 4 将 `exec` 换为对应的 `libcamera-vid` 命令即可。

可选硬件编码（减轻 CPU，但多客户端时 SPS/PPS 等问题较多，稳定性不如采集端旋转）：

```yaml
    - "ffmpeg:picam_raw#video=h264#rotate=180#hardware"
```

#### 方案对比

| 方案 | CPU 开销 | 录像 / 直播 / 检测框 | 推荐度 |
|------|----------|----------------------|--------|
| **`--rotation 180` 在 exec 里** | 极低（ISP 内完成） | 全部正确 | ⭐ 首选 |
| go2rtc `ffmpeg:#rotate=180` | 高（需重编码） | 全部正确 | 备选 |
| 仅在播放器 / CSS 旋转 | 无 | 录像仍为倒的 | ❌ 不适合 NVR |
| 仅转 Frigate UI | 低 | 录像与检测框仍错 | ❌ 不推荐 |

#### 注意点

1. **仅支持 0° 与 180°**：libcamera / rpicam 栈在采集端**不支持** 90° / 270°（transpose）。若侧装需 90°，只能走 FFmpeg 软件转码，Pi 上 CPU 压力会显著上升。
2. **旋转放在最上游**：与 go2rtc 唯一采集入口原则一致；Frigate 的 detect、record、snapshot 与检测框方向才能一致。
3. **分辨率仍用原生模式**：如 1920×1080、1296×972 等（见「接入 NVR」分辨率表）；加 `--rotation 180` 不改变编码参数。
4. **不要用非原生分辨率**：例如 1280×720 仍可能导致无首帧等问题，与是否旋转无关。
5. **与 MJPEG `:8999` 方案互斥**：切换前须停用 `camera-stream`，避免摄像头 busy（见「接入 NVR → 与上一节 MJPEG 方案的关系」）。
