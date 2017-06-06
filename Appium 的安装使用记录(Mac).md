# Appium 的安装使用记录

[Appium 官网](http://appium.io)

[Appium-中文各种平台的配置](http://appium.io/slate/cn/master/?ruby#客户端类库列表及appium服务端支持)

[Getting started with appium](http://appium.io/slate/en/tutorial/ios.html?ruby#getting-started-with-appium)

[MAC下搭建appium UI自动化环境详细步骤](http://qa.blog.163.com/blog/static/190147002201510161119832/)

[appium安装的所有文档（英文）](https://github.com/appium/appium/tree/master/docs/en/appium-setup)

[在Mac OS X 上使用 Appium](https://github.com/appium/appium/blob/master/docs/en/appium-setup/running-on-osx.md)

[在Windows上使用Appium](https://github.com/appium/appium/blob/master/docs/en/appium-setup/running-on-windows.md)


[appium/sample-code](https://github.com/appium/sample-code)


[npm 使用介绍](http://www.runoob.com/nodejs/nodejs-npm.html)

[package.json位于模块的目录下，用于定义包的属性](https://docs.npmjs.com/files/package.json)

## 配置测试环境
>iOS 系统要求
>
>- Mac OS X 10.10以上, 推荐10.11.1以上
>
>- XCode >= 6.0, 推荐7.1.1 以上
>
>- 果苹开发工具 (iPhone simulator SDK, command line tools)



## 一 安装npm
> npm（node package manager），通常称为node包管理器。顾名思义，它的主要功能就是管理node包，包括：安装、卸载、更新、查看、搜索、发布等。

- **方法一 通过Node.js安装**

> Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境。	
> Node.js 使用了一个事件驱动、非阻塞式 I/O 的模型，使其轻量又高效	
> Node.js 的包管理器 npm，是全球最大的开源库生态系统。

由于新版的Node.js已经集成了`npm`，也就是说你安装了Node.js,那么`npm`就安装在你的电脑里了。

[安装包在这里下载](https://www.npmjs.com/get-npm?utm_source=house&utm_medium=homepage&utm_campaign=free%20orgs&utm_term=Install%20npm)

Node.js 安装好后，使用`npm -v`是否安装成功
>注意如果`npm -v`用不了，则将`/usr/local/bin`添加到`$PATH`里面

- **方法二 使用brew安装**

使用`brew`安装，使用 `brew -v`检查是否有安装 Homebrew
>如果没有安装，用下面的命令安装. 可参考 [Install Ruby](http://appium.io/slate/en/tutorial/ios.html?ruby#install-ruby)
>
> `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

如有安装，则用下面的命令安装 node：
	
	brew install node

- **方法三 自已编译安装**

```
git clone git://github.com/ry/node.git
cd node
./configure
make
sudo make install
```

#### 授权 `npm` 使用 iOS Simulator
	npm install -g authorize-ios
如果你使用的是  [Appium.app](https://github.com/appium/appium-desktop/releases/tag/v1.0.2-beta.2)， 你可以在图形界面授权iOS。并且在每次Xcdoe重新安装之后，都要重新授权一次

## 二 安装appium
不要使用root账号安装appium,请使用普通用户安装（为什么？）

	npm install -g appium
>如果用root权限安装了, 用下面的命令卸载，再用普通用户安装？

>```
>$ sudo npm uninstall appium -g   //卸载appium
>$ sudo chmod -R 777 /usr/local   //给予非root用户权限
>$ npm install -g appium         //重新安装
>```
>

## 三 安装 Appium Client

	> npm install wd 
还可以到[Appium Git](https://github.com/appium)上下载对应的版本client，自已编译安装：
>比如安装python-client：

>```
>git clone git@github.com:appium/python-client.git
>cd python-client
>python setup.py install
>```

## 四 检查Appium依赖库是否正常
Appium提供了一个appium-doctor，用于检查Appium的依赖库是否安装或是否合适
安装 appium-doctor

	npm install -g appium-doctor
运行` appium-doctor` 并用 `--ios ` 或 `--android`参数查看对应的依赖库是否安装好

	appium-doctor --ios
	
当没有安装好的时候会出现这样的询问:

>```
>info AppiumDoctor ### Diagnostic completed, one fix needed. ###
>info AppiumDoctor 
>info AppiumDoctor ### Fixing:  ✖ Xcode Command Line Tools are NOT >installed! ###
>info AppiumDoctor The following command need be executed: xcode-select -->install
>? Fix it: (Use arrow keys)
>❯ yes 
>  no 
>  always 
>  never
>```

 用光标移动选择`yes` 或`always`可以导向自动安装.当然也有可能需要要手动安装的:` ### Manual Fixes Needed ###`,跟着提示去Fix就可以。如果一切都正常会出现这个：
  
>```
>info AppiumDoctor ### Diagnostic completed, no fix needed. ###
>info AppiumDoctor 
>info AppiumDoctor Everything looks good, bye!
>info AppiumDoctor 

>```

**运行`appium -v`，如果出现版本输出如下，那Appium就安装成功了，可以继续去获取 iOS sample app开始测试了**

	$ appium -v
	1.6.4
	
## 使用图形界面 Appium Gui
[Appium.app](https://github.com/appium/appium-dot-app)
[Appium.exe](https://github.com/appium/appium-dot-exe)
	
## 五 运行 Appium 的iOS示例APP

### 编译iOS示例APP UICatalog

- **途径一**

在用户`〜`目录下运行：

`npm install sample-apps`

> 这里的 sample-apps 是Appium从苹果示例代码[fork](https://github.com/appium/ios-uicatalog)的。
完成之后你在这个位置找到编译好的UICatalog.app ：

	node_modules/sample-apps/node_modules/ios-uicatalog/build/Release-iphonesimulator/UICatalog-iphonesimulator.app
	
>注意这个 UICatalog.app 只能在模拟机上运行，真机上的要另外编译。
>
>可以在目录`〜/node_modules/sample-apps/pre-built`下找到一些已经编译好的其它程序

- **途径二** 

直接从[Apple Sample Code](https://developer.apple.com/library/content/samplecode/UICatalog/UIKitCatalogiOSCreatingandCustomizingUIKitControls.zip)或[Appium](https://github.com/appium/ios-uicatalog)下载对应的原码，使用XCode或`xcodebuild `编译对应的app。

>使用Apple官方代码为例，用 `xcodebuild`命令编译：
>
>`git clone https://github.com/appium/ios-uicatalog` # 获取对应的代码
>
>`cd UIKitCatalogiOSCreatingandCustomizingUIKitControls/Objective-C` # 进入工程目录 
>
>`xcodebuild -sdk iphonesimulator` # 编译模拟机上运行的包
>
> UIKitCatalog.app在`工程目录/build/Release-iphonesimulator/UIKitCatalog.app`

将 UIKitCatalog.app 放入一个测试目录 UIKitCatalog 进入这个目录运行：

## 五 启动 Appium

创建模块
创建模块，package.json 文件是必不可少的。我们可以使用 NPM 生成 package.json 文件，生成的文件包含了基本的结果。

```
node .
module.js:471
    throw err;
    ^

Error: Cannot find module '/Users/stoull/npm_AppiumTest'
    at Function.Module._resolveFilename (module.js:469:15)
    at Function.Module._load (module.js:417:25)
    at Module.runMain (module.js:604:10)
    at run (bootstrap_node.js:390:7)
    at startup (bootstrap_node.js:150:9)
    at bootstrap_node.js:505:3
linkapps-Mac:npm_AppiumTest stoull$ ls
UIKitCatalog.app	appium.txt		node_modules
linkapps-Mac:npm_AppiumTest stoull$ vi appium.txt 
linkapps-Mac:npm_AppiumTest stoull$ npm init
This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `npm help json` for definitive documentation on these fields
and exactly what they do.

Use `npm install <pkg> --save` afterwards to install a package and
save it as a dependency in the package.json file.

Press ^C at any time to quit.
package name: (npm_appiumtest) 
version: (1.0.0) 
description: 
entry point: (index.js) 
test command: 
git repository: 
keywords: 
author: 
license: (ISC) 
About to write to /Users/stoull/npm_AppiumTest/package.json:

{
  "name": "npm_appiumtest",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}


Is this ok? (yes) yes
linkapps-Mac:npm_AppiumTest stoull$ ls
UIKitCatalog.app	node_modules
appium.txt		package.json
linkapps-Mac:npm_AppiumTest stoull$ npm install -g
/usr/local/lib
└── npm_appiumtest@1.0.0 

linkapps-Mac:npm_AppiumTest stoull$ 
```

到这里失败了〜〜〜〜〜！！！

## 五 启动 Appium
如果到第四步都正常，那么就输入这个命令吧: 

	$ appium
	
运行真机测试（-U :设备的UUID。-app: app的 BoundleID）：

	appium -U xxx-UUID-xx --app xxx-BoundleID-xxx

Helpful Links

Link | Summary
--- | ---
[npm](https://www.npmjs.org/) | The main registry for npm packages. Appium is published here.
[rubygems](http://rubygems.org/) | The main registry for Ruby gems. The appium ruby bindings are published here.
[RVM](http://rvm.io/) | RVM’s homepage. Extensive documentation is available.
[Ruby](https://www.ruby-lang.org/en/) | The Ruby language homepage. Useful for keeping up to date with Ruby releases.

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
***
#### 授权 `npm` 使用 iOS Simulator
	npm install -g authorize-ios
如果你使用的是  [Appium.app](https://github.com/appium/appium-desktop/releases/tag/v1.0.2-beta.2)， 你可以在图形界面授权iOS。并且在每次Xcdoe重新安装之后，都要重新授权一次

#### 测试不同的iOS SDKs
Appium 使用苹果提供的 instruments 来启动 iOS 模拟器，默认它会使用当前安装的 Xcode 和该 Xcode 下安装好的最高版本的 iOS SDK。这就意味着如果你想测试 iOS 6.1， 但是你安装了 iOS 7.0， 那么 Appium 会强制使用 7.0 的模拟器。 唯一的方法就是安装多个Xcode，然后在安装不同的 SDK。然后在启动 Appium 前，切换到你要测试的特定的版本。

	sudo xcode-select --switch &lt;path to required xcode&gt;

#### 使用Xcode 8 (包含iOS10)的 XCUITest测试
为了支持Xcode 8 （以及所有iOS10及以上版本）的自动测试，你需要单独安装[Carthage](https://github.com/Carthage/Carthage)依赖库管理工具

	brew install carthage
> Carthage 是类似于 CocoaPods 的第三方库管理工具，了解Carthage可以参考这个[如何使用Carthage管理iOS依赖库](http://www.jianshu.com/p/5ccde5f22a17)
	
## 使用 Jenkins 测试iOS程序(在Mac上)
首先确认你的mac电脑能连接到Jenkins master，并确认你运行了上面所说的`authorize-ios`,然后下载 `jenkins-cli.jar `,

	wget https://jenkins.ci.cloudbees.com/jnlpJars/jenkins-cli.jar




