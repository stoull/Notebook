# Mac 实用工具


#### 定时关机

`shutdown -h +120` 	// 两个小时后关机

#### 查看系统日志
日志目录：`/var/log/`

#### 查看用`dmg`安装的包信息

`pkgutil --pkgs`	// List all currently installed package IDs on --volume
`pkgutil --pkg-info com.tec.pkg.agent`

查看包文件

`pkgutil --lsbom com.tec.pkg.agent`

`pkgutil --files com.tec.pkg.agent` or `pkgutil --files com.tec.pkg.agent | less`

查看系统安装软件记录: `/var/log/install.log`


ip-guard: 目录

/usr/local/OCularApp

/Users/OcularApp/Agt4Chk.app

/usr/local/.OCular


[ip-guard](http://www.ip-guard.net/en/index.html)

[电脑总是弹出“TEC Guangzhou Solutions Limited"的系统扩展](https://discussionschinese.apple.com/thread/253457485)

[IPGUARD Agt4Chk LSDHelper.app LAgent LAgentUser 方法](https://www.jianshu.com/p/a3c8e984cde5)