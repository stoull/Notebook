# npm常用指令

npm（node package manager）是你安装 Node.js 时开箱即用的依赖/包管理器。它为开发者提供了一种在全局和本地安装包的方法











### 初始化

`npm init`： 生成一份`package.json`配置，会以询问的方式进行一些初始化配置。

参数,可以通过这两个配置跳过询问环节，直接生成默认的配置:

* `--force`
* `--yes`

`npm help init`: 查看更多信息

### 配置

* 查看基本配置，后面增加参数-l能查看所有配置:
	> `npm config list`
	
* 设置下载地址，比如这里的淘宝镜像地址:
	> `npm config set registry https://registry.npm.taobao.org`
	
* 临时使用指定的下载地址下载指定的包`pkg`:
	> `npm --registry https://registry.npm.taobao.org install pkg`

* 设置安装路径:
	> `npm config set cache "D:\xxx\xxx\node_global"`: 

* 设置缓存路径:
	> `npm config set prefix "D:\xxx\xxx\npm_cache"`

* 查看某个属性:
	> `npm config get xxx`

npm安装包版本控制

安装依赖包时，在`package.json`文件会指定相应的版本及控制，如：

```
"react": "18.3.1",
"react-scripts": "5.0.1",
"react-chartjs-2": ">=5.2.0",
"react-dom": "^18.3.1",
```

**部分规则如下：**

* `无符号`: 类似`||`，仅接受指定的特定版本（例如 1.2.1）。
latest: 使用可用的最新版本。
* `^`: 只会执行不更改最左边非零数字的更新。 如果写入的是 ^0.13.0，则当运行 npm update 时，可以更新到 0.13.1、0.13.2 等，但不能更新到 0.14.0 或更高版本。 如果写入的是 ^1.13.0，则当运行 npm update 时，可以更新到 1.13.1、1.14.0 等，但不能更新到 2.0.0 或更高版本。
* `~`: 如果写入的是 〜0.13.0，则当运行 npm update 时，会更新到补丁版本：即 0.13.1 可以，但 0.14.0 不可以。
* `>`: 接受高于指定版本的任何版本。
* `>=`: 接受等于或高于指定版本的任何版本。
* `<=`: 接受等于或低于指定版本的任何版本。
* `<`: 接受低于指定版本的任何版本。
* `=`: 接受确切的版本。
* `-`: 接受一定范围的版本。例如：2.1.0 - 2.6.2。
* `||`: 组合集合。例如 < 2.1 || > 2.6。可以合并其中的一些符号，例如 1.0.0 || * >=1.1.0 <1.2.0，即使用 1.0.0 或从 1.1.0 开始但低于 1.2.0 的版本。


### 安装依赖

* `npm install`: 没带任何参数会直接安装对应目录下，package.json中声明的依赖包。
* `npm install pkg`: 安装pkg依赖包。注意，这种写法不会保存到package.json中，一般不会这样用
* `npm install pkg --save`: 安装pkg依赖包，并记录在package.json的dependencies中
* `npm install pkg --save-dev`: 安装pkg依赖包，并记录在package.json的devDependencies中，可以用简写-D
* `npm install pkg --global`: 安装pkg到全局，可以用简写

### 查看

* `npm list` or `npm ls`: 查看当前目录下安装的所有安装包及其依赖包。
* `npm list --depth 0`: 查看当前目录下安装的所有安装包，其中 --depth 参数后面的数字表示的需要列出依赖包的层级
* `npm -g list --depth 0`: 查看全局已安装的依赖包
* `npm list pkg`: 以树形结构列出pkg及其依赖包的信息
* `npm view pkg version`: 查看pkg这个安装包的版本
* `npm view pkg versions`: 查看pkg所有的版本
* `npm view pkg`: 查看pkg的详细信息

### 升级

* `npm outdated`: 查看过期的包
* `npm update`: 会检查云端的版本信息，对比本地安装包的版本规则，然后更新到对应规则的最新版本。
* `npm update pkg`: 只升级指定的pkg
* `npm update -g`: 升级全局安装的依赖包

### 卸载

* `npm uninstall pkg`: 卸载pkg，并从package.json、package-lock.json中删除掉
* `npm uninstall pkg --no-save`: 卸载pkg，但是不会从package.json、package-lock.json中删除，仍保留

### 清除缓存

* `npm cache clean`: 清除npm缓存
* `npm cache clean --force`: 强制清除npm缓存,  Recommended protections disabled

#### npm其它的命令 `npm --help` or `man npm` or `npm help update`

```$npm --help
npm <command>

Usage:

npm install        install all the dependencies in your project
npm install <foo>  add the <foo> dependency to your project
npm test           run this project's tests
npm run <foo>      run the script named <foo>
npm <command> -h   quick help on <command>
npm -l             display usage info for all commands
npm help <term>    search for help on <term>
npm help npm       more involved overview

All commands:

    access, adduser, audit, bugs, cache, ci, completion,
    config, dedupe, deprecate, diff, dist-tag, docs, doctor,
    edit, exec, explain, explore, find-dupes, fund, get, help,
    help-search, hook, init, install, install-ci-test,
    install-test, link, ll, login, logout, ls, org, outdated,
    owner, pack, ping, pkg, prefix, profile, prune, publish,
    query, rebuild, repo, restart, root, run-script, sbom,
    search, set, shrinkwrap, star, stars, start, stop, team,
    test, token, uninstall, unpublish, unstar, update, version,
    view, whoami

Specify configs in the ini-formatted file:
    /Users/hut/.npmrc
or on the command line via: npm <command> --key=value
```

参考： [npm常用命令汇总](https://www.cnblogs.com/shapeY/p/15048861.html)