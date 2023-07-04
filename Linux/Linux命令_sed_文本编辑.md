#sed 命令

功能强大的流式文本编辑器

Sed is the ultimate stream editor.

sed 是一种流编辑器，它是文本处理中非常重要的工具，能够完美的配合正则表达式使用，功能不同凡响。处理时，把当前处理的行存储在临时缓冲区中，称为“模式空间”（pattern space），接着用sed命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。接着处理下一行，这样不断重复，直到文件末尾。文件内容并没有 改变，除非你使用重定向存储输出。Sed主要用来自动编辑一个或多个文件；简化对文件的反复操作；编写转换程序等。

###格式：

`sed s/day/night/ <old.txt new.txt>`

**例：**

`echo Sunday | sed 's/day/night/'`

输出：`Sunnight`

这个替换命令有六个部分：
>s:	替换命令
>
>/../../:	分隔符
>
>day: 	正则表达式的搜索模式
>
>night:	用来替换成的字符串
>
><old.txt:	将要进查找的文件
>
>new.txt>:	将执行结果存入建新的文件

###分隔符/的转义符: `\`, `_`, `:` 或者 `｜`

例要将`/usr/local/bin`替换成`/common/bin`:

`sed 's/\/usr\/local\/bin/\/common\/bin/' <old.txt >new.txt`

或者

`sed 's:/usr/local/bin:/common/bin:' <old.txt >new.txt`

####符号&对应匹配的字符串
给匹配到的字符串加刮号:
`sed 's/[a-z]*/(&)/' <old.txt >new.txt` :

可多次使用&替代符
`echo "123 abc" | sed 's/[0-9]*/& &/'`

输出：`123 123 abc`

###使用`\1`来使用匹配分组：
\1 表示第一个匹配的分组，\2表示第二个匹配的分组,以此类推。sed最多可保存9个匹配分组

**例：**

保留一行中第一个单词，删除其它的字符：
`sed 's/\([a-z]*\).*/\1/'`

`echo abcd123 | sed 's/\([a-z]*\).*/\1/'`
输出为：`abcd`

交换顺序：
`echo abcd123 | sed 's/\([a-z][a-z]*\) \([a-z][a-z]*\)/\2 \1/'`
输出为：`123abcd`

检测重复单词:
`sed -n '/\([a-z][a-z]*\) \1/p'`

##sed标签
`/g` 全局

`/p` 打印

`/1``/2`指定分组

#### 参考资料
[Sed - An Introduction and Tutorial by Bruce Barnett](https://www.grymoire.com/Unix/Sed.html#uh-0)

[The Grymoire](https://www.grymoire.com/index.html)



