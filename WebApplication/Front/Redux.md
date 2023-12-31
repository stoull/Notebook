# React Redux

安装： [npm install react-redux](https://redux.js.org/introduction/installation)

[中文文档](https://www.reduxjs.cn)

Redux is a state management framework that can be used with a number of different web technologies, including React.

Redux Keep the app state in a single location:

整个app使用Redux状态管理：

single Redux store -> subscribed by React components -> dispatch actions -> update single Redux store


* In Redux, there is a single state object that's responsible for the entire state of your application, housed in the Redux `store`.

* `state`is read-only: you never modify state directly, instead, you return a new copy of state.

* the role of `reducer `: The reducer is simply a pure function that takes `state` and `action`, then returns new state. 

* `store`中的方法：
	- getState()
	- dispatch(action)
	- subscribe(listener)
	- replaceReducer(nextReducer)
	
示例代码：

```
const INCREMENT = 'INCREMENT';
const DECREMENT = 'DECREMENT';

const counterReducer = (state = 0, action) => {
  switch(action.type) {
    case INCREMENT:
      return state + 1;
    case DECREMENT:
      return state - 1;
    default:
      return state;
  }
};

const LOGIN = 'LOGIN';
const LOGOUT = 'LOGOUT';

const authReducer = (state = {authenticated: false}, action) => {
  switch(action.type) {
    case LOGIN:
      return {
        authenticated: true
      }
    case LOGOUT:
      return {
        authenticated: false
      }
    default:
      return state;
  }
};

const rootReducer = Redux.combineReducers({
  count: counterReducer,
  auth: authReducer
});

const store = Redux.createStore(rootReducer);

const loginAction = (message) => {
  type: LOGIN,
  message: message
}

store.dispatch(loginAction('Hut!'));
store.dispatch(loginAction('Hut!'));

```

### Use Middleware to Handle Asynchronous Actions

#### Redux Thunk middleware

```
const REQUESTING_DATA = 'REQUESTING_DATA'
const RECEIVED_DATA = 'RECEIVED_DATA'

const requestingData = () => { return {type: REQUESTING_DATA} }
const receivedData = (data) => { return {type: RECEIVED_DATA, users: data.users} }

const handleAsync = () => {
  return function(dispatch) {
    dispatch(requestingData());
    setTimeout(function() {
      let data = {
        users: ['Jeff', 'William', 'Alice']
      }
      dispatch(receivedData(data));
    }, 2500);
  }
};

const defaultState = {
  fetching: false,
  users: []
};

const asyncDataReducer = (state = defaultState, action) => {
  switch(action.type) {
    case REQUESTING_DATA:
      return {
        fetching: true,
        users: []
      }
    case RECEIVED_DATA:
      return {
        fetching: false,
        users: action.users
      }
    default:
      return state;
  }
};

const store = Redux.createStore(
  asyncDataReducer,
  Redux.applyMiddleware(ReduxThunk.default)
);
```


### 帮助实现`state immutability`，JS中的一些方法

* `.push()` and `.splice()` directly modify the array

* `.concat()` doesn’t modify array but just returns a new array. Both arrays still exist separately in memory.

* `.slice()` doesn’t modify array but just returns a new array. Both arrays still exist separately in memory.

* Spread operator `[…array]` doesn’t modify array but just returns a new array. To clone an array but add additional values in the new array, you could write [...myArray, 'new value']. It only provides immutable array operations for one-dimensional arrays.

* insert a new value
	
	```
	[...myArray, 'new value']
	```
	
* remove item at index 
	
	```
	return [
        ...state.slice(0, action.index),
        ...state.slice(action.index + 1, state.length)
      ];
      
    // or 
    
    return state.filter((_, index) => index !== action.index);
	```

* 使用复制函数

	`const newObject = Object.assign({}, obj1, obj2);`
	
	> newObject将复制obj1，然后将obj1中没有obj2属性写入到newObject
	
	
## react-redux

因redux不是开箱即用的库，需要使用`react-redux`包

* React Redux provides a small API with two key features: `Provider` and `connect`. The `Provider` is a wrapper component from React Redux that wraps your React app. This wrapper then allows you to access the Redux `store` and `dispatch` functions throughout your component tree. `Provider` takes two props, the Redux store and the child components of your app. Defining the Provider for an App component might look like this:

```
const Provider = ReactRedux.Provider;

<Provider store={store}>
  <App/>
</Provider>
```

* React Redux is available as a global variable here, so you can access the Provider with dot notation. 

`mapDispatchToProps()`

`mapStateToProps()`


* `connect`: The `connect` method from React Redux can handle this task. This method takes two optional arguments, `mapStateToProps()` and `mapDispatchToProps()`. They are optional because you may have a component that only needs access to state but doesn't need to dispatch any actions, or vice versa.

	To use this method, pass in the functions as arguments, and immediately call the result with your component. This syntax is a little unusual and looks like:
	`connect(mapStateToProps, mapDispatchToProps)(MyComponent)`


```
// Redux:
const ADD = 'ADD';

const addMessage = (message) => {
  return {
    type: ADD,
    message: message
  }
};

const messageReducer = (state = [], action) => {
  switch (action.type) {
    case ADD:
      return [
        ...state,
        action.message
      ];
    default:
      return state;
  }
};

const store = Redux.createStore(messageReducer);

// React:
const Provider = ReactRedux.Provider;
const connect = ReactRedux.connect;

class Presentational extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      input: ''
    }
    this.handleChange = this.handleChange.bind(this);
    this.submitMessage = this.submitMessage.bind(this);
  }
  handleChange(event) {
    this.setState({
      input: event.target.value
    });
  }
  submitMessage() {
    this.props.submitNewMessage(this.state.input);
    this.setState((state) => ({
      input: ''
    }));
  }
  render() {
    return (
      <div>
        <h2>Type in a new Message:</h2>
        <input
          value={this.state.input}
          onChange={this.handleChange}/><br/>
        <button onClick={this.submitMessage}>Submit</button>
        <ul>
          {this.props.messages.map( (message, idx) => {
              return (
                 <li key={idx}>{message}</li>
              )
            })
          }
        </ul>
      </div>
    );
  }
};

const mapStateToProps = (state) => {
  return {messages: state}
};

const mapDispatchToProps = (dispatch) => {
  return {
    submitNewMessage: (message) => {
      dispatch(addMessage(message))
    }
  }
};

const Container = connect(mapStateToProps, mapDispatchToProps)(Presentational);

class AppWrapper extends React.Component {
  render() {
    return (
      <Provider store={store}>
        <Container/>
      </Provider>
    );
  }
};
```

### 实现开发中Redux的样子

```
/*
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider, connect } from 'react-redux'
import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'

import rootReducer from './redux/reducers'
import App from './components/App'

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

ReactDOM.render(
  <Provider store={store}>
    <App/>
  </Provider>,
  document.getElementById('root')
);
*/
```