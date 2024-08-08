# Add React Native to existing iOS and Andriod


* `mkdir IntegrateRN`
* `cd IntegrateRN`
* `npm init -`
* `touch index.js`
* modified `package.json` scripts to 
	
	```
	"scripts": {
	  "start": "npx react-native start",
	}
	```
	
* `sudo npm install --global yarn`
* `yarn add react-native`
	react-native@0.72.0 has unm et peer dependency "react@18.2.0"
* `yarn add reac@your-version-above`
* `mkdir ios`under the root of `IntegrateRN`, and your iOS project to the directory of `ios`
* `cd ios`
* `pod init`
* 将`Podfile`的内容更改如下：

	```
	require_relative '../node_modules/react-native/scripts/react_native_pods'
require_relative '../node_modules/@react-native-community/cli-platform-ios/native_modules'
platform :ios, '13.0'
target 'yourreactnativeapp' do
  use_react_native!
end
	```
* `pod install`
* 在iOS工程中加入指向RN的入口

```
// ViewController.swift

import UIKit
import React

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func loadView() {
        loadReactNativeView()
    }

    func loadReactNativeView() {
        let jsCodeLocation = URL(string: "http://localhost:8081/index.bundle?platform=ios")!
        
        let rootView = RCTRootView(
            bundleURL: jsCodeLocation,
            moduleName: "YourApp",
            initialProperties: nil,
            launchOptions: nil
        )
        self.view = rootView
    }
    
}
```

* 更改`index.js`的内容为：

```
import React from 'react';
import {
    AppRegistry,
    Text,
    View
  } from 'react-native';

const YourApp = () => {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>
        Hello World! 🎉
      </Text>
    </View>
  );
}

AppRegistry.registerComponent('YourApp', () => YourApp);
```

[深入理解react-native](http://blog.ilibrary.me/2016/12/25/react-native-internal#react-native-架构)

[Add React Native to existing iOS](https://www.youtube.com/watch?v=3wftC30CN2I)

[How to add React Native to an existing iOS app in 2022](https://fek.io/blog/how-to-add-react-native-to-an-existing-i-os-app-in-2022/)

[How to add React Native to an existing Android app in 2022](https://fek.io/blog/how-to-add-react-native-to-an-existing-android-app-in-2022/)