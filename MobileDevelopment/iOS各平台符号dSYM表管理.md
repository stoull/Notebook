# Bugly及Google Crashlytics上传iOS符号表

## 工具

查看当前机器上的所有符号表：

`mdfind -name .dSYM | while read -r line; do dwarfdump -u "$line"; done`

## Bugly上传iOS 符号表

### 下载bugly的符号表工具

从 [Bugly Downloads](https://bugly.qq.com/v2/downloads) 页中找到**iOS端**的符号表工具，并下载。

符号表工具SDK介绍：符号表上传工具，支持用户本地上传符号表到Bugly平台。该工具基于java实现，需要运行在Java环境中，详细请参考使用指引。


[Bugly iOS 符号表配置](https://bugly.qq.com/docs/user-guide/symbol-configuration-ios/?v=20240216160622)

### dSYM文件在哪里？

打到对应的Archives->'右键Show in Finder'->'选择xx.xcarchive文件'->'右键Show Package Content'->'dSYMs'->'找到yourAppName.app.dSYM'，就是它了！！！

或通过`通过iTunes Connect找回`


### 如何上传符号表到bugly平台？

* 目前只能通过上面下载的符号表工具进行上传符号表，具体官方说明为：

	> 目前只支持通过符号表工具上传，请下载符号表工具上传（内附详细使用说明文档），下载链接：[https://bugly.qq.com/v2/downloads](https://bugly.qq.com/v2/downloads)
* 在上面步骤下载的工具文件夹里面会有一个名为`符号表上传工具使用说明.doc`的文档，说明了怎么样使用下载的工具上传符号表
* 使用工具中的`buglyqq-upload-symbol.jar`包上传 dSYM 文件。上传时dSYM 文件需要压缩成`.zip`文件。


执行命令：

```
java -jar buglyqq-upload-symbol.jar -appid <APP ID> 
                                    -appkey <APP KEY>
                                    -bundleid <App BundleID>
                                    -version <App Version>
                                    -buildNo <App Build Number>
                                    -platform <App Platform>
                                    -inputSymbol <Original Symbol File Path>
                                    -inputMapping <mapping file>
```

参数说明：

* `-appid` : 在bugly.qq.com 或者 bugly.tds.qq.com上产品对应的appid
* `-appkey` : 在bugly.qq.com 或者 bugly.tds.qq.com 上产品对应的appkey
* `-bundleid`:  在bugly.qq.com 或者 bugly.tds.qq.com 注册产品时，填写的BundleID，Android平台是应用包名，iOS平台叫bundle id
* `-version`:  App版本号  (PS:注意版本号里不要有特殊字符串，比如( )，不然运行可能会报错)
* `-buildNo`: 可选参数, 构建号，如果上传的是mapping.txt文件，并且初始化Bugly时有使用构建号，则上传符号表时一定要填写正确的构建号，否则会导致Java堆栈无法还原。
* `-platform`: 平台类型，当前支持的三个选项 分别是 Android、IOS、MAC，注意大小写要正确。
* `--inputSymbol`: 原始符号表[dsym、so]所在文件夹目录地址，如果是Android平台同时包含mapping和so，此处输入两个原始符号表存储的共同父目录。
* `-inputMapping`: mapping所在文件夹目录地址[Android平台特有，ios忽略]

示例:

```
ava -jar buglyqq-upload-symbol.jar -appid a278f01047
 				   -appkey 1e5ab6b3-b6fa-4f9b-a3c2-743d31dffe86 
 				   -bundleid com.tencent.demo.buglyprodemo 
 				   -version 4.3.0 
 				   -buildNo 2 
 				   -platform Android 
 				   -inputSymbol /Users/mary/Downloads/upload_target/obj/arm64-v8a 
 				   -inputMapping /Users/mary/workspace/apm/QAPM_SDK/app/build/outputs/mapping/r8/release/mapping.txt
```

如果看到200则表示上传成功，否则会看到错误日志信息。

#### 如未安装Java 

如报:`The operation couldn’t be completed. Unable to locate a Java Runtime.`表示没有安装java, 或者使用`java -version`检查

如未安装Java ，按如下安装Java JDK:

[How do I install Java for my Mac?](https://www.java.com/en/download/help/mac_install.html)

[Download Java for macOS-下载jre-8u401-macosx-x64.dmg](https://www.java.com/en/download/)

终端运行`java -version`如下表示成功：

```
% java -version 
java version "1.8.0_401"
Java(TM) SE Runtime Environment (build 1.8.0_401-b10)
Java HotSpot(TM) 64-Bit Server VM (build 25.401-b10, mixed mode)
```

### 上传到Bugly

* 进入到下载的符号表工具：`cd /Users/hut/Downloads/buglyqq-upload-symbol-v3.3.5`
* 运行上传指令：

```
java -jar buglyqq-upload-symbol.jar -appid 4a76xxxxx -appkey 64fa0ebc-aab3-4665-832f-xxxxxxxx -bundleid com.xxxxx.xxxxx -version 2.5.1 -buildNo 25 -platform IOS -inputSymbol /Users/hut/Downloads/yourAppName.app.dSYM
```

结果：

```
##[info]atta statistics upload response code: 200 response message: 
##[info]-----------------------------------------------------------------------------
##[info]-----------------------------------------------------------------------------
##[info]上传成功！您可以在异常详情页点击"手工还原"以及时还原堆栈信息。
##[info]-----------------------------------------------------------------------------
##[info]-----------------------------------------------------------------------------
```


## Google Crashlytics 上传iOS 符号表

参考：

[Get readable crash reports in the Crashlytics dashboard](https://firebase.google.com/docs/crashlytics/get-deobfuscated-reports?platform=ios)