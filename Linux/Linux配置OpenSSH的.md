# OpenSSH的使用

SSH (Secure Shell)是一种协议，它使用客户端-服务器架构促进两个系统之间的安全通信，并允许用户远程登录服务器主机系统。与其他远程通信协议（如 FTP 或 Telnet ）不同，SSH 对登录会话进行加密，使得入侵者很难收集未加密的密码。

ssh 程序旨在替换用于登录远程主机（如 telnet 或 rsh ）的旧、不太安全的终端应用。名为 scp 的相关程序 取代了设计用于在主机之间复制文件的旧程序，如 rcp。由于这些较旧的应用程序不会加密客户端和服务器之间传输的密码，因此尽可能避免这些密码。使用安全方法登录远程系统可降低客户端系统和远程主机的风险。

### ssh主要功能

* 防止数据被拦截, 防止捕获密钥信息
* 防止IP欺骗，模拟特定的主机

### SSH连接的过程

以下一系列事件有助于保护两个主机之间的 SSH 通信的完整性。

1. 制作加密握手，以便客户端能够验证它是否与正确的服务器通信。
2. 客户端和远程主机之间的连接传输层使用对称密码进行加密。
3. 客户端向服务器验证自身。
4. 客户端通过加密连接与远程主机交互。

传输层构建了一个安全隧道以在两个系统之间传递信息后，服务器会告知客户端支持的不同身份验证方法，例如使用私钥编码签名或输入密码。然后，客户端尝试使用以下任一支持的方法对服务器进行身份验证。

在 SSH 传输层成功验证后，可以通过称为多路复用的技术打开多个通道[1].这些通道各自处理不同终端会话和转发 X11 会话的通信。

## 配置文件


配置文件主要有服务端和客户端的配置文件

**系统范围的配置文件：**

| 文件 | 描述 | 备注 |
| ---- | ------- | --- |
|`/etc/ssh/ssh_config`|默认的 SSH 客户端配置文件。请注意，如果 ~/.ssh/config 存在，它将被 ~/.ssh/config 覆盖。| --- |
|`/etc/ssh/sshd_config`|sshd 守护进程的配置文件。| --- |
|`/etc/ssh/ssh_host_ecdsa_key`|sshd 守护进程使用的 ECDSA 私钥。| --- |
|`/etc/ssh/ssh_host_ecdsa_key.pub`|sshd 守护进程使用的 ECDSA 公钥。| --- |
|`/etc/ssh/ssh_host_rsa_key`|sshd 守护进程用于 SSH 协议版本 2 的 RSA 私钥。| --- |
|`/etc/ssh/ssh_host_rsa_key.pub`|sshd 守护进程用于 SSH 协议版本 2 的 RSA 公钥。| --- |
|`/etc/pam.d/sshd`|sshd 守护进程的 PAM 配置文件。| --- |
|`/etc/sysconfig/sshd`|sshd 服务的配置文件。| --- |

**用户特定配置文件：**

| 文件 | 描述 | 备注 |
| ---- | ------- | --- |
|`~/.ssh/authorized_keys`|保存服务器的授权公钥列表。当客户端连接到服务器时，服务器通过检查存储在此文件中的签名公钥来验证客户端的身份验证。| --- |
|`~/.ssh/id_ecdsa`|包含用户的 ECDSA 私钥。| --- |
|`~/.ssh/id_ecdsa.pub`|用户的 ECDSA 公钥.| --- |
|`~/.ssh/id_rsa`|ssh 用于 SSH 协议版本 2 的 RSA 私钥。| --- |
|`~/.ssh/id_rsa.pub`|ssh 用于 SSH 协议版本 2 的 RSA 公钥。| --- |
|`~/.ssh/known_hosts`|包含用户访问的 SSH 服务器的主机密钥。此文件对于确保 SSH 客户端连接到正确的 SSH 服务器非常重要。| --- |


## OpenSSH 服务管理

* `systemctl start sshd.service`: 启动服务
* `systemctl stop sshd.service`: 停止服务
* `systemctl enable sshd.service`: 开机启动服务


### 配置密钥对

* ssh key的类型有四种，分别是dsa、rsa、 ecdsa、ed25519。
根据数学特性，这四种类型又可以分为两大类，dsa/rsa是一类，ecdsa/ed25519是一类，后者算法更先进。
* ecdsa因为政治原因和技术原因，也不推荐使用。dsa因为安全问题，已不再使用了。
* rsa是目前兼容性最好的，应用最广泛的key类型，在用ssh-keygen工具生成key的时候，默认使用的也是这种类型。不过在生成key时，如果指定的key size太小的话，也是有安全问题的，推荐key size是3072或更大。
* ed25519是目前最安全、加解密速度最快的key类型，由于其数学特性，它的key的长度比rsa小很多，优先推荐使用。它目前唯一的问题就是兼容性，即在旧版本的ssh工具集中可能无法使用。不过据我目前测试，还没有发现此类问题。

SSH客户端默认查找顺序(如没有指定路径)：

1. `~/.ssh/id_rsa`
2. `~/.ssh/id_dsa`
3. `~/.ssh/id_ecdsa`
4. `~/.ssh/id_ed25519`

#### 配置密钥对进行登录的一般流程为：

1. 本地生成密钥对
	* 私钥：`~/.ssh/id_rsa` 或者 `~/.ssh/id_ed25519`
	* 公钥：`~/.ssh/id_rsa.pub` 或者 `~/.ssh/id_ed25519.pub`
2. 将公钥上传到服务器的文件`~/.ssh/authorized_keys`中
3. 确认公私钥存储文件的权限



### 生成密钥对

`ssh-keygen -t ed25519 -C "your_email@example.com"`

If you are using a legacy system that doesn't support the Ed25519 algorithm, use:
`ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

生成的密钥对将存储到`~/.ssh/`目录下,`~/.ssh/id_ed25519`和 `~/.ssh/id_ed25519.pub`文件

#### 将生成的密钥对，添加到客户端及服务端:

1. Start the ssh-agent in the background.
	- `eval "$(ssh-agent -s)"`
2. Add your SSH private key to the ssh-agent.
	- `ssh-add ~/.ssh/id_ed25519` 
3. 将公钥添加到服务器
	- 方法1：手动复制
		* `cat ~/.ssh/id_rsa.pub` 然后复制到 `echo "xxxx" >> ~/.ssh/authorized_keys`文件中，或者`cat path/to/id_rsa.pub >> ~/.ssh/authorize`
	- 方法2：使用ssh-copy-id
		* `ssh-copy-id user@remote-server`: 将复制最新修改的 ~/.ssh/id*.pub 公钥到对应服务器~/.ssh/authorize中, 需要登录密码
		* `ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname`：需要登录密码
3. 配置客户端的ssh连接
	* 使用非默认路径的私钥
		- `touch ~/.ssh/config`
		- 保存如下配置
		
		
			```
			Host:		hostName的别名
			HostName: 	是目标主机的主机名，也就是平时我们使用ssh后面跟的地址名称。
			Port：		指定的端口号。
			User：		指定的登陆用户名。
			IdentifyFile：指定的私钥地址。
			```
			示例配置文件：
			
			```
			Host youhost.com
				HostName ahut.site
				Port 31800
				User hut
			  	AddKeysToAgent yes
			  	UseKeychain yes
			  	IdentityFile /Users/hut/Auth/AWS/xxxx.pem
			```

### 服务器权限配置

* `chmod 700 ~/.ssh`

* `chmod 600 ~/.ssh/authorized_keys`


[Red Hat Enterprise Linux - 系统管理员指南 - 第12章 OpenSSH](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-openssh)


[Red Hat Enterprise Linux - 系统管理员指南](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/7/html/system_administrators_guide/index)
