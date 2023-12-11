# About npx

[About npm](./About npm.md)


Npm is the management system for Node.js packages

npm（node package manager）是你安装 Node.js 时开箱即用的依赖/包管理器。它为开发者提供了一种在全局和本地安装包的方法。

有时你可能想看一下特定的包，并尝试一些命令，但如果不在本地的 node_modules 文件夹中安装依赖项，你就无法做到这一点。


npm 本身并不运行任何软件包。如果你想使用 npm 运行一个包，你必须在 package.json 文件中指定这个包。

当可执行文件通过 npm 包安装时，npm 会创建链接指向它们。

* 本地安装的链接是在 `./node_modules/.bin/` 目录下创建的
* 全局安装会在全局 bin/ 目录下创建链接（例如：Linux 上的 `/usr/local/bin` 或 Windows 上的 `%AppData%/npm`）


### 使用 npm 执行一个包

* `$ ./node_modules/.bin/your-package`\
* 或者可以通过在脚本部分的 `package.json` 文件中添加一个本地安装的软件包来运行它，像这样：

	```
	{
  "name": "your-application",
  "version": "1.0.0",
  "scripts": {
    "your-package": "your-package"
  }
}
	```
	然后使用`npm run`来运行它`npm run your-package`
	

## npx

* 自从 npm 5.2.0 版本以来，npx 就被预先捆绑在 npm 中，所以它现在几乎是一个标准。

* npx 也是一个 CLI 工具，其目的是使安装和管理托管在 npm 注册表中的依赖关系变得容易。

### 查看npx是否已安装

* `$ which npx`
* `npm install -g npx`: 全局安装


### 使用 npx 执行一个包

`npx your-package`



### npx执行以前没有安装的软件包


npx另一个主要优势是能够执行以前没有安装的软件包。

如 `npx cowsay wow`

* 不需要安装对应的包，可以只使用 CLI 工具，方便调试
* 可以节省磁盘空间，全局变量受到更少的污染
* 可以用 npx 来运行任何 GitHub gist 和仓库

### 使用npx测试不同版本的包

以`create-react-app`包为例

 * `npm v create-react-app`输出包`create-react-app`的dist 标签。
 * `npx create-react-app@next sandbox`在沙盒目录内创建next dist标签的应用程序。npx 会暂时安装下一个版本的 create-react-app，然后它就会执行，安装应用程序的依赖。
 * `cd sandbox`
 * `npm start`


[npm 和 npx 的区别是什么](https://www.freecodecamp.org/chinese/news/npm-vs-npx-whats-the-difference/)
