# Linux Shell环境env

## 环境变量

- Shell环境变量(Environment variables)包含了shell所需要的信息及配置信息。
- Shell通过环境变量运行命令、显示提示信息以及搜索可执行文件
- 不同的发行版本有不同的环境变量，并且可以更改。

### `env`

`env`命令可以打印当前的环境变量，或者指定命令运行于自定环境，而不更改当前的环境

路径：`/usr/bin/env`

`-i`: 忽略环境继承，使用空环境，可使用`Name=Value`命令指定参数。

参数格式为：`Name=Value Command`

Name： 环境变量Name, 可使用字母(a-zA-Z)和数字(0-9)和下划线`_`, 一般使用大写字母作为变量名。

Command：为要更改的命令

例：

* 更改TZ环境变量运行`date`命令

`TZ=MST7MDT date` 或者 `env TZ=MST7MDT date`

* 只使用当前环境的`PATH`, `IDIR`及`LIBDIR`运行`make`命令

`env -i PATH=$PATH IDIR=/$HOME/include LIBDIR=/$HOME/lib make`

#### set

```
$ name=jadi
$ desc='A programmer who enjoys cycling and promotes freedom'
$ echo $name
jadi
$ echo $desc
A programmer who enjoys cycling and promotes freedom
```

**注意**

 * `=`号前后不应该有空格
 * 当变量值有空格时，使用双引号""
 * 仅当引用变量时才使用`$`号，定义变量的时候不应该使用

#### unset

```
$ name=jadi
$ echo $name
jadi
$ unset name
$ echo $name
```

#### export

使用`=`号定义的变量只对当前的shell有用，对其它子shell没有用。如果要使用变量在所有shell可用，使用`export`

```
$ export name=jadi
$ echo $name
jadi
$ bash
$ echo $name
jadi
```
#### . (and source)

`.`就是环境变量命令，可在文件`/etc/profile`中找到。它将当前资源路径添加到当前环境变量中。即将`.`(表示当前路径)添加到`PATH`中。如运行可执行性文件时，如果可执行性文件不在`PATH`目录下，则不可执行，这时候需要在文件前加`./file`。

>
Note: If you just execute a file (without source or dot) bash creates a child, runs the executable there and then closes it.

The source command is commonly used when you want to load new/updated environment variables or functions from a script.

#### Aliases

定义别名，可以`~/.bashrc`文件中找到

```
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias testnet='ping 4.2.2.4'
```

## Shell状态

Shell可能有三种启动状态：

1.  login shell: 当使用ssh登录Linux机器，这是交互式的登录状态( interactive login session)
	* 加载`/etc/profile`文件
	* `/etc/profile`文件中有一行运行`/etc/profile.d/`中的所有文件
	* `/home/USERNAME/.bash_profile` `/home/USERNAME/. bash_login ` `/home/USERNAME/. profile ` 这三个文件按顺序查找，只要找到一个就运行，后面的就不会运了
	* 最后运行`/home/USERNAME/.bashrc`,这里设置个人配置

2. Interactive (non-login) shell: 当在机器上打开`terminal`, 这也是交互式的，但不是登录状态。只有两个文件决定环境：
	* `/etc/bash.bashrc`(or /etc/bashrc in some systems)
	* `/home/USERNAME/.bashrc`

3. Non Interactive Shell: 当在shell中运行命令产生新的shell时（如使用bash命令），进入非交互式shell(non interactive)
	* 没有特定的环境文件，但使用`BASH_ENV`变量，这个变量指向什么就运行什么
	* On most Linux distributions, this environment value is not set by default.

> Technically when you run a new command from a shell, a sup-shell starts, runs the commands and then returns back to your shell. This is called "non interactive" shell.

## A few more files

#### `/etc/skel`
This directory contains files which will be used as a starting template for each new user.

#### `.bash_logout`
This runs when you logout from a login shell. In many distros it only clears the screen so the next person will not be able to watch what you were doing before you logout.

[Customize and use the shell environment](https://linux1st.com/1051-customize-and-use-the-shell-environment.html)












