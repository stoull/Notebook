# React

* React is a JavaScript library for building User Interfaces - Declarative UI Programming.
	- In a model view controller architecture, React is the 'View' which is responsible for how the
app looks and feels.
* React is an Open Source view library created and maintained by Facebook. 
* React uses a syntax extension of `JavaScript` called `JSX` that allows you to write HTML directly within JavaScript. 
	- JavaScript can directly write within JSX. Simply include the code you want to be treated as JavaScript within curly braces: { 'this is treated as JavaScript code' }.
* Because JSX is not valid JavaScript, JSX code must be compiled into JavaScript. transpiler like [Babel.js](https://babeljs.io/setup).
	- `ReactDOM.render(JSX, document.getElementById('root'))`. This function call is what places your JSX into React's own lightweight representation of the DOM. 


### JSX

形如：

	const JSX =  <h1> Hi Rn </h1>;

* JSX is a convenient tool to write readable HTML within JavaScript.
* nested JSX must return a single element
 - several JSX elements written as siblings with no parent wrapper element will not transpile
* JSX 使用 `ReactDOM.render()`方法渲染成html页面，如：`ReactDOM.render(JSX, document.getElementById('challenge-node'))`
* JSX的注释写在`{/* */}`里面，使用camelCase如 `onClick`,`onChange `, 而不是`onchange`或`on_change`
* JSX使用`className`而非`class`, 因`class`被Javascript占用。
* Any JSX element can be written with a self-closing tag, and every element must be closed. 如`<hr />`

* Components are the core of React. Everything in React is a component.
	
	- a stateless functional component:
	
	```
	const DemoComponent = function() {
  return (
    <div className='customClass' />
  );
};
	```
* React component is an `ES6` class which extends `React.Component`. It has a render method that returns HTML (from JSX) or null. 
	- another way to define components class `MyComponent `:
	
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
	`const Welcome = (props) => <h1>Hello, {props.user}!</h1>`
	`<Welcome user={user.name}`
