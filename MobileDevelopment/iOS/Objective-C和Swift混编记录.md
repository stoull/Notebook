## Objective-C 工程中使用 Swift文件

1. 新建一个*.swift 文件
2. 根据XCode提示或手动生成ProjectName-Bridging-Header.h文件
3. 配置工程 `PROJECT -> Build Settings`
	
	>```
	>Defines Module : NO
	>Embedded Content Contains Swift : NO
	>Install Objective-C Compatibility Header : YES
	>Objective-C Bridging Header : ProjectName-Bridging-Header.h
	>```
	
4. 在新建的类class前面加上`@objc`如下：

	>```
	>@objc class LBCollaAddFileVC: UIViewController {
	>    override func viewDidLoad() {
	>       super.viewDidLoad()
	>    }
	>}
	>```

5. 在需要使用该`.Swift`文件的`.h`文件引入 `#import "LinkPortal-Swift.h"` 文件，这样就可以使用工程ProjectName module 下的所有Swift文件了
> 注意是引入 `#import "LinkPortal-Swift.h"` 文件，不是`#import "*.swift"`文件
>
>同一个App Target中引入代码：
> 
>|  | Import into Swift | Import into Objective-C |
>| ---- | ----| ---- |
>| Swift code | No import statement | `#import "ProductModuleName->Swift.h"` |
>| Objective-C code | No import statement; Objective-C bridging header required | `#import "Header.h"` |
>不同语言引入Frameworks
>
>|  | Import into Swift | Import into Objective-C |
>| ---- | ----| ---- |
>| Any language framework | `import FrameworkName` | `@import FrameworkName;` |
	
6. 在`*.Swift`文件中使用Pods中的第三方库，在`ProjectName-Bridging-Header.h`文件中引入对应的文件，如引入Masonry ：`#import <Masonry/Masonry.h>`即可在同一个ProjectName module下所有*.Swift文件都可以作swift语法使用Masonry的代码。

*********
**参考资料：**

[官方资料-原理](https://developer.apple.com/library/content/documentation/Swift/Conceptual/BuildingCocoaApps/index.html)

[官方资料-代码](https://developer.apple.com/library/content/documentation/Swift/Conceptual/BuildingCocoaApps/MixandMatch.html#//apple_ref/doc/uid/TP40014216-CH10-ID122)

[简书-Objective-C和Swift混编的一些经验](http://www.jianshu.com/p/a5e6e574145b)

[Using Swift with Cocoa and Objective-C中文手册](https://github.com/CocoaChina-editors/Welcome-to-Swift/blob/master/UsingSwiftwithCocoaandObjective-C中文手册.md)

[Can't use Swift classes inside Objective-C](https://stackoverflow.com/questions/24206732/cant-use-swift-classes-inside-objective-c?noredirect=1&lq=1)



## Swift 工程中使用 C 代码

[Interacting with C APIs](https://developer.apple.com/library/content/documentation/Swift/Conceptual/BuildingCocoaApps/InteractingWithCAPIs.html)