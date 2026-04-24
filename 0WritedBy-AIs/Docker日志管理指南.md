# Docker 日志管理指南

> 个人备忘文档 | 最后更新：2026-04-10

---

## 目录

1. [核心理念](#1-核心理念)
2. [应用输出到 stdout](#2-应用输出到-stdout)
3. [查看日志](#3-查看日志)
4. [日志文件位置](#4-日志文件位置)
5. [保存日志到文件](#5-保存日志到文件)
6. [配置日志轮转](#6-配置日志轮转防止磁盘撑满)
7. [进阶：Loki + Grafana 集中管理](#7-进阶loki--grafana-集中管理)
8. [常见问题](#8-常见问题)

---

## 1. 核心理念

Docker 容器日志管理遵循 **12-Factor App** 原则：

- ✅ 应用只负责将日志输出到 **stdout / stderr**
- ✅ 日志的收集、存储、轮转由 **平台（Docker）统一管理**
- ❌ 不在容器内部写文件、不在容器内部做 logrotate

```
应用 → stdout/stderr → Docker 引擎捕获 → json-file 存储到宿主机
                                        → 或转发到 Loki / ELK 等平台
```

---

## 2. 应用输出到 stdout

### Python

```python
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("App started")
```

### Node.js

```javascript
// console.log 默认就是 stdout，console.error 是 stderr
console.log("Info message")
console.error("Error message")
```

### nginx / mosquitto 官方镜像

官方镜像默认已输出到 stdout，无需额外配置。

---

## 3. 查看日志

### 基本命令

```bash
# 查看全部日志
docker logs <容器名或ID>

# 实时跟踪（类似 tail -f）
docker logs -f <容器名>

# 只看最后 N 行
docker logs --tail 100 <��器名>

# 带时间戳
docker logs -t <容器名>
```

### 常用组合

```bash
# 实时跟踪 + 最后 50 行 + 时间戳
docker logs -f -t --tail 50 <容器名>

# 查看某时间之后的日志
docker logs --since "2026-04-10T08:00:00" <容器名>

# 查看某段时间范围内的日志
docker logs --since "2026-04-10T08:00:00" --until "2026-04-10T09:00:00" <容器名>
```

### docker-compose 项目

```bash
# 查看所有服务日志
docker-compose logs -f

# 只看某个服务
docker-compose logs -f app
docker-compose logs -f nginx
```

---

## 4. 日志文件位置

Docker 默认使用 `json-file` 驱动，日志文件存储在宿主机：

```
/var/lib/docker/containers/<容器ID>/<容器ID>-json.log
```

### 快速找到某容器的日志路径

```bash
docker inspect <容器名> --format='{{.LogPath}}'
```

### 日志文件格式（JSON，每行一条）

```json
{"log":"App started\n","stream":"stdout","time":"2026-04-10T08:00:00Z"}
{"log":"Error occurred\n","stream":"stderr","time":"2026-04-10T08:00:01Z"}
```

---

## 5. 保存日志到文件

### 一次性导出

```bash
# 导出全部日志
docker logs <容器名> > app.log 2>&1

# 导出带时间戳的日志
docker logs -t <容器名> > app.log 2>&1

# 只导出最近 1000 行
docker logs --tail 1000 <容器名> > app.log 2>&1

# 导出某段时间的日志
docker logs --since "2026-04-10T00:00:00" <容器名> > app-20260410.log 2>&1
```

### 实时持续写入文件（后台运行）

```bash
docker logs -f <容器名> >> app.log 2>&1 &
```

### 定时备份脚本

```bash
#!/bin/bash
# save_logs.sh - 每天定时备份日志

CONTAINER="your-app"
LOG_DIR="/data/logs"
DATE=$(date +%Y%m%d)

mkdir -p "$LOG_DIR"
docker logs --since "24h" "$CONTAINER" > "$LOG_DIR/${CONTAINER}-${DATE}.log" 2>&1

# 保留最近 30 天的备份，删除更早的
find "$LOG_DIR" -name "*.log" -mtime +30 -delete

echo "日志已保存到 $LOG_DIR/${CONTAINER}-${DATE}.log"
```

```bash
# 添加定时任务，每天凌晨 1 点执行
crontab -e
0 1 * * * /path/to/save_logs.sh
```

---

## 6. 配置日志轮转（防止磁盘撑满）

> ⚠️ **必须配置！** 不配置的话 json.log 会无限增长撑满磁盘。

### 方式一：在 docker-compose.yml 中配置（推荐）

```yaml
services:
  app:
    image: your-app
    logging:
      driver: "json-file"
      options:
        max-size: "20m"    # 单文件最大 20MB
        max-file: "5"      # 最多保留 5 个文件（共最多 100MB）

  nginx:
    image: nginx
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  mqtt:
    image: eclipse-mosquitto
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 方式二：全局配置（对所有容器生效）

编辑 `/etc/docker/daemon.json`：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "20m",
    "max-file": "5"
  }
}
```

修改后重启 Docker：

```bash
sudo systemctl restart docker
```

> ⚠️ 注意事项：
> - 轮转配置只对**新创建的容器**生效
> - 已有容器需重建：`docker-compose up -d` 会自动重建
> - 轮转后旧文件无法通过 `docker logs` 查看，只能直接读取文件

---

## 7. 进阶：Loki + Grafana 集中管理

多个服务日志分散时，推荐使用 **Promtail + Loki + Grafana** 集中查询，比 ELK 更轻量。

```
容器 stdout → Promtail 采集 → Loki 存储 → Grafana 查询
```

### docker-compose.yml

```yaml
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock
      - ./promtail-config.yaml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  loki-data:
  grafana-data:
```

### promtail-config.yaml

```yaml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: [__meta_docker_container_name]
        target_label: container
```

### 启动

```bash
docker-compose up -d
# 打开浏览器访问 http://<你的IP>:3000
# 在 Grafana 中添加 Loki 数据源（URL 填 http://loki:3100）
# 即可按容器名过滤搜索所有日志
```

---

## 8. 常见问题

### Q：`docker logs` 看不到日志？
- 确认应用确实输出到 stdout，而不是写到容器内部文件
- 检查使用的 log driver：`docker inspect <容器名> | grep LogConfig`
- 若 driver 是 `none`，则日志被丢弃，改为 `json-file`

### Q：磁盘被日志占满了怎么办？
```bash
# 查看哪个容器日志最大
du -sh /var/lib/docker/containers/*/*-json.log | sort -rh | head -10

# 清空某容器日志（不影响容器运行）
truncate -s 0 $(docker inspect <容器名> --format='{{.LogPath}}')
```

### Q：如何查看已轮转的旧日志？
```bash
# 直接读取宿主机上的日志文件（需要 root）
ls /var/lib/docker/containers/<容器ID>/
# 轮转文件命名如：<容器ID>-json.log.1  <容器ID>-json.log.2
```

### Q：日志太多，想按关键词过滤？
```bash
# 配合 grep 过滤
docker logs <容器名> 2>&1 | grep "ERROR"

# 实时过滤
docker logs -f <容器名> 2>&1 | grep --line-buffered "ERROR"
```

---

## 快速参考

| 需求 | 命令 |
|---|---|
| 实时查看日志 | `docker logs -f <容器名>` |
| 查看最后 100 行 | `docker logs --tail 100 <容器名>` |
| 导出日志到文件 | `docker logs <容器名> > app.log 2>&1` |
| 查询日志文件路径 | `docker inspect <容器名> --format='{{.LogPath}}'` |
| 清空日志文件 | `truncate -s 0 $(docker inspect <容器名> --format='{{.LogPath}}')` |
| 查找占用磁盘最多的日志 | `du -sh /var/lib/docker/containers/*/*-json.log \| sort -rh \| head -10` |