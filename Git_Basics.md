
>
 git有三种状态：Change, Staged, Committed。
 Change(Unstaged)：你改动了一个，没有调用任何git命令前，就是这种状态。
 Staged：调用git add或者git commit -a之后，进入Staged状态，表示申明要变动了。
 Committed：Commit，生成新的版本commit号，进入此状态。
 */

```

// Git Basics - Getting a Git Repository


// * 初始化一个git仓库
// ====================================================================
git init


// * 把这个文件夹的内容加入版本控制
// ====================================================================
git add *.c
git add LICENSE
git commit -m 'initial project version' // 初始化commit,log message为initial project version

// Remove untracked files from the working tree
git-clean -


// * 克隆一个仓库
// ====================================================================
git clone https://github.com/libgit2/libgit2
git clone https://github.com/libgit2/libgit2 mylibgit //给克隆下来的仓库取一个自己的名字


// * 查看git 文件状态
// ====================================================================
git status
git status -s  or git status --short
/*
Tracked: unmodified, modified, staged
Untracked: not in your last snapshot and are not in your staging area
*/


// * 将文件加入版本控制
// ====================================================================
git add yourFileName // yourFileName must integrity like ' LB_OutLinkCell.h ' include '.h'



// * 设置忽略文件
// ====================================================================
touch .gitignore  //gitignore配置文件https://github.com/github/gitignore
全局配置方法：
Git config —global core.excludesfile = ~/.gitignore



// * 查看具体那一行代码作了修改
// ====================================================================
git diff XXXX

git diff --cached



// * committing your Changes
// ====================================================================
git commit

git commit -m "Story 182: Fix benchmarks for speed" // 用-m 把commit message 加进去

// use git commit -a to skip the git add part 、、Git automatically stage every file
git commit -a




// * 提交到remote服务器
// ====================================================================
git remote add origin https://github.com/stoull/CoarseExchange.git
git push -u origin master




// * 移除文件版本控制
// ====================================================================
git rm yourFileName // yourFileName must integrity like ' LB_OutLinkCell.h ' include '.h'
// also
git rm log/\*.log
git rm \*~

git rm -f // 用-f是强制移除文件




// * 重命名文件
// ====================================================================
git mv file_from file_to
// 相当于
mv file_from file_to
git rm file_from
git add file_to

@"fetch更新本地仓库两种方式："
// ====================================================================
//方法一
git fetch origin master //从远程的origin仓库的master分支下载代码到本地的origin master

git log -p master.. origin/master//比较本地的仓库和远程参考的区别

git merge origin/master//把远程下载下来的代码合并到本地仓库，远程的和本地的合并

//方法二
git fetch origin master:temp //从远程的origin仓库的master分支下载到本地并新建一个分支temp

git diff temp//比较master分支和temp分支的不同

git merge temp//合并temp分支到master分支

git branch -d temp//删除temp



// *查看commit历史记录 log
// ====================================================================
git log

git log -p -2
/*One of the more helpful options is -p, which shows the difference introduced in each commit. You can also use -2, which limits the output to only the last two entries:*/

git log --stat
/*the --stat option prints below each commit entry a list of modified files, how many files were changed, and how many lines in those files were added and removed.*/

git log --pretty=oneline // or short,full,fuller,or format
git log --pretty=format:"%h - %an, %ar : %s"
/*This option changes the log output to formats other than the default. A few prebuilt options are available for you to use. The oneline option prints each commit on a single line, which is useful if you’re looking at a lot of commits. In addition, the short, full, and fuller options show the output in roughly the same format but with less or more information*/

git log --pretty=format:"%h %s" --graph
/* showing your branch and merge history */

// 限制log输出的消息
// ====================================================================
git log -2 //-n show the last n commits
git log --since=2.weeks
git log -S function_name

// 条件查找
// ====================================================================
git log --pretty="%h - %s" --author=gitster --since="2008-10-01" \ --before="2008-11-01" --no-merges -- t/


// * 撤销，重做
// ====================================================================
git commit --amend //当你commit之后发现有文件没有加到stage或写错了commit message
// 你可以
git commit -m 'initial commit'
git add forgotten_file
git commit --amend

// * Unstaging a Staged File 这个在你删除文件之后，可用于复原工作
// ====================================================================
git reset HEAD yourFileName

// 完了之后用git status 会告诉你要用下面这个命令
git checkout -- yourFileName

// * 还原一个已修改的文件
// ====================================================================
git checkout -- yourFileName
git checkout -- [file] // 很危险无法撤消，除非你知道所有这些改变你都放弃的话，就可以

// * git远程服务器版本控制
// ====================================================================
git clone https://github.com/stoull/ticgit
git remote
git remote -v //
git remote add shortCutName https://github.com/stoull/ticgit  //  use the string pb on the command line in lieu of the whole URL
git fetch shortCutName

git fetch [remote-name]
git push origin master
git remote show origin
git remote rename pb paul
git remote rm paul

// git 加标记 Tag
// ====================================================================
git tag
git tag -1 "v1.8.5*" // 只查看v1.8.5*这些版本的tag

// git tag 分为lightweight and annotated， lightweight 像commit一样打个tag， 而annotated是复制所有内容存入数据库
// annotated
git tag -a v1.4 -m "my version 1.4" // 创建一个annotated 标记
git show v1.4

// lightweight
git tag v1.4-lw
git tag

// 查看tag记录
git log --pretty=oneline

// sharing tags push 不分把打的tag传上去需要你这样才可以
git push origin [tagname]
// push 所有tags
git push origin --tags

// chect out Tags
git checkout -b [branchname] [tagname]

// 给 git 命令用 shortCut
// ====================================================================
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

git stash


// 和远程之间的互动

git clone https://github.com/USERNAME/REPOSITORY.git
# Clones a repository to your computer

git fetch remotename
# Fetches updates made to a remote repository

git merge remotename/branchname
# Merges updates made online with your local work

git pull remotename branchname
# Grabs online updates and merges them with your local work



@"Git基本常用命令如下："
// ====================================================================

mkdir：         XX (创建一个空目录 XX指目录名)

pwd：          显示当前目录的路径。

git init          把当前的目录变成可以管理的git仓库，生成隐藏.git文件。

git add XX       把xx文件添加到暂存区去。

git commit –m “XX”  提交文件 –m 后面的是注释。

git status        查看仓库状态

git diff  XX      查看XX文件修改了那些内容

git log          查看历史记录

git reset  –hard HEAD^ 或者 git reset  –hard HEAD~ 回退到上一个版本

(如果想回退到100个版本，使用git reset –hard HEAD~100 )

cat XX         查看XX文件内容

git reflog       查看历史记录的版本号id

git checkout — XX  把XX文件在工作区的修改全部撤销。

git rm XX          删除XX文件

git remote add origin https://github.com/tugenhua0707/testgit 关联一个远程库

git push –u(第一次要用-u 以后不需要) origin master 把当前master分支推送到远程库

git clone https://github.com/tugenhua0707/testgit  从远程库中克隆

git checkout –b dev  创建dev分支 并切换到dev分支上

git branch  查看当前所有的分支

git checkout master 切换回master分支

git merge dev    在当前的分支上合并dev分支

git branch –d dev 删除dev分支

git branch name  创建分支

git stash 把当前的工作隐藏起来 等以后恢复现场后继续工作

git stash list 查看所有被隐藏的文件列表

git stash apply 恢复被隐藏的文件，但是内容不删除

git stash drop 删除文件

git stash pop 恢复文件的同时 也删除文件

git remote 查看远程库的信息

git remote –v 查看远程库的详细信息

git push origin master  Git会把master分支推送到远程库对应的远程分支上


```


#Git 常见用法

### 1. 如文件名含有空格，则用 “” 将文件名括起来

### 2. 如果不是通过 git 删除的文件，如用rm 或Finder中删除的文件。如果也要在git中移除对应版本管理
用这个命令

	git ls-files --deleted -z | xargs -0 git rm

> 来源[stackoverflow](https://stackoverflow.com/questions/492558/removing-multiple-files-from-a-git-repo-that-have-already-been-deleted-from-disk "stackoverflow") 







