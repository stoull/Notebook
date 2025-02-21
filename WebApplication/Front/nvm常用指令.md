# nvm常用指令

nvm：node 版本管理器，也就是说：一个 nvm 可以管理多个 node 版本（包含 npm 与 npx），可以方便快捷的 安装、切换 不同版本的 node。

## 安装

* brew: `brew install nvm`
* official: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash`
	最新版本及详情见：[nvm - official README](https://github.com/nvm-sh/nvm/blob/master/README.md)


## 常用示例指令

```
nvm install 8.0.0                     Install a specific version number
nvm use 8.0                           Use the latest available 8.0.x release
nvm run 6.10.3 app.js                 Run app.js using node 6.10.3
nvm exec 4.8.3 node app.js            Run `node app.js` with the PATH pointing to node 4.8.3
nvm alias default 8.1.0               Set default node version on a shell
nvm alias default node                Always default to the latest available node version on a shell

nvm install node                      Install the latest available version
nvm use node                          Use the latest version
nvm install --lts                     Install the latest LTS version
nvm use --lts                         Use the latest LTS version

nvm set-colors cgYmW                  Set text colors to cyan, green, bold yellow, magenta, and white
```




## 常用指令

* `nvm list`:  查看安装的所有node的版本
* `nvm ls-remote available`: 显示可下载的node版本
* `nvm install latest`: 安装最新版本 ( 安装时可以在上面看到 node.js 、 npm 相应的版本号 ，不建议安装最新版本) 	如 `nvm install 10.24.1`
* `nvm install 版本号`: 安装指定的版本的nodejs
* `nvm list or nvm ls`: 查看目前已经安装的版本 （ 当前版本号前面没有 * ， 此时还没有使用任何一个版本，这时使用 node.js 时会报错 ）
* `nvm use 版本号`: 使用指定版本的nodejs （ 这时会发现在启用的 node 版本前面有 * 标记，这时就可以使用 node.js ）



* `nvm list available`:  查看当前可安装的版本
* `nvm install xx.xx.xx`:   安装xx.xx.xx版本的node
* `nvm use xx.xx.xx`:  使用（切换到）xx.xx.xx版本的node
* `nvm uninstall xx.xx.xx`:   卸载xx.xx.xx版本的node
* `nvm arch`:  显示node是运行在32位还是64位。
* `nvm on`:  开启node.js版本管理
* `nvm off`:  关闭node.js版本管理
* `nvm proxy [url]`:  设置下载代理。不加可选参数url，显示当前代理。将url设置为none则移除代理。
* `nvm node_mirror [url]`:  设置node镜像。默认是https://nodejs.org/dist/。如果不写url，则使用默认url。设置后可至安装目录settings.txt文件查看，也可直接在该文件操作。
* `nvm npm_mirror [url]`:  设置npm镜像。https://github.com/npm/cli/archive/。如果不写url，则使用默认url。设置后可至安装目录settings.txt文件查看，也可直接在该文件操作。