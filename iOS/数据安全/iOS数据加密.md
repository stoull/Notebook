# iOS数据加密
参考资料：[Securing iOS Data at Rest: Encryption](https://code.tutsplus.com/tutorials/securing-ios-data-at-rest-encryption--cms-28786)


[分组密码工作模式](https://zh.wikipedia.org/wiki/分组密码工作模式)

在存储一些大数据文件的时候，如果不想用Apple的Data Protection，这个时候最好是使用加密框架对数据进行加密处理。比如APP存储用户聊天信息，或一些私密的照片或涉及到消费记录信息等等，这个时候一定要对数据进加密码存储。
iOS `Common Crypto`库提供了对 AES 加解密的支持。当然对于APP也有两种加解密的业务流程，一是用户输入密码进行数据的加解密的操作，还有就是通过服务端的提供密钥进行加解密的操作。

## AES

## 生成密钥

## 服务端的密钥

## 区块加密和初始化向量

## AES 加解密

