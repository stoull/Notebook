# Mac 终端检查MD5及SHA值

## 各算法的hash值生成
推荐使用：`SHA-256` 和 `SHA3`
其它的算法：`SHA1`, `MD5`, and `CRC32` 这些可能不安全（有概率两个不同的文件会生成相同的hash值）

* 显示文件 `SHA256` 的hash 值：

`shasum -a 256 [filenames]`

* 显示文件 `SHA1` 的hash 值：

`shasum -a 1 [filenames]`

>SHA1 函数返回以 160 位校验和的十六进制值的文本表示形式表示的 40 个字符的字符串。
>531bd67968883a0ec24e8519ccf9d528fff248fe
>或者：F7:A0:E6:E8:A9:2F:B6:92:D4:5C:F2:92:CE:F1:CA:3F:FB:DB:D4:91

* 显示文件 `MD5` 的hash 值：

`md5 -r 256 [filenames]`

示字符串的md5`echo "string" | md5`

* 显示文件 `CRC32 ` 的hash 值：

`crc32 [filenames]`

## 使用checksum文件，检查多个文件的hash值

有时候下载多个文件的时候，可能会包含一个checksum文件，名为`SHA1SUMS`或以`.sha1`、`.xz`为后缀的文件[sha1sum](https://en.wikipedia.org/wiki/Sha1sum), 这个文件以`hash值 对应文件名`一行一行的格式包含了各文件的hash值。当需要检查多个文件的时候，会特别的方便。

checksum 文件有: `md5sum`/`sha1sum`/`sha256sum`

* 检查`SHA256` checksum 文件:

`shasum -a 256 -c [SHA256SUMS]`

* 检查`SHA1` checksum 文件:

`shasum -a 1 -c [SHA1SUMS]`

* 检查`MD5` checksum 文件:

`md5sum -c [MD5SUMS]`

### 生成checksum文件
生成对应的 checksum 文件只要将各个文件以`hash值 对应文件名`一行一行的格式写入到checksum文件中，也可以复制进去，但可以使用`>`操作符：

`shasum -a 256 [files] > [SHA256SUMS]`

例如：`shasum -a 256 sqlite-jdbc-3.36.0.jar > sqlite_SHA256SUMS`

`c0f13672668ec479dbf685dcadf6c2dd2fb44f266f99a90624dde46eb5524aaf  sqlite-jdbc-3.36.0.jar`

[Techniques for verifying shasums conveniently](https://thomask.sdf.org/blog/2019/05/05/techniques-for-verifying-shasums-conveniently.html)