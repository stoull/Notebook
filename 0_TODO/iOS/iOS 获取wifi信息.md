# iOS 获取wifi信息

//获取 WiFi 信息 Swift

```
//获取 WiFi 信息
func getWifiInfo() -> (ssid: String, mac: String) {
    if let cfas: NSArray = CNCopySupportedInterfaces() {
        for cfa in cfas {
            if let dict = CFBridgingRetain(
                CNCopyCurrentNetworkInfo(cfa as! CFString)
                ) {
                if let ssid = dict["SSID"] as? String,
                    let bssid = dict["BSSID"] as? String {
                    return (ssid, bssid)
                }
            }
        }
    }
    return ("未知", "未知")
}
```
//获取 WiFi 信息 Objective-C

```
- (NSDictionary *)getWifiInfo {
    NSArray *cfas = CFBridgingRelease(CNCopySupportedInterfaces());
    for (id cfa in cfas) {
        CFStringRef cfaString = (__bridge CFStringRef)cfa;
        NSDictionary* netInfo = CFBridgingRelease(CNCopyCurrentNetworkInfo(cfaString));
        return netInfo;
    }
    return nil;
}
```