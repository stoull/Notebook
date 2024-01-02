# Web Development

## Web

### Web UI

#### [Bootstrap](https://getbootstrap.com)

Bootstrap is a front end framework used to design responsive web pages and applications. It takes a mobile-first approach to web development, and includes pre-built CSS styles and classes, plus some JavaScript functionality.

[Build fast, responsive sites with Bootstrap](https://getbootstrap.com)

jQuery is a JavaScript library designed to simplify HTML DOM tree traversal and manipulation, as well as event handling, CSS animations, and Ajax. 

installation: `npm install jquery`

[jQuery](https://jquery.com)

[Downloading jQuery](https://jquery.com/download/)

#### import 

方案一：

```
<script type="text/javascript" src="./static/js/jquery-3.7.1.min.dev.js"></script>
	or 
<script type="text/javascript" src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
// then can use jquery in main.js
<script type="text/javascript" src="./static/js/main.js"></script>
	
```

方案二：

```
var script = document.createElement('script');
script.src = './static/js/jquery-3.7.1.min.dev.js'; // or 'https://code.jquery.com/jquery-3.7.1.min.js'; Check https://jquery.com/ for the current version
document.getElementsByTagName('head')[0].appendChild(script);
```

测试：

```
$(document).ready(function (){
    console.log('document is ready')

    console.log(window.jQuery)
	console.log(window.jQuery === $);
	console.log(typeof($));
})
```
<script> 需要在<head> 位置才能在ready之前


#### 选择器`$`


```
例1:
$(document).ready(function() {
});

例2:
$('.quote-text').animate({ opacity: 0 }, 500, function () {
  $(this).animate({ opacity: 1 }, 500);
  $('#text').text(randomQuote.quote);
});
```

#### SASS

Sass 是一款强化 CSS 的辅助工具，它在 CSS 语法的基础上增加了变量 (variables)、嵌套 (nested rules)、混合 (mixins)、导入 (inline imports) 等高级功能，这些拓展令 CSS 更加强大与优雅。使用 Sass 以及 Sass 的样式库（如 Compass）有助于更好地组织管理样式文件，以及更高效地开发项目。

[Sass中文网](https://www.sass.hk)


### Web HttpReqeust


[Axios](https://github.com/axios/axios)

* Make XMLHttpRequests from the browser
* Make http requests from node.js
* Supports the Promise API
* Intercept request and response
* Transform request and response data
* Cancel requests

AJAX

>
`AJAX` = Asynchronous JavaScript And XML.
>
>`AJAX` is not a programming language.
>
>`AJAX` just uses a combination of:

* A browser built-in XMLHttpRequest object (to request data from a web server)
* JavaScript and HTML DOM (to display or use the data)

jQuery AJAX

“Ajax” stands for Asynchronous Javascript And XML, jQuery provides a condensed format to make XMLHTTPRequest. AJAX is the art of exchanging data with a server and updating parts of a web page — without reloading the whole page.

* Cross-browser support
* Simple methods to use
* Define the type of request

jQuery ajax base syntax:

```
$.ajax({name:value, name:value, … })
$.ajax makes the call to ajax, then the methods are called in place of a name and the callbacks as value, as the example given below.
jQuery ajax Example:
```

## React

React is a popular JavaScript library for building reusable, component-driven user interfaces for web pages or applications.

React combines HTML with JavaScript functionality into its own markup language called JSX. React also makes it easy to manage the flow of data throughout the application.