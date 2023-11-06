# Nginx Basic

Nginx ("engine x") 是一个高性能的 HTTP 和 反向代理 服务器，也是一个 IMAP/POP3/SMTP 代理服务器。 Nginx 是由 Igor Sysoev 为俄罗斯访问量第二的 Rambler.ru 站点开发的，第一个公开版本0.1.0发布于2004年10月4日。其将源代码以类BSD许可证的形式发布，因它的稳定性、丰富的功能集、示例配置文件和低系统资源的消耗而闻名。

Nginx 解决了服务器的C10K（就是在一秒之内连接客户端的数目为10k即1万）问题。它的设计不像传统的服务器那样使用线程处理请求，而是一个更加高级的机制—事件驱动机制，是一种异步事件驱动结构。它可以轻松在百万并发连接下实现高吞吐量的Web服务，同时诸多应用场景下的问题都可以通过种种Nginx模块得以解决，而我们所需的工作量也并不大。

### Why Nginx

- 缓存及分配request
- 负载均衡，多服务器的负载均衡，同一机器的多服务
- 安全, 反向代理
- SSL,处理对外ssl加密，多服务器统一的https加密出口
- 对responses数据的压缩
- Nginx可代替Python处理静态文件的请求，可提高性能
- 热部署，即更改配置文件后，不需要停止服务，也可使新的配置生效
- 与Nginx类似的服务Apache

## 安装Nginx

mac上：`brew install nginx`

Debian上: `sudo apt install nginx` 或者：

`sudo apt-get update`

`sudo apt-get install nginx`

CentOS: `sudo yum install nginx` 或者：`sudo dnf install nginx`

运行: `nginx` ,终端无任何输出则为成功开启服务。并在浏览器上访问`http://localhost:8080`即可看到nginx服务
>
nginx目录为：`/usr/local/etc/nginx`
>
配置文件: cd /usr/local/etc/nginx/nginx.conf
>
nginx命令，在终端没有输出则是最好的结果，表示成功执行

可使用`ps -ef | grep nginx`命令查看进程内容

```
$ ps -ef | grep nginx
root      160967       1  0 07:51 ?        00:00:00 nginx: master process nginx
nginx     160968  160967  0 07:51 ?        00:00:00 nginx: worker process
ec2-user  160970  133420  0 07:51 pts/0    00:00:00 grep --color=auto nginx
```

## Nginx服务控制

* `nginx -h`: 显示帮助栏
* `nginx -t`: 测试nginx设置文件是否正确

当nginx启动后，可以使用`nginx -s signal`进行控制，`signal`有如下参数：

* `nginx -s stop` — fast shutdown
* `nginx -s quit` — graceful shutdown
* `nginx -s reload` — reloading the configuration file, will not in interrupted the server
* `nginx -s reopen` — reopening the log files

如停止nginx服务：`nginx -s quit`, 重新载入: `nginx -s reload`

也可以使用`systemctl`进行管理：

>
`sudo systemctl stop nginx` : 停止服务
>
`sudo systemctl start nginx`: 开启服务
>
`sudo systemctl restart nginx`: 重新启动服务
>
`sudo systemctl reload nginx`: 重新载入服务, 不需要停止ngin服务，不需要中断请求
>
`sudo systemctl disable nginx` : 禁止开机自动启动
>
`sudo systemctl disable nginx` : 启用开机自动启动


## Nginx服务文件结构

### 可执行文件
`/usr/local/bin/nginx`

### Content
* `/var/www/*.html`: Nginx服务的静态资源存放目录。刚安装有 `index.html`访问成功及`50x.html`访问失败等默认文件。此目录可使用配置文件更改到别处。

### Server Configuration

* `/etc/nginx`: Nginx服务的配置目录，所有配置文件都在此目录下
* `/etc/nginx/nginx.conf`: 主要的nginx配置文件，配置nginx的全局配置。主要学习点
* `/etc/nginx/conf.d/`: nginx服服务配置文件，一般于nginx.conf引用
* `/etc/nginx/sites-available/`: 这个目录存储每一个网站的"server blocks"。nginx通常不会使用这些配置，除非它们陪连接到 sites-enabled 目录 (see below)。一般所有的server block 配置都在这个目录中设置，然后软连接到别的目录 。
* `/etc/nginx/sites-enabled/`: 存放的是当前启用的网站配置文件的符号链接。也就是说，sites-enabled中存放的配置文件是实际生效的配置文件。
* `/etc/nginx/snippets`: 这个目录主要可以包含在其它nginx配置文件中的配置片段。重复的配置都可以重构为配置片段。
* `/etc/nginx/mime.types`: 记录的是HTTP协议中的Content-Type的值和文件后缀名的对应关系
* `/etc/nginx/ koi-utf、koi-win、win-utf`: 这三个文件都是与编码转换映射相关的配置文件，用来将一种编码转换成另一种编码
* `/etc/nginx/*.default`: 均为对应参数的备份文件 

>`/etc/nginx/conf.d/`: 全局服务文件
>`/etc/nginx/sites-enabled/`: 如支持多个网站，每个网站服务可单独定义一配置文件，方便管理。一般先写入`/etc/nginx/sites-available/`文件

### Server Logs

* `/var/log/nginx/access.log`: 每一个访问请求都会记录在这个文件中，除非你做了其它设置
* `/var/log/nginx/error.log`: 任何Nginx的错误信息都会记录到这个文件中


测试配置文件：`sudo nginx -t`

## Nginx配置文件`nginx.conf`

配置文件结构

```
# 全局区
user nginx
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
...
              
# events块
events {
	worker_connections 768;
	# multi_accept on;   
   ...
}

# http块
http      
{
    # http全局块
    	include /etc/nginx/mime.types;
	default_type application/octet-stream;
	
	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;
	
    ...   
    # 虚拟主机server块
    server        
    { 
        # server全局块
        	listen 80 default_server; # 处理没有匹配到server的请求
		listen [::]:80 default_server;
        ...       
        # location块
        location [PATTERN]   
        {
        	location = /.well-known {
				root /var/www/.well-known/;
			}
            ...
        }
        location [PATTERN] 
        {
            ...
        }
    }
    
    # 虚拟主机server块
    server
    {
      ...
    }
    
    # http全局块
    	 include /etc/nginx/conf.d/*.conf;
	 include /etc/nginx/sites-enabled/*;
    ...     
}
```

说明：

* **全局区** : nginx配置全局定义区。一般有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，配置文件引入，允许生成worker process数等。
* **events块** : 配置影响nginx服务器或与用户的网络连接。有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，是否允许同时接受多个网路连接，开启多个网络连接序列化等。
* **http块** : 可以嵌套多个server，配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，连接超时时间，单连接请求数等。
* **server块 **:  配置虚拟主机的相关参数，一个http中可以有多个server。

> 虚拟主机server可分离出主配置文件，常在文件`/etc/nginx/conf.d/*.conf`,`/etc/nginx/sites-enabled/*`中配置

* **location块** : 配置请求的路由，以及各种页面的处理情况。

[NGINX-Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html)

[Nginx中文文档](https://blog.redis.com.cn/doc/)

[Nginx学习笔记 -初识Nginx](https://www.cnblogs.com/FLY_DREAM/p/14265110.html)

[Nginx 基本配置详解](https://zhuanlan.zhihu.com/p/24524057?refer=wxyyxc1992)

[NGINX Basics and Best Practices](https://www.nginx.com/c/nginx-basics-and-best-practices/)