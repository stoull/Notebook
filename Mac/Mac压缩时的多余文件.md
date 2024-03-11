# Mac压缩时的多余文件

在使用Mac系统自带的压缩工具压缩文件夹的时候，如果这个压缩文件在Windows或其它系统中解压，会出现多余的文件夹或文件，如：`_MACOSX`, `.DS_Store`,或其它的`.*`文件, 前两个文件在MacOS系统上都是对用户不可见的文件，如果在Mac上解压，将不会看到这些文件。

* `_MACOSX`： It's Extra Metadata only used for MacOS。像文件的编码，文件系统的支持，字体信息等？
* `.DS_Store`： Desktop Services Store， 类似windows上的`destop.ini`文件。是由`Finder`创建的，用来存储用户设置用的信息，如图标的位置，背景图等信息。


## 压缩的时候怎么移除这些文件

因为这些文件是MacZip GUI(即选中要压缩的文件->右键->压缩)压缩时自动加上去，方便Mac用户的，如果给其它的系统用户，就不需要这些文件了。

因为这是系统工龄自动添加的，思路一就是不使用系统的图形压缩工具。二因为这两个文件都是针对文件夹的，思路可以通过压缩文件，而不是压缩文件夹来实现。

### 法一：使用`zip`命令
* 通过**Terminal**使用`zip`命令进行压缩
	1. 打开`Terminal`App
	2. 使用`cd`命令进入想要压缩的文件夹内
	3. 使用如下命令过过滤不需要添加进压包的文件，这里是`_MACOSX`及所有的`.*`文件（包`.DS_Store`文件）
	
		`zip -r dir.zip . -x '**/.*' -x '**/__MACOSX'`
	
		或者只过滤`.DS_Store`文件：
	
		`zip -r dir.zip . -x '**/.DS_Store'`

示例：
像你桌面上有一个名为`bundle`的文件夹，你想把这个文件夹压缩给Windows的用户用，使用如下的命令：

	cd ~/Desktop/bundle
	zip -r bundle.zip . -x '.*' -x '__MACOSX'

这个时候，会在`bundle`的文件夹内生成一个名为`bundle.zip`文件,这个压缩包就不会有`__MACOSX`和`.*`文件。

* 使用第三方压缩工具
	* [Keka.github](https://github.com/aonez/Keka)
	* [Keka.io](https://www.keka.io/en/)


## 法二：只压缩文件 目前测试不行！！！！！

<!--### 法二：只压缩文件

进入想要压缩的目录内，选中所有的文件， 然后右键，压缩。这个时候会生成一个名为`Archive.zip`的文件。因为不是压缩的文件夹，所以不包含不需要的文件。-->



