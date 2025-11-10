## 解决 Docker 镜像拉取超时的方法

### 方法 1：配置 Docker 镜像加速器（推荐）

配置国内镜像源以加速拉取。

#### macOS（Docker Desktop）

1. 打开 Docker Desktop
2. 进入 Settings → Docker Engine
3. 在 JSON 配置中添加：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://ccr.ccs.tencentyun.com"
  ]
}
```

4. 点击 Apply & Restart

#### Linux

编辑或创建 `/etc/docker/daemon.json`：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://ccr.ccs.tencentyun.com"
  ]
}
EOF

# 重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 方法 2：使用国内镜像仓库

修改 `docker-compose.yml`，使用国内镜像：

```yaml
services:
  mariadb:
    # 使用阿里云镜像
    image: registry.cn-hangzhou.aliyuncs.com/library/mariadb:latest
    # 或使用腾讯云镜像
    # image: ccr.ccs.tencentyun.com/library/mariadb:latest
    # 或使用网易镜像
    # image: hub-mirror.c.163.com/library/mariadb:latest
```

### 方法 3：手动拉取镜像

先手动拉取，再启动服务：

```bash
# 使用镜像加速器拉取
docker pull docker.mirrors.ustc.edu.cn/library/mariadb:latest

# 或者使用阿里云
docker pull registry.cn-hangzhou.aliyuncs.com/library/mariadb:latest

# 然后给镜像打标签
docker tag registry.cn-hangzhou.aliyuncs.com/library/mariadb:latest mariadb:latest

# 再运行 docker compose
docker compose up -d
```

### 方法 4：使用代理（如果有）

```bash
# 设置代理环境变量
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port

# 然后拉取镜像
docker pull mariadb:latest
```

### 方法 5：增加超时时间

如果网络较慢，可以增加超时时间：

```bash
# 设置 Docker 客户端超时
export DOCKER_CLIENT_TIMEOUT=300
export COMPOSE_HTTP_TIMEOUT=300

# 然后运行
docker compose up -d
```

### 推荐的完整解决方案

1. 配置镜像加速器（方法 1）
2. 重启 Docker
3. 验证配置：

```bash
docker info | grep -A 10 "Registry Mirrors"
```

4. 重新拉取镜像：

```bash
docker compose pull
docker compose up -d
```

### 如果仍然失败，使用国内镜像源

修改你的 `docker-compose.yml`：

```yaml
services:
  mariadb:
    # 使用中科大镜像源
    image: docker.mirrors.ustc.edu.cn/library/mariadb:latest
    # 或者使用阿里云
    # image: registry.cn-hangzhou.aliyuncs.com/library/mariadb:latest
    container_name: mariadb
    restart: unless-stopped
    ports:
      - "3306:3306"
    # ... 其他配置保持不变
```

### 验证镜像加速器是否生效

```bash
# 查看 Docker 信息
docker info

# 测试拉取镜像
docker pull mariadb:latest
```

### 常用国内镜像源列表

- 中科大：`https://docker.mirrors.ustc.edu.cn`
- 网易：`https://hub-mirror.c.163.com`
- 百度云：`https://mirror.baidubce.com`
- 腾讯云：`https://ccr.ccs.tencentyun.com`
- 阿里云：需要登录后获取专属加速地址

### 快速解决步骤

```bash
# 1. 配置镜像加速器（macOS）
# 在 Docker Desktop 的 Settings → Docker Engine 中添加镜像源

# 2. 重启 Docker Desktop

# 3. 清理并重新拉取
docker compose down
docker compose pull
docker compose up -d
```

优先使用方法 1（配置镜像加速器），这是最稳定的方案。配置后重启 Docker，再重新运行 `docker compose up -d`。