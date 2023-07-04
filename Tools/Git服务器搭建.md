# Git服务器搭建


[4.2 Git on the Server - Getting Git on a Server](https://git-scm.com/book/sv/v2/Git-on-the-Server-Getting-Git-on-a-Server)

### 创建bare仓库
创建任何一个git服务，首先需要一个git仓库，基于这个git仓库创建一个bare仓库，以.git结尾，创建bare仓库如下：

```
$ git clone --bare my_project my_project.git
Cloning into bare repository 'my_project.git'...
done.
```

上面的命令相当于：
```
cp -Rf my_project/.git my_project.git
```

### 创建server上的仓库
一个git仓库在server上就对应一个bare仓库，所以将上面创建的bare仓库放到服务器上就成了一个git仓库:

```
scp -r my_project.git user@git.example.com:/srv/git
```
这个时候，就应该可以使用`clone`命令了：

```
$ git clone user@git.example.com:/srv/git/my_project.git


$ git clone ssh://127.0.0.1:/srv/git/my_project.git

```



如果用户使用`ssh`连接服务器，并有对：`/srv/git/my_project.git`有写的权限，那这个用户同样也可以使用`push`命令。

#### 权限问题

使用命令`git init --shared`, git 会自动增加用户组对对应仓库的写权限，并且不会改变仓库的状态，如`commits, refs`等，：

```
$ ssh user@git.example.com
$ cd /srv/git/my_project.git
$ git init --bare --shared
```

上面的命令相当于：

`git config core.sharedRepository group`

最后如果当前`/srv/git/my_project.git`的系统用户组没有写权限，则还需要增加系统用户组对`/srv/git/my_project.git`的写权限。

```
sudo groupadd git		// 新增一个用户组git, 专用于git用户
usermod -a -G git pi		// 将当前用户pi(自已),加入这个用户组
sudo chmod -R ug+w /srv/git/my_project.git		// 增加对仓库目录的权限
sudo chown -R git:git /srv/git/my_project.git		// 改变仓库的所属
```
现在应该只要将用户的ssh public key上传的服务器，并可通过ssh访问，应该就可以对仓库进行push操作了。





