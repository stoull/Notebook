# npm本地化方案

## 其它方案

npm对于包`package`的 [定义](https://docs.npmjs.com/about-packages-and-modules)，发现可以通过很多方式安装本地包（或自己写的包）

* 本地文件引用
* config 包
* git仓库包：方便团队或公司内共享

### git仓库包方案

npm 支持的 git url 格式:

`<protocol>://[<user>[:<password>]@]<hostname>[:<port>][:][/]<path>[#<commit-ish> | #semver:<semver>]`

git 路径后可以使用 # 指定特定的 git branch/commit/tag, 也可以 #semver: 指定特定的 semver range.

如：

```
git+ssh://git@github.com:npm/npm.git#v1.2.0
git+ssh://git@github.com:npm/npm#sm:^4.0
git+https://isaacs@github.com/npm/npm.git
git://github.com/npm/npm.git#v6.0.27
git+ssh://localhost:/Users/Shared/git/inverterkit.git
```

 这个时候只要将git url配置加入到`package.json`的`dependencies`中就可以安装了：

使用https授权的配置：

`"package-name": "git+https://<github_token>:x-oauth-basic@github.com/<user>/<repo>.git"`

使用ssh授权的配置：

`"package-name": "git+ssh://git@github.com:<user>/<repo>.git"`

如:

`"inverterkit": "git+ssh://git@20.6.1.65:hut/inverterkit.git"`

详见：[npm install安装本地/私有git源包](https://ithack.github.io/2019/06/28/npm-install安装本地or私有git源包.html)


## npm本地仓库服务方案
这里使用[verdaccio](https://github.com/verdaccio/verdaccio)实现。

>Verdaccio is an Italian name for the mixture of black, white, and yellow pigments resulting in a grayish or yellowish (depending on the proportion) soft greenish brown.

类似的服务还有: 
[sinopia](https://github.com/rlidwka/sinopia),
[local-npm](https://github.com/local-npm/local-npm) 。

### 安装

#### 使用docker进行安装：

拉取verdaccio的镜像image：

`docker pull verdaccio/verdaccio`

运行容器，8883为服务的访问的端口

`docker run -it --rm --name verdaccio -p 8883:4873 verdaccio/verdaccio`

#### 使用npm进行安装

`npm install --location=global verdaccio@next`

并使用`verdaccio`命令运行

### 运行起来后

运行起来后，可以通过网页访问：

`http://127.0.0.1:8883`

添加一个用户：
`npm adduser --registry http://127.0.0.1:8883/`

添加完成后就可以在网页上登录了

在项目根目,运行

`npm publish --registry http://127.0.0.1:8883`

verdaccio会根据`package.json`里面的内容，创建一个版本，可刷新`http://127.0.0.1:8883/`查看

这个时候就可以指定本地registry进行安装了：

`npm --registry http://localhost:8883 install inverterkit`


