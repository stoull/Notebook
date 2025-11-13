# Docker指令入门




docker build -t vault:latest . : 读取Dockerfile，生成名为my-app、标签为latest的镜像 


docker run -d -p 9090:8000 vault:latest : 基于镜像创建并后台运行容器，并将主机8080端口映射到容器8000端口


gunicorn --config gunicorn.config.py app:app


docker container exec -it nginx-server sh : 进入容器


docker compose up -d --build --no-deps nginx : 更新特定的容器


### Docker Engine

1. **docker服务控制管理**

	| Operation | Command | --- |
	| --- | --- | --- |
	| Status | sudo systemctl status docker |
	| Start | sudo systemctl start docker |
	| Stop | sudo systemctl stop docker |
	| Restart | sudo systemctl restart docker |
	| Enable during startup | sudo systemctl enable docker |
	| Disable during startup | sudo systemctl disable docker |
	| View systemd journal | sudo journalctl -u docker |

2. **镜像(images)相关**

	* `docker images` or `docker image ls`:  列出所有的本地镜像
	* `docker image rm image_name`: 删除镜像 
	
	* Docker Hub镜像的搜索与拉取:
	
		`docker search debian`
		`docker search --filter is-official=true --filter stars=3 debian`
		`docker image pull debian`
	
	* 按tag及本地拉取, 对应的tag在Docker CLI中获取不到, 需要用其中方法获取,如api或网页:
	
		`docker image pull debian:bookworm`
		`docker pull ubuntu:24.04`
		`docker image pull myregistry.local:5000/testing/test-image`

	* 镜像的创建
	
		`docker build -t <image_name> <path_to_Dockerfile>`
		`docker build -t smart_clock . `
		`docker build -t smart_clock:1.0 . `
		
		>* `.`为docker的build环境, docker会在当前目录下查找Dockerfile并进行build动作.
		>* 其中`-t`为给镜像取一个tag名称为smart_clock, 如没有执行`docker build . `则没有tag, 已有的镜像可使用`docker image tag`设置tag名称
		> `-t smart_clock:1.0`如果不指定后面的tag`:1.0`, 则默认为latest.


	* 镜像的导入与导出:
	
		`docker image  save -o <file-name.tar> <image-name>`: `image-name` 可以多个
		`docker image  load -i <file-name.tar>`
	
	更多指令:
	
	| Command| Description|
	| --- | ---|
	| `docker image history` | Show the history of an image |
	| `docker image import` | Import the contents from a tarball to create a filesystem image |
	| `docker image inspect` | Display detailed information on one or more images |
	| `docker image load` | Load an image from a tar archive or STDIN |
	| `docker image prune` | Remove unused images |
	| `docker image rm` | Remove one or more images |
	| `docker image save` | Save one or more images to a tar archive (streamed to STDOUT by default) |
	| `docker image tag` | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |
	| `docker image ls` | List images |
	| `docker image pull` | Download an image from a registry |
	| `docker image push` | Upload an image to a registry |
	
	[详见- Manage images ](https://docs.docker.com/reference/cli/docker/image/)
	
3. **容器(containers)相关**

	* `docker ps` or `docker ps -a`: 列出正在运行的或所有的容器.
	* `docker container create -it --name smart_clock`: 只创建一个容器,不运行
	* `docker container start --attach -i smart_clock`: 运行容器
	* `docker container stop <container_id or name>`: 停止容器
	* `docker container rm <container_id or name>`: 删除容器
	* `docker logs <container_id or name>`: 查看日志输出
	* 容器创建与运行
		
	  	`docker container run -it --rm --name name_you_want -p 8080:80 Image_Name`
	  	`docker container run -it --rm -d --name name_you_want -p 127.0.0.1:8080:80/tcp Image_Name`
	  	
	  	* `-it`: 为常用的选项,即可用交互式终端与创建的容器进行连接, 进行输入与输出
	  	* `--rm`: Automatically remove the container and its associated anonymous volumes when it exits
	  	* `--name smart_clock`: 给运行的容器取名为smart_clock, 后面对这个容器操作(eg. docker container stop smart_clock)可使用这个名称. 不然只能使用容器id, 或者查找其随机生成的名称.
	  	* `-p 8080:80`: 为`-p <host_port>:<container_port>`, 将容器的端口publish到主机系统的端口, 这里是主机8080端口的数据都会转发到容器内的80端口.
	  	* `-d`: 在后台运行容器, 并返回一个容器ID, 可以使用`docker logs smart_clock`查看日志.
	  	
	* 容器终端交互
	
		当容器启动后,可用交互式终端连接容器,可以对内部进行文件操作:
		`docker container exec -it Your_Container_Name sh`
		
		也可以不用交互式, 如: `smart_clock`容器内创建`/usr/share/nginx/html/alert.html`文件:
		
		`docker exec -d smart_clock touch /usr/share/nginx/html/alert.html`
	
4. **存储(数据,资料)卷相关**

	* `docker volume ls`: 列出当前已创建的存储卷
	* `docker volume create a-test-volume`: 创建存储卷
	* `docker volume inspect a-test-volume`: 查看存储卷信息
	* `docker run -itd --rm --name smart_clock --mount source=a-test-volume,target=/data smart_clock`: 将创建的卷挂载到smart_clock容器
	* `docker run -itd --rm --name smart_clock -v a-test-volume:/data smart_clock`: 将创建的卷挂载到smart_clock容器
	* `docker volume rm a-test-volume`: 删除存储卷

	**存储卷与主机文件系统之间的关系:**
	一般将存储卷挂载到容器的某个目录下, 只要写入到这个目录的数据,是不会因为容器的停止或者删除而丢失的. 在Linux系统中, Docker的volumes是直接暴露Linux的文件系统中的, 而MacOS则不是的:
	
	```
	$ sudo docker volume inspect vault
	[
	    {
	        "CreatedAt": "2024-08-22T16:58:33+08:00",
	        "Driver": "local",
	        "Labels": null,
	        "Mountpoint": "/var/lib/docker/volumes/a-test-volume/_data",
	        "Name": "a-test-volume",
	        "Options": null,
	        "Scope": "local"
	    }
	]
	```
		
	* `Mountpoint`:即为这个数据卷在主机中的存储位置
	* `Scope`: 中的local,为本地存储目录
	
	**注意**在Mac系统中,Docker的volumes不直接暴露在 macOS 的文件系统中. 而是存储在 Docker 虚拟机的文件系统中. 
	
	如果想查看某个卷的内容，可以使用以下命令启动一个临时容器，并将卷挂载到该容器中：`docker run --rm -v a-test-volume:/data alpine ls /data`

5. **网络控制相关**

	* `docker network create demo-network -d bridg`: 创建bridg类型的网络
	* `docker network ls`: 打印所有的网络
	* `docker run -itd --rm --name smart_clock -p 8080:80 -v a-test-volume:/data --network demo-network smart_clock`: 启动容器时,指定加入网络
	* `docker run -itd --rm --name smart_clock2 -p 8081:80 -v a-test-volume:/data smart_clock`: 创建另外一个没有配置网络的容器
	* `docker exec -it smart_clock2 sh`: 进入smart_clock2容器的终端
	* `docker network connect demo-network smart_clock2`: 将容器`smart_clock2`加入网络`demo-network`
	* `docker network disconnect <network_name> <container_id>`: 从指定网络中断开容器连接
	* `ping smart_clock`
	* `ping smart_clock2`


6. 多容器
7. 其它


### Docker Build

Docker Build implements a client-server architecture, where:

Client: Buildx is the client and the user interface for running and managing builds.
Server: BuildKit is the server, or builder, that handles the build execution.
When you invoke a build, the Buildx client sends a build request to the BuildKit backend. BuildKit resolves the build instructions and executes the build steps. The build output is either sent back to the client or uploaded to a registry, such as Docker Hub.

Buildx and BuildKit are both installed with Docker Desktop and Docker Engine out-of-the-box. When you invoke the docker build command, you're using Buildx to run a build using the default BuildKit bundled with Docker.

当构建完成一个Dockerfile之后，使用下面的指令构建镜像：

`docker build -t my-app:latest .`: 读取Dockerfile，生成名为my-app、标签为latest的镜像
`docker run -d -p 8080:80 my-app:latest`: 基于镜像创建并后台运行容器，并将主机8080端口映射到容器80端口

### Docker Compose 指令

Docker Compose 指令的基本格式是 `docker compose [OPTIONS] [COMMAND] [ARGS...]`。通常在包含 `docker-compose.yml` 文件的目录下执行。

#### 1. 生命周期管理

*   **启动服务**
    ```bash
    docker compose up
    ```
    *   `-d`：后台运行（分离模式）。**最常用**：`docker compose up -d`
    *   `--build`：在启动容器前重新构建镜像。例如：`docker compose up -d --build`

*   **停止并移除容器、网络**
    ```bash
    docker compose down
    ```
    *   `-v`：同时移除 **数据卷**。**警告**：这会删除所有数据，请谨慎使用。
    *   `--rmi all`：移除所有相关的镜像。

*   **启动已存在的服务**
    ```bash
    docker compose start [SERVICE...]
    ```
    启动已被停止的容器，不会重新创建容器。

*   **停止运行中的服务**
    ```bash
    docker compose stop [SERVICE...]
    ```
    优雅地停止容器，不会移除容器。

*   **重启服务**
    ```bash
    docker compose restart [SERVICE...]
    ```
    先 `stop` 再 `start`。

#### 2. 查看状态与日志

*   **查看服务运行状态**
    ```bash
    docker compose ps
    ```
    列出所有 Compose 管理的容器状态。

*   **查看服务日志**
    ```bash
    docker compose logs
    ```
    *   `-f`：跟踪日志输出（类似 `tail -f`）。
    *   `[SERVICE]`：查看特定服务的日志。例如：`docker compose logs -f nginx`

*   **查看镜像**
    ```bash
    docker compose images
    ```
    列出 Compose 文件使用的镜像。

#### 3. 执行命令与进入容器

*   **在运行的容器中执行命令**
    ```bash
    docker compose exec [SERVICE] [COMMAND]
    ```
    *   例如：进入 `web` 服务的 bash 终端：`docker compose exec web bash`
    *   例如：在 `database` 服务中执行 `psql` 命令：`docker compose exec database psql -U user -d dbname`

*   **在容器中启动交互式 Shell** (旧版本写法，现在 `exec` 更常用)
    ```bash
    docker compose run [SERVICE] [COMMAND]
    ```
    *   会启动一个新的容器来运行一次性命令，适合执行数据库迁移等任务。
    *   默认会创建匿名卷，可以使用 `--no-deps` 不启动依赖的服务，`--rm` 运行后自动删除容器。

#### 4. 构建与拉取

*   **构建或重新构建服务镜像**
    ```bash
    docker compose build
    ```
    *   `--no-cache`：构建时不使用缓存。

*   **拉取服务依赖的镜像**
    ```bash
    docker compose pull
    ```

---

### 二、只更新特定容器的指令

这是日常开发和运维中非常常见的需求。有多种方法可以实现，核心思想是 **只重建和重启你关心的那个服务**。

假设我们有一个 `docker-compose.yml` 文件，定义了 `web`, `app`, `database` 三个服务，现在只想更新 `app` 服务。

#### 方法 1：使用 `docker compose up` 指定服务名 (最推荐)

这是最直接、最常用的方法。

```bash
# 1. 首先，确保你已经更新了 app 服务的镜像（例如通过 docker build 或 docker pull）
# 2. 然后执行：
docker compose up -d --no-deps app
```

*   `-d`：后台运行。
*   `--no-deps`：**关键选项**。它表示 **不重启与 `app` 服务相关联的依赖服务**（例如 `database`）。如果没有这个选项，Compose 可能会尝试重启 `app` 所依赖的服务。
*   `app`：指定要更新的服务名称。

这条命令会：
1.  停止旧的 `app` 容器。
2.  基于最新的镜像（如果镜像有变动）创建一个新的 `app` 容器。
3.  启动新的容器。
4.  `web` 和 `database` 服务完全不受影响。

#### 方法 2：先停止再启动 (适合临时修改)

如果你只是修改了配置文件或代码，并想快速重启单个服务，可以：

```bash
# 1. 停止特定服务
docker compose stop app

# 2. 启动特定服务 (会使用最新的镜像和配置)
docker compose start app
```
或者更简单：
```bash
docker compose restart app
```
但注意，`restart` 命令默认不会拉取新镜像，它只是重启现有的容器。如果你已经通过 `docker compose pull app` 拉取了新镜像，或者重新构建了镜像，使用 `restart` 是不会生效的，需要用 `up`。

#### 方法 3：组合使用 `pull` 和 `up`

如果你需要从镜像仓库拉取最新镜像并更新特定容器：

```bash
# 1. 拉取特定服务的最新镜像
docker compose pull app

# 2. 重启该服务以使用新镜像
docker compose up -d --no-deps app
```

#### 方法 4：强制重建特定容器

如果你修改了 `Dockerfile` 或构建上下文，需要强制重建镜像和容器：

```bash
docker compose up -d --build --no-deps app
```
*   `--build`：强制在启动前构建镜像。

### 总结

| 场景 | 推荐命令 |
| :--- | :--- |
| **通用启动** | `docker compose up -d` |
| **停止并清理** | `docker compose down` |
| **查看日志** | `docker compose logs -f [service]` |
| **进入容器** | `docker compose exec [service] bash` |
| **只更新特定容器** | `docker compose up -d --no-deps [service]` |
| **拉取新镜像并更新特定容器** | `docker compose pull [service] && docker compose up -d --no-deps [service]` |
| **代码/配置更新后重建特定容器** | `docker compose up -d --build --no-deps [service]` |

记住 `--no-deps` 这个选项，它是实现“只更新特定容器”而不影响其依赖服务的关键。


[Docker docs](https://docs.docker.com/manuals/)

[Docker Networking – Basics, Network Types & Examples](https://spacelift.io/blog/docker-networking)








