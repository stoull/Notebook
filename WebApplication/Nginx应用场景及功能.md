# Nginx应用场景及功能


## 静态HTTP服务器

```
# html服务
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	
	server_name www.domain.com
	
    	location / {
    		index index.html;
        	root /var/www;
        	try_files $uri $uri/ =404;
    	}
}

# 图片服务
server {
	listen 80;
	listen [::]:80;
	
	root /var/www;
	
    	# 请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
    	location ~* \.(gif|jpg|png)$ {
    		root /data/images;
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


[What are some common use cases for NGINX?](https://medium.com/@teeppiphat/nginx-and-use-cases-8ced7e2d80dc)