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

### 光标称动



