# Mac 实用工具

#### 更改图片大小
`sips -Z 640 *.jpg`

>sips is the command being used and -Z tells it to maintain the image's aspect ratio. "640" is the maximum height and width to be used and "*.jpg" instructs your computer to downsize every image ending in .jpg. It's really simple and shrinks your images very quickly. Be sure to make a copy first if you want to preserve their larger size as well.

保存原图，将处理后的图片输出到文件夹`resized`:

`mkdir -p resized && sips -Z 640 *.jpg --out resized/`

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

#### 列出brew安装path
`brew --cellar`

- Run these two commands in your terminal to add Homebrew to your PATH:
    ```(echo; echo 'eval "$(/usr/local/bin/brew shellenv)"') >> /Users/kevin/.zprofile```
    ```eval "$(/usr/local/bin/brew shellenv)"```

ip-guard: 目录 a

/usr/local/OCularApp

/Users/OcularApp/Agt4Chk.app

/usr/local/.OCular

[ip-guard Frequently Asked Questions](http://ip-guard.com/support/faq)

[ip-guard](http://www.ip-guard.net/en/index.html)

[强制删除IP-GUARD的MAC客户端](https://www.sophistwy.com/2019/07/01/强制删除IP-GUARD的MAC客户端LAGENT/)

[电脑总是弹出“TEC Guangzhou Solutions Limited"的系统扩展](https://discussionschinese.apple.com/thread/253457485)

[IPGUARD Agt4Chk LSDHelper.app LAgent LAgentUser 方法](https://www.jianshu.com/p/a3c8e984cde5)