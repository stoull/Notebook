
[Frequently asked questions about iCloud Keychain](https://support.apple.com/en-us/HT204085)

[iCloud security and privacy overview](https://support.apple.com/en-us/HT202303)

[How Safe Are Keychain and iCloud Keychain?](https://discussions.apple.com/thread/7606304?start=0&tstart=0)

[How is the System Keychain secured in OS X?](https://apple.stackexchange.com/questions/53579/how-is-the-system-keychain-secured-in-os-x)

[Mac上的钥匙串究竟如何安全?](https://www.zhihu.com/question/58502851)

[Security Flaw in OS X displays all keychain passwords in plain text](https://medium.com/@brentonhenry/security-flaw-in-os-x-displays-all-keychain-passwords-in-plain-text-a530b246e960)





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