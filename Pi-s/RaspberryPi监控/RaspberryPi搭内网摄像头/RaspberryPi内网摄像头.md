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


## 使用VPN查看摄像头

使用[tailscale.com](https://tailscale.com), TailScale[源码](https://github.com/tailscale/tailscale) 安装VPN，使用VPN连接到家里的内网进行查看。

