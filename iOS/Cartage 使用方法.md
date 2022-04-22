# Cartage 使用方法

[Carthage/Carthage](https://github.com/Carthage/Carthage#for-all-platforms) 官方

## 创建 Cartfile

```
cd ~/To/Your/Project/Path
touch Cartfile
open -a Xcode Cartfile
```

Cartfile为包的管理配置文件，这里安装Alamofire，将下面的内容写放文件：

```
github "Alamofire/Alamofire" ~> 5.4
```

格式解释
包源：

* `github`: 包源为github, 用`Username/ProjectName`的格式指定。如上面的 `github "Alamofire/Alamofire"`
* git: 指定源为自己的git仓库。根据git仓库服务的配置，可有`git://`, `http://`, `ssh://`等远程地址。如: `ssh://hut@192.168.0.120:29418/your_frame.git`

包版本：

*  `== 1.0` 代表定死的为1.0版本
*  `>= 1.0` 代表使用1.0或更高的版本
*  `~> 1.0` 代表使用可兼容 1.0 版本的版本，即下一个主版本前的所有版本，如上面的 `~> 5.4` 表示使用兼容版本5.4和版本。

Cartfile的文件格式可详见： [Carthage/Carthage](https://github.com/Carthage/Carthage#for-all-platforms) 官方

## 编译对应的依赖包

`carthage update --platform iOS`

这个命令会从包源下载最新的代码，`--platform iOS`指定编译iOS平台的frameworks。如果不指定`--platform` 则会编译所有平台的frameworks。
>--platform: the platforms to build for (one of 'all', 'macOS', 'iOS', 'watchOS', 'tvOS', or comma-separated values of the formers except for 'all'

#### 编译指定的依赖包
carthage update Alamofire --platform iOS

如果文件内为：
`github "SoySauceLab/CollectionKit"`

则使用命令：
carthage update CollectionKit

使用 `carthage help update` 查看更多的选项。


### 编译模拟器使用的包
> Building platform-independent XCFrameworks (Xcode 12 and above)

如果出现：`Building for iOS Simulator, but the linked and embedded framework was built for iOS`错误，说明没有对模拟器的包，使用xcframeworks解决。[StackOverflow](https://stackoverflow.com/questions/65303304/xcode-12-3-building-for-ios-simulator-but-the-linked-and-embedded-framework-wa)

`carthage update --use-xcframeworks`

这个将会生成 `XCFramework`

`carthage update --use-xcframeworks --platform iOS` 将会生成iOS及对应模拟器可用的包

## 编译结果

当运行`carthage update` 之后，carthage 会生成文件`Cartfile.resolved`，及文件夹`Carthage`.

* **Cartfile.resolved** 这个文件记录了所有依赖包安装的版本信息，这样可以保证在下次update的时候，或者同事checkout之后，安装的都是同一个版本的依赖包。需加入版本管理。
* **Carthage** 这个目录下包含两个目录

 > **Build**: 存储编译好的frameworks，这些frameworks可以直接加入到工程中使用。这些frameworks可能是本地编译的，也有可能是从源上下载的已编译好的。
  > **Checkouts**: 这是依赖包的源代码。Carthage内部管理对应的缓存数据。
  
  不要更改`Checkouts`中的源代码。如果真要更改，使用`carthage update` 中的 ` --use-submodules` 选项。
  
## 加入工程

在工程配置页中，选择`target`->`your project traget`->`Frameworks, Libraries, and Embedded Content`, 将`Carthage/Build/iOS`目录下的`Alamofire.framework`拖入到这里，并将`Embed`选项改为`Embed&Sign`

处理[App Store submission bug](http://www.openradar.me/radar?id=6409498411401216)的问题，即frameworks不能包含图片文件。使用 `carthage copy-frameworks` 命令处理。
选 `Build Phases`在中间内容区的左上角点击加号->`New Run Script Phase`,然后加入命令`/usr/local/bin/carthage copy-frameworks`,并增加需要拷贝的frameworks：

`$(SRCROOT)/Carthage/Build/iOS/Alamofire.framework`

## 更新依赖包

`carthage update --platform iOS`

