#Xcode-常用代码块


#### MARK

```
// MARK: - <#Description#>
```

#### 注释

```
/**
 **<#对方法功能的简单描述#>**
 - Parameter para1: <#对参数1的描述#>
 - Parameter para2: <#对参数2的描#>
 - Throws: <#对异常错误的说明#>
 - Returns: <#对返回值的说明描述#>
 * <#Discussion 使用 -或* 开头分条说明#>
 * Examples:
 ```
 protocol GTModbusDataReadProtocol: GTModbusProtocol {}
 ```
 */
```

	
#### 注释-OC

```
    /**
         @abstract <#对方法功能的简单描述#>
         @param param1           <#对参数1的描述#>
         @param param2           <#对参数2的描述#>
         @discussion <#对该方法的特别说明，条件，环境，行为等因素#>
         @return <#对返回值的说明描述#>
         */
```

#### UserDefault使用

```
 var <#defaultsKey#>: <#Type#> {
     get { return <#typeof#>(forKey: #function) }
     set { set(newValue, forKey: #function) }
 }
```

[XcodeCodeSnippets](https://github.com/ismetanin/XcodeCodeSnippets)