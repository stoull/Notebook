# 系统或开发用到的工具

### 1 `open-terminal.sh`：在Xcode中使用快捷键打开终端并进入项目所在的目录



 使用当前目录打开终端，可配合开发工具使用，如Xcode -> Settings -> Behaviors -> + -> Custom 可取一个‘Open Termianl’的名字 -> 按Command设置快捷键如‘Command+T’ -> 左侧最底部，Run choice the script

> Command+T 之前是打开新Tab的快截键，按按如下改回来：
`Setting(command,) -> keyBindings -> Customized(x) 中找到被替换的New Window Tab`

### 2. `fix-wrong-folder-extension.py`：片文件目录有后缀的问题

查找当前目录下，所有有后缀名（extension）的目录, 有后缀名的目录会导致在某些系上会按文件打开，而导致文件夹打开失败

`python3 fix-wrong-folder-extension.py -d /path/to/your/file --withfix`

* `-d`: 为所需要处理的目录
* `--withfix`: 对所查找到的不正确目录名称进行移除后缀的操作