#iperf3网络测速


### netstat

```
brew install iperf3 # MacOS
sudo apt install iperf3 # Ubuntu
sudo yum install iperf3 # CentOS
```

注意端口占用：5201

由于这种测速是测两台机器之间的网速，我们需要部署两个点，一台用来当做服务器，另一台用来当做客户端。

* 服务端：`iperf3 -s` （或者 `iperf3 -p <port> -s`）;
* 客户端：`iperf3 -c <server-address>`（或者 `iperf3 -p <port> -c <server-address>`）;

#### netstat

`netstat [-acCeFghilMnNoprstuvVwx][-A<网络类型>][--ip]`

`netstat -a` : 列出所有端口


[网络测速工具 iperf](https://blog.xizhibei.me/2020/01/13/speed-test-tool-iperf/)

[netstat命令](https://www.cnblogs.com/peida/archive/2013/03/08/2949194.html)