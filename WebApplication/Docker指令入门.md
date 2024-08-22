# Docker指令入门

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
		
	  	`docker container run -it --rm --name smart_clock -p 8080:80 smart_clock`
	  	`docker container run -it --rm -d --name smart_clock -p 127.0.0.1:8080:80/tcp smart_clock`
	  	
	  	* `-it`: 为常用的选项,即可用交互式终端与创建的容器进行连接, 进行输入与输出
	  	* `--rm`: Automatically remove the container and its associated anonymous volumes when it exits
	  	* `--name smart_clock`: 给运行的容器取名为smart_clock, 后面对这个容器操作(eg. docker container stop smart_clock)可使用这个名称. 不然只能使用容器id, 或者查找其随机生成的名称.
	  	* `-p 8080:80`: 为`-p <host_port>:<container_port>`, 将容器的端口publish到主机系统的端口, 这里是主机8080端口的数据都会转发到容器内的80端口.
	  	* `-d`: 在后台运行容器, 并返回一个容器ID, 可以使用`docker logs smart_clock`查看日志.
	  	
	* 容器终端交互
	
		当容器启动后,可用交互式终端连接容器,可以对内部进行文件操作:
		`docker container exec -it smart_clock sh`
		
		也可以不用交互式, 如: `smart_clock`容器内创建`/usr/share/nginx/html/alert.html`文件:
		
		`docker exec -d smart_clock touch /usr/share/nginx/html/alert.html`
	
4. **存储(数据,资料)卷相关**

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


[Docker docs](https://docs.docker.com/manuals/)

[Docker Networking – Basics, Network Types & Examples](https://spacelift.io/blog/docker-networking)








