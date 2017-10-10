
## Keychain 钥匙串

[Keychain Securing](https://code.tutsplus.com/tutorials/securing-ios-data-at-rest--cms-28528)

存储大文件最好用苹果的Data Protection API 做安全处理，但处理一些小的数据信息如用户密码,ID等一些敏感信息，或或网络授权的Unique token。这个时候都好是用KeyChain去存储这些信息。

KeyChain是系统提供的服务，将用户数据以加密的方式存储于本地，这样即使你将APP删除了，对应的信息还是存在的，在下次安装后仍可以获取之前存存储的信息。如果开启的iCloud同步，KeyChain存储的这些数据，将同步用户的每一个终端。

KeyChain存储数据的安全标准或者白皮书之类的还没有找到，目前的参考的是：[How Safe Are Keychain and iCloud Keychain?](https://discussions.apple.com/thread/7606304?start=0&tstart=0) 和 [iCloud security and privacy overview](https://support.apple.com/en-us/HT202303)。
注意在很多情况下： **KeyChain的数据加密是基于用户设置的密码或 Touch ID**

使用KeyChain可以直接使用官方C写的Keychain Services API,也有一些特别好的第三方库可以使用，[Strongbox](https://github.com/granoff/Strongbox)(Swift) 和[SAMKeychain](https://github.com/soffes/SAMKeychain)(Object-C)

每一项密码的存储都一个service name一个account以及需要存储的密码，为了存储对应的信息，需要取一个独一无二的service name，像Bundle Identifier一样。形如：com.apple.account.IdentityServices.token。对应的用户名可以是用户的用户名或APP服务的名t称，具体看功能。如：

![](./source/keychain_detail.png)


## KeyChain存储密码

#### KeyChain中数据操作的Dictionary

```
import Security

class func passwordQuery(service: String, account: String) -> Dictionary<String, Any>
{
    let dictionary = [
        kSecClass as String : kSecClassGenericPassword,
        kSecAttrAccount as String : account,
        kSecAttrService as String : service,
        kSecAttrAccessible as String : kSecAttrAccessibleWhenUnlocked //If need access in background, might want to consider kSecAttrAccessibleAfterFirstUnlock
    ] as [String : Any]
     
    return dictionary
}
```
上面包这个字典包含了 service 和 account 以及处理的密码类型 kSecClassGenericPassword.也可以设置安全保护类型 `kSecAttrAccessible`，这里设置的为：`kSecAttrAccessibleWhenUnlocked`。

### KeyChain中增加密码
在很多接口方法都使用相似的字典作为参数。下面用一个方法生成这个字典

```
@discardableResult class func setPassword(_ password: String, service: String, account: String) -> Bool
{
    var status : OSStatus = -1
    if !(service.isEmpty) && !(account.isEmpty)
    {
        deletePassword(service: service, account: account) //delete password if pass empty string. Could change to pass nil to delete password, etc
         
        if !password.isEmpty
        {
            var dictionary = passwordQuery(service: service, account: account)
            let dataFromString = password.data(using: String.Encoding.utf8, allowLossyConversion: false)
            dictionary[kSecValueData as String] = dataFromString
            status = SecItemAdd(dictionary as CFDictionary, nil)
        }
    }
    return status == errSecSuccess
}
```

### KeyChain中删除密码

```
@discardableResult class func deletePassword(service: String, account: String) -> Bool
{
    var status : OSStatus = -1
    if !(service.isEmpty) && !(account.isEmpty)
    {
        let dictionary = passwordQuery(service: service, account: account)
        status = SecItemDelete(dictionary as CFDictionary);
    }
    return status == errSecSuccess
}
```
### KeyChain中查询密码

```
class func password(service: String, account: String) -> String //return empty string if not found, could return an optional
{
    var status : OSStatus = -1
    var resultString = ""
    if !(service.isEmpty) && !(account.isEmpty)
    {
        var passwordData : AnyObject?
        var dictionary = passwordQuery(service: service, account: account)
        dictionary[kSecReturnData as String] = kCFBooleanTrue
        dictionary[kSecMatchLimit as String] = kSecMatchLimitOne
        status = SecItemCopyMatching(dictionary as CFDictionary, &passwordData)
         
        if status == errSecSuccess
        {
            if let retrievedData = passwordData as? Data
            {
                resultString = String(data: retrievedData, encoding: String.Encoding.utf8)!
            }
        }
    }
    return resultString
}
```

## KeyChain存储公钥和私钥
推荐使用keychain存储公钥和私钥，像APP需要存储 EC 或 RSA `SecKey`信息。
像使用keychain存储密码一样，就是告诉keychain现在要存储的是key，public 或private，只要指定对应的类型就可以。
下面是存储 RSA 私钥 `SecKey`的代码：

```
class func keyQuery(service: String, account: String) -> Dictionary<String, Any>
{
    let tagString = "com.mydomain." + service + "." + account
    let tag = tagString.data(using: .utf8)! //Store it as Data, not as a String
    let dictionary = [
        kSecClass as String : kSecClassKey,
        kSecAttrKeyType as String : kSecAttrKeyTypeRSA,
        kSecAttrKeyClass as String : kSecAttrKeyClassPrivate,
        kSecAttrAccessible as String : kSecAttrAccessibleWhenUnlocked,
        kSecAttrApplicationTag as String : tag
        ] as [String : Any]
     
    return dictionary
}
 
@discardableResult class func setKey(_ key: SecKey, service: String, account: String) -> Bool
{
    var status : OSStatus = -1
    if !(service.isEmpty) && !(account.isEmpty)
    {
        deleteKey(service: service, account:account)
        var dictionary = keyQuery(service: service, account: account)
        dictionary[kSecValueRef as String] = key
        status = SecItemAdd(dictionary as CFDictionary, nil);
    }
    return status == errSecSuccess
}
 
@discardableResult class func deleteKey(service: String, account: String) -> Bool
{
    var status : OSStatus = -1
    if !(service.isEmpty) && !(account.isEmpty)
    {
        let dictionary = keyQuery(service: service, account: account)
        status = SecItemDelete(dictionary as CFDictionary);
    }
    return status == errSecSuccess
}
 
class func key(service: String, account: String) -> SecKey?
{
    var item: CFTypeRef?
    if !(service.isEmpty) && !(account.isEmpty)
    {
        var dictionary = keyQuery(service: service, account: account)
        dictionary[kSecReturnRef as String] = kCFBooleanTrue
        dictionary[kSecMatchLimit as String] = kSecMatchLimitOne
        SecItemCopyMatching(dictionary as CFDictionary, &item);
    }
    return item as! SecKey?
}

```

## KeyChain访问的密码保护
设置对应的存储安全类型为`kSecAttrAccessibleWhenUnlocked`,这个时候只有在设置处于锁屏的状态下对应的数据才是不可访问的，而还是依赖于用户是否设置密码或 Touch ID。如果用户没有设置密码的话就存在风险。

使用`kSecAccessControlApplicationPassword` KeyChain数据访问类型，可以使用指定的密码进行加密码。这样在用户没有设置密码或 Touch ID的时候，数据仍使用指定的密码加密，如果用户有设置密码或 Touch ID也不影响，只是多增加了一层加密。这样的话数据就会安全很多。

使用方案一：可将密码存储于服务器上。当你的App连接上服务器，并通过认证后，这个时候服务器可通过HTTPS返回的正确密码来访问KeyChain上的item。 最好是使用这种方法处理对应的密码。将密码写在代码之中，这种硬编码的方式不太好。

使用方案二：让用户来设置密码，如果用户没有设置密码或Touch ID，这个时候就我们自己去保证用户设置密码的安全性（使用 [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)）。

**`kSecAccessControlApplicationPassword`在iOS9以上有用**

```
if #available(iOS 9.0, *)
{
	// 将这段代码替换上面查询密码的那段代码
    var error: Unmanaged<CFError>?
    let accessControl = SecAccessControlCreateWithFlags(kCFAllocatorDefault, kSecAttrAccessibleWhenUnlocked, SecAccessControlCreateFlags.applicationPassword, &error)
    if accessControl != nil
    {
        dictionary[kSecAttrAccessControl as String] = accessControl
    }
     
    let localAuthenticationContext = LAContext.init()
    let theApplicationPassword = "passwordFromServer".data(using:String.Encoding.utf8)!
    localAuthenticationContext.setCredential(theApplicationPassword, type: LACredentialType.applicationPassword)
    dictionary[kSecUseAuthenticationContext as String] = localAuthenticationContext
}
```

在前面那个查询密码的方法中，对应的参数使用的是`kSecAttrAccessible`,这里在字典里面用的是`kSecAttrAccessControl`两个参数只是使用一个，不然会得到`OSStatus`为`50`的错误。

## 用户认证授权
从iOS8开始, 可以设置存储到KeyChain的数据，在访问的时候需要通过用户的密码或Touch ID进行认证，认证通后才能访问对应的数据。系统默认Touch ID为优先的认证方式，失败后才推证密码界面进行认证。将数据存储到KeyChain是不需要进行认证的。

可以设置`.userPresence`来设置需要通过访问认证对应的数据。但如果用户没有设置密码信息，这种方式就会认证失败。

```
if #available(iOS 8.0, *)
{
    let accessControl = SecAccessControlCreateWithFlags(kCFAllocatorDefault, kSecAttrAccessibleWhenUnlockedThisDeviceOnly, .userPresence, nil)
    if accessControl != nil
    {
        dictionary[kSecAttrAccessControl as String] = accessControl
    }
} 
```

这种方法可以很好的防止APP被他人恶意使用。

如果你的APP没有服务端的密码支持，这种方式也是终端授权的首选方式。

在询问授权的时候，可以向用户提供一些文字，说明需要要授权的缘由。

	dictionary[kSecUseOperationPrompt as String] = "Authenticate to retrieve x"
	
当使用`SecItemCopyMatching()`查询数据的时候，它会调用授权的界面等待用户使用指纹或密码去授权。`SecItemCopyMatching()`会一直等到用户完成对应的认证才返回对应的结果。返回需要在主线程中处理各种UI交互。

```
DispatchQueue.global().async
{
    status = SecItemCopyMatching(dictionary as CFDictionary, &passwordData)
    if status == errSecSuccess
    {
        if let retrievedData = passwordData as? Data
        {
            DispatchQueue.main.async
            {
                //... do the rest of the work back on the main thread
            }   
        }
    }
}
```

同样的，如果在对应的参数字典中设置了`kSecAttrAccessControl`，就需要移除`kSecAttrAccessible`，两者只能使用一个，不能同时作用去查询。

对应的Object-C代码：
```
UIDevice *device = [UIDevice currentDevice];
    if ([device.systemVersion integerValue] >= 8.0) {
        
        // 设置查询变量
        NSMutableDictionary *dictionary = [NSMutableDictionary dictionary];
        [dictionary setObject:@"kSecClassGenericPassword" forKey:@"kSecClass"];
        [dictionary setObject:@"com.stoull.hut" forKey:@"kSecAttrServer"];
        [dictionary setObject:@"hut" forKey:@"kSecAttrAccount"];
        CFErrorRef error;
        
        // 获取 kSecAttrAccessControl 值
        SecAccessControlRef accessControl = SecAccessControlCreateWithFlags(kCFAllocatorDefault, kSecAttrAccessibleWhenUnlockedThisDeviceOnly, kSecAccessControlUserPresence, &error);
        if (accessControl != nil) {
            [dictionary setObject:(__bridge id _Nonnull)(accessControl) forKey:@"kSecAttrAccessControl"];
        }
        [dictionary setObject:@"I need you" forKey:@"kSecUseOperationPrompt"];
        
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 1), ^{
            CFTypeRef passwordData;
            CFDictionaryRef diction = (__bridge CFDictionaryRef)dictionary;
            
            // 开始授权
           OSStatus status = SecItemCopyMatching(diction, &passwordData);
            if (status == errSecSuccess) {
                
                //  成功之后需要回主线程做动作
                dispatch_async(dispatch_get_main_queue(), ^{
                    
                    //
                });
            }
        });
        
    }
```

## 最后：
如果用户没有设置密码或指纹信息，KeyChain和Data Protection APIs都没有进行加密码。虽然苹果一直在升级，但在处理一些敏感的数据的时候，还是多注意数据的安全性，以防被攻击。

学习资料：iOS安全白皮书 [About Software Security](https://developer.apple.com/library/content/documentation/Security/Conceptual/Security_Overview/Introduction/Introduction.html#//apple_ref/doc/uid/TP30000976)

[About Keychain Services](https://developer.apple.com/library/content/documentation/Security/Conceptual/keychainServConcepts/01introduction/introduction.html#//apple_ref/doc/uid/TP30000897)


[How Safe Are Keychain and iCloud Keychain?](https://discussions.apple.com/thread/7606304?start=0&tstart=0)

[How is the System Keychain secured in OS X?](https://apple.stackexchange.com/questions/53579/how-is-the-system-keychain-secured-in-os-x)

Apple Support:

[iCloud security and privacy overview](https://support.apple.com/en-us/HT202303)

[Frequently asked questions about iCloud Keychain](https://support.apple.com/en-us/HT204085)
