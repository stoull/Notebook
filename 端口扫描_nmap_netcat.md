

nmap (“Network Mapper”)是一个用于网络探测和安全审核的开源工具。如果 nmap 没有安装或者你不希望使用 nmap，那你可以用 netcat/nc 命令进行端口扫描。它对于查看目标计算机上哪些端口是开放的或者运行着服务是非常有用的。你也可以使用 nmap 命令进行端口扫描。

如果没有安装 nmap 使用 netcat 进行端口扫描：

##netcat 语法
>-z 参数用来告诉 nc 报告开放的端口，而不是启动连接。在 nc 命令中使用 -z 参数时，你需要在主机名/ip 后面限定端口的范围和加速其运行：
>
>参数说明：
>
* -z：端口扫描模式即零 I/O 模式。
* -v：显示详细信息 [使用 -vv 来输出更详细的信息]。
* -n：使用纯数字 IP 地址，即不用 DNS 来解析 IP 地址。
* -w 1：设置超时值设置为1。

```
nc -z -v {host-name-here} {port-range-here} 
nc -z -v host-name-here ssh 
nc -z -v host-name-here 22 
nc -w 1 -z -v server-name-here port-Number-her 
### 扫描 1 to 1023 端口 ### 
nc -zv vip-1.vsnl.nixcraft.in 1-1023 
```
输出示例：

```
linkapps-Mac:ss stoull$ nc -z -v app.xxx.cn 212
found 0 associations
found 1 connections:
     1:	flags=82<CONNECTED,PREFERRED>
	outif en0
	src 192.168.4.122 port 52627
	dst 120.23.237.15 port 22222
	rank info not available
	TCP aux info available

Connection to app.xxx.cn port 212 [tcp/*] succeeded!
```

扫描特定端口：

```
nc -zv v.txvip1 443 
nc -zv v.txvip1 80 
nc -zv v.txvip1 22 
nc -zv v.txvip1 21 
nc -zv v.txvip1 smtp 
nc -zvn v.txvip1 ftp 
##使用1秒的超时值来更快的扫描
netcat -v -z -n -w 1 v.txvip1 1-1023 
```

******

##nmap 语法

如果没有安装 nmap 使用下面的命令安装：
	
	brew nmap
	
Nmap介绍:
>Nmap是一款用于网络发现和安全审计的安全工具，常用于端口扫描。
>
>用法： nmap [扫描类型] [参数] 目标IP　　　

```
　　1. 扫描类型
　　　　-sT　　TCP 连接扫描，会在目标主机中记录大量的链接请求和错误信息
　　　　-sS　　SYN扫描，只完成三次握手前两次，很少有系统记入日志，默认使用，需要root(admin)权限
　　　　-sP　　Ping扫描，默认使用，只有能Ping得通才会继续扫描
　　　　-P0　　扫描之前不需要Ping，用于绕过防火墙禁Ping功能
　　　　-sA　　高级的扫描方式，用来穿过防火墙的规则集
　　　　-sV　　探测端口号版本　
　　　　-sU　　UDP扫描，扫描主机开启的UDP的服务，速度慢，结果不可靠　
　　　　-sX -sN 　　秘密的FIN数据包扫描，圣诞树(Xmas Tree)和空模式，针对Unix和Linux主机，系统要求遵循TCP RFC文档

　　2. 扫描参数
　　　　-v　　显示扫描过程，推荐使用
　　　　-h　　帮助文档
　　　　-p　　指定端口号，如[1-65535],[22,135,1433,3306,]等格式
　　　　-O　　启动远程操作系统监测，存在误报
　　　　-A　　全面系统监测，使用脚本检测，扫描等
　　　　-T4　 针对TCP端口禁止动态扫描延迟超过10ms
　　　　-iL　　批量扫描，读取主机列表，如[-iL  C:\ip.txt]
```
扫描案例:

* 扫描C段（局域网）存活主机

```
nmap -sP www.XXX.com/24
nmap -sP 192.168.1.*  （注释：“*”为通配符）
```

* 扫描指定IP开放端口号

```
nmap -sS -p- -v 192.168.1.100
　　　　-p-为全端口扫描，和[1-65535]一样，建议使用
不使用默认Nmap认为危险的100个端口号
```

* 扫描指定IP所开端口及服务版本

```
nmap -sV -v 192.168.1.100
```


* 探测主机操作系统

```
nmap -O www.XXX.com

扫描准确度以百分比显示，未必准确
```


* 穿透防火墙扫描

```
nmap -P0  www.XXX.com
```


* 全面探测，-A包含OS 探测，版本探测，脚本扫描，traceroute

```
nmap -A www.XXX.com
```

* 使用脚本扫描，

```
nmap --script="脚本名称" www.XXX.com
如在局域网上扫找 Conficker 蠕虫病毒
nmap -PN -T4 -p139,445 -n -v --script=smb-check-vulns --script-args safe=1 192.168.0.1-254
脚本放在Nmap安装目录script下，官网可查各个脚本功能
```


[参考这个 nmap端口扫描技术](https://nmap.org/man/zh/man-port-scanning-techniques.html 'nmap端口扫描技术')

[nmap 的高级用法](http://metasploit.lofter.com/post/d9d60_2596ae)

