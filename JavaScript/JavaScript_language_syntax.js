

let person = {
	name:"Hut",
	age:30
}

console.log(person.name);

console.log(person['age']);

let selectedColors = ['red', 'blue'];
selectedColors[2] = 82;

// here will save 5:index5 as third item in the array
selectedColors[5] = 'index5';
console.log(selectedColors);
console.log(selectedColors[0]);


// Performing a task
function greet(name, lastName) {
	console.log('Hello ' + name + " " + lastName)
}

greet(person.name, 'Chen')
greet("Jane", 'Xiu')

// Caculaing a value
function square(number) {
	return number * number
}

let result = square(4)
console.log(result)


// 面向对象

// 一个计算工资的例子
let baseSalary = 30_000;
let overtime = 10;
let rate = 20;
function getWage(baseSalary, overtime, rate) {
	return baseSalary + (overtime * rate)
}

let totalWage = getWage(baseSalary, overtime, rate)
console.log(totalWage)

// 将上面的例子对象化, 类似class
let employee = {
	baseSalary: 20_000,
	overtime: 10,
	rate: 18,
	getWage: function() {
		return baseSalary + (this.overtime * this.rate);
	}
}
console.log(employee.getWage());


const circle = {
	radius: 1,
	location: {
		x: 1,
		y: 1
	},
	draw: function() {
		console.log('draw')
	}
};

circle.draw();

// 工厂方法 Factory Function
function createCricle(radius) {
	return {
		radius,
		draw: function () {
			console.log('draw createCricle');
		}
	}
}

let circle1 = createCricle(1);
let circle2 = createCricle(2);

circle1.draw();
circle2.draw();

// Constructor function 类似Class的工厂方法
function Circle(radius) {
	// Private 属性 外部不可见
	let defaultLocation = {x: 0, y:0};

	// 类方法
	let turnAround = function(factor) {
	let defaultLocation = {x: 0, y:0};
	console.log('trun around at location: ' + defaultLocation);
		// ...
	}

	this.radius = radius;
	this.draw = function() {
		turnAround()
		console.log('draw Constructor function radius: ' + radius);
	}
	console.log('this', this)

	// 给属性增加setter和getter方法
	Object.defineProperty(this, 'defaultLocation', {
		get: function() {
			return defaultLocation
		},
		set: function(newValue) {
			if (!newValue.x || !newValue.y)
			  throw new Error('Invalid location')
			defaultLocation = newValue
		}
	});
}

const anotherCirle = new Circle(2);
// anotherCirle.defaultLocation = 1;
anotherCirle.draw();

// 在JS中所有都function是object.
const Circel_similar = new Function('radius', `
this.radius = radius;
this.draw = function() {
  console.log('draw in similar as Function')
};
`);

const anothCircle_similar = new Circel_similar(1);
anothCircle_similar.draw()


// Value Types (值类型)
// Number, String, Boolean, Symbol, undefined, null

// Reference Types  (引用类型)
// Object Function

// Object 示例
let obj = { value: 10 };
function increase(obj) {
	obj.value++;
};
increase(obj);
console.log('obj example ' + obj.value);


// 在JS中可以给一个object任意增删property
circle.color = 'red'; 	// 新增一个属性 or circle['color']='red';
console.log('add new property to a object color: ' + circle.color);
delete circle.color;	// 删除一个属性 or circel['color']

// for 循环
console.log('if and for 循环')
for (let key in circle) {
	if (typeof circle[key] != 'function')
		console.log(key, circle[key]);
}

console.log('打印 Object 的keys')
const circleKeys = Object.keys(circle);
console.log(circleKeys);

if ('radius' in circle)  {
	console.log('Circle has radius');
}

// 类 Class
class Animal {
  constructor(name) {
    this.speed = 0;
    this.name = name;
  }
  run(speed) {
    this.speed = speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }
  stop() {
    this.speed = 0;
    alert(`${this.name} stands still.`);
  }
}

let animal = new Animal("My animal");

class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }

  stop() {
    super.stop(); // call parent stop
    this.hide(); // and then hide
  }
}

let rabbit = new Rabbit("White Rabbit");

rabbit.run(5); // White Rabbit runs with speed 5.
rabbit.stop(); // White Rabbit stands still. White Rabbit hides!


// ECMAScript 2015, also known as ES6, introduced JavaScript Classes.
// JavaScript Classes are templates for JavaScript Objects.
class Rectangle {
	// Public field
	height = 0;
	width;

	// Private field
	#max_width = 0;

	constructor(height, width) {
		this.height = height;
		this.width = width;
		this.max_width = width*10;
	}

	static displayName = "Rectangle";
	static isSame(a, b) {
		const aWidth = a.width;
		const aHeight = a.height;
		const bWidth = b.width;
		const bHeight = b.height;
		return aWidth == bWidth && aHeight == bHeight;
	}

	// Getter
	get area() {
		return this.calcArea();
	}

	// Method
	calcArea() {
		return this.height * this.width;
	}

	// Generatro methods
	*getSides() {
		for (let side=0; side<4; side++) {
			if (side%1 == 0) {
				yield height;
			} else {
				yield width;
			}
		}
	}
}

const square_10 = new Rectangle(10, 10);
const square_12 = new Rectangle(12, 12);

console.log(square_10.area);
console.log(Rectangle.displayName);
const isSame = Rectangle.isSame(square_10, square_12)










