## SSH远程登录和SCP远程文件传输

### 远程登录：SSH

SSH是一种网络协议，用于计算机之间的远程登录及其他网络服务。

#### 1. 远程登录

用登录名为 username, 远程服务地址为host

		$ ssh username@host
		
如指定端口号为 2222 (默认端口号为22)：

		$ ssh -p 2222 username@host

也可以使用 -l 指定登录名

		$ ssh -l username -p 2222 host
		
#### 2. 公钥登录
如果觉得用密码账号登录特别不方便，可以试试公钥登录。

> 所谓"公钥登录"，原理很简单，就是用户将自己的公钥储存在远程主机上。登录的时候，远程主机会向用户发送一段随机字符串，用户用自己的私钥加密后，再发回来。远程主机用事先储存的公钥进行解密，如果成功，就证明用户是可信的，直接允许登录shell，不再要求密码。

首先你需要用SSH生成一对密钥：

		$ ssh-keygen
		
运行上面的命令以后，系统会出现一系列提示，可以一路回车。完成之后，你应该可以在你的$HOME/.ssh/目录下看到两个文件，id_rsa就是你的私钥，而id_ras.pub则是你的公钥，现在你需要将你的公钥拷贝到服务器上，如果你的系统有ssh-copy-id命令，拷贝会很简单：

		$ ssh-copy-id username@host
		
否则，你需要手动将你的私钥拷贝的服务器上的~/.ssh/authorized_keys文件中：

		$ ssh user@host 'mkdir -p .ssh && cat >> .ssh/authorized_keys' < ~/.ssh/id_rsa.pub
		
> 上面这条命令由多个语句组成，依次分解开来看：
> 
> 1. "$ ssh user@host"，表示登录远程主机；
> 2. 单引号中的mkdir .ssh && cat >> .ssh/authorized_keys，表示登录后在远程shell上执行的命令：
> 3. "$ mkdir -p .ssh"的作用是，如果用户主目录中的.ssh目录不存在，就创建一个；
> 4. 'cat >> .ssh/authorized_keys' < ~/.ssh/id_rsa.pub的作用是，将本地的公钥文件~/.ssh/id_rsa.pub，重定向追加到远程文件authorized_keys的末尾。
> 
> #### *参考资料*

> [SSH原理与运用（一）：远程登录](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html "一些简单的SSH基础")

> [16 条技巧让你更高效使用 SSH](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html "很COOL 但讲的不是很清晰SSH用法")

<br/>

### 远程文件传输命令 ： SCP

scp是secure copy的简写，用于在Linux下进行远程拷贝文件的命令，和它类似的命令有cp，不过cp只是在本机进行拷贝不能跨服务器，而且scp传输是加密的。
> 1．命令格式：
> 
> scp [参数] [原路径] [目标路径]

#### 复制文件
##### 从本地复制到远程服务器
使用用户名username的授权，将本地桌面上的mainfest.plist文件复制到 198.168.4.85 的/home/wwwroot/common/mainfest.plist目录下面。

`$ scp /Users/stoull/Desktop/LinkBox/mainfest.plist username@198.168.4.85:/home/wwwroot/common/mainfest.plist`

##### 从远程服务器复制到本地
如果要将远程的mainfest.plist文件复制到本地桌面，只要把两个参数对换即可

`$ scp username@198.168.4.85:/home/wwwroot/common/mainfest.plist /Users/stoull/Desktop/LinkBox/mainfest.plist`

##### 指定端口
`$ scp -P 333333 /Users/stoull/Desktop/LinkBox/mainfest.plist username@198.168.4.85:/home/wwwroot/common/mainfest.plist`

#### 复制目录
复制目录 加参数 -r (递归复制整个目录)
`$ scp /Users/stoull/Desktop/LinkBox/ username@198.168.4.85:/home/wwwroot/common/LinkBox`

#### 参数详细说明

> 1．命令格式：
> 
> scp [参数] [原路径] [目标路径]
>
>命令参数：
>
-1  强制scp命令使用协议ssh1  
-2  强制scp命令使用协议ssh2  
-4  强制scp命令只使用IPv4寻址  
-6  强制scp命令只使用IPv6寻址  
-B  使用批处理模式（传输过程中不询问传输口令或短语）  
-C  允许压缩。（将-C标志传递给ssh，从而打开压缩功能）  
-p 保留原文件的修改时间，访问时间和访问权限。  
-q  不显示传输进度条。  
-r  递归复制整个目录。  
-v 详细方式显示输出。scp和ssh(1)会显示出整个过程的调试信息。这些信息用于调试连接，验证和配置问题。   
-c cipher  以cipher将数据传输进行加密，这个选项将直接传递给ssh。   
-F ssh_config  指定一个替代的ssh配置文件，此参数直接传递给ssh。  
-i identity_file  从指定文件中读取传输时使用的密钥文件，此参数直接传递给ssh。    
-l limit  限定用户所能使用的带宽，以Kbit/s为单位。     
-o ssh_option  如果习惯于使用ssh_config(5)中的参数传递方式，   
-P port  注意是大写的P, port是指定数据传输用到的端口号   
-S program  指定加密传输时所使用的程序。此程序必须能够理解ssh(1)的选项。

