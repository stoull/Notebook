# React Navigation


[React Navigation](https://reactnavigation.org/docs/getting-started)

## Installation

`npm install @react-navigation/native`
`npm install react-native-screens react-native-safe-area-context`
`npx pod-install ios`

### Wrapping your app in NavigationContainer

```
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';

export default function App() {
  return (
    <NavigationContainer>{/* Rest of your app code */}</NavigationContainer>
  );
}
```

### NativeStackNavigator

`npm install @react-navigation/native-stack`

### 

* `navigation.navigate('Details')`: 推出stack中的
* `navigation.push('Details')`: 重复推出stack中的