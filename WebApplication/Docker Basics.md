# Docker Basics


## 安装


## node hello world

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

## nginx示例

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

[How to create a static web server for HTML with NGINX](https://thatdevopsguy.medium.com/how-to-create-a-static-web-server-for-html-with-nginx-99bf8226bce6)
