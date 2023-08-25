# App WiFi网络-权限及申请


## 当前需求

* 手机连接IOT设备的热点网络。
* 手机获取周围WiFi信息供用户选择，并输入对应的密码，让设备配网。

## 相关技术

[Apple documentation - TN3111: iOS Wi-Fi API overview](https://developer.apple.com/documentation/technotes/tn3111-ios-wifi-api-overview#Add-an-accessory-to-the-users-network%22https://developer.apple.com/documentation/technotes/tn3111-ios-wifi-api-overview#Add-an-accessory-to-the-users-network%22)

[Apple Developer Forums - How To Get Wi-Fi Scan List Using Network Extension Framework In iOS 11](https://developer.apple.com/forums/thread/88418)



### Get Current WiFi Info

[stackoverflow.com - How to get available wifi network name in iOS using swift](https://stackoverflow.com/questions/31715055/how-to-get-available-wifi-network-name-in-ios-using-swift/41964782)


### Get WiFi List 

Get entitlement:

`com.apple.developer.networking.HotspotHelper`

[Apple - Contact Apple For Network-Extension](https://developer.apple.com/contact/network-extension)

- 已知VPN应用可过
- 设备配网没有发现通过的，苹果提供的解决方案: [Apple  Documentation - Configuring a Wi-Fi Accessory to Join the User’s Network](https://developer.apple.com/documentation/networkextension/configuring_a_wi-fi_accessory_to_join_the_user_s_network) , 理由：
	* Apple is very concerned about user privacy
	* Real-time Wi-Fi scan results represents a serious privacy challenge

### Tutorial

[medium - Connecting to preferred WiFi without leaving the app in iOS 11.](https://medium.com/@Chandrachudh/connecting-to-preferred-wifi-without-leaving-the-app-in-ios-11-11f04d4f5bd0)


### 实例

[掘金 - iOS 无法获取 WiFi 列表？一定是因为你不知道这个框架](https://juejin.cn/post/6844903529618866183)

[掘金 -Network Extension 申请表格填写及邮件往来](https://juejin.cn/post/6844903529706946567)