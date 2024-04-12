# RN开发中遇到的问题


## 一、安装报错

### 问题：`pod install`过程安装`glog`报错

报错信息如下：

```
...
Installing Yoga (1.14.0)
Installing boost (1.76.0)
Installing fmt (6.2.1)
Installing glog (0.3.5)

[!] Error installing glog

――― MARKDOWN TEMPLATE ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

...

### Error

Errno::EACCES - Permission denied @ dir_s_mkdir - /Users/hut/Library/Caches/CocoaPods/Pods/External/glog/2263bd123499e5b93b5efe24871be317-04b94/d20240412-6854-bh5njn
/opt/homebrew/Cellar/ruby/3.2.2_1/lib/ruby/3.2.0/fileutils.rb:2261:in `mkdir'
/opt/homebrew/Cellar/ruby/3.2.2_1/lib/ruby/3.2.0/fileutils.rb:2261:in `copy'

...

```

可以看到`Errno::EACCES - Permission denied`说明没有权限，一路检查目录`/Users/$USER/Library/Caches/CocoaPods/`下的权限，皆无问题后。

发现此问题是因为需要创建的目录文件已存在于glog的缓存目录下：`glog/2263....bh5njn`, ruby没有权限进行覆盖写入而报这个错误，可以将这个目录手动删除即可。

`cd /Users/$USER/Library/Caches/CocoaPods/Pods/External`






## 二、运行报错

### * folly问题：`redefinition with different types ('uint8t' (aka 'unsigned char')`

>/Users/hut/Desktop/InterRN/iOS/Pods/Headers/Private/RCT-Folly/folly/portability/Time.h:52:17 Typedef redefinition with different types ('uint8_t' (aka 'unsigned char') vs 'enum clockid_t'

#### 解决方法:  removing that line 52 in Time.h

```
sed -i '' 's/typedef uint8_t clockid_t;//' "${SRCROOT}/Pods/RCT-Folly/folly/portability/Time.h"
```

### * hermes-engine 问题：

>Sandbox: rsync.samba(18749) deny(1) file-read-data /Users/hut/Library/Developer/Xcode/DerivedData/IntegrateRNiOS-edulwnwkohfcryampzapqzlxsnpf/Build/Products/Debug-iphoneos/XCFrameworkIntermediates/hermes-engine/Pre-built/hermes.framework/Info.plist

#### 解决方法:  
"Check that `ENABLE_USER_SCRIPT_SANDBOXING` is disabled in the project's build settings."


### * Command PhaseScriptExecution failed with a nonzero exit code 问题：

都安装好后，跑项目出现如下错误：

```
React-rncore: 
Command PhaseScriptExecution failed with a nonzero exit code
```

```
FBReactNativeSpec: 
Command PhaseScriptExecution failed with a nonzero exit code
```

是因为xcode环境文件`xcode.env`


> `xcode.env` file exists to make it easy for developers to tell Xcode where to find the node executable on their system. This file is intended to be checked in to source control, and it is a generic mechanism that works on most machines.


一般的`.xcode.env`文件内容如下:

`export NODE_BINARY=$(command -v node)`

但从同事那拉下来后，在工程目录下多出一个`xcode.env.lcoal`的文件，内容为：

`export NODE_BINARY=/usr/local/opt/node@18/bin/node`

导致这个问题

#### 解决方法:  根据`node`的位置，移除`xcode.env.lcoal`文件或者更新正确的`.xcode.env`文件内容



