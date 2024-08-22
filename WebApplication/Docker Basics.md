# Docker Basics

## Docker 基本概念

* **Docker Engine引擎**

	The core component of Docker that enables container management. It includes the Docker daemon (dockerd), which runs as a background service, and the Docker CLI (docker), which provides a command-line interface for interacting with Docker.
 
* **Docker Image镜像**

	A Docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.
	Container images become containers at runtime and in the case of Docker containers – images become containers when they run on Docker Engine.
* **Docker Container容器**

	A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another.

* **Docker Registry仓库**

	A repository that stores Docker images. Docker Hub is the default public registry that allows developers to access and share images. 
	

## 安装


## hello world with node

`Dockerfile`配置文件：

```
FROM node:20-alpine
WORKDIR /app
COPY . .
CMD node helle-world.js
```

`.dockerignore` Docker忽略文件

```
node_modules/
```

* `docker build -t hello-world .`- 创建
* `docker images` - 查看
* `docker run hello-world` - 运行
* `docker run -p 8080:8080 react-docker` - 运行，并将容器的8080端口转发到物理机的8080端口
* `docker run -p 8080:8080 -v "$(pwd):/app" -v /app/node_modules react-docker` 将当前文件夹挂载到docker容器内的app目录，这样任何在当前文件夹更改的文件都会在docker容器内的app目录进行实时更改，`$(pwd)`在运行时表示当前目录， `-v`表示Volume. `-v /app/node_modules react-docker` 确保可以挂载？？？
* `docker run -it hello-docker sh`: 运行并进入容器的内的终端
* `docker ps` - 查看所有活动的容器， 加上`-a`列出所有的容器
* `docker stop id` - 停止运行容器，id为容器id
* `docker remove` - 删除容器
* `docker container prune` - 删除所有没有运行的容器

### nginx示例

```
FROM nginx:1.15.8-alpine
#configuration
copy ./nginx.conf /etc/nginx/nginx.conf
#content, comment out the ones you dont need!
copy ./*.html /usr/share/nginx/html/
#copy ./*.css /usr/share/nginx/html/
#copy ./*.png /usr/share/nginx/html/
#copy ./*.js /usr/share/nginx/html/
```

## 存储(数据,资料)卷

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

## 网络控制

* `docker network create demo-network -d bridg`: 创建bridg类型的网络
* `docker network ls`: 打印所有的网络
* `docker run -itd --rm --name smart_clock -p 8080:80 -v a-test-volume:/data --network demo-network smart_clock`: 启动容器时,指定加入网络
* `docker run -itd --rm --name smart_clock2 -p 8081:80 -v a-test-volume:/data smart_clock`: 创建另外一个没有配置网络的容器
* `docker exec -it smart_clock2 sh`: 进入smart_clock2容器的终端
* `docker network connect demo-network smart_clock2`: 将容器`smart_clock2`加入网络`demo-network`
* `ping smart_clock`
* `ping smart_clock2`

[How to create a static web server for HTML with NGINX](https://thatdevopsguy.medium.com/how-to-create-a-static-web-server-for-html-with-nginx-99bf8226bce6)
