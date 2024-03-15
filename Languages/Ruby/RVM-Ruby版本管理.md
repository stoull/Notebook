# RVM-Ruby版本管理

Ruby enVironment (Version) Manager (RVM) 

## Install

* 安装rvm需要用到GPG keys，首先要安装GPG工具：

	`brew install gnupg` or `brew install gpg`

		Also known as: gnupg@2.4, gpg, gpg2
		Formerly known as: gnupg2
		GNU Pretty Good Privacy (PGP) package

* 安装rvm的GPG keys，用来验证安装包的正确性：

	`gpg --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB`

	或者：

	`gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB`

	GPG keys 会安装到：`~/.gnupg/`目录下

* 安装rvm

	`\curl -sSL https://get.rvm.io | bash`


## 指令说明

#### 常用指令：

* `rvm list`				# 列出已安装的ruby解释器版本
* `rvm list known`		# 列出可安装的ruby解释器版本
* `rvm install <version>`	# 安装的ruby版本
* `rvm use <version>`	# 切换到指定的版本
* `rvm remove <version>`	# 移除指定的ruby版本
* `rvm get <version>`		# 更新对应的版本到stable, master


#### 版本切换：

* `current`			# 打印当前使用的版本
* `do`				# runs a command against specified and/or all rubies
* `gemdir`			# 打印当前使用有gem目录即`($GEM_HOME)`
* `use <version>`		# 切换到指定的版本（已安装的版本）
* `use default`		# 切换到默认版本，如果没有设置则切换到系统版本,设置2.7.2为默认版本：`use 2.7.2 default`
* `use system`		# 换到系统版本
* `wrapper`			# creates wrapper executables for a given ruby & gemset

## 使用

更新最新版本的信息：

`curl -L https://get.rvm.io | bash -s stable`

信息将会更新到目录：`~/.rvm`目录下面

载入最新的版本：`source ~/.rvm/script/rvm`

安装想要的版本：`rvm install 2.7.2`


### 问题

```
Error running '__rvm_make -j4',
please read /Users/hut/.rvm/log/1710404760_ruby-2.7.1/make.log

There has been an error while running make. Halting the installation.
```

`rvm install 2.7.2 --with-openssl-dir=$(brew --prefix openssl)`

## gem

RubyGems是Ruby的一个包管理器，提供了分发Ruby程序和库的标准格式“gem”, 与apt-get、portage、yum和npm非常相似。

`gem env home` 即 `($GEM_HOME)`

`gem`示例：

* `gem install rake`
* `gem list --local`
* `gem build package.gemspec`
* `gem push package-0.0.1.gem`
* `gem help install`

## Gem Sets

gemset 是为了创建不同的 gem 环境

rvm中不仅提供了ruby的版本控制，还提供了对gem集合的管理方式。存放在目录：`ls ~/.rvm/gems` 下

[The Basics of RVM](https://rvm.io/rvm/basics)