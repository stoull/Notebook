# iOS数据加密
参考资料：[Securing iOS Data at Rest: Encryption](https://code.tutsplus.com/tutorials/securing-ios-data-at-rest-encryption--cms-28786)

[分组密码工作模式](https://zh.wikipedia.org/wiki/分组密码工作模式)

在存储一些大数据文件的时候，如果不想用Apple的Data Protection，这个时候最好是使用加密框架对数据进行加密处理。比如APP存储用户聊天信息，或一些私密的照片或涉及到消费记录信息等等，这个时候一定要对数据进加密码存储。
iOS `Common Crypto`库提供了对 AES 加解密的支持。当然对于APP也有两种加解密的业务流程，一是用户输入密码进行数据的加解密的操作，还有就是通过服务端的提供密钥进行加解密的操作。

## AES(Advanced Encryption Standard)
高级加密标准（英语：Advanced Encryption Standard，缩写：AES），在密码学中又称[Rijndael](https://zh.wikipedia.org/wiki/Rijndael)加密法，是美国联邦政府采用的一种区块加密标准。这个标准用来替代原先的[DES](https://zh.wikipedia.org/wiki/資料加密標準)，已经被多方分析且广为全世界所使用。

相对于DES，AES加密法可以支援更大范围的区块和密钥长度：AES的区块长度固定为128位元，密钥长度则可以是128，192或256位元。对于一些敏感的信息推荐使用256位的密钥。

[RNCryptor](https://github.com/RNCryptor/RNCryptor)是一个非常好的AES加密第三方工具，可快速的集成AES，而不用关心低层的实现。但如果你存储特别特别重要的信息，那最好不要使用第三方你的工具，自己处理会好一些。因为有非常多的APP使用相同的代码的时候，会让黑客的工作简单很多。使用自己的解决方案会让别人黑你的APP困难很多，也可以防止自动化功击。所以在选择第三方的时候最好了解其工作原理，去选择是否选择对应的工具。

## 生成密钥
千万不要使用用户的明文密码作为AES加密的密钥，这样很容易遭字典功击。但如何用户设置的是非常简单的密码？如何可以确保用户使用的密码足够复杂？

### 密码扩展 
AES 的密钥最好使用“盐”（salt）对用户的明文密码作处理，就是[hashing](https://en.wikipedia.org/wiki/Hash_function)多次，salt一系列的随机数据。如果没有对明文加盐处理，就可能使用字典进行暴力功击，而对应用来匹配用户明文密码的表叫“彩虹表”。

产生盐的方法也最好是使用`SecRandomCopyBytes `方法生成密码用的随机字节。如果使用C 中的 `rand()`函数生成随机数，对应随机数很容易预测。

产生salt的代码：

```
var salt = Data(count: 8)
salt.withUnsafeMutableBytes { (saltBytes: UnsafeMutablePointer<UInt8>) -> Void in
    let saltStatus = SecRandomCopyBytes(kSecRandomDefault, salt.count, saltBytes)
    //...
```

这样我们就做好了密码的扩展

### PBKDF2
当然有现成的密码扩展方法：Password-Based Key Derivation Function ([PBKDF2](https://en.wikipedia.org/wiki/PBKDF2))。推荐使用这种方法去生成对应的密钥，这种方法可以防止各种暴力功击：

```
var setupSuccess = true
var key = Data(repeating:0, count:kCCKeySizeAES256)
var salt = Data(count: 8)
salt.withUnsafeMutableBytes { (saltBytes: UnsafeMutablePointer<UInt8>) -> Void in
    let saltStatus = SecRandomCopyBytes(kSecRandomDefault, salt.count, saltBytes)
    if saltStatus == errSecSuccess
    {
        let passwordData = password.data(using:String.Encoding.utf8)!
        key.withUnsafeMutableBytes { (keyBytes : UnsafeMutablePointer<UInt8>) in
            let derivationStatus = CCKeyDerivationPBKDF(CCPBKDFAlgorithm(kCCPBKDF2), password, passwordData.count, saltBytes, salt.count, CCPseudoRandomAlgorithm(kCCPRFHmacAlgSHA512), 14271, keyBytes, key.count)
            if derivationStatus != Int32(kCCSuccess)
            {
                setupSuccess = false
            }
        }
    }
    else
    {
        setupSuccess = false
    }
}
```


## 加密模式和初始化向量
AES是使用CBC密码块链（cipher block chaining (CBC)）加密模式。在CBC模式中，每个明文块先与前一个密文块进行异或后，再进行加密。在这种方法中，每个密文块都依赖于它前面的所有明文块。同时，为了保证每条消息的唯一性，在第一个块中需要使用初始化向量(initialization vector (IV))。对应的图如下：

![Cbc_encryption](./source/Cbc_encryption.png)

![Cbc_decryption](./source/Cbc_decryption.png)

使用`SecRandomCopyBytes`创建初始化向量：

```
var iv = Data.init(count: kCCBlockSizeAES128)
iv.withUnsafeMutableBytes { (ivBytes : UnsafeMutablePointer<UInt8>) in
    let ivStatus = SecRandomCopyBytes(kSecRandomDefault, kCCBlockSizeAES128, ivBytes)
    if ivStatus != errSecSuccess
    {
        setupSuccess = false
    }
}
```

## AES 加解密
使用`CCCrypt`方法进行AES加解密操作。因为使用的是密码块链加密码方式，如果数据不是密码块链的整数倍的时候，我们就要告知对应方法的填充方式。最好是使用现在标准，PKCS7定义如何填充的标准，就使用`KCCOptionPKCS7Padding`选项。

全加密码代码：

```
class func encryptData(_ clearTextData : Data, withPassword password : String) -> Dictionary<String, Data>
{
    var setupSuccess = true
    var outDictionary = Dictionary<String, Data>.init()
    var key = Data(repeating:0, count:kCCKeySizeAES256)
    var salt = Data(count: 8)
    salt.withUnsafeMutableBytes { (saltBytes: UnsafeMutablePointer<UInt8>) -> Void in
        let saltStatus = SecRandomCopyBytes(kSecRandomDefault, salt.count, saltBytes)
        if saltStatus == errSecSuccess
        {
            let passwordData = password.data(using:String.Encoding.utf8)!
            key.withUnsafeMutableBytes { (keyBytes : UnsafeMutablePointer<UInt8>) in
                let derivationStatus = CCKeyDerivationPBKDF(CCPBKDFAlgorithm(kCCPBKDF2), password, passwordData.count, saltBytes, salt.count, CCPseudoRandomAlgorithm(kCCPRFHmacAlgSHA512), 14271, keyBytes, key.count)
                if derivationStatus != Int32(kCCSuccess)
                {
                    setupSuccess = false
                }
            }
        }
        else
        {
            setupSuccess = false
        }
    }
     
    var iv = Data.init(count: kCCBlockSizeAES128)
    iv.withUnsafeMutableBytes { (ivBytes : UnsafeMutablePointer<UInt8>) in
        let ivStatus = SecRandomCopyBytes(kSecRandomDefault, kCCBlockSizeAES128, ivBytes)
        if ivStatus != errSecSuccess
        {
            setupSuccess = false
        }
    }
     
    if (setupSuccess)
    {
        var numberOfBytesEncrypted : size_t = 0
        let size = clearTextData.count + kCCBlockSizeAES128
        var encrypted = Data.init(count: size)
        let cryptStatus = iv.withUnsafeBytes {ivBytes in
            encrypted.withUnsafeMutableBytes {encryptedBytes in
            clearTextData.withUnsafeBytes {clearTextBytes in
                key.withUnsafeBytes {keyBytes in
                    CCCrypt(CCOperation(kCCEncrypt),
                            CCAlgorithm(kCCAlgorithmAES),
                            CCOptions(kCCOptionPKCS7Padding + kCCModeCBC),
                            keyBytes,
                            key.count,
                            ivBytes,
                            clearTextBytes,
                            clearTextData.count,
                            encryptedBytes,
                            size,
                            &numberOfBytesEncrypted)
                    }
                }
            }
        }
        if cryptStatus == Int32(kCCSuccess)
        {
            encrypted.count = numberOfBytesEncrypted
            outDictionary["EncryptionData"] = encrypted
            outDictionary["EncryptionIV"] = iv
            outDictionary["EncryptionSalt"] = salt
        }
    }
 
    return outDictionary;
}
```

全解密代码：

```
class func decryp(fromDictionary dictionary : Dictionary<String, Data>, withPassword password : String) -> Data
{
    var setupSuccess = true
    let encrypted = dictionary["EncryptionData"]
    let iv = dictionary["EncryptionIV"]
    let salt = dictionary["EncryptionSalt"]
    var key = Data(repeating:0, count:kCCKeySizeAES256)
    salt?.withUnsafeBytes { (saltBytes: UnsafePointer<UInt8>) -> Void in
        let passwordData = password.data(using:String.Encoding.utf8)!
        key.withUnsafeMutableBytes { (keyBytes : UnsafeMutablePointer<UInt8>) in
            let derivationStatus = CCKeyDerivationPBKDF(CCPBKDFAlgorithm(kCCPBKDF2), password, passwordData.count, saltBytes, salt!.count, CCPseudoRandomAlgorithm(kCCPRFHmacAlgSHA512), 14271, keyBytes, key.count)
            if derivationStatus != Int32(kCCSuccess)
            {
                setupSuccess = false
            }
        }
    }
     
    var decryptSuccess = false
    let size = (encrypted?.count)! + kCCBlockSizeAES128
    var clearTextData = Data.init(count: size)
    if (setupSuccess)
    {
        var numberOfBytesDecrypted : size_t = 0
        let cryptStatus = iv?.withUnsafeBytes {ivBytes in
            clearTextData.withUnsafeMutableBytes {clearTextBytes in
            encrypted?.withUnsafeBytes {encryptedBytes in
                key.withUnsafeBytes {keyBytes in
                    CCCrypt(CCOperation(kCCDecrypt),
                            CCAlgorithm(kCCAlgorithmAES128),
                            CCOptions(kCCOptionPKCS7Padding + kCCModeCBC),
                            keyBytes,
                            key.count,
                            ivBytes,
                            encryptedBytes,
                            (encrypted?.count)!,
                            clearTextBytes,
                            size,
                            &numberOfBytesDecrypted)
                    }
                }
            }
        }
        if cryptStatus! == Int32(kCCSuccess)
        {
            clearTextData.count = numberOfBytesDecrypted
            decryptSuccess = true
        }
    }
     
    return decryptSuccess ? clearTextData : Data.init(count: 0)
}
```

测试加解密码是否正确：

```
class func encryptionTest()
{
    let clearTextData = "some clear text to encrypt".data(using:String.Encoding.utf8)!
    let dictionary = encryptData(clearTextData, withPassword: "123456")
    let decrypted = decryp(fromDictionary: dictionary, withPassword: "123456")
    let decryptedString = String(data: decrypted, encoding: String.Encoding.utf8)
    print("decrypted cleartext result - ", decryptedString ?? "Error: Could not convert data to string")
}
```


扩展阅读：
[Securing Communications on iOS](https://code.tutsplus.com/articles/securing-communications-on-ios--cms-28529)