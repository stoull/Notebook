#Xcode中Command+T打开终端

使用Xcode Behaviors功能，创建使用快捷键`Command`+`T`打开工程目录所在的终端

1. 创建打开终端的`.sh`脚本。

	将如下代码保存为名为`open-terminal.sh`的脚本文件，保存到你喜欢的，不太会更改的地方就行，之后每次按快捷键会运行这个文件：
	
	```
	#!/bin/bash
	open -a Terminal "`pwd`"
	```
	注意确保`open-terminal.sh`文件的权限用户可运行。
2. Xcode(屏幕最左上角，apple右边) -> Behaviors -> Edte Behaviors
3. `+`添加Custom的Behaviors, 填写一个自己能识别用处的名字，在最Behaviors这最右边可以设置这它的快捷键，如command+t.
4. 左边设置Behaviors具体内容的区域，拉到最底下，勾选`Run`，这个Behaviors用来运行脚本，然后选择刚保存的脚本文件。