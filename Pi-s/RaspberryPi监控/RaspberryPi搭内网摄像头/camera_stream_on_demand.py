#!/usr/bin/python3
"""
On-demand MJPEG camera server for Raspberry Pi (Picamera2 / libcamera).

- Multiple clients can watch /stream.mjpg at the same time (one encode pipeline).
- Camera starts on first viewer; stays running until service shutdown or resolution change.
  (Does NOT stop when HTTP clients disconnect — avoids libcamera hang on repeated open/close.)
"""

import io
import json
import logging
import socketserver
import threading
import time
from http import server

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

HOST = ""
PORT = 8999

# ov5647 native modes only — do NOT use non-native sizes (e.g. 1280x720).
FULL_SENSOR_SIZE = (2592, 1944)

RESOLUTION_PRESETS = {
    (640, 480): {"label": "640×480", "fps": 25},
    (1296, 972): {"label": "1296×972", "fps": 20},
    (1920, 1080): {"label": "1920×1080", "fps": 15},
    FULL_SENSOR_SIZE: {"label": "2592×1944", "fps": 5, "hard_reset": True},
}

FIRST_FRAME_TIMEOUT_SEC = 12.0
FULL_SENSOR_FRAME_TIMEOUT_SEC = 25.0
FRAME_STALL_SEC = 12.0
STREAM_IDLE_SEC = 15.0
RECOVERY_COOLDOWN_SEC = 45.0
STREAM_WRITE_TIMEOUT_SEC = 8.0
CAMERA_STOP_TIMEOUT_SEC = 8.0
HARD_RESET_STOP_TIMEOUT_SEC = 20.0
SWITCH_READY_TIMEOUT_SEC = 45.0
VIEWERS_IDLE_TIMEOUT_SEC = 4.0
RESTART_SETTLE_SEC = 0.6
HARD_RESET_SETTLE_SEC = 3.0
VIEWER_DRAIN_SEC = 4.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("camera-stream")

PAGE = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pi Camera</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 1rem; background: #111; color: #eee; }
    img { max-width: 100%; height: auto; border: 1px solid #333; min-height: 240px; background: #222; }
    .meta { color: #aaa; font-size: 0.9rem; margin-top: 0.5rem; }
    .status { color: #8cf; font-size: 0.85rem; }
    .res-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0; }
    .res-row button {
      background: #2a2a2a; color: #eee; border: 1px solid #444; border-radius: 6px;
      padding: 0.45rem 0.75rem; cursor: pointer; font-size: 0.9rem;
    }
    .res-row button:hover { background: #383838; }
    .res-row button.active { background: #1a5a8a; border-color: #3a8ad4; }
    .res-row button:disabled { opacity: 0.5; cursor: wait; }
  </style>
</head>
<body>
  <h1>Pi Camera (on-demand)</h1>
  <div class="res-row" id="res-btns"></div>
  <img id="stream" alt="live stream">
  <p class="status" id="status">Connecting…</p>
  <p class="meta">Stream starts when this page loads. 摄像头首次连接后保持运行，仅断开 HTTP 流，避免反复启停导致 Pi 卡死。<br>
  2592×1944 为传感器全分辨率，Pi 4 上 MJPEG 切换较慢；日常推荐最高 1920×1080。</p>
  <script>
    let img = document.getElementById('stream');
    const status = document.getElementById('status');
    const resBtns = document.getElementById('res-btns');
    let retries = 0;
    let switching = false;
    let currentW = 0;
    let currentH = 0;
    const MAX_RETRIES = 5;

    const PRESETS = [
      { w: 640, h: 480, label: '640×480' },
      { w: 1296, h: 972, label: '1296×972' },
      { w: 1920, h: 1080, label: '1920×1080' },
      { w: 2592, h: 1944, label: '2592×1944 ⚠' },
    ];

    function updateButtons() {
      resBtns.querySelectorAll('button').forEach((btn) => {
        const active = Number(btn.dataset.w) === currentW && Number(btn.dataset.h) === currentH;
        btn.classList.toggle('active', active);
      });
    }

    function buildButtons() {
      PRESETS.forEach(({ w, h, label }) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.dataset.w = w;
        btn.dataset.h = h;
        btn.textContent = label;
        btn.addEventListener('click', () => setResolution(w, h));
        resBtns.appendChild(btn);
      });
    }

    function bindStreamHandlers() {
      img.onload = () => {
        status.textContent = `Live · ${currentW}×${currentH}`;
        retries = 0;
      };
      img.onerror = () => {
        if (switching) return;
        if (retries >= MAX_RETRIES) {
          status.textContent = 'Stream failed — refresh the page or pick another resolution';
          return;
        }
        retries += 1;
        status.textContent = `Stream failed, retry in 3s (${retries}/${MAX_RETRIES})…`;
        setTimeout(loadStream, 3000);
      };
    }

    function loadStream() {
      if (switching) return;
      status.textContent = retries
        ? `Reconnecting (${retries})…`
        : `Connecting · ${currentW}×${currentH}…`;
      img.src = '/stream.mjpg?t=' + Date.now();
    }

    async function stopStream() {
      img.onload = null;
      img.onerror = null;
      img.removeAttribute('src');
      const parent = img.parentNode;
      const fresh = document.createElement('img');
      fresh.id = 'stream';
      fresh.alt = 'live stream';
      parent.replaceChild(fresh, img);
      img = fresh;
      await new Promise((r) => setTimeout(r, 300));
    }

    async function fetchJson(url, options = {}, timeoutMs = 20000) {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), timeoutMs);
      try {
        const r = await fetch(url, { ...options, signal: ctrl.signal });
        const j = await r.json();
        return { ok: r.ok, status: r.status, body: j };
      } finally {
        clearTimeout(timer);
      }
    }

    async function refreshStatus() {
      try {
        const { ok, body } = await fetchJson('/status', {}, 5000);
        if (!ok) return;
        currentW = body.width;
        currentH = body.height;
        updateButtons();
      } catch (e) {
        console.warn('status fetch failed', e);
      }
    }

    async function setResolution(w, h) {
      if (switching || (w === currentW && h === currentH)) return;
      switching = true;
      retries = 0;
      let switched = false;
      resBtns.querySelectorAll('button').forEach((b) => { b.disabled = true; });
      status.textContent = `Switching to ${w}×${h}…`;

      try {
        await stopStream();
        const { ok, body } = await fetchJson('/resolution', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ width: w, height: h }),
        }, 90000);
        if (!ok) throw new Error(body.error || 'resolution switch failed');

        currentW = body.width;
        currentH = body.height;
        updateButtons();
        switched = true;
      } catch (e) {
        status.textContent = `Switch failed: ${e.message}`;
        bindStreamHandlers();
      } finally {
        switching = false;
        resBtns.querySelectorAll('button').forEach((b) => { b.disabled = false; });
      }

      if (switched) {
        bindStreamHandlers();
        loadStream();
      }
    }

    buildButtons();
    bindStreamHandlers();
    refreshStatus().then(loadStream);
  </script>
</body>
</html>
"""


class StreamingOutput(io.BufferedIOBase):
    def __init__(self, on_frame=None):
        self.frame = None
        self.frame_seq = 0
        self.condition = threading.Condition()
        self._on_frame = on_frame

    def write(self, buf):
        if not buf:
            return len(buf)
        with self.condition:
            self.frame = buf
            self.frame_seq += 1
            self.condition.notify_all()
        if self._on_frame:
            self._on_frame()
        return len(buf)


class CameraManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._start_lock = threading.Lock()
        self._viewers = 0
        self._picam2 = None
        self._output = None
        self._active = False
        self._starting = False
        self._ready = threading.Event()
        self._generation = 0
        self._last_frame_time = 0.0
        self._resolution_switching = False
        self._recovering = False
        self._last_recovery_time = 0.0
        self._switch_ready = threading.Event()
        self._switch_ready.set()
        self.width = 640
        self.height = 480
        self.fps = RESOLUTION_PRESETS[(640, 480)]["fps"]
        self._watchdog_stop = threading.Event()
        self._watchdog = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog.start()

    @property
    def viewers(self):
        with self._lock:
            return self._viewers

    @property
    def active(self):
        with self._lock:
            return self._active

    @property
    def generation(self):
        with self._lock:
            return self._generation

    @property
    def switching(self):
        with self._lock:
            return self._resolution_switching

    @property
    def recovering(self):
        with self._lock:
            return self._recovering

    def frame_age_sec(self):
        with self._lock:
            if not self._active or self._last_frame_time <= 0:
                return None
            return round(time.monotonic() - self._last_frame_time, 1)

    def resolution_label(self):
        with self._lock:
            return f"{self.width}x{self.height}"

    def _touch_frame_time(self):
        with self._lock:
            self._last_frame_time = time.monotonic()

    def _bump_generation_locked(self):
        self._generation += 1
        output = self._output
        if output is not None:
            with output.condition:
                output.condition.notify_all()

    def _needs_hard_reset(self, old_size, new_size):
        return old_size == FULL_SENSOR_SIZE or new_size == FULL_SENSOR_SIZE

    def _first_frame_timeout(self):
        if (self.width, self.height) == FULL_SENSOR_SIZE:
            return FULL_SENSOR_FRAME_TIMEOUT_SEC
        return FIRST_FRAME_TIMEOUT_SEC

    def _wait_first_frame(self, output):
        timeout = self._first_frame_timeout()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with output.condition:
                if output.frame is not None:
                    log.info("First frame ready (%d bytes)", len(output.frame))
                    return True
                output.condition.wait(timeout=0.2)
        log.error("No first frame within %.0fs", timeout)
        return False

    def _video_configuration(self, picam2):
        buffers = 1 if (self.width, self.height) == FULL_SENSOR_SIZE else 2
        return picam2.create_video_configuration(
            main={"size": (self.width, self.height)},
            buffer_count=buffers,
            controls={"FrameRate": self.fps},
        )

    def _stop_picam2_timed(self, picam2, timeout, hard=False):
        done = threading.Event()

        def _run():
            try:
                self._stop_camera_worker(picam2, hard=hard)
            finally:
                done.set()

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        if done.wait(timeout):
            return True
        log.error("picam2 stop timed out after %.0fs (hard=%s)", timeout, hard)
        return False

    def _start_camera_unlocked(self):
        log.info(
            "Starting camera (%dx%d @ %dfps, JpegEncoder)",
            self.width,
            self.height,
            self.fps,
        )
        output = StreamingOutput(on_frame=self._touch_frame_time)
        picam2 = Picamera2()
        picam2.configure(self._video_configuration(picam2))
        picam2.start_recording(JpegEncoder(), FileOutput(output))

        if not self._wait_first_frame(output):
            try:
                picam2.stop_recording()
            finally:
                picam2.close()
            raise RuntimeError("camera produced no frames")

        with self._lock:
            self._output = output
            self._picam2 = picam2
            self._active = True
            self._last_frame_time = time.monotonic()
            self._bump_generation_locked()

    def _recover_after_stall(self):
        now = time.monotonic()
        with self._lock:
            if not self._active or self._viewers == 0:
                return
            if self._resolution_switching or self._recovering:
                return
            if now - self._last_recovery_time < RECOVERY_COOLDOWN_SEC:
                return
            self._recovering = True
            self._last_recovery_time = now
            self._bump_generation_locked()

        log.warning("Recovering camera after frame stall")
        try:
            time.sleep(0.3)
            self._drain_stale_viewers(2.0)
            hard = (self.width, self.height) == FULL_SENSOR_SIZE
            with self._start_lock:
                self._full_restart_unlocked(hard_reset=hard)
        except Exception as exc:
            log.error("Recovery failed: %s", exc)
            self._stop_camera(reason="recovery failed")
        finally:
            with self._lock:
                self._recovering = False

    def _wait_viewers_idle(self, timeout=VIEWERS_IDLE_TIMEOUT_SEC):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if self._viewers == 0:
                    return True
            time.sleep(0.1)
        with self._lock:
            viewers = self._viewers
        log.warning("viewers still connected after %.0fs (%d active)", timeout, viewers)
        return False

    def _drain_stale_viewers(self, timeout=VIEWER_DRAIN_SEC):
        if self._wait_viewers_idle(timeout):
            return
        with self._lock:
            if self._viewers > 0:
                log.warning("Clearing stale viewer count (%d)", self._viewers)
                self._viewers = 0

    def _full_restart_unlocked(self, hard_reset=False):
        stop_timeout = HARD_RESET_STOP_TIMEOUT_SEC if hard_reset else CAMERA_STOP_TIMEOUT_SEC
        settle = HARD_RESET_SETTLE_SEC if hard_reset else RESTART_SETTLE_SEC
        log.info(
            "Full camera restart -> %dx%d @ %dfps (hard_reset=%s)",
            self.width,
            self.height,
            self.fps,
            hard_reset,
        )
        with self._lock:
            self._bump_generation_locked()
            picam2 = self._picam2
            self._picam2 = None
            self._output = None
            self._active = False

        if picam2 is not None:
            self._stop_picam2_timed(picam2, stop_timeout, hard=hard_reset)
            time.sleep(settle)

        try:
            self._start_camera_unlocked()
        except RuntimeError:
            if not hard_reset:
                raise
            log.warning("camera start failed after hard reset, retrying")
            time.sleep(2.0)
            self._start_camera_unlocked()

    def _wait_switch_ready(self):
        if not self._switch_ready.wait(SWITCH_READY_TIMEOUT_SEC):
            raise RuntimeError("resolution switch still in progress")

    def _ensure_camera(self):
        with self._lock:
            if self._active and self._output is not None:
                return self._output, self._generation
            if self._starting:
                need_start = False
            else:
                self._starting = True
                self._ready.clear()
                need_start = True

        if not need_start:
            wait_timeout = self._first_frame_timeout() + 5
            if not self._ready.wait(wait_timeout):
                raise RuntimeError("timed out waiting for camera start")
            with self._lock:
                if not self._active or self._output is None:
                    raise RuntimeError("camera start failed")
                return self._output, self._generation

        try:
            with self._start_lock:
                with self._lock:
                    if self._active and self._output is not None:
                        return self._output, self._generation
                self._start_camera_unlocked()
            self._ready.set()
            with self._lock:
                return self._output, self._generation
        except Exception:
            self._ready.set()
            raise
        finally:
            with self._lock:
                self._starting = False

    def _stop_camera_worker(self, picam2, hard=False):
        try:
            picam2.stop_recording()
        except Exception as exc:
            log.warning("stop_recording failed: %s", exc)
        if hard:
            time.sleep(1.0)
        try:
            picam2.close()
        except Exception as exc:
            log.warning("picam2.close failed: %s", exc)
        if hard:
            time.sleep(0.5)

    def _stop_camera(self, reason="idle"):
        with self._lock:
            if not self._active:
                return
            picam2 = self._picam2
            self._picam2 = None
            self._output = None
            self._active = False
            self._starting = False
            self._ready.clear()
            self._bump_generation_locked()

        if picam2 is None:
            return

        log.info("Stopping camera (%s)", reason)
        done = threading.Event()

        def _run():
            try:
                self._stop_camera_worker(picam2)
            finally:
                done.set()

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        if not done.wait(CAMERA_STOP_TIMEOUT_SEC):
            log.error(
                "Camera stop timed out after %.0fs; restart the service if the next start fails",
                CAMERA_STOP_TIMEOUT_SEC,
            )

    def set_resolution(self, width, height):
        preset = RESOLUTION_PRESETS.get((width, height))
        if preset is None:
            raise ValueError(f"unsupported resolution: {width}x{height}")

        self._switch_ready.clear()
        try:
            with self._lock:
                old_size = (self.width, self.height)
                new_size = (width, height)
                if old_size == new_size:
                    return {
                        "width": width,
                        "height": height,
                        "fps": self.fps,
                        "changed": False,
                    }
                self._resolution_switching = True
                camera_active = self._active and self._picam2 is not None
                hard_reset = self._needs_hard_reset(old_size, new_size)
                self.width = width
                self.height = height
                self.fps = preset["fps"]
                self._bump_generation_locked()

            log.info(
                "Resolution set to %dx%d @ %dfps (hard_reset=%s)",
                width,
                height,
                preset["fps"],
                hard_reset,
            )
            self._drain_stale_viewers()

            with self._start_lock:
                if camera_active:
                    self._full_restart_unlocked(hard_reset=hard_reset)

            return {
                "width": width,
                "height": height,
                "fps": preset["fps"],
                "changed": True,
            }
        finally:
            with self._lock:
                self._resolution_switching = False
            self._switch_ready.set()

    def list_resolutions(self):
        with self._lock:
            current = (self.width, self.height)
        return [
            {
                "width": w,
                "height": h,
                "label": preset["label"],
                "fps": preset["fps"],
                "current": (w, h) == current,
            }
            for (w, h), preset in RESOLUTION_PRESETS.items()
        ]

    def _watchdog_loop(self):
        while not self._watchdog_stop.is_set():
            time.sleep(2.0)
            with self._lock:
                if not self._active or self._viewers == 0 or self._resolution_switching:
                    continue
                last_frame = self._last_frame_time
            stalled = time.monotonic() - last_frame
            if stalled > FRAME_STALL_SEC:
                log.warning(
                    "Frame stall detected (%.1fs) — browser will reconnect via /status",
                    stalled,
                )

    def acquire_viewer(self):
        if not self._switch_ready.wait(SWITCH_READY_TIMEOUT_SEC):
            raise RuntimeError("camera busy switching resolution")

        with self._lock:
            stale = self._viewers > 0

        if stale:
            log.info("Retiring %d stale stream(s) before new viewer", self._viewers)
            with self._lock:
                self._bump_generation_locked()
            self._wait_viewers_idle(max(VIEWERS_IDLE_TIMEOUT_SEC, STREAM_IDLE_SEC))
            with self._lock:
                if self._viewers > 0:
                    log.warning("Clearing stale viewer count (%d)", self._viewers)
                    self._viewers = 0

        with self._lock:
            self._viewers += 1
            log.info("Viewer connected (%d active)", self._viewers)

        try:
            output, generation = self._ensure_camera()
            return output, generation
        except Exception:
            with self._lock:
                self._viewers = max(0, self._viewers - 1)
                log.info("Viewer aborted during camera start (%d active)", self._viewers)
            raise

    def release_viewer(self):
        with self._lock:
            self._viewers = max(0, self._viewers - 1)
            log.info(
                "Viewer disconnected (%d active, camera stays %s)",
                self._viewers,
                "on" if self._active else "off",
            )

    def is_generation_current(self, generation):
        with self._lock:
            return generation == self._generation

    def shutdown(self):
        self._watchdog_stop.set()
        with self._lock:
            self._viewers = 0
        self._stop_camera(reason="shutdown")


camera = CameraManager()


class StreamingHandler(server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        log.debug("%s - " + fmt, self.client_address[0], *args)

    def _send_json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html"):
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/status":
            self._send_json(
                200,
                {
                    "viewers": camera.viewers,
                    "camera_active": camera.active,
                    "switching": camera.switching,
                    "recovering": camera.recovering,
                    "frame_age_sec": camera.frame_age_sec(),
                    "generation": camera.generation,
                    "size": camera.resolution_label(),
                    "width": camera.width,
                    "height": camera.height,
                    "fps": camera.fps,
                },
            )
            return

        if path == "/resolutions":
            self._send_json(200, {"presets": camera.list_resolutions()})
            return

        if path == "/stream.mjpg":
            self.connection.settimeout(STREAM_IDLE_SEC)
            try:
                output, generation = camera.acquire_viewer()
            except Exception as exc:
                log.error("Stream setup failed for %s: %s", self.client_address[0], exc)
                self.send_error(503, f"Camera unavailable: {exc}")
                return

            self.send_response(200)
            self.send_header("Age", "0")
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.send_header("Connection", "close")
            self.end_headers()

            last_sent_seq = -1
            try:
                while camera.is_generation_current(generation):
                    with output.condition:
                        if not output.condition.wait(timeout=0.5):
                            if not camera.is_generation_current(generation):
                                break
                            continue
                        frame = output.frame
                        seq = output.frame_seq
                    if frame is None or seq == last_sent_seq:
                        continue
                    if not camera.is_generation_current(generation):
                        break
                    last_sent_seq = seq
                    chunk = (
                        b"--FRAME\r\n"
                        b"Content-Type: image/jpeg\r\n"
                        + f"Content-Length: {len(frame)}\r\n\r\n".encode("ascii")
                        + frame
                        + b"\r\n"
                    )
                    self.connection.settimeout(STREAM_WRITE_TIMEOUT_SEC)
                    self.wfile.write(chunk)
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError) as exc:
                log.info("Stream ended for %s: %s", self.client_address[0], exc)
            finally:
                camera.release_viewer()
            return

        self.send_error(404)

    def do_POST(self):
        path = self.path.split("?", 1)[0]

        if path == "/resolution":
            try:
                data = self._read_json_body()
                width = int(data["width"])
                height = int(data["height"])
                result = camera.set_resolution(width, height)
                self._send_json(200, result)
            except (KeyError, TypeError, ValueError) as exc:
                self._send_json(400, {"error": str(exc)})
            except Exception as exc:
                log.error("Resolution switch failed: %s", exc)
                self._send_json(500, {"error": str(exc)})
            return

        self.send_error(404)


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    address = (HOST, PORT)
    httpd = StreamingServer(address, StreamingHandler)
    log.info(
        "Listening on http://0.0.0.0:%d/  default=%dx%d",
        PORT,
        camera.width,
        camera.height,
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.info("Shutting down")
    finally:
        camera.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
