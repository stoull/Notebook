## 根据请求`User-Agent`判定平台

### [User-Agent格式](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)：

`Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>`

### 可根据`system-information`判定苹果平台：

`iPhone`	- 苹果手机

`iPad`	- 苹果iPad平板电脑

`Macintosh`	- 苹果电脑

`iPhone OS` - 苹果手机

`Mac OS`	- 苹果电脑

`like Mac OS`	- 苹果除电脑外的设备

### 实际测试数据
#### Mac Safari:
>
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15

####Mac Google Chrome:
>
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36

####iPhone Safari:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1

####iPhone 微信:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.25(0x1800192b) NetType/WIFI Language/zh_CN

####iPhone Firefox:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1

####iPhone Chrome:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/105.0.5195.147 Mobile/15E148 Safari/604.1

####iPhone Edge:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/105.0.1343.47 Version/15.0 Mobile/15E148 Safari/604.1

####iPhone QQ浏览器:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 MQQBrowser/13.1.6 Mobile/15E148 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1

####iPhone Opera:
>
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 OPT/3.3.6

####iPhone DuckDuckGo:
Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 DuckDuckGo/7 Safari/605.1.15

### 安卓设备
####小米手机系统浏览器：
>
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/79.0.3945.147 Safari/534.24 XiaoMi/MiuiBrowser/13.6.15

### 查看设备的`User-Agent`:
可以访问下面内网地址查看对应的设备的[`User-Agent`](http://20.6.1.128:5000/User-Agent):

`http://20.6.1.128:5000/User-Agent`