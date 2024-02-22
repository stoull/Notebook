# React Native Bridge

## What is React Native bridging?

> React Native Bridging is a concept that was developed by the React team to help the mobile app developers build their own custom modules, if not provided by the default Components given by React.
> 
> React Native provides developers with a variety of modules that developers can use to create functionality in the application. For example, React Native provides its own “Net Info” module to check for Internet Connectivity in applications. However, sometimes an app needs access to a platform API for which React doesn’t have a module yet. Or maybe the app needs a custom functionality that cannot be achieved using default React Native modules.
Hence, React Native allows us to write Native Code (Android and iOS) and communicate between native code and React Native JavaScript code to achieve custom-developed functionality.
> 
> According to the documentation, React Native team believes that if React Native doesn’t support a native feature that you need, you should be able to build it yourself by using Bridging.
> 
> There are two ways to bridge native code to JavaScript:
> 
	* Native Modules
	* Native UI Components

by -- [Rupesh Chaudhari](https://medium.com/simform-engineering/bridging-for-ios-and-android-in-react-native-64b8ce60a8c2)

### Bridges用来翻译ReactJS的绘制指令给原生组件进行绘制，同时把原生组件接收到的用户事件反馈给ReactJS。

深入 Bridge 前面有提到, RN厉害在于它能打通JS和Native Code, 让JS能够调用丰富的原生接口,充分发挥硬件的能力, 实现非常复杂的效果,同时能保证效率和跨平台性。
打通RN任督二脉的关键组件就是Bridge. 在RN中如果没有Bridge, JS还是那个JS，只能调用JS Engine提供的有限接口，绘制标准html提供的那些效果,那些摄像头，指纹，3D加速,声卡, 视频播放定制等等，JS都只能流流口水，原生的、平台相关的、设备相关的效果做不了， 除非对浏览器进行定制。
Bridge的作用就是给RN内嵌的JS Engine提供原生接口的扩展供JS调用。所有的本地存储、图片资源访问、图形图像绘制、3D加速、网络访问、震动效果、NFC、原生控件绘制、地图、定位、通知等都是通过Bridge封装成JS接口以后注入JS Engine供JS调用。理论上，任何原生代码能实现的效果都可以通过Bridge封装成JS可以调用的组件和方法, 以JS模块的形式提供给RN使用。

每一个支持RN的原生功能必须同时有一个原生模块和一个JS模块，JS模块是原生模块的封装，方便Javascript调用其接口。Bridge会负责管理原生模块和对应JS模块之间的沟通, 通过Bridge, JS代码能够驱动所有原生接口，实现各种原生酷炫的效果。
RN中JS和Native分隔非常清晰，JS不会直接引用Native层的对象实例，Native也不会直接引用JS层的对象实例(所有Native和JS互掉都是通过Bridge层会几个最基础的方法衔接的)。
Bridge 原生代码负责管理原生模块并生成对应的JS模块信息供JS代码调用。每个功能JS层的封装主要是针对ReactJS做适配，让原生模块的功能能够更加容易被用ReactJS调用。MessageQueue.js是Bridge在JS层的代理，所有JS2N和N2JS的调用都会经过MessageQueue.js来转发。JS和Native之间不存在任何指针传递，所有参数都是字符串传递。所有的instance都会被在JS和Native两边分别编号，然后做一个映射,然后那个数字/字符串编号会做为一个查找依据来定位跨界对象。

- [深入理解react-native](http://blog.ilibrary.me/2016/12/25/react-native-internal#react-native-架构)


### RCTBridge in iOS

* 在原生App中最好只有一个`RCTBridge`实例对象，并使用这个`RCTBridge`初始化`RCTRootView`进行页面交互的渲染加载。
* 

使用oc作桥接




[Native Bridging for iOS and Android in React Native](https://medium.com/simform-engineering/bridging-for-ios-and-android-in-react-native-64b8ce60a8c2)

[Project react-native-bridging ](https://github.com/mobile-simformsolutions/react-native-bridging)

[https://www.jianshu.com/p/cc39a8964269](https://www.jianshu.com/p/cc39a8964269)

[React native 技术详解](https://www.lumin.tech)