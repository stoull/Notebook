# Nginx问题记录

### 运行时的root问题
当安装好nginx，运行nginx报错：

```
$ nginx
nginx: [alert] could not open error log file: open() "/var/log/nginx/error.log" failed (13: Permission denied)
2023/10/31 01:39:50 [warn] 194413#194413: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:5
2023/10/31 01:39:50 [emerg] 194413#194413: mkdir() "/var/lib/nginx/tmp/client_body" failed (13: Permission denied)
```

当使用`sudo nginx`运行时：

```
$ sudo nginx
$ ps -ef | grep nginx
root      194703       1  0 01:48 ?        00:00:00 nginx: master process nginx
nginx     194704  194703  0 01:48 ?        00:00:00 nginx: worker process
```
可见使用`root`用户运行`master process`，使用`nginx`用户运行`worker process`

在配置文件`/etc/nginx/nginx.conf`中第一行为：

`user nginx;`

在Debian系统中不指定是使用`www-data`用户

即表示nginx服务使用用户`nginx`运行。需要创建nginx用户并让它有资源目录根目录的权限。

这样运行nginx，只在master process运行在root环境下，因为只有 root processes 可以监听1024以下的端口，像80/443.

>The main purpose of the master process is to read and evaluate configuration files, as well as maintain the worker processes.
>
The worker processes do the actual processing of requests.
>
[NGINX Document - Master and Worker Processes](https://docs.nginx.com/nginx/admin-guide/basic-functionality/runtime-control/#master-and-worker-processes)

如果要让master process使用非root用户运行:

更改Nginx目录下下面文件的所属关系：

* error_log
* access_log
* pid
* client_body_temp_path
* fastcgi_temp_path
* proxy_temp_path
* scgi_temp_path
* uwsgi_temp_path

更改监听的端口号为1024上，如8080. 登录为对应的nginx用户，运行`nginx -c /path/to/nginx.conf`

[Running Nginx as non root user](https://stackoverflow.com/questions/42329261/running-nginx-as-non-root-user)


### server问题

一个server只能监听一个端口

### alias 匹配问题

 * root的处理结果是：root路径＋url中的location路径
 * alias的处理结果是：使用alias路径替换location路径
 * alias是一个目录别名的定义，root则是最上层目录的定义。
 * 还有一个重要的区别是alias后面必须要用“/”结束，否则会找不到文件的。。。而root则可有可无~~

例：

```
location /images/ {
        alias /var/www/data/images/;
        expires 30d;
        add_header Vary Accept-Encoding;
        access_log off;
}
```

请求url: `http://hut.local/images/icon_cow.jpg`。将会使用`/var/www/data/images/`完全替换`/images/`得到file path: `/var/www/data/images/icon_cow.jpg`











