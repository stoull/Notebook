#iOS数据安全

iOS只要涉及到用户数据的存储，就需要考虑数据的安全问题。这里总结下数据安全的问题。

## 系统资源的访问
当我们要访问，获取或修改系统的资源，或App之间进行数据共享的时候，都需要确认获取对应的权限才能获取对应的数据。比如获取相册照片或将相片存入照片，读取用户通讯录，日历信息等。从iOS 10开始，如果要访问系统用户的数据都需要在 `info.plist` 文件中声明本APP想要获取哪些系统权限。
有很多系统提供的 frameworks 我们的APP都可以获取对应的数据，下面的是一些对应的需要在`info.plist` 文件声明的key.

* Bluetooth Sharing: `NSBluetoothPeripheralUsageDescription`
* Calendar: `NSCalendarsUsageDescription`
* CallKit: `NSVoIPUsageDescription`
* Camera: `NSCameraUsageDescription`
* Contacts: `NSContactsUsageDescription`
* Health: `NSHealthShareUsageDescription,NSHealthUpdateUsageDescription`
* HomeKit: `NSHomeKitUsageDescription`
* Location: `NSLocationAlwaysUsageDescription, NSLocationUsageDescription, NSLocationWhenInUseUsageDescription`
* Media Library: `NSAppleMusicUsageDescription`
* Microphone: `NSMicrophoneUsageDescription`
* Motion: `NSMotionUsageDescription`
* Photos: `NSPhotoLibraryUsageDescription`
* Reminders: `NSRemindersUsageDescription`
* Speech Recognition: `NSSpeechRecognitionUsageDescription`
* SiriKit: `NSSiriUsageDescription`
* TV Provider: `NSVideoSubscriberAccountUsageDescription`

比如你要访问系统的相册，你就需要在`info.plist`文件需要对应的声明：

```
<key> NSPhotoLibraryUsageDescription </key>
<string>APPNAME wants access your photos</string>
```
如果没有添加这个声明的话，当你想调用Photos时，程序就会崩溃。

## 数据保护的接口

在应用内部的数据，我们需要考虑数据需要不要需要存储，对于非常重要的数据，比如涉及到用户个人信息的数据，能放内存就放内存，能不存本地就尽量不要存在本地。

但很多时候还是需要将数据存储到本地，这个时候就要考虑数据的安全问题，这个时候最好启用苹果的 "Data Protection"。

>
>Data Protection:
>
>iOS provides APIs that allow an app to make files accessible only while the device is unlocked to protect their contents from prying eyes. With data protection, files are stored in encrypted form and are decrypted only after the user enters his or her passcode.

开启 Data Protection 保护后，会加密app所在的沙盒目录。对应的加密依赖于用户密码，因此用户密码复杂度越高加密就越安全。可在 YOURPROJECT -> Capabilities -> Data Protection 中开启数据保护。开启后也会更新对应的provisioning文件和entitlements文件，加入Data Protection的信息。在entitlements文件中可以看到增加了`Data Protection (com.apple.developer.default-data-protection)`这个属性，这个就是数据保护策略。Data Protection 提供四个级别的数据保护，可见 [NSFileProtectionType](https://developer.apple.com/documentation/foundation/nsfileprotectiontype?language=swift)：

* `none` 没有保护。
* `complete` 当设备锁屏的时候，数据将无法访问。这个是当你启用保护时默认的级别。
* `completeUnlessOpen` 如果文件没有关闭话，不管设备有没有锁屏都可以访问数据。在锁屏的时候也可以创建文件。适合程序在进入后台或用户锁屏后还要进行数据操作的程序，比如上传视频数据到服务端。
* `completeUntilFirstUserAuthentication` 当设备重启后，如果用户没有解锁文件数据将不可访问。当用户解锁后，数据才可以访问，并且以后锁屏之后都可以访问。这个适合用户锁屏后还要进行数据操作的程序，比如播放音乐。

`NSFileProtectionComplete`是默认级别。数据保护过程会发出两个通知`UIApplicationProtectedDataDidBecomeAvailable` 和 `UIApplicationProtectedDataWillBecomeUnavailable `，在这里可通过这两个通知来获取数据是否可访问。这样可根据数据是否保护去访问数据，可防止设备锁屏之后，程序试图访问文件数据而发生崩溃。

> ```
>NotificationCenter.default.addObserver(forName: .UIApplicationProtectedDataDidBecomeAvailable, object: nil, queue: OperationQueue.main, using: { (notification) in
    //...
})
>
NotificationCenter.default.addObserver(forName: .UIApplicationProtectedDataWillBecomeUnavailable, object: nil, queue: OperationQueue.main, using: { (notification) in
    //...
})
>```

当然，也可以通过 `UIApplication.shared.isProtectedDataAvailable` 来判断数据是否可用。

有些时候需要单独设置每一个文件的保护级别，这个也是可以的。当在创建文件或文件夹的时候，可以使用`FileManager`这个类设置对应的保护级别。

>```
let ok = FileManager.default.createFile(atPath: somePath, contents: nil, attributes: [FileAttributeKey.protectionKey.rawValue: FileProtectionType.complete])
do
{
    try FileManager.default.createDirectory(atPath: somePath, withIntermediateDirectories: true, attributes: [FileAttributeKey.protectionKey.rawValue: FileProtectionType.complete])
}
catch
{
    print(error)
}
```

将数据写入文件的时候也可以设置对应的保护级别，`NSData`对象有一个方法，通过这个方法将数据写入文件可以设置对应的保护级别。

>```
let data = Data.init()
let fileURL = try! FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false).appendingPathComponent("somedata.dat")
do
{
    try data.write(to: fileURL, options: ([.atomic, .completeFileProtection]))
}
catch
{
    print(error)
}
```

改别已存在文件的保护级别：

>```
do
{
    try FileManager.default.setAttributes([FileAttributeKey.protectionKey : FileProtectionType.complete], ofItemAtPath: path)
}
catch
{
    print(error)
}
```

也可设置Core Data model的保护级别

>```
let storeURL = docURL?.appendingPathComponent("Model.sqlite")
let storeOptions: [AnyHashable: Any] = [NSPersistentStoreFileProtectionKey: FileProtectionType.complete]
do
{
    try coordinator.addPersistentStore(ofType: NSSQLiteStoreType, configurationName: nil, at: storeURL, options: storeOptions)
}
catch
{
    print(error)
}
>```

## 数据的合法性

**NSSecureCoding**

数据的合法性和完整性，也是数据安全需要考虑的一方面，在代码的时候考虑进去。不要盲目的相信你上次存的数据是完整的，或没有被别人修改过，如果是恶意的修改呢。使用`NSCoding`可以很方便的实现对象存储，但如果要存储用户的账户信息，或者是用于连接服务端的API key，NSCoding是不是会管你存储的东西没有损坏，有没有被修改等。所以在遇到存储敏感信息的时候，可考虑使用 `NSSecureCoding`安全进行对象存储。
和使用`NSCoding`一样的，需要进行存储的类遵守`NSSecureCoding`协议：

```
class ArchiveExample : NSObject, NSSecureCoding
{
    var stringExample : String?
    ...
```
重写自定义类中的 `supportsSecureCoding`

```
static var supportsSecureCoding : Bool
{
    get
    {
        return true
    }
}
```
重写如何自定义类中的反序列化的方法`init?(coder aDecoder: NSCoder)`需要修改成`decodeObject(of:forKey:)`这样可以确保读取的对象信息是正确的。

>```
required init?(coder aDecoder: NSCoder)
{
    stringExample = aDecoder.decodeObject(of: NSString.self, forKey: "string_example") as String?
}
func encode(with aCoder: NSCoder)
{
    aCoder.encode(stringExample, forKey:"string_example")
}
>```

对应的使用`NSSecureCoding`,在使用的是 `NSKeyedUnarchiver` 反序列化存储数据时，确定对应的属性`requiresSecureCoding`为`true`。

>```
class func loadFromSavedData() -> ArchiveExample?
{
    var object : ArchiveExample? = nil
    let path = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)[0] as String
    let url = NSURL(fileURLWithPath: path)
    let fileURL = url.appendingPathComponent("ArchiveExample.plist")
    if FileManager.default.fileExists(atPath: (fileURL?.path)!)
    {
        do
        {
            let data = try Data.init(contentsOf: fileURL!)
            let unarchiver = NSKeyedUnarchiver.init(forReadingWith: data)
            unarchiver.requiresSecureCoding = true
            object = unarchiver.decodeObject(of: ArchiveExample.self, forKey: NSKeyedArchiveRootObjectKey)
            unarchiver.finishDecoding()
        }
        catch
        {
            print(error)
        }
    }
    return object;
}
>```

将`requiresSecureCoding`设置为`true` 也可以防止在使用`NSKeyedUnarchiver`进行存储的时候，自定义类为没有实现`NSSecureCoding`的发生。

>```
func save()
{
    let path = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)[0] as String
    let url = NSURL(fileURLWithPath: path)
    let filePath = url.appendingPathComponent("ArchiveExample.plist")?.path
    let data = NSMutableData.init()
    let archiver = NSKeyedArchiver.init(forWritingWith: data)
    archiver.requiresSecureCoding = true
    archiver.encode(self, forKey: NSKeyedArchiveRootObjectKey)
    archiver.finishEncoding()
    let options : NSData.WritingOptions = [.atomic, .completeFileProtection]
    do
    {
        try data.write(toFile: filePath!, options:options)
    }
    catch
    {
        print(error)
    }
}
>```

除了使用`NSSecureCoding`之外，也最好在数据序列化的时候，检查对应的完整性和合法性。

## 其它场景的数据安全

##### 数据共享时的安全

在使用App Group时，数据需要在主程序和Extension程序之间共享数据，这个时候也需要考虑数据共享时的安全性问题。而且随着没iOS不断的出新版本，用户使用起来越来越方便，但也有很多的新特性如果处理不好，就存在泄漏应用数据的可能性。从iOS 9开始，你可以将你的数据内容放到Spotlight搜索，在iOS10你可以将数据内容曝露给Widgets，像锁屏时屏示展示的天气等。所以在使用这些新功能的时候，特别注意数据共享的安全性。

iOS 10 也加入了Handoff功能，你在Mac上复制一下文件，可直接粘贴到iPhone上面，也要很小心的使用这个功能。可以将敏感的信息禁用掉这个功能，也可以设置没复制后数据在剪切板的有效期。

>```
let stringToCopy = "copy me to pasteboard"
let pasteboard = UIPasteboard.general
if #available(iOS 10, *)
{
    let tomorrow = Date().addingTimeInterval(60 * 60 * 24)
    pasteboard.setItems([[kUTTypeUTF8PlainText as String : stringToCopy]], options: [UIPasteboardOption.localOnly : true, UIPasteboardOption.expirationDate: tomorrow])
}
else
{
    pasteboard.string = stringToCopy
}
>```

##### 数据备份时的安全
在本地存储的文件有可能会自动备份到iTunes或iCloud，虽然备份的时候可以加密，但还是有一些很不一般的文件不想让它备份，不想让它离开这个设备。这个时候可以给文件的`isExcludedFromBackup`的属性设置为`true`。

>```
let path: String = ...
var url = URL(fileURLWithPath: path)
do
{
    var resourceValues = URLResourceValues()
    //or if you want to first check the flag:
    //var resourceValues = try url.resourceValues(forKeys: [.isExcludedFromBackupKey])
    resourceValues.isExcludedFromBackup = true;
    try url.setResourceValues(resourceValues)
}
catch
{
    print(error)
}
>```

##### 有关于屏幕的安全

当程序进入后台的时候，iOS会截取对应的程序屏幕，用于对应程序进入或推出后台的动画。在开启程序切换器，切换不同后台程序时的动画也用的是这个截图，这个截图会存储在设备上面。
所以有些敏感的信息，不希望被系统截图用于切换动画。这个时候可以在程序进入后台前将对应的UI隐藏掉，在程序进入前台前将对应的UI再显示出来，如在一个你不想被截图的ViewController里可以在程序进入后台前将对应的UI隐藏掉

```
NotificationCenter.default.addObserver(self, selector: #selector(didEnterBackground), name: .UIApplicationDidEnterBackground, object: nil)
NotificationCenter.default.addObserver(self, selector: #selector(willEnterForeground), name: .UIApplicationWillEnterForeground, object: nil)
```

记得在view消失后，移除出应的没观察：

```
NotificationCenter.default.removeObserver(self, name: .UIApplicationDidEnterBackground, object: nil)
NotificationCenter.default.removeObserver(self, name: .UIApplicationWillEnterForeground, object: nil)
```

##### 有关于键盘的安全

在使用键盘输入的时候，会有一个自动更正（auto-correct）的功能，当用户在输入的时候，这个功能会去学习，并将学习到的词频记入缓存，在下次输入的时候，就会根用户的习惯自动填充。在安全性高的时候，不希望记住输入的信息缓存，这个时候就要关闭自动更正这个功能。

	textField.autocorrectionType = UITextAutocorrectionType.no

在用户输入密码等敏感信息的时候，也要将输入变成隐式输入：

	textField.isSecureTextEntry = true

##### 有关于日志的安全

调试的日志信息（Debug logs）保存在文件中，并且可以在你编译的App中获取到。所以在你写代码和调试的时候，都要确定没有敏感的信息输出到控制台，像用户的密码等。在发布APP的时候不要忘记检查下对应的输出日志。所以在调试时，查看查看敏感信息都断点会比打印出来安全。

##### 网络缓存安全

### 数据销毁
在删除对应的数据之后，真正的数据并没有完全的被删除，只是移除了文件对应的引用。如果是特别机密的文件就有可能需要将每一byte的数据移除，防止别人恢复。要真正的删除一个文件，一个方法是在删除这个文件之前，随机的写入些数据覆盖原先的文件数据，然后移除出应的文件引用。
下面的C代码可以覆盖原先的文件数据，可以在`FileManager``removeFile `文件前调用这个方法，覆盖文件数据后再删除对应的文件，就可以真正的删除对应的文件数据了。在Swift工程中使用C代码需要`Bridging-Header.h`文件，并添加`int SecureWipeFile(const char *filePath);`文件，可见示例代码:[示例代码]()

```
#import <string.h>
#import <sys/stat.h>
#import <unistd.h>
#import <errno.h>
#import <fcntl.h>
#import <stdio.h>
#import <stdlib.h>
 
#define MY_MIN(a, b) (((a) < (b)) ? (a) : (b))
int SecureWipeFile(const char *filePath)
{
    int lastStatus = -1;
    for (int pass = 1; pass < 4; pass++)
    {
        //setup local vars
        int fileHandleInt = open(filePath, O_RDWR);
        struct stat stats;
        unsigned char charBuffer[1024];
         
        //if can open file
        if (fileHandleInt >= 0)
        {
            //get file descriptors
            int result = fstat(fileHandleInt, &stats);
            if (result == 0)
            {
                switch (pass)
                {
                        //DOD 5220.22-M implementation states that we write over with three passes first with 10101010, 01010101 and then the third with random data
                    case 1:
                        //write over with 10101010
                        memset(charBuffer, 0x55, sizeof(charBuffer));
                        break;
                    case 2:
                        //write over with 01010101
                        memset(charBuffer, 0xAA, sizeof(charBuffer));
                        break;
                    case 3:
                        //write over with arc4random
                        for (unsigned long i = 0; i < sizeof(charBuffer); ++i)
                        {
                            charBuffer[i] = arc4random() % 255;
                        }
                        break;
                         
                    default:
                        //at least write over with random data
                        for (unsigned long i = 0; i < sizeof(charBuffer); ++i)
                        {
                            charBuffer[i] = arc4random() % 255;
                        }
                        break;
                }
                 
                //get file size in bytes
                off_t fileSizeInBytes = stats.st_size;
                 
                //rewrite every byte of the file
                ssize_t numberOfBytesWritten;
                for ( ; fileSizeInBytes; fileSizeInBytes -= numberOfBytesWritten)
                {
                    //write bytes from the buffer into the file
                    numberOfBytesWritten = write(fileHandleInt, charBuffer, MY_MIN((size_t)fileSizeInBytes, sizeof(charBuffer)));
                }
                 
                //close the file
                lastStatus = close(fileHandleInt);
            }
        }
    }
    return lastStatus;
}
```

主要参考这个 [Securing iOS Data at Rest](https://code.tutsplus.com/series/securing-ios-data-at-rest--cms-1185) 的学习笔记总结
