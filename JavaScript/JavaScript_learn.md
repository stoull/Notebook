

// This is an in-line comment.

/* This is a
multi-line comment */

Data types: `undefined`, `null`, `boolean`, `string`, `symbol`, `bigint`, `number`, and `object`.

全局作用域, 变量提升（不管在哪儿定义的，整个环境都可以用）
`var ourName = "ccc";`

块级声明变量（只有作用域里才能用的变量）
`let camper = "James";`
块级声明常量（只有作用域里才能用的变量）
`const FAV_PET = "Cats";`
`const product = 8 * 10;`

操作符号
`+=` `-=` `*=` `/=`

`const product = 11%2;`
`const ourStr = "I come first. " + "I come second.";`

转义符为`\`
```const sampleStr = "Alan said, \"Peter is learning JavaScript\".";```
```const goodStr = 'Jake asks Finn, "Hey, let\'s go on an adventure?"'; ```

|转义|输出|
|----|----|
|`\'`|single quote|
|`\"`|double quote|
|`\\`|backslash|
|`\n`|newline|
|`\r`|carriage return|
|`\t`| tab |
|`\b`|word boundary|
|`\f`|form feed|
 
In JavaScript all variables and function names are case sensitive.

When JavaScript variables are declared, they have an initial value of undefined 


### 字符串操作
>
>let firstName = "Kevin";
>
>firstName.length; firstName[firstName.length-2];
>
>let fullName = firstName + "Chen"

```
slice(start, end)
substring(start, end)
substr(start, length)
```
// 大小定转换
'a'.toUpperCase()
'A'.toLowerCase() 

### array

```
const sandwich = ["peanut butter", "jelly", "bread"];

const myArray = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, "SkyWalker"],
  [[10, 11, 12], 13, 14],
];

const myData = myArray[2][1]; // 8
```

更多方法有：
>```toString(), push(), pop(), shift(), unshift(), splice(), slice(), indexOf(), every(), forEach(), map() etc```

```
const arr1 = [1, 2, 3];
arr1.push(4); 		// 在最后面增加一个元素 [1,2,3,4]
arr1.unshift(8);		// 在最前面增加一个元素 [8,1,2,3,4]
const oneDown = arr1.pop();		// 移除最后面的一个元素 4
const oneShift = arr1.shift();	// 移除最前面的一个元素 8


// 删除array中间截n个值 splice
let array = ['I', 'am', 'feeling', 'really', 'happy'];
let newArray = array.splice(3, 2);	// 3为开始位置，2为长度 newArray 为 ['really', 'happy'] array 为 ['I', 'am', 'feeling']

// 替换 splice
const numbers = [10, 11, 12, 12, 15];
const startIndex = 3;
const amountToDelete = 1;
numbers.splice(startIndex, amountToDelete, 13, 14);    // 结果为[ 10, 11, 12, 13, 14, 15 ]

// 复制array中间截n个值 slice
slice() takes only 2 parameters — the first is the index at which to begin extraction, and the second is the index at which to stop extraction

let weatherConditions = ['rain', 'snow', 'sleet', 'hail', 'clear'];
let todaysWeather = weatherConditions.slice(1, 3);	// 结果 todaysWeather为['snow', 'sleet'] weatherConditions 保持不变

// 全部复制
let thisArray = [true, true, undefined, false, null];
let thatArray = [...thisArray];	// thatArray 为 [true, true, undefined, false, null] thisArray保持不变

// 全部插入
let thisArray = ['sage', 'rosemary', 'parsley', 'thyme'];
let thatArray = ['basil', 'cilantro', ...thisArray, 'coriander'];

// 查找
let fruits = ['apples', 'pears', 'oranges', 'peaches', 'pears'];

fruits.indexOf('dates');	// -1
fruits.indexOf('oranges');	// 2
fruits.indexOf('pears');	// 1

```


### function

```
function testFun(param1, param2) {
  console.log(param1, param2);
}
```


### condition
```
if (k==12) {

} else if () {

} else {

}

switch (lowercaseLetter) {
  case "a":
    console.log("A");
    break;
  case "b":
    console.log("B");
    break;
}

1 == '1'	// true	JavaScript performs type conversion from string to number
1 === 1	// true
1 === '3'	// false
0 != 2 	// true
4 !== '4'	// true
7 > '3' 	// true
6 >= 6		// true
a ? b : c

if (num > 5 && num < 10) {
  return "Yes";
}

if (num > 10 || num < 5) {
  return "No";
}
```

### Object

```
const ourDog = {
  "name": "Camper",
  "legs": 4,
  "tails": 1,
  "friend names": ["everything!"],
  "bark": "bow-wow"
};

const dogName = ourDog.name;
const fNames = ourDog['friend names'];
ourDog['new property'] = "new value";
ourDoc.speed = 32;
delete ourDog.bark;		// remove the property of 'bark'
ourDog.hasOwnProperty("bark");	// 是否有bark属性
'bark' in ourDog;	// 是否有bark属性
```
loop all keys in an object:

```
const users = {
  Alan: {
    online: false
  },
  Jeff: {
    online: true
  },
  Sarah: {
    online: false
  }
}

function countOnline(usersObj) {
  let onlineUserCount = 0
  for (let user in usersObj) {
    if (usersObj[user].online == true) {
      onlineUserCount += 1
    }
  }
  return onlineUserCount
}

console.log(countOnline(users));
```

### Lookup
```
const alpha = {
  1:"Z",
  2:"Y",
  3:"X",
  4:"W",
  ...
  24:"C",
  25:"B",
  26:"A"
};

const thirdLetter = alpha[2];	// Y
```

### Nested Objects

```
const myStorage = {
  "car": {
    "inside": {
      "glove box": "maps",
      "passenger seat": "crumbs"
     },
    "outside": {
      "trunk": "jack"
    }
  }
};

const gloveBoxContents = myStorage.car.inside['glove box']; // maps
```

### Loop

```
while (a>0) {
}

do {
  ourArray.push(i);
  i++;
} while (i < 5);

for (let i = 0; i < 10; i += 2) {
  ourArray.push(i);
}
```


### Random

```
Math.random()		// 生成0～1的随机数，不包括1
Math.floor(Math.random() * 20);	// 生成0～19的随机数，不包括20 Math.floor()，round取整

Math.floor(Math.random() * (max - min + 1)) + min // 生成min-max的随机数

```


### 类型转换
const a = parseInt("007");		// 7 string to int 默认为十进制，可设置进制2～36如下：

const a = parseInt("10011", 2);		// 19 



## ES6

### 变量提升

```
const s = [1,2,3,4];
s = [2,3];	// error
s[1] = 2;		// right
```

`Object.freeze(obj);`		// Prevent Object Mutation


### 匿名函数

```
const magic = () => {
  return new Date();
}
```

等同与

```
let magic = function() {
  return new Date();
};
```
传参数：
`const doubler = (item) => item * 2;`

如只有一个参数：
`const doubler = item => item * 2;`

多个参数:

```
const multiplier = (item, multi) => item * multi;
multiplier(4, 2);
```

设置默认值：
`const increment = (number=0, value=1) => number + value;`


### Use the Rest Parameter with Function Parameters

```
const sum = (...args) => {
  let total = 0;
  for (let i=0; i<args.length; i++) {
    total += args[i];
  }
  return total;
}
```

### Array 拆包：

```
const arr1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY'];
let arr2;
arr2 = [...arr1] 	// arr2 为 ['JAN', 'FEB', 'MAR', 'APR', 'MAY'];
```

### 解构及赋值

```
const HIGH_TEMPERATURES = {
  yesterday: 75,
  today: 77,
  tomorrow: 80
};

需对应key值

const {today, tomorrow} = HIGH_TEMPERATURES;
等同与：
const today = HIGH_TEMPERATURES.today;
const tomorrow = HIGH_TEMPERATURES. tomorrow;

// 赋新值 可嵌套
const {today: highToday, tomorrow: highTomorrow} = HIGH_TEMPERATURES;
等同与：
const highToday  = HIGH_TEMPERATURES.today
const highTomorrow = HIGH_TEMPERATURES. tomorrow

函数参数解构
const profileUpdate = ({ yesterday, today, tomorrow}) => {
	return [yesterday, today, tomorrow];
}

console.log(profileUpdate(HIGH_TEMPERATURES))

```

#### 解构赋值

```
const [a, b,,, c] = [1, 2, 3, 4, 5, 6];
console.log(a, b, c);	// a,b,c为1，2，5

转换a和b的值：
let a = 8, b = 6;
[a, b] = [b, a];

const [a, b, ...arr] = [1, 2, 3, 4, 5, 7];
console.log(a, b);		// 1,2
console.log(arr);		// [3，4，5，7]
```

### String 
使用 \`而不是（'或者"）表示string的起止，参数引用格式：`${variable}`， 示例：

```
const person = {
  name: "Zodiac Hasbro",
  age: 56
};

const greeting = `Hello, my name is ${person.name}!
I am ${person.age} years old.`;

console.log(greeting);
```

###  Concise Declarative

#### 对象创建
```
const createPerson = (name, age, gender) => {
  return {name, age, gender};
};

或者
const createPerson = (name, age, gender) =>（{name, age, gender});

等同与：
const createPerson = (name, age, gender) => {
  return {
    name: name,
    age: age,
    gender: gender
  };
};
```

#### Class定义及创建

```
class Book {
  constructor(author) {
    this._author = author;
  }
  
  // getter
  get writer() {
    return this._author;
  }
  
  // setter
  set writer(updatedAuthor) {
    this._author = updatedAuthor;
  }
}
```

#### 函数定义

```
const bicycle = {
  gear: 2,
  setGear(newGear) {
    this.gear = newGear;
  }
};
```

### 代码 module 共享

```
<script type="module" src="filename.js"></script>
export { uppercaseString, lowercaseString };
import {uppercaseString, lowercaseString} from './string_functions.js';
import * as myMathModule from "./math_functions.js";

如果一个文件里只有一个export的函数或者属性，可以使用`default`关键字，这样在`import`文件中使用任何名字引用这个属性
// math_functions.js
export default function add(x, y) {
  return x + y;
}

// string_functions.js
import subtract from './math_functions.js'; // 这里 subtract 就是function()
```


### Promise

```
const makeServerRequest = new Promise((resolve, reject) => {
  let responseFromServer = true;
    
  if(responseFromServer) {
    resolve("We got the data");
  } else {  
    reject("Data not received");
  }
});

makeServerRequest.then(result => {
  console.log(result);
});

makeServerRequest.catch(error => {
  console.log(error);
});
```


## Regular Expressions

##### 语法定义

使用`/regular expression here/` 格式定义，如：

`let catRegex = /cat/;`

### 存在 test

`et petString = "James has a pet cat.";`
`let catRegex = /cat/;	`

#####  使用`|`表示或匹配多个期望值：

`let petRegex = /dog|cat|bird|fish/;`

##### `i` 忽略大小写

`let hosterRegex = /James/i;`

##### 进行结果运算

`let result = petRegex.test(petString);`

### 匹配 match

##### 单个匹配

```
let extractStr = "Extract the word 'coding' from this string.";
let codingRegex = /coding/; 
let result = extractStr.match(codingRegex);  // result[0] 为 coding

result 为：
[ 'coding',
  index: 18,
  input: 'Extract the word \'coding\' from this string.',
  groups: undefined ]

```

##### 多个匹配

```
let twinkleStar = "Twinkle, twinkle, little star";
let starRegex = /twinkle/ig;
let result = twinkleStar.match(starRegex); // result 为：['Twinkle', 'twinkle']

/[aeiou]/ig
/[A-Za-z0-9_]/ig		// same as  /\w/g
/\w/					// same as  /[A-Za-z0-9_]/ig
/\W/					// same as /[^A-Za-z0-9_]/
/\s/					// same as /[ \r\t\f\n\v]/
/\S/					// same as [^ \r\t\f\n\v]

\d		// digits
\D		// non-digits

/[^aeiou0-9]/gi
/^Cal/
/caboose$/
/s+/g
/Aa*/g
/Tim{3,}ber/		// 3 or more
/Tim{3}ber/			// exactly 3 times
/favou?rite/		// match ‘favorite’ or ‘favourite’

/(?=\w{6,})(?=\w*\d{2,})/ // match 大于六位，且有连续的两个数字

```

##### Lazy Matching

```
let aString = "titanic";
let greedyMatch = "/t[a-z]*i/";		// return ["titani"]
let lazyMatch = "/t[a-z]*i/";		// return ["ti"]
```


##### Group

```
/P(engu|umpk)in/	// match 'Penguin' or 'Pumpkin'
let repeatRegex = /(\w+) \1 \1/;	// \1 means same as the first group

```

##### Replace

```
let wrongText = "The sky is silver.";
let silverRegex = /silver/;
wrongText.replace(silverRegex, "blue");	// 结果为 "The sky is blue"

"Code Camp".replace(/(\w+)\s(\w+)/, '$2 $1');  // 结果为 "Camp Code"

"Any string".replace(/^\s+|\s+$/g, '');  // 移除字符串前后的空格

```


## Data Structures

console.log(typeof "");




## Object Oriented Programming

`this` keyword present the class self.


### Constructor

```
function Bird(name, color) {
  this.name = name;
  this.color = color;
  this.numLegs = 2;
  
  // Here age is a private propety
  let age = 3;
}

let blueBird = new Bird();

```

> Anytime a constructor function creates a new object, that object is said to be an instance of its constructor. 

#### `instanceof` check class type return `true` or `false`

`blueBird  instanceof  Bird;` // will return `true`

`blueBird.constructor === Bird`	// will return `true` but constructor can be overwritten

#### `ownProps` Properties

```
for (let property in blueBird) {
  if(blueBird.hasOwnProperty(property)) {
    ownProps.push(property);
  }
}
console.log(ownProps);	// name color and numLegs
```

#### `Prototype` Properties
* `prototype` as a "recipe" for creating objects. Nearly every object in JavaScript has a prototype property which is part of the constructor function that created it.
* an object inherits its prototype directly from the constructor function that created it
* an object’s prototype itself is an objec
* prototype chain

`Bird.prototype.canFly = true`	// Added a class property to the class of `Bird`, so every instance of Bird has this property

```
let ownProps = [];
let prototypeProps = [];

for (let property in duck) {
  if(duck.hasOwnProperty(property)) {
    ownProps.push(property);
  } else {
    prototypeProps.push(property);
  }
}

console.log(ownProps);
console.log(prototypeProps);

```

`Bird.prototype.isPrototypeOf(blueBird);`
`Object.prototype.isPrototypeOf(Bird.prototype);`

`Object` is a supertype for all objects in JavaScript.

#### `Prototype` set more Properties at once

```
Bird.prototype = {
  constructor: Bird,
  numLegs: 2, 
  eat: function() {
    console.log("nom nom nom");
  },
  describe: function() {
    console.log("My name is " + this.name);
  }
};
```

#### 继承 Inherite

父类：

```
function Animal() { }
Animal.prototype.eat = function() {
  console.log("nom nom nom");
};

```

子类：

```
function Bird() { }
Bird.prototype = Object.create(Animal.prototype);
Bird.prototype.constructor = Bird;

// 子类的方法
Bird.prototype.fly = function() {
  console.log("I'm flying!");
};

let duck = new Bird();
duck.eat();
duck.fly();
```

#### mixins Extension 扩展

> A mixin allows other objects to use a collection of functions.

A collection of functions:

```
let flyMixin = function(obj) {
  obj.fly = function() {
    console.log("Flying, wooosh!");
  }
};

```

Apply the collection of functions to objects:

```
let bird = {
  name: "Donald",
  numLegs: 2
};

let plane = {
  model: "777",
  numPassengers: 524
};

flyMixin(bird);
flyMixin(plane);
```

#### Block Immediately Invoked Function Expression (IIFE)


```
(function () {
  console.log("Chirp, chirp!");
})();
```

**often used to group related functionality into a single object or module**

相关功能方法:

```
function glideMixin(obj) {
  obj.glide = function() {
    console.log("Gliding on the water");
  };
}
function flyMixin(obj) {
  obj.fly = function() {
    console.log("Flying, wooosh!");
  };
}
```

利用代码块合并成一个模块:

```
let motionModule = (function () {
  return {
    glideMixin: function(obj) {
      obj.glide = function() {
        console.log("Gliding on the water");
      };
    },
    flyMixin: function(obj) {
      obj.fly = function() {
        console.log("Flying, wooosh!");
      };
    }
  }
})();
```

```
motionModule.glideMixin(duck);
duck.glide();
```

























