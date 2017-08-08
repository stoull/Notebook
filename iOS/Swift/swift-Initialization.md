Throughout the tutorial, remember this one golden rule: You cannot use an instance until it is fully initialized. “Use” of an instance includes accessing properties, setting properties and calling methods.

medium:

[Swift Init()](https://medium.com/the-traveled-ios-developers-guide/they-say-it-s-all-about-how-you-finish-d0203c7fbe8a)

简书：

[Swift初始化init中的一些坑](http://www.jianshu.com/p/2c3db48101da)


```
class historyDocument: NSObject {

    var serialNumber: Int64
    var fileName: String?
    
    convenience init(serialNumber: Int64, fileName: String?) {
        self.serialNumber = serialNumber
        self.fileName = fileName
        self.init()
    }
    
    override init() {
        serialNumber = 0
        fileName = "fileName"
        super.init()
    }
    
    
    // 解码
    required init?(coder aDecoder: NSCoder)
    {
        serialNumber = aDecoder.decodeInt64(forKey: "serialNumber")
        fileName = aDecoder.decodeObject(forKey: "fileName") as? String
    }
    
    // 编码
    func encode(with aCoder: NSCoder)
    {
        aCoder.encode(serialNumber, forKey: "serialNumber")
        aCoder.encode(fileName, forKey:"fileName")
    }
}
```

初始化

类的初始化：

1. 每个类都一个系统自带的初始化的方法。如：

```
struct MagicStick {
  let owner: String
  let material: String
  let length: Double
}

// 这个就是使用系统自带的初始化的方法 
// 1. 参数位置必需要按属性位置
let haiBoStick = MagicStick.init(owner: "鲁伯·海格", material: "橡木", length:180)
```

2. 如果不想破坏默认的初始化方法，又想用新的初始化方法。使用 extension

```
extension MagicStick {
    init(owner: String, material: String) {
        self.owner = owner
        self.material = material
        self.length = 120.0
    }
}

let harry = MagicStick.init(owner: "哈利", material: "槭木", length:180.0)
        let fuTeMo = MagicStick.init(owner: "伏地魔", material: "凤凰羽毛")
```
