# Flutter


## 安装Flutter SDK

* 一是通过VS Code安装
	1. 首先安装VSCode上面的Flutter扩展[Flutter extension for VS Code](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)
	- 按 Command + Shift + P。输入flutter,选择Flutter: New Project. 根据提示进行安装

* 二是直接下载安装
	- 将flutter的安装路径添加到path. `export PATH=$HOME/development/flutter/bin:$PATH` 到 ~/.zshenv
		`echo 'export PATH=$HOME/flutter/bin:$PATH' >> ~/.zprofile`


[Install the Flutter SDK](https://docs.flutter.dev/get-started/install/macos/mobile-ios)

## 创建项目

`flutter create helloworld --template app` == `flutter create helloworld`



Flutter SDK


`flutter create .`: 创建工程文件，或补全完整的工程文件

`flutter run -d 'iPhone 16'`

`flutter devices`

`flutter run -d ios`

`flutter doctor`




`dart run main.dart`



```
open -a Simulator
flutter devices
flutter run -d 'iPhone 16'
flutter doctor -v
```
flutter run -d 'iPhone SE'



## 包管理

Flutter 通过 Dart 的包管理工具 pub 来管理包（package）

Pub[https://pub.dev/](https://pub.dev/)是 Google 官方的 Dart Packages 仓库，类似于 node 中的 npm仓库、Android中的 jcenter, iOS中的pod，Debian/Ubuntu中的apt，CentOS 中的yum，macOS中的brew。

Flutter 项目默认的配置文件是`pubspec.yaml`，类似于：


```
name: form_app
description: A sample demonstrating different types of forms and best practices
publish_to: "none"
version: 1.0.0+1

environment:
  sdk: ^3.7.0-0

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.0
  intl: ^0.20.0
  http: ^1.0.0
  json_annotation: any
  english_words: ^4.0.0
  window_size:
    git:
      url: https://github.com/google/flutter-desktop-embedding.git
      path: plugins/window_size
  go_router: ^15.0.0

dev_dependencies:
  analysis_defaults:
    path: ../analysis_defaults
  flutter_test:
    sdk: flutter
  json_serializable: ^6.2.0
  build_runner: ^2.1.8

flutter:
  uses-material-design: true
```

- `dependencies`：应用或包依赖的其他包或插件。
- `dev_dependencies`：开发环境依赖的工具包（而不是flutter应用本身依赖的包)
- `sdk: flutter`: 表示从本地的flutter中下载，不需要从网络拉取


