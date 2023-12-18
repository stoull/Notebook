# About npm

Npm is the management system for Node.js packages

NPM is the default package manager for the Node.js runtime environment. It helps developers to easily manage and share JavaScript libraries, frameworks, and tools. With a vast ecosystem of over a million packages, NPM simplifies the process of finding, installing, and maintaining packages to streamline your development workflow.


Node.js is an open-source, cross-platform JavaScript runtime built on Chrome’s V8 engine. It allows developers to run JavaScript on the server side, enabling the creation of scalable and high-performance web applications. NPM is an integral part of the Node.js ecosystem, facilitating easy package management and project setup.

[Wiki - NPM](https://en.wikipedia.org/wiki/Npm)

[About npm - npmjs.com](https://www.npmjs.com/about)


## Install

### Install on Mac

`brew install npm` or  `brew install node`

Check the installed result and version:

```
$ node -v
v21.4.0
$ npm -v
10.2.4
```

### other platform
[Download Node.js®](https://nodejs.org/en/)

[Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)


### The manifest file `package.json`

`package.json`文件记录着项目的名称，描述及作者等信息，以及项目工程的包依赖关系，如下：

```
{
  "name": "metaverse", // The name of your project
  "version": "0.92.12", // The version of your project
  "description": "The Metaverse virtual reality. The final outcome of all virtual worlds, augmented reality, and the Internet.", // The description of your project
  "main": "index.js"
  "license": "MIT" // The license of your project
  "dependencies": {
  }
  "devDependencies": {
  }
}
```

##### `package.json`文件字段一些说明

* `version` 表明了当前的版本。
* `name` 设置了应用程序/软件包的名称。
* `description` 是应用程序/软件包的简短描述。
* `main` 设置了应用程序的入口点。
* `private` 如果设置为 true，则可以防止应用程序/软件包被意外地发布到 npm。
* `scripts` 定义了一组可以运行的 node 脚本。
* `dependencies` 设置了作为依赖安装的 npm 软件包的列表。
* `devDependencies` 设置了作为开发依赖安装的 npm 软件包的列表。
* `engines` 设置了此软件包/应用程序在哪个版本的 Node.js 上运行。
* `browserslist` 用于告知要支持哪些浏览器（及其版本）。

	[详见-package-json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)

#### 使用`npm init`创建`package.json`文件

使用`npm init`命令将会问询关于项目的一些信息，如项目名称，版本号，描述作者等信息，然后根据获取到的信息生成`package.json`文件。

具体的问询信息如下：

```
package name: (npm) 
version: (1.0.0) 
description: 
entry point: (index.js) 
test command: 
git repository: 
keywords: 
author: 
license: (ISC) 
```

也可以用`npm init --yes`或者`npm init --y`生成默认的配置`package.json`文件

### `npm install` 安装模块

`npm install <module>`

使用上面的方法安装对应的模块，对应的模块将会安装在`/node_modules`目录下。所有的本地模块都将安装到`/node_modules`目录下。如安装expresss：`npm install express`，将会在`package.json`文件里新增如下内容：

```
"dependencies": {
    "express": "^4.18.2"
  }
```

#### `npm install <module>` 选项

模块引用中，很多模块可能是需要引用到项目中实现某些业务功能，有些可能是用来帮忙我们搭建开发环境，方便调试，有些则可能是用来发布，帮助压缩工程文件，更好的使用项目上线的。所有对模块的管理有很多的策略，如有些只是开发的时候要用到,就只要安装到开发环境，而辅助调试的工具可能安装到全局比较好如`nodemon`，有些模块则需要指定对应的模块版本，不然不同版本一起工作会出问题，就出现了`package.json`文件中的几个模块：

`dependencies`: 应用运行时需要的模块，如`express`

`devDependencies`: 仅在应用开发时使用到的模块,如 `webpack`, `gulp` ，用于压缩 css、js 的模块

`peerDependencies`: 这是指定项目对其他包的要求的一种方式。它允许你指定项目所依赖的其他包的版本范围，以确保项目与这些包兼容。

`optionalDependencies`: 这是指定项目的可选依赖项，这些包在安装时不会触发错误，即使它们无法被解析或安装。

##### 使用`npm install <module>`安装时的选项

运行`npm install <module>`则是使用的默认选项`npm install --save-prod`.

`-P, --save-prod`: 模块将会安装到`/node_modules`, 并写入到`dependencies`。这是默认的选项，除非使用`-D` or `-O`或者使用`--no-save`，才不会写到`dependencies`

`-D, --save-dev`: 模块将被写入到`devDependencies`.

`-O, --save-optional`: 模块将被写入到`optionalDependencies`.

`--no-save`: 模块只会安装到`/node_modules`，不会写入`package.json`文件

#### `npm install`

使用`npm install`将会自动安装`dependencies`, `devDependencies`, 及`optionalDependencies`中的模块。

`npm install --production` 或`npm install ----omit=dev`将不会安装`devDependencies`中模块，如不想安可选模块，可使用`npm install --omit=optional`

#### `npm install -g`安装全局模块

使用`npm install <module>`安装方式的模块都为`local packages`，即包文件都在本`/node_modules`的目录下，信息在本项目的`package.json`文件中。项目里有哪个文件引用到这模块，node.js将会遍历 `/node_modules`中的文件，找到对应的模块。但在其它项目中引这里的模块将会报错。

使用`local packages`可以使用每一个项目都单独安装对应的模块，这样模块可以单独管理，使用不同版本。但有些包，像很多CLI工具，如`nodemon`用来监视node.js应用程序中的任何更改并自动重启服务, 或者`serve`serve helps you serve a static site, single page application or just a static file (no matter if on your device or on the local network)，这样可能全局会比较好。

使用`npm install <module> -g` 会将包安装到全局，这样用户下的所有项目可以项目这个模块，如`npm install nodemon -g`

##### 查看模块的位置`npm root`

使用`npm root`查看模块的安装位置，加上`-g`则表示查看全局的位置

local packages path:

```
$ npm root
/Users/hut/Desktop/NPM/node_modules
```

global packages path:

```
$ npm root -g
/usr/local/lib/node_modules
```

`npm root -g`

### 其它

* `npm help`: 查看帮忙
* `npm ls --depth 0`: 查所有已安装的模块
* `npm ls --depth 0 -g`： 查所有已安装的全局模块

* `npm install [package-name]@[version-number]`: 安装指定版本的模块，如`npm install express@4.18.2`, `npm install express@latest`



[npm-install - npm Docs](https://docs.npmjs.com/cli/v10/commands/npm-install)

















































































































