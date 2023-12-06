# Nginx应用场景及功能

[nginx uri 如何匹配 location 规则](https://www.cnblogs.com/dreamanddead/p/how-uri-match-location-rule-in-nginx.html)

## 静态HTTP服务器

```
server {
	# html服务
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		root /var/www/html;
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
}

server {
	# 图片服务
	listen 8080;
	listen [::]:8080;
	
	root /var/www/data/images;

	# 请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
	location ~* \.(gif|jpg|png)$ {
		try_files $uri $uri/ =502;
	}
	
    location ~* \.(gif|jpg|png)$ {
		expires 30d;
    	add_header Vary Accept-Encoding;
      	access_log off;
	}
}
```

* `listen 80 default_server;`: 配置监听端口及服务, `default_server`，定义此服务为默认的 server，处理一些没有匹配到 server_name 的请求。
* `server_name www.domain.com`：定义此服务只处理www.domain.com的请求
* `location`: 定义路由，`http://domain.com`会返回`/var/www/index.html`文件，而`http://domain.com/*.jpg`则会在`/var/www/data/images`目录下匹配对应的图片。
* ` ~ \.(gif|jpg|png)$ `: 请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。此处仅支持gig,jpg,png格式图片的支持。
* `try_files $uri $uri/ =502;` 尝试寻找匹配 uri 的文件，没找到直接返回 404
* `expires 30d`: 缓存时间为30d

`nginx =t`: 测试配置
`nginx -s reload`: 使用配置文件生效

## 静态资源服务器

## 反向代理和负载均衡

```
upstream backend {
	ip_hash;	# 同一个客户的请求会被分配到同一个地址
	# 默认是循环，而weight是配制权重
	server 127.0.0.1:8000 weight=3;
	server 127.0.0.1:8001;
	server 127.0.0.1:8002;
}

server {
	listen		80;
	server_name	localhost;

	location /app {
	  proxy_pass http://backend
	}
}

```


## 虚拟主机
在同一个服务器上运行多个服务，在server块中，只要指定特server name和不同端口, 就可以在同同一个服务器上运行多个主机。

### 不同服务共同端口

```

# nginx 80端口配置 （监听a二级域名）
server {
    listen  80;
    server_name     a.com;
    location / {
        proxy_pass      http://localhost:8080; # 转发
    }
}

# nginx 80端口配置 （监听b二级域名）
server {
    listen  80;
    server_name     b.com;
    location / {
        proxy_pass      http://localhost:8081; # 转发
    }
```

## SSL证书

查看SSL模块是否已安装：`nginx -V`
在`configure arguments:`参数中，如有`--with-http_ssl_module`说明ssl模块已经安装
如未安装需先安装

### 上传证书

在nginx目录下新建`cert`目录用于放置证书文件,

`$cd /etc/nginx`	: `/etc/nginx`目录可能根据不同的系统会有变化
`sudo mkdir cert`: 新建目录

可使用不同工具上传证书相关的`.key`及`.pem`文件至这个目录，这里使用scp上传到用户的home目录：

```
scp /path/to/thefile.key ubuntu@xx.xx.xx.xx:~/
scp /path/to/thefile.pem ubuntu@xx.xx.xx.xx:~/
```
然后移至对应的目录

```
sudo mv ~/thefile.key /etc/nginx/cert/
sudo mv ~/thefile.pem /etc/nginx/cert/
```
### 配置文件
nginx.conf配置文件如下：

```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	# SSL configuration
	# 服务器端口使用443，开启ssl
	listen 443 ssl default_server;
	listen [::]:443 ssl default_server;

	# ssl证书地址
    	ssl_certificate     /etc/nginx/cert/onehut.site_bundle.pem;  # pem文件的路径
    	ssl_certificate_key  /etc/nginx/cert/onehut.site.key; # key文件的路径
    
    	# ssl验证相关配置
    	ssl_session_timeout  60m;    #缓存有效期
    	ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;    #加密算法
    	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;    #安全链接可选的加密协议
    	ssl_prefer_server_ciphers on;   #使用服务器端的首选算法
	
	root /var/www;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	# 域名，多个以空格分开
	server_name onehut.site www.onehut.site;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
}
```

### 重启nginx
重启前使用`sudo nginx -t`测试配置文件的正确性
`sudo nginx -s reload` 重启服务

使用https访问，通过则表示已生效。


### 参考
[Nginx 服务器 SSL 证书安装部署](https://cloud.tencent.com/document/product/400/35244)

[Module ngx_http_ssl_module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)

[What are some common use cases for NGINX?](https://medium.com/@teeppiphat/nginx-and-use-cases-8ced7e2d80dc)