# About Bundler

## Bundle with React Native

`react-native bundle --platform ios --entry-file index.js --bundle-output ./bundles/main.jsbundle --assets-dest  ./bundles --dev false`

`react-native bundle --entry-file index.js --platform ios --dev true --bundle-output ./ios/bundle/main.jsbundle --assets-dest ./ios/bundle`

You can use the `react-native-xcode.sh` script in `node_modules/react-native/scripts/` to generate that pre-bundled file.

## Bundle with Metro

### Install

`npm install --save-dev metro metro-core`

### 配置`metro.config.js`文件

默认的配置信息，将下面的内容保存到`metro.config.js`文件，放在项目的根目录：

```
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 *
 * @type {import('metro-config').MetroConfig}
 */
const config = {};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

* react-native

`npm install @react-native/metro-config`

* 如果使用expo:

`npx expo customize metro.config.js` 生成默认`metro.config.js`文件

内容大概为：

```
const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);
module.exports = config;
```

## 打包

`react-native bundle --platform android --dev false --entry-file index.js --bundle-output dist/index.bundle --assets-dest dist/`

该命令最终会调用 metro 包的 Server.js 文件的 build() 方法以及 getAssets() 方法来完成打包工作。

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

## Bundle with webpack

### install

`npm install webpack webpack-cli --save-dev`

`react-scripts: npm install react-scripts@latest`



[A beginner’s guide to Metro Bundler](https://medium.com/geekculture/a-beginners-guide-to-metro-bundler-f639d641468b)

[React Native 技术详解 (三) - 打包工具 Metro Bundler](https://www.lumin.tech/blog/react-native-3-metro/)

[Metro bundler](https://docs.expo.dev/guides/customizing-metro/)

[ELI5: Metro - JavaScript Bundler for React Native](https://developers.facebook.com/blog/post/2021/11/01/eli5-metro-javascript-bundler-react-native/)