# git stash

Often, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The problem is, you don’t want to do a commit of half-done work just so you can get back to this point later. The answer to this issue is the git stash command.

Stashing takes the dirty state of your working directory — that is, your modified tracked files and staged changes — and saves it on a stack of unfinished changes that you can reapply at any time (even on a different branch).

[Git Tools - Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)

###一个使用场景：

本地有更改，但需要同步拉远程的最新代码，后续进行开发，此时pull会报错，如下：

```
$ git pull

Updating 893120b..7b89f3a
error: Your local changes to the following files would be overwritten by merge:
	RaspberryPi/RaspberryPiNotes.md
Please commit your changes or stash them before you merge.
Aborting
```

看到有`commit your changes` or `stash them before you merge`

一般会先`commit`你的信息，这个时候直接 Fast-forward `git pull`是会报错的。应该会先使用`git pull --rebase`，但这样会产生新的commit, 如果不想发生新的commit, 想保持当前的更改，又想拉远程最新的代码，好像可以`stash them before you merge`, 步骤过程如下：


#### 1. git stash - 存储

```
$git stash
Saved working directory and index state WIP on master: 893120b Add new notes
```

#### 2. git stash list - 列出存储

```
git stash list
stash@{0}: WIP on master: 893120b Add new notes
```

#### 3. git pull - 拉代码

```
git pull

Updating 893120b..7b89f3a
Fast-forward
...
```

#### 4. git stash apply - 恢复stash存储的代码

```
$ git stash apply
Auto-merging RaspberryPi/RaspberryPiNotes.md
CONFLICT (content): Merge conflict in RaspberryPi/RaspberryPiNotes.md
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   "1_NewThing/\345\205\263\344\272\216Modbus.md"
	new file:   "ZOthers/others.md"

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   "RaspberryPi/RaspberryPiNotes.md"
```

#### 5. 处理冲突

RaspberryPiNotes.md有冲突，处理冲突。然后继续更改或者提交属于你自己的commit。

## stash 的使用

由上面的示例可以看出`stash`可存储当前乱糟糟的工作台（未commit），并且将这个工作台（未commit）放到一边，让分支回到之前干净的工作台（commit），这样我们将可以在这个上面做合并，继续开发等操作。当使用`stash apply`会将之前放一边的工作台，合并到当前最新的工作台（commit）中。

总之`stash`就是保存当前正在操作的工作台到后台，等之后恢复使用。

这个时候就有一堆的操作了，比如那这个工作台保存在哪里了？我恢复完了可能就不需要了，那怎么删除？如果时候太久，我不知道我工作台上有那些东西，或更改要怎么看？


- `git stash`: 将目前的工作台存储
- `git stash list`:	列出所有的存储列表
- `git stash drop stash@{0}`: 删除对应的stash
- `git stash clear`:	删除所有的`stash`
- `git stash show`:	查看存储堆中的第一个stash的diff, 可用 `stash@{0}` 指定. 后面可跟`--patch` 即 `-p`查看全部的diff
- `git stash show -p`:	删除所有的`stash`
- `git stash apply`:	将存储堆中的第一个stash应用的当前工作台
- `git stash apply n`: 对应stash@{n}中的内容
- `git stash pop`: 将存储堆中的第一个stash应用的当前工作台，并将这个stash从存储中删除掉
`git stash branch newBranch`, 新健一个名为newBranch的分支，并将将存储堆中的第一个stash应用在这个分支上。

#### 更多 `git stash --help`

> git-stash - Stash the changes in a dirty working directory away

```
GIT-STASH(1)                      Git Manual                      GIT-STASH(1)

NAME
       git-stash - Stash the changes in a dirty working directory away

SYNOPSIS
       git stash list [<log-options>]
       git stash show [-u | --include-untracked | --only-untracked] [<diff-options>] [<stash>]
       git stash drop [-q | --quiet] [<stash>]
       git stash pop [--index] [-q | --quiet] [<stash>]
       git stash apply [--index] [-q | --quiet] [<stash>]
       git stash branch <branchname> [<stash>]
       git stash [push [-p | --patch] [-S | --staged] [-k | --[no-]keep-index] [-q | --quiet]
                    [-u | --include-untracked] [-a | --all] [(-m | --message) <message>]
                    [--pathspec-from-file=<file> [--pathspec-file-nul]]
                    [--] [<pathspec>...]]
       git stash save [-p | --patch] [-S | --staged] [-k | --[no-]keep-index] [-q | --quiet]
                    [-u | --include-untracked] [-a | --all] [<message>]
       git stash clear
       ......
```

[Git Tools - Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)