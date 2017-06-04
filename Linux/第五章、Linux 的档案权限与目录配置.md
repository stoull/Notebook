# 第五章、Linux 的档案权限与目录配置

#### 权限组

在Linux中，每一个文件及目录都有三种权限组的配置，所有者权限、群组权限和所有用户权限。

- 所有者权限（owner）: 这个是应用于文件所者的权限配置，不会影响它身份的权限
- 用户群组权限（group）: 用户群组权限配置拥有这个些文件的群组的权限，不会影响其它的用户
- 所有用户权限（all users）: 设置系统中其中用户访问这个文件或目录的权限

#### 权限类型：

每个文件或目录的每一个权限组都三种权限配置：

- `r` 读  (read) : 拥有此权限的用户可阅读这个文件的内容
- `w` 写 (write) : 拥有此权限的用户可以写入修复文件或目录的内容
- `x` 执行  (execute) : 执行权限影响用户是否可以运行文件或查看对应的目录内容

使用 ls -l 查看`uninstall.exe `文件：

```
$ ls -l uninstall.exe 
-rw-r--r--  1 stoull  staff  223712 Feb 15  2011 uninstall.exe
```

**-rw-r--r--  1 stoull  staff  223712 Feb 15  2011 uninstall.exe** 这一行的解释如下：

![文件属性理释](http://linux.vbird.org/linux_basic/0210filepermission//centos7_0210filepermission_2.gif)

注意前面十个字符就和权限有关：

![文件属性理释](http://linux.vbird.org/linux_basic/0210filepermission//0210filepermission_3.gif)




