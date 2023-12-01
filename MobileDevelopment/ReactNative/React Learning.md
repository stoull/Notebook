# React Native

[reactnative docs](https://reactnative.dev/docs/getting-started)

[React Native 中文网](https://reactnative.cn/docs/getting-started)

[React-Native学习指南](https://github.com/reactnativecn/react-native-guide)

[集成到现有原生应用](https://reactnative.cn/docs/integration-with-existing-apps?language=swift#2-事件处理)

[Add React Native to existing iOS app 2022](https://www.youtube.com/watch?v=3wftC30CN2I)

[React Native Upgrade Helper](https://react-native-community.github.io/upgrade-helper/?from=0.71.3&to=0.72.3)

### Expo
[expo-GitHub](https://github.com/expo/expo)

[Install EXpo modules](https://docs.expo.dev/bare/installing-expo-modules/)


# React Native

### Den Env


* `brew install npm`
* `npx create-expo-app --help ` :会提示安装`expo`,进行安装`expo`, 使用如下:

	* `$ npx create-expo-app <path> [options]` : 使用`npx`初始化 expo
	* `$ yarn: yarn create expo-app <path> [options]` : 使用`npx`初始化 expo
	
* `npx create-expo-app@latest --example with-router <path>`: Creates a new Expo project from [example repo](https://github.com/expo/examples)
* `npm install expo-font axios react-native-dotenv` 安装其它依赖包，总的可见于`package.json`
* `npm start`: 运行服务

如遇网络问题, 使用`expo-cli`:

* `npm install -g expo-cli`
* `expo-cli start --tunnel`

expo-router 版本匹配问题：

```
Some dependencies are incompatible with the installed expo version:
  expo-font@11.6.0 - expected version: ~11.4.0
  expo-linking@6.0.0 - expected version: ~5.0.2
  ...
Your project may not work correctly until you install the correct versions of the packages.
Fix with: npx expo install --fix
```

Warning: Invalid version react-native@0.72.3 for expo sdkVersion 49.0.0. Use react-native@0.72.5

使用如下检查更新：

* `npx expo install --fix`
* `npm start --clean-cache`


### React Native vs React JS

|React Native|----|React JS|
|----|----|----|
|Custom|----|HTML Components|
|Native UI|----|HTML/CSS output|
|CSS Subset|----|Standar styling|
|No URLs|----|URL based|
|React Navigation|----|React Router|
|Expo+Simulators|----|Test in browser|


> * t3 create turbo
> * TmaGui
> * Tamagui + Solito + Next + Expo Monorepo
> * Solito: React Native + Next.js
> * axios
> * [Watchman](https://facebook.github.io/watchman/)
> * JavaScriptCore.Framework

React Native 工具:

> Expo, and Expo - Router [Expo](https://github.com/expo/expo) and [Expo-Dcos](https://docs.expo.dev/routing/introduction/)
> 
> rapidapi [World’s Largest API Hub - rapidapi.com](https://rapidapi.com)
> 

React Native

```
import React from 'react'
import {View, Text} from 'react-native
const App = () =>
return (
	<View>
		<Text> Hello World! </Text>
	</View>
)}
```

### npm build

在package.josn文件中增加如下代码,生成`main.jsbundle`文件：

```
"scripts": {
"build:ios": "node node_modules/react-native/local-cli/cli.js bundle --entry-file='index.js' --bundle-output='./main.jsbundle' --dev=false --platform='ios' --assets-dest='./ios'"
}
```

* `--entry-file`: path to our index.js file
* `--bundle-output`: path of where `main.bundlejs` will be created
* `--dev=false`: bunch of perf optimisations are made when false
* `--platform`: ios



### Routing

[React Router Native Tutorial](https://www.youtube.com/watch?v=VYSIT2leZ1g)

[React Native File Based Routing with Expo Router](https://galaxies.dev/react-native-file-based-routing)


### Deploy and Pubish

[https://juejin.cn/post/7190203133585260599](https://juejin.cn/post/7190203133585260599)

[集成热更新（CodePush）](https://todoit.tech/rn/devops/hotfix.html)

[React-Native私服热更新的集成与使用](https://cloud.tencent.com/developer/article/1896497)
