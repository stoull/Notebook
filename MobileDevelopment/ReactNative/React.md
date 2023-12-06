# React

* React is a JavaScript library for building User Interfaces - Declarative UI Programming.
	- In a model view controller architecture, React is the 'View' which is responsible for how the
app looks and feels.
* React is an Open Source view library created and maintained by Facebook. 
* React uses a syntax extension of `JavaScript` called `JSX` that allows you to write HTML directly within JavaScript. 
	- JavaScript can directly write within JSX. Simply include the code you want to be treated as JavaScript within curly braces: { 'this is treated as JavaScript code' }.
* Because JSX is not valid JavaScript, JSX code must be compiled into JavaScript. transpiler like [Babel.js](https://babeljs.io/setup).
	- `ReactDOM.render(JSX, document.getElementById('root'))`. This function call is what places your JSX into React's own lightweight representation of the DOM. 


## JSX

形如：

	const JSX =  <h1> Hi Rn </h1>;

* JSX is a convenient tool to write readable HTML within JavaScript.
* nested JSX must return a single element
 - several JSX elements written as siblings with no parent wrapper element will not transpile
* JSX 使用 `ReactDOM.render()`方法渲染成html页面，如：`ReactDOM.render(JSX, document.getElementById('challenge-node'))`
* JSX的注释写在`{/* */}`里面，使用camelCase如 `onClick`,`onChange `, 而不是`onchange`或`on_change`
* javascript的代码可以写在`{ js code}`中。也可写在`render()`方法中，`return`之前可以直接使用js代码，不需要`{}`
* JSX使用`className`而非`class`, 因`class`被Javascript占用。
* Any JSX element can be written with a self-closing tag, and every element must be closed. 如`<hr />`

* Components are the core of React. Everything in React is a **component**.
	
	- A **stateless functional component**:
	
	```
	const DemoComponent = function() {
  return (
    <div className='customClass' />
  );
};
	```
* React component is an `ES6` class which extends `React.Component`. It has a render method that returns HTML (from JSX) or null. 
	- another way to define **components** class `MyComponent `:
	
	```
	class Kitten extends React.Component {
	  constructor(props) {
	    super(props);
	  }
	  render() {
	    return <h1>Kitten class</h1>
  }
};
	```
	注：`render()`方法中，return之前可以直接使用js代码，不需要`{}`

* 使用多个component组合, 如创建一个app, 有`Navbar`,`Dashboard`,`Footer`, 这个时间需要创建一个父component,命名为`App`, 如下：

	```
	return (
		 <App>
		  <Navbar />
		  <Dashboard />
		  <Footer />
		 </App>
		)
	```
* components can nest. break down your UI into its basic building blocks, and those pieces become the components.
* JSX使用props在各Components间进行传值,如：

	- 单个props值
	`const Welcome = (props) => <h1>Hello, {props.username}!</h1>` 定义
	传值: `<Welcome username={user.name}` 
	- 多个props值
	
	```
	<ParentComponent>
  <ChildComponent colors={["green", "blue", "red"]} />
</ParentComponent>
	
	const ChildComponent = (props) => <p>{props.colors.join(', ')}</p>
	```
	- 默认值及类型约束
	 
	`ChildComponent.defaultProps = { location: 'San Francisco' }`： 设置默认值。
	
	`MyComponent.propTypes = { handleClick: PropTypes.func.isRequired }`
	`PropTypes.func` 表示MyComponent的prop类型是function, isRequired表示一定要赋这个`function`值。更多类型及使用可参见[prop-types](https://www.npmjs.com/package/prop-types)
	
	- ES6 class component 中使用props
	
		在字Components中使用`this.props.theParameters` 访问theParameters参数。 如：
		
		```
	    constructor(props) {
	        super(props);
	        this.name = props.name
	    }
	
	    render() {
	        return (
	            <p>{this.name}</p>
	        );
	    }
		```
		

### Stateful component

State consists of any data your application needs to know about, that can change over time. You want your apps to respond to state changes and present an updated UI when necessary. 

ou have access to the state object throughout the life of your component. You can update it, render it in your UI, and pass it as props to child components. The state object can be as complex or as simple as you need it to be.

#### Stateless component  vs Stateful component

* A stateless functional component is any function you write which accepts props and returns JSX. 
* Stateless functional componentis a class that extends `React.Component`, but does not use internal state
* A stateful component is a class component that does maintain its own internal state

#### State

使用`this.state = {}`进行定义，使用`this.state.name`获取其中的值，如下：
	
```
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: 'Initial State'
    };
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.setState({
      name: 'React Rocks!'
    })
  }
  render() {
    return (
      <div>
        <button onClick={this.handleClick}>Click Me</button>
        <h1>{this.state.name}</h1>
      </div>
    );
  }
};
```

* `state`用于追踪数据的变化并在界面上发生改变
* React使用虚拟DOM检测`state`中的属性发生改变时，会触发`render()`方法，以及`prop`中有用到`state`的子视图。但只有有必须渲染的，才会渲染到真正的DOM中。
*  `state`是私有的，只有在本component才能引用。如果要在子视图中使用，需要通过`props`.
*  使用`this.setState()`. React 可能 batch multiple setState() calls into a single update. 所以在`setState`中不能直接使用属性`this.state.xxx`,而要使用方法如下：

	```
	this.setState((state, props) => ({
  counter: state.counter + props.increment
}));
	```
	```
	this.setState(state => ({
  counter: state.counter + 1
}));
	```
* 父子`component`之前的交互，通过props传方法

### Component 生命周期

* React provides a synthetic event system which wraps the native event system present in browsers.
*  if you want to attach an event handler to the document or window objects, you have to do this directly.

主要的生命周期点有：

* `componentWillMount() `: Is called before the render() method when a component is being mounted to the DOM
* `componentDidMount() `: This method is called after a component is mounted to the DOM. 在这之后所有的`setState()`都会re-rendering components。这里可以进行网络请求，设置事件监听
* `shouldComponentUpdate() `: akes nextProps and nextState as parameters。在此方法决定那些变化需要re-rendering，返回true or false
* `componentDidUpdate() `
* `componentWillUnmount()`

### Inline Styles in React

styling your components

* Inline Styles

`<div style= {{color: 'red', fontSize: 72}}>Big Red</div>`

* using a style object

```
const styles = {
  color: "purple",
  fontSize:40,
  border: '2px solid purple',
  width: 235,
  margin: 5
}

class MyComponent extends React.Component {
	constructor(props) {
    super(props);
    this.state = {
      display: true
    }
    this.toggleDisplay = this.toggleDisplay.bind(this);
  }
  toggleDisplay() {
    this.setState(state => ({
      display: !state.display
    }));
  }
  
    render() {
    if (this.state.display) {
        return (
       		<div>
         			<button onClick={this.toggleDisplay}>Toggle Display</button>
         			<h1 style={styles} >Displayed!</h1>
       		</div>
    	);
    } else {
    	    return (
       		<div>
         			<button onClick={this.toggleDisplay}>Toggle Display</button>
       		</div>
    		);
    }
  }
};
```

* 使用if/else简写判断 `&&` 可将上面的`render()`改写成如下：

```
render() {
    return (
      <div>
       <button onClick={this.toggleDisplay}>Toggle Display</button>
         {this.state.display && <h1 style={styles} >Displayed!</h1>}
      </div>
    );
```

* `condition ? expressionIfTrue : expressionIfFalse;`
* 多个数据创建

	```
	const renderFrameworks = frontEndFrameworks.map((item) =>
  <li key={item}>{item}</li>
);
	```

### 将 React 转成html 放到服务器Server

* 刚开始加载会是空白页。 如果不将React app 转成html, app将会是空的html, 并且有很大的js bundle。这要将bundle下载，再转成html
* 转成html可以被搜索引擎搜索到。
* 更快的打开，因为html比JavaScript小。