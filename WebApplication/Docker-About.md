# Docker入门使用

## Installation 

### Debian

* 1. Set up Docker's apt repository.

```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

* Install the Docker packages.

安装最新版本：`sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

安装指定版本：

List the available versions: 

`apt-cache madison docker-ce | awk '{ print $3 }'`
	
Select the desired version and install:
	
```
VERSION_STRING=5:24.0.0-1~debian.11~bullseye
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```

* 3. sudo docker run hello-world

`sudo docker run hello-world`

详见官文：[Install Docker Engine](https://docs.docker.com/engine/install/)

## Docker Desktop

## Docker CLI



[Use the Docker command line docker](https://docs.docker.com/engine/reference/commandline/cli/)

## 问题

#### 

```
WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
exec /usr/local/bin/docker-entrypoint.sh: exec format error
```

[A step-by-step guide to create Dockerfile](https://medium.com/@anshita.bhasin/a-step-by-step-guide-to-create-dockerfile-9e3744d38d11)

[Docker之一----基础介绍和命令详解](https://www.cnblogs.com/struggle-1216/p/12187586.html)




















