
## Keychain 钥匙串

[Keychain Securing](https://code.tutsplus.com/tutorials/securing-ios-data-at-rest--cms-28528)

存储大文件最好用苹果的Data Protection API 做安全处理，但处理一些小的数据信息如用户密码,ID等一些敏感信息，或或网络授权的Unique token。这个时候都好是用KeyChain去存储这些信息。

KeyChain是系统提供的服务，将用户数据以加密的方式存储于本地，这样即使你将APP删除了，对应的信息还是存在的，在下次安装后仍可以获取之前存存储的信息。如果开启的iCloud同步，KeyChain存储的这些数据，将同步用户的每一个终端。

KeyChain存储数据的安全标准或者白皮书之类的还没有找到，目前的参考的是：[How Safe Are Keychain and iCloud Keychain?](https://discussions.apple.com/thread/7606304?start=0&tstart=0) 和 [iCloud security and privacy overview](https://support.apple.com/en-us/HT202303)。

使用KeyChain可以直接使用官方C写的Keychain Services API,也有一些特别好的第三方库可以使用，[Strongbox](https://github.com/granoff/Strongbox)(Swift) 和[SAMKeychain](https://github.com/soffes/SAMKeychain)(Object-C)

每


```
// 从KeyChain中查找密码
- (NSString *)querypasswordWithServer:(NSString*)keychainService andAccount:(NSString*)account {
    //query for existing item
    NSDictionary *query = @{(__bridge id)kSecClass : (__bridge id)kSecClassGenericPassword,
                            (__bridge id)kSecAttrService : keychainService,
                            (__bridge id)kSecAttrAccount : account,
                            (__bridge id)kSecAttrSynchronizable : @YES,
                            (__bridge id)kSecReturnAttributes : (__bridge id)kCFBooleanTrue,
                            (__bridge id)kSecReturnData : (__bridge id)kCFBooleanTrue};
    
    CFDictionaryRef valueAttributes = NULL;
    OSStatus status = SecItemCopyMatching((__bridge CFDictionaryRef)query,
                                          (CFTypeRef *)&valueAttributes);
    NSDictionary *attributes = (__bridge_transfer NSDictionary *)valueAttributes;
    //attributes has 8 key/value pairs but I don't see the stored encoded value as one of them
    
    if (status == errSecSuccess) {
        NSString* myString = [[NSString alloc] initWithData:[attributes objectForKey:(__bridge id)kSecValueData] encoding:NSUTF8StringEncoding];
        //myString is @""
        return myString;
    }
    return nil;
}
```



学习资料：iOS安全白皮书 [About Software Security](https://developer.apple.com/library/content/documentation/Security/Conceptual/Security_Overview/Introduction/Introduction.html#//apple_ref/doc/uid/TP30000976)

[About Keychain Services](https://developer.apple.com/library/content/documentation/Security/Conceptual/keychainServConcepts/01introduction/introduction.html#//apple_ref/doc/uid/TP30000897)


[How Safe Are Keychain and iCloud Keychain?](https://discussions.apple.com/thread/7606304?start=0&tstart=0)

[How is the System Keychain secured in OS X?](https://apple.stackexchange.com/questions/53579/how-is-the-system-keychain-secured-in-os-x)

Apple Support:

[iCloud security and privacy overview](https://support.apple.com/en-us/HT202303)

[Frequently asked questions about iCloud Keychain](https://support.apple.com/en-us/HT204085)