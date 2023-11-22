# myGro 技术设计文档


支持系统：iOS 12+ 并适配iPad, 支持dark mode

屏幕方向：仅支持正方向竖屏

### 开发语言
swift 5 ，以Objective-C为辅

### 技术详情

框架MVVM

app manager
app error
autho

####界面：

：[ProgressHUD](https://github.com/stoull/ProgressHUD) fork订制版本
##### 下拉刷新
ESPullToRefresh： [ESPullToRefresh](https://github.com/eggswift/pull-to-refresh)
##### 弹框界面
Popover: [Popover](https://github.com/corin8823/Popover)

##### Swift弹框
SwiftEntryKit: [SwiftEntryKit](https://github.com/huri000/SwiftEntryKit)

##### 自动布局
SnapKit: [SnapKit](https://github.com/SnapKit/SnapKit) MIT license

#### 异步事件处理
iOS 13.0+ ：[Combine](https://developer.apple.com/documentation/combine)

#### 数据处理

JSON 解析:

[SwiftyJSON](https://github.com/SwiftyJSON/SwiftyJSON), 使用[MIT License](https://github.com/SwiftyJSON/SwiftyJSON/blob/master/LICENSE)

#### 网络设计方案

HTTP使用： [Alamofire](https://github.com/Alamofire/Alamofire) 自由开源公共软件，使用[MIT License](https://github.com/Alamofire/Alamofire/blob/master/LICENSE)开源共享协议

MQTT使用：[CocoaMQTT](https://github.com/emqx/CocoaMQTT)自由开源公共软件，使用[BSD License](https://github.com/emqx/CocoaMQTT/blob/master/epl-v10)开源共享协议

#### 网络图片
Kingfisher：[Kingfisher](https://github.com/onevcat/Kingfisher)

#### 数据存储方案

#### 系统权限
PermissionsKit: [PermissionsKit](https://github.com/sparrowcode/PermissionsKit)

数据库使用: 
CoreData

[SQLite.swift](https://github.com/stephencelis/SQLite.swift)自由开源公共软件，使用[MIT license](https://github.com/stephencelis/SQLite.swift/blob/master/LICENSE.txt)开源共享协议

> 可选 [realm-cocoa](https://github.com/realm/realm-cocoa) 使用[Apache 2.0 license](https://github.com/realm/realm-core)。如未来考虑跨平台或其它更多的复杂功能会考虑使用realm。

#### 数据加密
CryptoSwift：[CryptoSwift](https://github.com/krzyzanowskim/CryptoSwift)

#### 蓝牙

可通信的蓝牙信息：

Bluetooth Low Energy/BTLE/Bluetooth 4.0 或苹果支持的Bluetooth profiles [Bluetooth profiles supported by iOS](https://support.apple.com/en-us/HT204387) 不需要作[MFi认证](https://mfi.apple.com)。

传统蓝牙需要作[MFi认证](https://mfi.apple.com)。

[Bluetooth profiles supported by iOS](https://support.apple.com/en-us/HT204387)

[Bluetooth和苹果MFi认证相关总结](https://www.jianshu.com/p/6de5398d6332)

[MFi是什么？关于苹果MFi认证MFi开发MFi外设，你所必须要知道的事情](https://www.jianshu.com/p/b90b0c45398d)


Apple：[Core Bluetooth](https://developer.apple.com/documentation/corebluetooth)

>
具体详情可见：[Apple Bluetooth](https://developer.apple.com/bluetooth/)

#### wifi配网等功能

app 内 wifi管理：
[iOS Wi-Fi Management APIs](https://developer.apple.com/library/archive/qa/qa1942/_index.html)


[Network Extension](https://developer.apple.com/documentation/networkextension)

[Wi-Fi Configuration](https://developer.apple.com/documentation/networkextension/wi-fi_configuration)

[MFi Program](https://mfi.apple.com)

[Configuring a Wi-Fi Accessory to Join the User’s Network](https://developer.apple.com/documentation/networkextension/configuring_a_wi-fi_accessory_to_join_the_user_s_network)


使用Socket进行TCP、UDP连接: 
Network.framework
[CocoaAsyncSocket](https://github.com/robbiehanson/CocoaAsyncSocket)

