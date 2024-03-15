# iOS自动化打包

## CI/CD

CI/CD(Continuous Integration/Continuous)，或持续集成/持续交付或部署，是一种采用自动化技术的软件开发实践。通过持续的代码交付，频繁可靠的更新加快了发布周期。

![持续集成/持续交付或部署](./images/Cicd-page-graphic.png)
[引用自：unity.com](https://unity.com/cn/solutions/what-ci-cd#how-are-cicd-and-devops-related)

**CI: 持续集成(Continuous Integration)**

开发成员整合代码，并通过自动化构建（编译，自动化测试，代码分析）来快速发现问题。

* 编译打包-build
* 自动化测试-test Or Unit Test
* 代码分析-source code analysis
	
**CD: 持续交付或持续部署(Continuous Delivery or Continuous Deployment)**

**持续交付**：将App在测试平台自动化构建版本并发布测试

**持续部署**：将App自动化生成新版本，并上传到生产环境。

## 关于`xcodebuild `

xcodebuild(Xcode的命令行工具)是一系列的命令集，通过命令调用Xcode对Xcode项目进行编译打包，是CI/CD开发的有效工具。xcodebuild是Xcode的内置工具，一般安装了Xcode就有xcodebuild。

### 查看`xcodebuild`是否安装

```
% xcodebuild -version
Xcode 15.2
Build version 15C500b
```

### 安装`xcodebuild`

* 手动安装
	
如果没有也可以在这里下载：[Download for Apple Developers](https://developer.apple.com/download/all/)，需要登录。
	
* 通过命令安装：
`xcode-select --install`

>macOS comes bundled with xcode-select, a command-line tool that is installed in `/usr/bin`.

### 切换`xcodebuild`使用的Xcode版本

如果电脑上安装了多个Xcode版本，就是需要确认当前`xcodebuild`使用的Xcode版本，及在各个版本之间切换。

* `xcode-select --print-path`: 查看当前使用的Xcode版本
* `sudo xcode-select -switch <path/to/>Xcode.app`: 切换Xcode版本

## Xcode项目中的概念

* project文件: 以`. xcodeproj` 结尾的文件，连接及组织项目里的所有代码及资源
	* 代码文件，布局文件，图片及其它各种资源文件
	* 项目的目录结构，及内外部的Libraries
	*  编译配置(build configurations), project下一般有有`Debug`和`Release`两种编译配置。
	*  不同的targets和Scheme
	*  [Xcode Project](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Projects.html#//apple_ref/doc/uid/TP40009328-CH5-SW1)
* workspace文件: 以`. xcworkspace` 结尾的文件
	* 可以包含多个project项目，如`Pods`生成的`mypro.xcworkspace `里就有`mypro.xcodeproj`和Pods文件夹内的`Pods.xcodeproj`两个项目
	* Workspaces Extend the Scope of Your Workflow 如你在项目中可以快捷找到Pods中库内的方法定义
	* Projects in a Workspace Share a Build Directory
	* [Xcode Workspace](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Workspace.html#//apple_ref/doc/uid/TP40009328-CH7-SW1)
* Target
* Scheme
* Build configuration
* Certificate, identifier, and profile
* 



## `xcodebuild`的使用




**参考资料：**

[Building from the Command Line with Xcode FAQ](https://developer.apple.com/library/archive/technotes/tn2339/_index.html#//apple_ref/doc/uid/DTS40014588-CH1-HOW_DO_I_BUILD_MY_PROJECTS_FROM_THE_COMMAND_LINE_)

[Xcode - Archive export files](https://help.apple.com/xcode/mac/current/#/deva1f2ab5a2)






## Xcode Server

[Continuous integration using Xcode Server](https://help.apple.com/xcode/mac/current/#/dev466720061)


## Xcode Cloud

Xcode Cloud 是专为 Apple 开发者设计的一项内置于 Xcode 中的持续集成和交付服务。了解资格及要求、入门工具，以及如何管理订阅。

[开始使用 Xcode Cloud](https://developer.apple.com/cn/xcode-cloud/get-started/)

[Xcode Cloud-documentation](https://developer.apple.com/documentation/xcode/xcode-cloud/)

[Xcode Cloud](https://developer.apple.com/xcode-cloud/)

