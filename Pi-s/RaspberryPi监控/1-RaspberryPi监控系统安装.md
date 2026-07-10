# 监测

##摄像头安装

### 物理安装和测试

**常用测试指令：**

* `vcgencmd get_camera`: 检测当时连接的摄像头信息
* `libcamera-hello --list-cameras`: 检测当时连接的摄像头信息
* `libcamera-still -o ./libcamera-still-test.jpg`: 测试拍摄一张libcamera-still-test.jpng照片,存到当前目录下。
*  `libcamera-vid -t 10000 -o ~/Shared/video.h264`: 测试录制一个10s的视频，PI5中`rpicam`可直接输出为mp4, `rpicam-vid  -t 10s -o test.mp4`

使用 `vcgencmd get_camera`，如果如下信息，则表示成功识别到摄像头：

```
$ vcgencmd get_camera
supported=1 detected=1, libcamera interfaces=1
or 
supported=1 detected=0, libcamera interfaces=1
$ libcamera-hello --list-cameras
Available cameras
-----------------
```


### 在Pi上采集摄像头并推流

在Pi上运行如下其中一个指令，采集视频流：

`libcamera-vid -t 0 -n --listen -o tcp://0.0.0.0:8888` // YUV420 编码（无损原始画质，带宽高）
`libcamera-vid -t 0 -n --inline --codec h264 --listen -o tcp://0.0.0.0:8888` // 强制使用 H.264 编码（有损画质，带宽低）


#### 1. 使用FFmpeg 查看视频流

```
brew update
brew install ffmpeg
```

使用ffplay查看视频流：

`ffplay tcp://192.168.1.193:8888`

#### 2. 使用VLC也可以查看视频流
[VLC-Download](https://www.videolan.org/vlc/) 安装完成后，将vlc指令加入环境：

`echo "alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'" >> ~/.zshrc`

使用vlc查看视频流：
	
`vlc --demux h264 --network-caching=300 --clock-synchro=0 tcp://192.168.1.193:8888`



## 仅开放网络摄像头

需求仅为多浏览器观看且按需采集。即：仅在有人观看时**启动**摄像头，并支持多终端同时拉流。

**重要**：观众断开后摄像头**保持运行**（仅断开 HTTP 流），避免 Pi 上 libcamera 因反复 `open/close` 卡死、导致 `:8999` 整站不可访问。只有**切换分辨率**或**重启服务**才会真正停摄像头。

**浏览器播 MJPEG 不稳定！！！**

**如果要做 24h 监控、录像、识别等，跳过到下一节「接入 NVR」。**

### 方案：`camera_stream_on_demand.py`

脚本路径：项目根目录 `camera_stream_on_demand.py`（配套 `camera-stream.service` 用于开机自启）。

#### 技术说明

基于 **Picamera2**（libcamera 栈）+ **硬件 MJPEG 编码器**，通过 HTTP 提供 MJPEG 流，浏览器/VLC 均可观看。

```
终端1 浏览器 ──┐
终端2 浏览器 ──┼──> /stream.mjpg ──> 观众计数 ──> Picamera2 采集+编码（单管线）
终端3 VLC    ──┘                              └──> 观众离开：仅减计数，摄像头常开
```

| 特性 | 说明 |
|------|------|
| 按需启动 | 第一个观众连上 `/stream.mjpg` 才 `start_recording()`；之后摄像头**保持运行**直到服务关闭或切换分辨率 |
| 多终端同看 | `ThreadingMixIn` 多连接；所有观众共享 **一条** 编码管线，不重复开摄像头 |
| 编码 | `JpegEncoder`（ov5647 上比 MJPEGEncoder 更可靠） |
| 默认画质 | **640×480 @ 25fps**（ov5647 原生分辨率，多观众最稳） |
| 分辨率限制 | 仅支持 **640×480 / 1296×972 / 1920×1080 / 2592×1944**，勿用 1280×720 |
| 空闲占用 | 无观众时 HTTP 服务仍常驻；摄像头若已启动会保持采集（传感器/编码持续占用，换取稳定性） |

HTTP 端点：

| 路径 | 作用 |
|------|------|
| `/` 或 `/index.html` | 预览页（含清晰度切换按钮） |
| `/stream.mjpg` | MJPEG 流（触发采集的入口） |
| `/status` | JSON 状态：观众数、分辨率、`camera_active` 等 |
| `/resolutions` | 可选分辨率列表及当前选中项 |
| `POST /resolution` | 切换分辨率，body：`{"width":640,"height":480}` |

预览页提供 **640×480 / 1296×972 / 1920×1080 / 2592×1944** 四个按钮；点击后服务端重启摄像头并以新分辨率推流，当前选中按钮高亮显示。

与上文 `libcamera-vid --listen` TCP 推流对比：本方案支持 **浏览器直接看**、**多观众扇出**、**首次按需启动**；TCP 方案适合单人 VLC 临时测试。

#### 部署与使用

**1. 复制脚本到 Pi**

```bash
scp camera_stream_on_demand.py pi@<树莓派IP>:~/
```

**2. 安装依赖（Pi 上）**

```bash
sudo apt update
sudo apt install -y python3-picamera2
```

**3. 启动**

```bash
python3 ~/camera_stream_on_demand.py
```

日志示例：`Listening on http://0.0.0.0:8999/`；有观众时输出 `Starting camera`；观众离开输出 `Viewer disconnected (... camera stays on)`，**不会**再输出 `Stopping camera`（除非切换分辨率或 `systemctl stop`）。

**4. 观看**

同一局域网内任意终端：

- 浏览器：`http://<树莓派IP>:8999/`
- 直接拉流：`http://<树莓派IP>:8999/stream.mjpg`（VLC：媒体 → 打开网络串流）
- 查状态：`http://<树莓派IP>:8999/status`

查 Pi IP：`hostname -I`

**5. 开机自启（可选）**

```bash
sudo cp ~/camera_stream_on_demand.py /home/pi/
sudo cp camera-stream.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now camera-stream.service
```

查看服务：`sudo systemctl status camera-stream`

**6. 常用调参**

编辑脚本顶部常量：

```python
PORT = 8999               # 监听端口
WIDTH = 640               # 必须 ov5647 原生之一: 640/1296/1920/2592
HEIGHT = 480              # 对应 480/972/1080/1944
FPS = 25                  # 帧率
STOP_GRACE_SEC = 5.0
FIRST_FRAME_TIMEOUT_SEC = 12.0
FRAME_STALL_SEC = 5.0
STREAM_IDLE_SEC = 45.0
```

画质档位（改 WIDTH/HEIGHT 即可，必须成对使用）：

| 档位 | 分辨率 | 适用 |
|------|--------|------|
| 流畅（默认） | 640×480 | 多终端同看 |
| 清晰 | 1296×972 | 单/双路观看 |
| 高清 | 1920×1080 | 单路、带宽充足 |
| 全分辨率 ⚠ | 2592×1944 | 传感器满幅；Pi 4 MJPEG 切换慢，进出该档位会 **hard reset**（约 20–30s） |

**不要用 1280×720** — 非 ov5647 原生模式，可能出现 `Camera started` 但 `/stream.mjpg` 永远无首帧、浏览器超时的现象。

**2592×1944** 硬件上支持，但全分辨率 JPEG 编码 + 切换时 libcamera 释放慢，容易拖死服务；日常监控建议最高 **1920×1080**。

#### 验证采集行为

1. 服务刚启动、未打开预览页 → `/status` 中 `camera_active: false`
2. 手机 + 电脑同时打开 `http://<树莓派IP>:8999/` → `viewers: 2`，`camera_active: true`
3. 全部关闭页面 → `viewers: 0`，但 `camera_active` **仍为 true**（摄像头常开）
4. 反复刷新页面 5–10 次 → `:8999` 应始终可访问，`viewers` 不应累积到 2、3、4…

#### 故障排查（画面卡死 / 网页打不开）

**现象**：`/stream.mjpg` 超时；Pi 日志只有 `Camera started`，无 `First frame ready` 或 `Viewer connected`。

**最常见原因**：分辨率不是 ov5647 原生模式（如 1280×720 或随意设 1920×1080 + MJPEGEncoder），管线启动但不产出 JPEG 帧。

**脚本已做的防护**（请更新到最新版）：

- 默认 **640×480 原生分辨率** + **JpegEncoder**
- 启动后 **等待首帧**（12s 超时），失败返回 503 而非无限挂起
- 并发观众 **共享同一次** 摄像头启动（`_ensure_camera`）
- 观众离开 **不** `stop_recording`（避免 libcamera 反复启停拖死进程）
- 帧停滞看门狗仅打日志，**不**自动 recover（recover 也可能挂死）

**处理步骤**：

```bash
# 更新脚本后重启
scp camera_stream_on_demand.py pi@hutpi.local:~/
sudo systemctl restart camera-stream

# 正常日志应包含：
# Viewer connected (1 active)
# Starting camera (640x480 @ 25fps, JpegEncoder)
# First frame ready (xxxxx bytes)
```

若仍失败，前台调试看完整报错：

```bash
python3 ~/camera_stream_on_demand.py
```

确认 `/status` 中 `"size": "640x480"`，不要仍是 1080p。


## 接入NVR

**适用场景**：24h 监控、运动/人形检测、事件录像、后续接 Home Assistant / 人脸识别等。若只需临时多人看一眼，用上一节 `:8999` MJPEG 即可。

NVR（Network Video Recorder，网络视频录像机）在这里指：**一条摄像头采集管线，由中间层扇出给多个消费者**，而不是每个应用各自再开一次摄像头。

### 为什么用 go2rtc + Frigate

树莓派 CSI 摄像头在 libcamera 栈下**只能被一个进程独占**。若 Frigate、浏览器、VLC 各自调用 `libcamera-vid` / `rpicam-vid`，第二个进程会 `camera busy`，或出现无首帧、服务卡死（与上一节 MJPEG 方案遇到的问题同源）。

因此推荐架构：

```
CSI 摄像头
    │
    ▼
libcamera-vid / rpicam-vid（宿主机上唯一采集进程，硬件 H.264）
    │
    ▼
go2rtc（:1984 Web / :8554 RTSP / :8555 WebRTC）
    ├→ Frigate Docker（detect + record，从 RTSP 拉流，不再开摄像头）
    ├→ 浏览器（WebRTC / MSE，低延迟预览）
    ├→ VLC / ffplay（RTSP）
    └→ Home Assistant（go2rtc 集成或 RTSP）
```

| 组件 | 角色 |
|------|------|
| `libcamera-vid` / `rpicam-vid` | 唯一打开摄像头，输出 H.264 到 stdout |
| **go2rtc** | 通过 `exec:` 拉起上述命令，维持一条管线，向多路消费者扇出 |
| **Frigate** | NVR + AI 检测；从 go2rtc 的 RTSP 取流，内部降采样做 detect |

**推荐部署**：go2rtc 跑在**宿主机**（必须能直接访问 CSI 摄像头），Frigate 用 **Docker** 且 `network_mode: host`（最简单，Frigate 用 `127.0.0.1:8554` 访问 go2rtc）。

### 与上一节 MJPEG 方案的关系

两方案**不能同时运行**——都会抢摄像头独占权。切换前停用 `:8999` 服务：

```bash
sudo systemctl stop camera-stream
sudo systemctl disable camera-stream
```

| 对比 | `:8999` MJPEG | go2rtc + Frigate |
|------|---------------|------------------|
| 用途 | 临时多人观看 | 24h 监控、录像、AI |
| 编码 | MJPEG（带宽大） | H.264（更适合录像/NVR） |
| 按需启停 | 首观众才开摄像头 | 摄像头随 go2rtc 常开 |
| 检测/录像 | 无 | Frigate 提供 |

### 1. 安装 go2rtc（宿主机）

**1.1 下载二进制**

```bash
sudo mkdir -p /var/lib/go2rtc && cd /var/lib/go2rtc
sudo curl -L -o go2rtc https://github.com/AlexxIT/go2rtc/releases/latest/download/go2rtc_linux_arm64
sudo chmod +x go2rtc
```

> 下载文件名**必须**与下面 systemd 里 `ExecStart` 一致。若误下成 `go2rtc_linux_arm64` 而未重命名，服务会 `status=203/EXEC` 崩溃重启，表现为 **8554 Connection refused**：
>
> ```bash
> sudo ln -sf /var/lib/go2rtc/go2rtc_linux_arm64 /var/lib/go2rtc/go2rtc
> ```

**1.2 确认本机采集命令（Pi 4 / Pi 5 不同）**

```bash
which libcamera-vid rpicam-vid
cat /proc/device-tree/model
```

| 机型 | 采集命令 | 说明 |
|------|----------|------|
| Pi 4 | `/usr/bin/libcamera-vid` | Bookworm 及以前常用名 |
| Pi 5 | `/usr/bin/rpicam-vid` | 新命名；无 `libcamera-vid` |

配置里请写**绝对路径**，避免 systemd 环境下 `$PATH` 不含 `/usr/bin` 导致 exec 失败。

**1.3 配置文件 `/var/lib/go2rtc/go2rtc.yaml`**

`picam` 是**自定义流名**，可改成任意标识（如 `front_door`）；RTSP 地址中的路径与此一致：`rtsp://<Pi-IP>:8554/picam`。

**Pi 4**（ov5647，1080p 示例）：

```yaml
api:
  listen: ":1984"    # Web 管理页、WebRTC/MSE 预览
rtsp:
  listen: ":8554"    # RTSP 扇出（Frigate / VLC / ffplay）
streams:
  picam:
    - exec:/usr/bin/libcamera-vid -t 0 --width 1920 --height 1080 --framerate 15 --nopreview --inline --codec h264 -o -
```

**Pi 5** 将 `exec` 行换成：

```yaml
    - exec:/usr/bin/rpicam-vid --camera 0 --mode 1920:1080 --framerate 15 --timeout 0 --nopreview --codec h264 --libav-video-codec h264 --libav-format h264 --inline -o -
```

分辨率须为 ov5647 **原生模式**之一，与上一节相同：

| 档位 | 分辨率 | NVR 建议 |
|------|--------|----------|
| 流畅 | 640×480 | 省 CPU/带宽，适合 detect 为主 |
| 清晰 | 1296×972 | 折中 |
| 高清 | 1920×1080 | 录像主码流推荐 |
| 全分辨率 | 2592×1944 | Pi 4 上编码压力大，慎用 |

**不要用 1280×720** — 非原生模式，易出现无首帧或 exec 启动后无输出。

Pi 5 必须加 `--libav-format h264`：输出到 pipe（`-o -`）时 libav 无法从「文件名」推断容器格式，缺省会 H.264 流 **EOF** / 灰屏。

**1.4 systemd 自启 `/etc/systemd/system/go2rtc.service`**

```ini
[Unit]
Description=go2rtc camera fan-out
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/var/lib/go2rtc
ExecStart=/var/lib/go2rtc/go2rtc
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now go2rtc
```

**1.5 验证**

```bash
sudo systemctl status go2rtc
ss -tlnp | grep -E '8554|1984'
curl -s http://127.0.0.1:1984/api/streams | python3 -m json.tool
```

- 管理页：`http://<Pi-IP>:1984/` → 点击流名 `picam` 应能 WebRTC/MSE 预览
- RTSP：`ffplay -rtsp_transport tcp rtsp://<Pi-IP>:8554/picam`

> `ffplay` 可能出现 `SETUP failed: 461 Unsupported transport`：客户端先试 UDP、go2rtc 回绝后自动改 TCP，一般可忽略；显式加 `-rtsp_transport tcp` 更干净。  
> `No accelerated colorspace conversion yuv420p to bgr24` 是 Mac 上用 CPU 做显示色彩转换，不影响出画。

### 2. Frigate（Docker）

Frigate **不再**直接 `exec` 开摄像头，而是从宿主机 go2rtc 拉 RTSP。detect 与 record 可共用同一路流，Frigate 内部缩放做检测，无需两条 `exec:`（两条 exec 会各开一个采集进程，第二个必 busy）。

**2.1 `docker-compose.yml` 示例**

```yaml
services:
  frigate:
    container_name: frigate
    image: ghcr.io/blakeblackshear/frigate:stable
    restart: unless-stopped
    network_mode: host
    privileged: true
    shm_size: "256mb"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./frigate/config:/config
      - ./frigate/storage:/media/frigate
```

`network_mode: host` 时容器内 `127.0.0.1` 即 Pi 本机。若用 bridge 网络，须把下面 RTSP 地址改成 Pi 局域网 IP（如 `192.168.1.193`）。

**2.2 `frigate/config/config.yml` 核心**

```yaml
mqtt:
  host: 127.0.0.1    # 按实际 MQTT 修改；无 MQTT 可先注释 mqtt 段

cameras:
  picam:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/picam
          input_args: preset-rtsp-generic
          roles:
            - detect
            - record
    detect:
      width: 640
      height: 480
      fps: 5
    record:
      enabled: true
      retain:
        days: 7
```

- `path` 中的 `picam` 须与 `go2rtc.yaml` 里 `streams` 的 key 一致
- `detect` 分辨率宜低于主码流（如 640×480 @ 5fps），降低 Pi 4 CPU
- 录像为 H.264 copy，避免软件 x264 转码

```bash
docker compose up -d
docker logs -f frigate
```

UI：`http://<Pi-IP>:5000`

### 3. 多终端同时观看

所有消费者都从 go2rtc 扇出，底层始终只有**一个** `libcamera-vid` / `rpicam-vid`：

| 终端 | 地址 | 说明 |
|------|------|------|
| 浏览器（推荐） | `http://<Pi-IP>:1984` | WebRTC 低延迟；点流名 `picam` |
| VLC / ffplay | `rtsp://<Pi-IP>:8554/picam` | 建议 `-rtsp_transport tcp` |
| Frigate | `http://<Pi-IP>:5000` | 检测框 + 事件录像 |
| Home Assistant | go2rtc 集成 | 或 RTSP 实体 |

可同时：Frigate 在录像 + 手机 VLC 在看 + 电脑浏览器 WebRTC。

### 4. 故障排查

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| `Connection refused`（8554） | go2rtc 未运行；二进制路径与 systemd 不一致 | `systemctl status go2rtc`；确认 `/var/lib/go2rtc/go2rtc` 存在且可执行 |
| RTSP `404 Not Found` / DESCRIBE 失败 | 流名错误；或 `exec` 命令不存在（Pi 4 配了 `rpicam-vid`） | `curl http://127.0.0.1:1984/api/streams`；`journalctl -u go2rtc -n 20` 看 `executable file not found` |
| `camera busy` | `camera-stream` 或其它进程占摄像头 | `sudo systemctl stop camera-stream`；`fuser` / `ps aux \| grep camera` |
| 有连接无画面 / EOF | Pi 5 缺 `--libav-format h264`；分辨率非原生 | 对照上文改 exec 参数 |
| Frigate 连不上 RTSP | Docker 非 host 仍用 `127.0.0.1` | 改为 Pi 局域网 IP 或改 `network_mode: host` |
| 两个 exec 流只有一路能看 | 摄像头独占，不能开两次采集 | 只保留一个 `exec:`；子码流由 Frigate 内部缩放 |

**常用诊断命令**：

```bash
journalctl -u go2rtc -f
curl -s http://127.0.0.1:1984/api/streams
ffprobe -rtsp_transport tcp rtsp://127.0.0.1:8554/picam
```

### 5. 与后续 AI / 人脸识别衔接

本节 Frigate 负责运动/人形检测与录像。若再接人脸识别，典型链路为（见下文「其它」）：

```
Pi Camera → go2rtc → Frigate（检测）→ MQTT → Double Take → CompreFace → Home Assistant
```

go2rtc 仍保持**唯一采集入口**；下游只消费 RTSP/事件，不再直接碰 CSI 摄像头。


## 其它
---

Pi 4B + 运动检测 + 人脸识别 + 录像

带 AI / 人脸识别的专用方案
摄像头帧 → 运动检测 →（有运动才）人脸检测 → 特征提取 → 身份比对 → 录像/告警

人脸识别中间件
Pi Camera → Frigate（运动/人形检测）→ MQTT → Double Take → CompreFace → 识别结果 → Home Assistant

运动检测：

flowchart LR
    subgraph capture [采集层]
        CAM[Picamera2]
        CAM --> MAIN[主码流 1080p 录像]
        CAM --> LORES[低分辨率 320x240 检测]
    end

    subgraph detect [检测层]
        LORES --> MOTION[运动检测 MOG2]
        MOTION -->|有运动| FACE[人脸检测]
        FACE -->|有人脸| RECOG[人脸识别]
    end

    subgraph action [动作层]
        RECOG --> RECORD[触发录像]
        RECOG --> ALERT[推送告警]
        RECOG --> DB[(SQLite 事件库)]
    end


核心原则：

双码流：低分辨率做检测，高分辨率只在触发时录像
运动门控：无运动不跑人脸识别（Pi 4B 上可省 80%+ CPU）
降采样：检测用 320×240 或 50% 缩放
硬件编码：录像走 H.264 硬件，不要软件 x264
