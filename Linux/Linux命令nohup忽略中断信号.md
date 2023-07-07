# Linux命令nohup后台运行

- `nohup` 英文全称 no hang up（不挂起）, 命令用于运行程序或者命令，并忽略所有中断信号SIGHUP。SIGHUP是当前控制终端关闭时发送到进程的信号。

- 通常，当您通过SSH运行命令时，如果连接断开，或者退出SSH，SSH会话将终止在当前TTY启动的进程。

- 如果你不想被某一程序被终止，可以使用`nohup`命令。它将忽略所有中断信号，启动的命令程序将继续运行。

- nohup 命令，在默认情况下（非重定向时），会输出一个名叫 nohup.out 的文件到当前目录下，如果当前目录的 nohup.out 文件不可写，输出重定向到 $HOME/nohup.out 文件中。

## nohup命令
`nohup Command [ Arg … ] [　& ]`

`Command`：要执行的命令。
`Arg`：一些参数，可以指定输出文件。
`&`：让命令在后台执行，终端退出后命令仍旧执行。

nohup命令仅接受两个选项--help和--version，除此之外没有任何其它没有任何选项。

## nohup 命令后台运行

nohup在前台使用不是很有用，因为在命令完成之前，您将无法在当前TTY交互。要使nohup启动的进程在后台运行，请在命令末尾添加&符号。

实例:
`nohup python3 -m http.server &`

命令将在后台运行Python的HTTP服务器，并在终端上打印作业ID和进程ID，并将标准输出定向到nohup.out

如果要停止运行，你需要使用以下命令查找到 nohup 运行脚本到 PID，然后使用 kill 命令来删除：

`ps -aux | grep " http.server" `

参数说明:

	- a : 显示所有程序
	- u : 以用户为主的格式来显示
	- x : 显示所有程序，不区分终端机

另外也可以使用 `ps -def | grep "runoob.sh"` 命令来查找。

找到 PID 后，就可以使用 kill PID 来删除。

`kill -9  进程号PID`

#### 标准错误与标准输出重定向

`nohup python3 -m http.server > access.log 2> error.log &`

命令将会把Python的HTTP服务器进程标准输出写入文件access.log，标准错误写入文件error.log。

`nohup python3 -m http.server > http_server.log 2>&1 &` : 将标准输出及标准错误定向到`http_server.log`
