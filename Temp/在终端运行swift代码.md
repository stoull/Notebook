# 在Linux终端运行swift代码

## 安装swift
如果电脑安装了xcode一般会有swift程序，如没有安装可自行安装如用brew进行安装[Homebrew Formulae](https://formulae.brew.sh/formula/swift),如：

`brew install swift`

如果不是macOS, 其它操作系统可从官网下载: [Swift.org Download](https://swift.org/download/)

* swift当前支持的系统有Apple家的系统及Linux, Windows和Android。详见[wiki_swift](https://en.wikipedia.org/wiki/Swift_(programming_language)) 或者 [Swift.org](https://swift.org/)

## 查看swift命令
在终端运行如下命令：

`$ whereis swift`

输出：`/usr/bin/swift`

`$ swift --version`

输出：
`swift-driver version: 1.26.9 Apple Swift version 5.5.1 (swiftlang-1300.0.31.4 clang-1300.0.29.6)`

## REPL(Read-Eval-Print Loop) 运行swift
在终端运行 `swift ` 可以像python一样进入REPL环境：

```
$ swift
Welcome to Swift version 5.5.1-dev.
Type :help for assistance.
```

关于[REPL](https://zh.wikipedia.org/zh-cn/读取﹣求值﹣输出循环)

运行swfit语句：

```
1> print("Hello")
Hello
```

## 使用swift命令

* 新建一个swift文件如：`hello_world.swift`， 并写入代码：

```
import Foundation
print("Hello world")
```

* 运行这个文件`swift ./hello_world.swift `
* 输出：`Hello world`

## 使用swiftc命令编译为可执行文件
### 如果只有一个.swift文件

运行`swiftc ./hello_world.swift` 就可以生成一个名为`hello_world`的可执行性文件

使用`./hello_world`运行这个可执行性文件

### 如果有多个.swift文件
如有两个以上的.swift文件，必须要有一个文件命名为`main.swift`,该文件为程序的入口，像Objective-C或C一样。

如文件`hello_world.swift`中的内容如下：

```
import Foundation
func sayHello() {
    print("Hello world")
}
```

文件`main.swift`中的内容如下：

```
import Foundation
func doSomething() {
    sayHello()
}
doSomething()
```

使用`swiftc`命令将文件 `hello_world.swift`及文件`main.swift`编译为可执行文件:

`$ swiftc ./main.swift ./hello_world.swift `

会生成一个名为`main`的可执行文件，运行:

`$ ./main `
输出：`Hello world`

[A Complete Guide to Swift Development on Linux](https://www.raywenderlich.com/8325890-a-complete-guide-to-swift-development-on-linux)
使用其它的开发工具，编写swift程序：
[Language Server Protocol (LSP)](https://microsoft.github.io/language-server-protocol/)