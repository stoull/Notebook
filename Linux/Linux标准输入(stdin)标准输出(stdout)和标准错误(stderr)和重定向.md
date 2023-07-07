# Linux标准输入(stdin)标准输出(stdout)和标准错误(stderr)和重定向

Linux 中一切皆文件，比如 C++ 源文件、视频文件、Shell脚本、可执行文件等，就连键盘、显示器、鼠标等硬件设备也都是文件。

一个 Linux 进程可以打开成百上千个文件，为了表示和区分已经打开的文件，Linux 会给每个文件分配一个编号（一个 ID），这个编号就是一个整数，被称为文件描述符（File Descriptor）。

但保留了文件描述符是 0、1、2。当运行命令时，命令启动的进程就会自动打开这三个保留的文件描述符。这三个文件描述符分别表示：

* `0`: 表示标准输入，全称 standard input，简称 stdin，默认是键盘的输入，对应的文件描述符是 /proc/self/fd/0
* `1`: 表示标准输出，全称 standard output，简称 stdout，默认是输出到屏幕，对应的文件描述符是 /proc/self/fd/1
* `2`: 标准错误，全称 standard error，简称 stderr，默认是输出到屏幕，对应的文件描述符是 /proc/self/fd/2

重定向符号：

* `>`: 以擦写的模式重定向至...
* `>>`:  以追加的模式重定向至...
* `&` ：表示等同于的意思
* `/dev/null`: 表示空设备文件

## 标准输入(stdin)

STDIN 标准输入，也就是文件描述符 1，默认为键盘。可以使用重定向符号 `<` 指定文件作为标准输入。

如果你将标准输入替换为文件，重定向符号 `<` 会将文件数据作为标准输入传递给指定的命令。

例如命令` cat < archive.tar | gzip -c > archive.tar.gz` 使用重定向符号 `<` 将`archive.tar` 文件作为标准输入传递给 cat 命令。

cat 命令接收标准输入后，又将 archive.tar 文件内容写入标准输出，最后通过管道传递给gzip命令进行压缩。

`cat < archive.tar | gzip -c > archive.tar.gz`

## 标准输出(stdout)

STDOUT  标准输出，也就是文件描述符 2，默认为屏幕。可以使用追加重定向符号 `>>` 或者覆盖符号`>` 将标准输出重定向到文件。例如命令 `pwd >> log` 会将 pwd 命令的标准输出追加到 log 文件, `pwd > log` 则会将log中的内容清除后，写入pwd的内容。

## 标准错误(stderr)

`ls file2 > file` 命令尝试使用重定向 `>` 符号将标准输出重定向到文件。如果当前目录没有 file2 文件。

ls 命令将会打印一个错误消息 `ls: cannot access 'file2': No such file or directory`，这通常称为标准错误 stderr。

默认情况下，Shell 将标准错误发送到屏幕。如果您需要将标准错误重定向到日志文件，可以使用重定向符号 > / >> 重定向错误。

`ls doesntExistFile.txt 2> errorLog.txt` 将标准错误重定向到errorLog.txt文件了。

## 不想任何输出及`2>&1`
可以将输入定向到空设备文件:`> /dev/null` 就不会任何输出了，输出到黑洞

`2>&1`: 即将标准错误定向到等同于标准输出的位置, 如：

`git push > log.txt 2>&1`

这个时候，屏幕上就真的不会显示任何东西了，标准输出、标准错误，全部都会存到log.txt文件里了。

`2> /dev/null 1> /dev/null` 是直接将标准错误重定向到空设备文件，而 `> /dev/null 2>&1`是将标准错误先重定向到标准输出，然后再重定向到空设备文件。

## 永久重定向

输出重定向有两种方式临时重定向和永久重定向。对于临时重定向，可以使用 > 或者 >> 符号。如果您有很多数据需要重定向，则可以使用 exec 命令进行永久重定向。

来自：
[标准输入/标准输出/标准错误与重定向](https://www.myfreax.com/stdout-stdin-and-redirection/)