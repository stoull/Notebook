#npm registry 源管理

To resolve packages by name and version, npm talks to a registry website that implements the CommonJS Package Registry specification for reading package info.

npm is configured to use the npm public registry at `https://registry.npmjs.org` by default. 

-- [registry](https://docs.npmjs.com/cli/v8/using-npm/registry)

## npm的registry


* 查看：`npm get registry`

```
% npm get registry
http://registry.npm.taobao.org/
```

* 设置: `npm set registry https://registry.npmjs.org`

上面为更改为默认源

* 临时指定安装源：

`npm --registry http://localhost:8883 install inverterkit`

从`http://localhost:8883`安装名为inverterkit的模块，不影响其它的registry。

本地源服务可使用：[verdaccio](https://github.com/verdaccio/verdaccio)

## 使用 nrm 管理工具

* 安装

`npm install -g nrm`

* 列出源列表 `nrm ls`

```
InverterKit % nrm ls
(node:3831) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
  npm ---------- https://registry.npmjs.org/
  yarn --------- https://registry.yarnpkg.com/
  tencent ------ https://mirrors.cloud.tencent.com/npm/
  cnpm --------- https://r.cnpmjs.org/
  taobao ------- https://registry.npmmirror.com/
  npmMirror ---- https://skimdb.npmjs.com/registry/
```
* 查看当前源 `nrm current`

```
nrm current
(node:3839) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
Your current registry(http://registry.npm.taobao.org/) is not included in the nrm registries.
Use the nrm add <registry> <url> [home] command to add your registry.
```

* 更改源

`nrm use tencent` 为使用tencent的源

* 增加源

`nrm add <registry> <url> [home]`

如`nrm add local http://localhost:8883`: 增加一个名为local的源

* 删除源 `nrm del registry`
* 测试速度 `nrm test registry`