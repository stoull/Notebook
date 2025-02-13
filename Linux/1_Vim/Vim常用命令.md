# Vim常用命令


[Vim Cheat Sheet](https://vim.rtorr.com)

### 使用`vi`打开或创建文件

`vi filename`: 从文件的开头编辑文件
`vi -r filename`: 恢复对异常退出文件的编辑

在非编辑状态下按`i`进入insecte模式

>
`i` - insert before the cursor
>
>`I` - insert at the beginning of the line
>
>`a` - insert (append) after the cursor

### 退出`vi`编辑器
在非编辑状态按下`:`, 光标会移动屏幕的最低部，这个时候可以输入保存及退出指令

`:w`: 保存当前的编辑内容
`:q`: 退出编辑（不保存）
`:wq`: 保存并退出
`:x`: 保存并退出
`:q!`: 强制退出

### 光标移动

* `0`: 移动到当前行的第一个字符位置(可能是空格)
* `^`: 移动到当前行的第一个非空格字符位置 
* `$`: 移动到当前行的最后一个字符位置(可能是空格)
* `g_`: 移动到当前行的最后一个非空格字符位置 
* `NG`: 移动到第N行
* `gg`: 相当于1G, 移动到第一行
* `G`: 移动到最后一行
* `tx`: 光标移动到字符x的前面, 相反方向为`T`
* `fx`: 光村移动到字符x上面, 相反方向为`F`
* * `cw`: 从当前位置开始删除到下个单词的开头位置

#### 单词的移动
* `w`: 光标移动到下字单词的开头
* `e`: 移动到单词的最后,
	默认单词是由字母和下划画组成,如果移动多个单词:
	* `W`: 移动到下一个空格后的单词的开头
	* `E`: 移动到下一个空格前单词的结尾
* `%`: 移动到下一个`(`, `{`, `[` , 并在对应的闭合部分切换
* `*`: 移动到下一个和光标下的单词一样的单词开头


### 操作

* `y`: yank复制选中区域
* `yy`: 复制当前行,相当于`ddP`,剪切当前行并复制在当前行
* `p`: 粘贴到当前行的下一行
* `P`: 粘贴到当前行的上一行
* `0y$`: 从一行的开头复制到结尾
* `dG`: 从当前行删除到最后一行

#### 撤销及重做

* `u`: undo
* `control+r`: redo
* `.`: 执行上一个操作

#### 搜索

* `/x`: 往文档的前方搜索
* `?x`: 往文档的后方搜索

`n`为移动到搜索结果的下一个, `N`为移动到搜索结果的上一个

#### 翻页

`control+f`: forwad 下一页
`control+b`:  back 上一页

### 文件操作

* `:e`: <path/to/file> → open
* `:w`: → save
* `:saveas`: <path/to/file> → save to <path/to/file>
* `:x, ZZ or :wq`: → save and quit (:x only save if necessary)
* `:q!`: → quit without saving, also: :qa! to quit even if there are modified hidden buffers.
* `:bn`: (resp. :bp) → show next (resp. previous) file (buffer)


## 区块选择

`control+v`: 开启区块选择

