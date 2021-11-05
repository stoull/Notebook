
## Closures Are Reference Types

## Escaping Closures

**`@escaping`**

>
An escaping closure that refers to self needs special consideration if self refers to an instance of a class. Capturing self in an escaping closure makes it easy to accidentally create a strong reference cycle.

More

>
If self is an instance of a structure or an enumeration, you can always refer to self implicitly. However, an escaping closure can’t capture a mutable reference to self when self is an instance of a structure or an enumeration. 

## Autoclosures
An autoclosure lets you delay evaluation, because the code inside isn’t run until you call the closure.

```
var customersInLine = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
print(customersInLine.count)
// Prints "5"

// 推迟加载属性
let customerProvider = { customersInLine.remove(at: 0) }
print(customersInLine.count)
```

