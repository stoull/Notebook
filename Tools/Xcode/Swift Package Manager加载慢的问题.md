# Swift Package Manager(SPM)加载慢的问题

在Xcode项目中添加了Package Dependencies会经常卡在 checking out 某个库上。大部分库都是github托管，国内网络原因，加上xcode无法走代理，一个下午都可能加载不出来。

解决思路就是能用各种方法，加快github的连接速度

## 方法一：使用Xcode命令行工具

在终端上走代理，通Xcode的命令行工具`xcodebuild -resolvePackageDependencies`在终端上完成SPM的加载

1. 打开代理，获取转发端口
2. 设置代理
>
```
export http_proxy=http://127.0.0.1:1087;
export https_proxy=http://127.0.0.1:1087;
export ALL_PROXY=socks5://127.0.0.1:1080
```

2. 使用xcode命令解析和更新swift packages
>
`xcodebuild -resolvePackageDependencies -scmProvider system -list -workspace XXXXX.xcworkspace`

#### 命令说明

> `-resolvePackageDependencies` resolves any Swift package dependencies referenced by the project or workspace

用法：

`xcodebuild -resolvePackageDependencies [-project <projectname>|-workspace <workspacename>] -clonedSourcePackagesDirPath <path>`

示例：

`xcodebuild -resolvePackageDependencies -scmProvider system -list -workspace XXXXX.xcworkspace`

`-scmProvider`: 强制`xcodebuild`命令使用系统的git及其配置，如果不执行这个，`xcodebuild`会使用xcode内置的git，内置的git就不会走终端的代理。

## 方法二：修改git的配置，让github走代理


* 1.设置代理

>
`git config --global https.github.com.proxy socks5://127.0.0.1:1080`

这个命令就是在git全局配置文件`~/.gitconfig`里增加了下面的配置：

```
[https "github.com"]
	proxy = socks5://127.0.0.1:1080
```

如果要撤销对应的代理，可使用下面的命令，或手动删除

`git config --global --unset https.github.com.proxy`

如果要设置所有git库的http或者https都走代理：

```
git config --global http.proxy http://0.0.0.0:1087
git config --global http.proxy socks5://0.0.0.0:1080

git config --global --get http.proxy
git config --global --get https.proxy

git config --global --unset http.proxy
git config --global --unset https.proxy
```

* 2.重新打开Xcode，加载包的速度就会好点儿




