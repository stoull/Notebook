# Linux 搭建代理服务器 - Squid

使用Squid搭建一个Web代理服务器。

[Squid](https://ubuntu.com/server/docs/proxy-servers-squid)

[Squid](https://ubuntu.com/server/docs/proxy-servers-squid)

[Squid: Optimising Web Delivery](http://www.squid-cache.org)


## CentOS based systems

CentOS 使用`yum`包管理工具

1. 更新包库
`sudo yum -y update`

2. 安装squid
`yum -y install squid`

3. 控制及查看squid
>
start it :
`$ sudo systemctl start squid`
>
automatically start squid at the time of boot:
`$ sudo systemctl enable squid`
>
view the status of your squid server:
`$ sudo systemctl status squid`
>
restart squid server:
`$ sudo systemctl restart squid`

4. 配制Squid Proxy 服务器
>
配置文件位置为：`/etc/squid/squid.conf`
>
`http_port 3128` 代理监听端口为3128, 注意防火墙打开这个端口。
`http_port 3128 transparent` transparent 为对request及response不作处理(未隐藏ip)

5. Access Control List (ACL) 限制ip访问
>
`acl localnet src 54.43.32.21` 允许ip为54.43.32.21的访问
`acl localnet src 54.43.32.21/24` 允许ip组的访问
>
> 其它的一些特殊ip
>
`acl localnet src 10.0.0.0/8	# RFC1918 possible internal network`
`acl localnet src 172.16.0.0/12	# RFC1918 possible internal network`
`acl localnet src 192.168.0.0/16	# RFC1918 possible internal network`
`acl localnet src fc00::/7		# RFC 4193 local private network range`
`acl localnet src fe80::/10	# 4291 link-local(directly plugged) machines`
>
test proxy:
`curl -x http://<squid-proxy-server-IP>:3128 -L http://www.google.com`

6. 使用`httpd-tools`设置基本的授权访问:

>
 * 安装`httpd-tools` : `yum -y install httpd-tools`
 * 安装完后，新建配置文件：`sudo touch /etc/squid/passwd && chown squid /etc/squid/passwd`
 * 新建用户： `htpasswd /etc/squid/passwd user_name`
 * Squid配置授权配置：`sudo vi /etc/squid/squid.conf`
 * 加入以下行：
```
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```
 * 重启服务：
`sudo systemctl restart squid`

[How to Install & Configure Squid Proxy Server in Centos 7](https://fedingo.com/how-to-install-configure-squid-proxy-server-in-centos-7/)

[How To Setup and Configure a Proxy Server – Squid Proxy](https://devopscube.com/setup-and-configure-proxy-server/)

## Debian based systems

## Squid Proxy Logs

`/var/log/squid/access.log:`

`/var/log/squid/cache.log:`

`/var/log/squid/store.log:`

使用命令查看：

`sudo tail /var/log/squid/access.log`

结果如下：


```
1691112128.537  28823 156.236.96.172 TCP_TUNNEL/200 139024 CONNECT img9.doubanio.com:443 - HIER_DIRECT/43.152.2.154 -
1691112128.537  40313 156.236.96.172 TCP_TUNNEL/200 156598 CONNECT img9.doubanio.com:443 - HIER_DIRECT/43.152.2.154 -
1691116334.800   3903 156.236.96.172 TCP_TUNNEL/200 5834 CONNECT httpbin.org:443 - HIER_DIRECT/100.26.90.23 -
1691116817.693   4076 156.236.96.172 TCP_TUNNEL/200 5834 CONNECT httpbin.org:443 - HIER_DIRECT/100.26.90.23 -
```

第一栏为时间，不太好人类阅读：

#！##@¥#@#@@3

可以在`squid.conf`更改log格式：

```
logformat denniswave [%{%Y/%m/%d %H:%M:%S}tl] %>a %Ss:%Sh "%rm %ru HTTP/%rv" %Hs %<st "%{Referer}>h" "%{User-Agent}>h" %ui %un
access_log /usr/local/squid/logs/access.log denniswave
那 aceess log 就會變成這樣：
[2009/10/27 13:24:40] 192.168.51.37 TCP_MISS:DIRECT "GET http://ad.yieldmanager.com/st? HTTP/1.1" 200 6128 "http://tw.mc729.mail.yahoo.com/mc/md.php?en=BIG5-HKSCS" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)" - -
```

```
cat access.log|gawk '{print $4}'|sort|uniq -c|sort -nr
```

[Squid 記錄檔-access.log](https://article.denniswave.com/6307/)

[Squid Web Cache wiki](https://wiki.squid-cache.org/Features/LogFormat)