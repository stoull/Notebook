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