#Markdown 语法笔记

真心不要用Markdown写 Markdown 语法笔记的笔记

[Basic Syntax](https://www.markdownguide.org/basic-syntax/)

## 折叠内容
<details>
  <summary>Click to expand!</summary>
  
## Heading

折叠内容的更多信息

1. A numbered
2. list
 * With some
 * Sub bullets
</details>

## 查看更多内容

<!-- more -->

## 下划线
---
***
___
<hr>
<hr style="border:1px solid gray"> </hr>

##缩进的问题

- **markdown 没有缩进这个概念**

	Markdown 从来都不提供「排版」这一功能，它做的事情只有「标记」——将*、# 等标记符号转换成相应的 HTML 标签。所以接受不缩进这个习惯，你会发现对齐也可以很漂亮。

- **在前面使用一个tab**
	
		在文字前面使用一个tab会一个tab有缩进。注意：两tab就会变成代码了
	
- **使用html语法实现**

	markdown支持html语法，图片居中，换行不换段，缩进这些可以直接用html, 如下一些常用的语法：

```
<p align=center>img</p> //图片居中显示
<br> // 换行

// 空格(不要忘了;号)
半角空格: &ensp;或 &#8194;
全角空格: &emsp;或 &#8195;
不换行空格: &nbsp;或 &#160;
```

##插入html的问题
```
 ```
 这两个符号中间就可以写html代码 
 ```
```

##页内跳转

```
## The Header
```

这样会生成一个 id `#the-header` (空格用 - 代替，大写变小写，”.” 会被移除，如`## 1.1 Hello World` 的id 为 `#11_hello_world`)

连接到对应的id位置,这样写连接:

```
[Link to Header](#the-header)
```

这相当于：
```
<a href="/current_url#the-header">Link to Header</a>
```

## 表格

|  表头   | 表头  |
|  ----  | ----  |
| 单元格  | 单元格 |
| 单元格  | 单元格 |


## 数学公式
详见: [Cmd Markdown 公式指导手册](https://ericp.cn/cmd)

或本地文件: [Markdown 数学公式指导手册.md](./Markdown 数学公式指导手册.md)




