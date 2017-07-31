## 软件包的管理

在任何一个操作系统上面，我们要安装一些程序来。在Windows里面，每一个程序都有一个Setup.exe文件。在Mac上面都有program.dmg文件，这些都只是双击它，同意一大堆不大会看许可证协议就可以安装成功。

##在linux上的的软件包管理
`包管理通常不仅限于软件的一次性安装，还包括了对已安装软件包进行升级的工具`

在linux上，一个软件包通常由二进制程序，库文件，配置文件和帮助文件组成。 其中：

>
* 二进制程序一般都放在/bin,/sbin,/usr/bin,/usr/sbin,/usr/local/bin和/usr/local/sbin这几个目录下边；
* 库文件都放在/lib,/lib64,/usr/lib,/usr/lib64,/usr/local/lib和/usr/local/lib64这些目录下；
* 配置文件一般都是放在/etc这个目录下；
* 而最基本的man帮助文件则是放在/usr/share/man这个目录下的。

在linux上，软件的安装方式一般有四种：

>
* 通用二进制编译:由志愿者把开发完成的源代码编译成二进制文件，打包后发布在网络上，大家都可以通过网络进行下载，到本地之后，经过解压配置就可以使用。
* 软件包管理器：使用包管理工具安装，有时候必须要解决软件包之间的依赖问题，例如rpm和deb等。
* 软件包前端管理工具：可以自动解决软件包依赖关系，例如yum和apt-get等。
* 源码包安装：从网络上下载软件的源码包到本地计算机，用gcc等编译工具编译成二进制文件后才能使用，有时必须要解决库文件的缺失问题。

 
大多数流行的 Linux 包管理工具:

|系统|格式|工具|
|------|------|------|
|CentOS|.deb|yum|
|Ubuntu|.deb|apt、apt-cache、apt-get、dpkg|
|Debian|.deb|apt、apt-cache、apt-get、dpkg|


#### macOS (OS X)上的管理工具

Homebrew: Package manager for OS X, based on Git

$ brew list


这里罗列了各系统的软体管理工组

[List of software package management systems](https://en.wikipedia.org/wiki/List_of_software_package_management_systems '')


##linux 源码安装软件原理
```
make 与 configure
在使用类似 gcc
的编译器来进行编译的过程并不简单，因为一套软件并不会仅有一支程序，而是有一堆程序码文件。所以除了每个主程序与副程序均需要写上一笔编译过程的命令外，还需要写上最终的连结程序。程序小的时候还好，如果是大了，编译命令就麻烦了，这个时候，可以使用　make
这个命令的相关功能来进行编译过程的命令简化了！
当运行 make 时，make 会在当时的目录下搜寻 Makefile或makefile
这个文档,而makefile里面则记录了原始码如何编译的详细信息，make
会自动的判别原始码是否经过变动了
make是一支程序，会支找makefile，那makefile是怎么写的呢？通常软件开发商都会写一会侦测程序来侦测使用者的作业环境，以及该作业环境是否有软件开发商所需要的其它功能，该侦测程序侦测完毕后，就会主动的创建这个
makefile的规则文件，通常地这支侦测程序文档名叫 configure或 config
侦测程序侦测的数据大约如下：
是否有适合的编译器可以编译本软件的程序码
是否已经存在本软件所需要的函数库，或其它需要依赖的软件
操作系统平台是否适合本软件，包括linux 的核心版本
核心的表头定义（header include）是否存在（驱动程序必须要侦测）

make 与 configure运行流程
先运行 configure来创建 makefile，这个步骤一定要成功，接着再以 make
来呼叫所需要的数据来编译即可
最后用 make install 即可安装相关的软件了
```