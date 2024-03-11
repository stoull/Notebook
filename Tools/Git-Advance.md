# Git使用过常中的问题及场景用法

## Git安装
CentOS 7
`sudo yum install git`
`git --version`

### 1. 如文件名含有空格，则用 “” 将文件名括起来
******
### 2. 如果不是通过 git 删除的文件，如用rm 或Finder中删除的文件。如果也要在git中移除对应版本管理

**Git 1.x 的版本**

	$ git add -u

This tells git to automatically stage tracked files -- including deleting the previously tracked files.

**Git 2.0 的版本**

To stage your whole working tree:

	$ git add -u :/
	
To stage just the current path:

	$ git add -u .

**也可以用这个命令**

	git ls-files --deleted -z | xargs -0 git rm

> 来源[stackoverflow](https://stackoverflow.com/questions/492558/removing-multiple-files-from-a-git-repo-that-have-already-been-deleted-from-disk "stackoverflow") 

******

### 3. Git合并-几种Merge方法

* `Fast-Forward Merge（快进式合并)` 就是普通合并，如果没有冲突将会直接将header移向分支快照
* `Three-Way Merge（三方合并）` 使用`--no-ff` 如 `git merge dev --no-ff` 就会使用些合并方法，形成一个新的快照
* `Squash Merge (合并提交)`

	>
所谓Squash Merge，是指Git在做两个分支间的合并时，会把被合并分支（通常被称为topic分支）上的所有变更“压缩（squash）”成一个提交，追加到当前分支的后面，作为“合并提交”（merge commit）
	>
Squash Merge不会像普通Merge那样在合并后的提交历史里保留被合并分支的分叉，被合并分支上的提交记录也不会出现在合并后的提交历史里，所有被合并分支上的变更都被“压缩”成了一个合并提交。

### 3. Fast-forward a branch to head?

像这样子：

```
Your branch is behind 'origin/master' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)
```
**方法一:** 合并分支

	git fetch origin master
	git merge origin/master
> 如果想保证只是Fast-forward 用这个命令 `git merge --ff-only origin/master`

**方法二:**

```
git checkout master
git pull origin
```
将会 fetch 并合并 origin/master 分支
******
### 4. 取git仓库里面的部分文件
最简单的取文件用：

如我只想取XVim项目 （https://github.com/XVimProject/XVim.git）里面的文档文件（Documents/Developers）可用如下命令：

	svn checkout https://github.com/XVimProject/XVim/trunk/Documents/Developers

再一个例子：

	svn checkout https://github.com/appium/appium/trunk/docs/en/appium-setup appium-setup
参考 [How do I clone a subdirectory only of a Git repository?](http://stackoverflow.com/questions/600079/how-do-i-clone-a-subdirectory-only-of-a-git-repository)

******

### 5. Reset uncommitted changes including files and folders.

You can run these two commands:

Revert changes to modified files.

`git reset --hard`

Remove all untracked files and directories. (`-f` is `force`, `-d` is `remove directories`)

`git clean -fd`

******
### 6.设置忽略文件

#### 创建独立的 .gitignore
在Git仓库的目录下创建一个名为 `.gitignore` 的文件，在commit前，Git就会用这个文件里面的“策略”，去判断那些文件或文件夹需要忽略（版本管理时需要无视的文件）。

 `.gitignore` 文件需要加入Git仓库中，这样别人Clone这个仓库后，都可以共享这个忽略文件策略。
 
 在Git上面维护着官方推荐的各种忽略'策略'文件[Gitignore Github public repository](https://github.com/github/gitignore)
 
 创建 `. gitignore`文件：
 
 	1. 在终端使用`cd`命令进入到对应的Git仓库。
 	2. 使用`touch .gitignore`命令，创建gitignore文件。
 

如果已经有文件加入版本管理了，而你想忽略它。这个时候你加入忽略策略，Git是不会忽略它的，这个时候你先把这个文件untrack，使用下面的命令：

	$ git rm --cached FILENAME

如果文件存在于多处，可使用下面的命令untrack移除所有的想要移除的文件，包含子目录中的

`find . -name FILENAME -print0 | xargs -0 git rm --ignore-unmatch`

#### 创建全局的 .gitignore
全局的Git忽略文件，目录为`~/.gitignore_global`，所有的仓库都会使用这个全局的忽略策略，也会使用独立的.gitignore策略。如何设置：

	1. 打开终端
	2. 使用下面的命令，加入一个全局策略
		$ echo .DS_Store >> ~/.gitignore_global 
	3. 运行这个命令,告诉所有人仓库使用这个全局策略：
	$ git config --global core.excludesfile ~/.gitignore_global

#### 隐性 .gitignore
如果你不想让你的 `. gitignore `分享给其他的人，不想加入版本管理，比如一些编辑器产生的文件，不同的人也会用不同的文件。
你可以在文件`.git/info/exclude`中编辑对应策略，所有这些策略都只会影响本地仓库。

******
### 7. 处理合并冲突 conflicts

使用`git log --merge`查看冲突日志，看谁提交的代码产生了conficts。

### 8. Merge (with squash) all changes from another branch as a single commit
```
git merge --squash <feature branch>
git commit 

使用`merge`，如果没有冲突会自动`commit`。使用 `--squash` 与使用merge是一样的效果, 但不会commit，不移动HEAD, 所以要额外的commit。其效果相当于将another分支上的多个commit合并成一个，放在当前分支上，原来的commit历史则没有拿过来。可以用来合并多个意义不大的commit.
判断是否使用`--squash`选项最根本的标准是，待合并分支上的历史是否有意义。

```

```
$ git log --merge
commit f98593256033d2e6b73ae234f509b6fc32fea369
Author: linkapp <stoull@linkapp-Mac.local>
Date:   Tue Aug 1 09:34:26 2017 +0800

    April Did it
    
commit 8ae832fd0f4813cbc91e06257b81535456161464
Author: linkapp <stoull@linkapp-Mac.local>
Date:   Tue Aug 1 09:33:21 2017 +0800

    Gun Do That
```
    
`git diff April/branchone GunZi/branchtwo` 查看哪些代码有冲突，也可以直接对比两个冲突的commit

	`git diff f98593256033d2e6b73ae234f509b6fc32fea369 8ae832fd0f4813cbc91e06257b81535456161464`


使用合并工具查看改变，并处理改变

	git mergetool

确定那些文件有冲突
```
diff common mine
diff common theirs
```

打开那些文件并处理冲突，处理完后，resolved 它：

	git add the_file
	
如果全部都处理完了

	git rebase --continue

### 8. Not a valid object name: 'master'.

当`git init`后，Git 不会自动创建 `master` 分支，要直到你第一次 `commit` 后才会创建对应的master分支。这个时候如果你去创建分支，就会报这个错误。所以解决这个问题就是，加一些文件进去，然后commit一下就可以了。

### 9. 配置账号信息(&working with different Git Accounts)

	$ git config --global user.name "YOUNAME"

	$ git config --global user.email youremail@mail.com

	$ git config --list   查看配置的信息
	
 Working with different Git accounts:
 
```
*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.
```
如果在一台电脑上有不同repository使用的不同帐号，可以通过‘git config user.name’设置该repository的用户名。这个时候去配置ssh配置文件```~/.ssh/config```，ssh会根据不同的用户选择对应的key进行push操作。[Generate ssh key]("https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent") , 文件格式如下, 对应文件可在本文件目录`./Linux/ssh_config_template`找到：

```
Host hutbe_github
	HostName github.com
	User hutbe
	AddKeysToAgent yes
	UseKeychain yes
	IdentityFile ~/.ssh/github_hutbe25519

Host stoull_github
	HostName github.com
	User stoull
	AddKeysToAgent yes
        UseKeychain yes
        IdentityFile ~/.ssh/github_stoull25519

Host growatt_git
	HostName 192.168.3.240
	User ios2
	AddKeysToAgent yes
	UseKeychain yes
	IdentityFile ~/.ssh/id_rsa
```
当你commit的时候增，作者信息：
```git commit --amend --author="author <your-email@xxx.com>"```
OR 指定用户名进行PUSH:
`git push https://username:password@myrepository.biz/file.git --all`

in this case https://username:password@myrepository.biz/file.git replace the origin in git push origin --all

To see more options for git push, try `git help push`
	
### 10. 将Remote上新建的的BugFix分支 fetch 到origin/BugFix后，将origin/BugFix 变成local分支的方法

	git checkout --track origin/BugFix
	
`--track` is shorthand for `git checkout -b [branch] [remotename]/[branch]` where `[remotename]` is origin in this case and `[branch]` is twice the same, `BugFix` in this case.

### 11. fatal: refusing to merge unrelated histories
当在本地建一个repository, commit, 然后Github上新建一个repository，加入文件。在本地git remote add ''。之后就不能合并，push等操作，报这个错误。

解决方法：

See the git [release changelog](https://github.com/git/git/blob/master/Documentation/RelNotes/2.9.0.txt#L58-L68) for more information.

You can use `--allow-unrelated-histories` to force the merge to happen.

见：[git-refusing-to-merge-unrelated-histories](https://stackoverflow.com/questions/37937984/git-refusing-to-merge-unrelated-histories)

### 12. Get error when Clone a huge git repository with slow internet connection
```
$ git clone https://github.com/CocoaPods/Specs.git master
Cloning into 'master'...
remote: Enumerating objects: 463, done.
remote: Counting objects: 100% (463/463), done.
remote: Compressing objects: 100% (390/390), done.
error: RPC failed; curl 18 transfer closed with outstanding read data remaining
fatal: the remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed
```

One way that works for me. The idea is to do a shallow clone first and then update the repository with its history.

```
$ git clone https://github.com/CocoaPods/Specs.git master --depth 1
$ cd master
$ git fetch --unshallow
```

### 13. Checkout a single file from a specific commit
checkout from a branch
`git show somebranch:from/the/root/myfile.txt > new_file_path/and_name_youwant.ext`
checkout from a commit:
`git show HASH:file/path/name.ext > new_file_path/and_name_youwant.ext`
the `HASH` is like this: `7bccc6db5d974de3ac0debe6b12bfc4b3781a5af`


### 14. Rename Master Branch
```
git branch -m master development
git branch -m published master
git push -f origin master 
```

### 撤消Merge   Undo a git merge with conflicts

`git merge --abort`

### 15. 合并分支时，只合并一个commit

`git merge topical_xFeature`
`git merge --squash topical_xFeature`
`git merge dev --no-ff`
Which one you choose is up to you. Generally, I wouldn't worry about having multiple smaller commits, but sometimes you don't want to bother with extra minor commits, so you just squash them into one.

### 16. 回撤commit
本地的commit:

```
git log
    commit 101: bad commit    # Latest commit. This would be called 'HEAD'.
    commit 100: good commit   # Second to last commit. This is the one we want.
```

```
git rebase -i HEAD~N
git reset --soft HEAD^n     # Use --soft if you want to keep your changes
git reset --hard HEAD^n     # Use --hard if you don't care about keeping the changes you made
```

已上传到服务器的commit:

```
git revert HEAD^n

Your changes will now be reverted and ready for you to commit:

git commit -m 'restoring the file I removed by accident'
git log
    commit 102: restoring the file I removed by accident
    commit 101: removing a file we don't need
    commit 100: adding a file that we need
    
git reset --hard <commit-hash>
git push -f origin master
```

### 17 删除分支
 删除远程分支
 
` $ git push -d <remote_name> <branchname> `

 删除本地分支
` $ git branch -d <branchname> `
` $ git branch -D <branchname> ` with force


### 18. Tag 相关

#### 增加 tag

git tag 分为 lightweight and annotated， lightweight 像commit一样打个tag， 而annotated是复制所有内容存入数据库

增加 annotated tag

`git tag -a v1.4 -m "my version 1.4"  // 创建一个annotated 标记`
`git show v1.4`

// 指定特定的版本
`git tag -a v1.2 9fceb02 -m "Message here"`

// If you forgot to tag the project at v1.2

`git tag -a v1.2 9fceb02 -m "my version 1.2"`

增加 lightweight tag

`git tag v1.4-lw`
`git tag`

#### 列出所有tags 以及对应的message信息:

`git tag -l -n9`

`git tag -l -n9 v3.* // 列出特定的版本`	

#### 将特定tag推送到远程
`git push origin <tag_name>`

#### 将所有tag推送到远程
`git push --tags`

#### 删除tag

`git push --delete origin tagname` // 远端

`git tag --delete tagname`	// 本地

### 19. 提交部分修改的文件，即commit一个修改过的文件

git commit file1 file2 file5 -m "commit message"

### 20. 撤销历史上的`merge`

如下图，主分支有commit -m ABCDEF, 有一个分支有commit -m 1234
如何让主分支保留CEF更改，而仅移除 commit D的分支合并

```
* commit F
| 
* commit E
|   
*   commit D
|\  Merge: C 4
| | 
| * commit 4
| | 
| * commit 3
| |
* | commit C
| | 
| * commit 2
| | 
| * commit 1
|/ 
* commit B
| 
* commit A
```

```
* commit F
| 
* commit E
|   
| * commit 4
| | 
| * commit 3
| |
* | commit C
| | 
| * commit 2
| | 
| * commit 1
|/ 
* commit B
| 
* commit A
```

### 21. Create a new branch from a tag - 从tag上创建分支

` git checkout -b <New Branch Name> <TAG Name>`

Steps to do it.

`git checkout -b NewBranchName v1.0`

Make changes to pom / release versions
Stage changes

`git commit -m "Update pom versions for Hotfix branch"`

Finally push your newly created branch to remote repository.

`git push -u origin NewBranchName`

### 22. 追踪文件的更改记录

* `git diff [filename]` 查看未Staged的文件变化
* `git diff --staged` 查看已Staged的文件变化
* `git diff --cached [filename]` 查看已Staged的文件变化与`git diff --staged`一样

#### 追踪单个文件的更改记录
`git log -p -- filename` 此命令会这个文件每一次有更改的commit,及详情

如:
`git log -p -- MyGro/NewVersion/PopView/MGPresentViewController.swift`

### 23. remote: error: object file ./objects/76/file is empty

* 1 删除所有因为数据损坏导致的空对象文件(remove any empty object files)。执行第一步没有任何输出

`$ find .git/objects/ -type f -empty | xargs rm`

* 2 下载上一步删除的对象文件(fetch down the missing objects)

`$ git fetch -p`


```
remote: error: object file ./objects/76/371ae3bca99d9d8463e21742ef9d41bc47dab9 is empty
```

* 3 做一次全面的存储对象检查(do a full object store check)

`git fsck --full`

### 24. 移除已被追踪（tracked）的文件

有时候更新了`.gitignore`文件，但如果新忽略的文件之前已经是`tracked`的状态，那么已经是`tracked`的文件还会显示已更改的状态。

* `.gitignore`文件只是用来防止将特定的未跟踪的文件`untrack`或文件夹加入`staged`。如果是`tracked`的就不能了。

这个时候需要手动移除`tracked`的文件为`untrack`，这样`.gitignore`的策略就能对对应的文件生效了。

从index中移除文件：

`git rm --cached <file>`

如果是文件夹，则递归（recursively）的移除其中的所有文件：

`git rm -r --cached <folder>`


### 25. 撤销reset, 恢复commit

`git reflog`: reflog记录了所有git操作，从里面可以找到reset的操作，并且有hash值

找到对应的commit 之后，执行对应的:

`git reset --hard hash`即可回到对应的位置


### 26. 修剪分支 prune
git delete not existing remote branches

当A机器上本地的远程X分支还在，但对应远程分支X已经被删除，这个时候A机器上的远程分支X就不能删除了。

先查看A机器上的所有分支：

`git branch -a`

如有`remotes/origin/dev_with_RN`分支，但`dev_with_RN`在上`origin `已经被删除了，这个时候A机器上的`remotes/origin/dev_with_RN`分支就不能被删除了, 当执行删除`git push -d origin dev_with_RN`的时候，会报：

> error: unable to delete 'dev_with_RN': remote ref does not exist

使用下面中的任何命令：

* `git branch -r -d origin/dev_with_RN`
* `git remote prune origin`
* `git remote prune origin --dry-run`: 模拟运行，输出对应的结果，但实际不会删除
* `git fetch origin --prune`

[git remote prune](https://git-scm.com/docs/git-remote#Documentation/git-remote.txt-empruneem)

[Cleaning up old remote git branches](https://stackoverflow.com/questions/3184555/cleaning-up-old-remote-git-branches)

### 27.移除Git项目中的大文件


如有移除所有commit中的 `Pods`目录如下，`filter-branch --tree-filter`遍历所有的commit， 并且执行'rm -rf Pods'命令。

`git filter-branch --tree-filter 'rm -rf Pods' HEAD`

如果其它分支都用到这个文件，则对应每一个分支都要运行一遍

注意：**所有commit都会作更改**

[How can I remove/delete a large file from the commit history in the Git repository?](https://stackoverflow.com/questions/2100907/how-can-i-remove-delete-a-large-file-from-the-commit-history-in-the-git-reposito)
