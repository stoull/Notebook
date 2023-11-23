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

```
```

## 静态资源服务器

## 反向代理和负载均衡

## HTTPS配置

## 虚拟主机



[What are some common use cases for NGINX?](https://medium.com/@teeppiphat/nginx-and-use-cases-8ced7e2d80dc)