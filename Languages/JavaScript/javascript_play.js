let person = {
	name: "Hut",
	age: 30
}

console.log(person.name);

let work = {
	type: "hard_model",
}

function hard_work(hours) {
	console.log(person.name + " hard_work " + hours)
}

console.log(person.age);
hard_work(8);

function a_test_func() {
	const w_per_m = 8
	const month = 3
	return w_per_m * month
}

console.log(a_test_func())

let employee = {
	bases: 8,
	pwe: 29,
	rate: 20,
	getWage: function() {
		return this.bases*this.pwe+this.rate;
	},
	per_f: function() {
		return "Run away"
	}
}

let aemp = employee;
console.log(aemp.getWage())

const circle = {
	radius: 1,
	location: {
		x: 1,
		y: 1
	},
	draw: function() {
		return "Drawed"
	}
}

console.log(circle.draw())

function Circle(radius) {
	let defaultLocation = {x: 3, y: 3}

	let turnArround = function(factor) {
		let defaultLocation = {x: 0, y:0};
		console.log('trun around at ' + defaultLocation); 

	}

	this.radius = radius;
	this.draw = function() {
		turnArround()
		console.log('darw Constructor function radius: ' + radius);
	}
	console.log('this', this)
}

const an_cirle = new Circle(2);
an_cirle.draw();


var Circle_similar = new Function('radius',`
	this.radius = radius;
	this.darw = function() {
		console.log('Circle_similar darw the function')
	};
`);

let an_2_cirle = new Circle_similar(5);
an_2_cirle.darw();

let obj = {value: 10};
function inrease(obj) {
	obj.value++;
}

inrease(obj);

console.log("obj " + obj.value);


// 匿名函数

const magic = () => {
	console.log('This is no name function!')
}

magic()

const doubler = item => item*2;


console.log(doubler(2))

const High_temperature = {
	yesterday: 75,
	tody: 77,
	tomorrow: 89
};

const {yesterday, tomorrow} = High_temperature;

console.log(yesterday + " : " + tomorrow)


const profileUpdate = ({yesterday, tody, tomorrow}) => {
	return [yesterday, tody, tomorrow];
};

console.log(profileUpdate(High_temperature))

console.log(typeof "Hello");




console.log(typeof null);
const type_null = Object.prototype.toString.call(null);
console.log(type_null);

let max = Number.MAX_SAFE_INTEGER;

let max1 = max + 1
let max2 = max + 2

console.log(`max is : ${max}. max1 == max2 is: ${max1==max2}`);














