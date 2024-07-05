# Swift中的特殊字符与正则匹配

Swift string中需要进行转义的特殊字符有:

| 符号 | 名称 | 显示 |
| --- | ---- | --- |
| \0 | 空字符(null character) | |
| \\  | 反斜线(backslash) | \ |
| \t | 水平制表符horizontal tab | 	|
| \n | 换行符(line feed) | --- |
| \r | 回车符carriage return | --- |
| \" | 双引号  (double quotation mark)| " |
| \' | 单引号single quotation mark | '  |

[Strings and Characters - docx.swift.org](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/stringsandcharacters/)

Special Characters in String Literals
String literals can include the following special characters:

* The escaped special characters \0 (null character), \\ (backslash), \t (horizontal tab), \n (line feed), \r (carriage return), \" (double quotation mark) and \' (single quotation mark)

* An arbitrary Unicode scalar value, written as \u{n}, where n is a 1–8 digit hexadecimal number (Unicode is discussed in Unicode below)

The code below shows four examples of these special characters. The wiseWords constant contains two escaped double quotation marks. The dollarSign, blackHeart, and sparklingHeart constants demonstrate the Unicode scalar format:

```
let wiseWords = "\"Imagination is more important than knowledge\" - Einstein"
// "Imagination is more important than knowledge" - Einstein
let dollarSign = "\u{24}"        // $,  Unicode scalar U+0024
let blackHeart = "\u{2665}"      // ♥,  Unicode scalar U+2665
let sparklingHeart = "\u{1F496}" // 💖, Unicode scalar U+1F496
```

Because multiline string literals use three double quotation marks instead of just one, you can include a double quotation mark (") inside of a multiline string literal without escaping it. To include the text """ in a multiline string, escape at least one of the quotation marks. For example:

```
let threeDoubleQuotationMarks = """
Escaping the first quotation mark \"""
Escaping all three quotation marks \"\"\"
"""
```

## 正则中匹配的特殊字符

Swift string中需要进行转义的特殊字符有: `*.?+$^[](){}|\/`


| 符号 | 名称 |  |
| --- | ---- | --- |
| `$` | 匹配输入字符串的结尾位置。如果设置了RegExp 对象的 Multiline 属性，则也匹配`\n`或`\r`。要匹配字符本身，请使用`\$` | --- |
| `( )` | 标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符，请使用 `\(`和`\)`。 | --- |
| `*` | 匹配前面的子表达式零次或多次。要匹配 `*` 字符，请使用 `\*`。 | --- |
| `+` | 匹配前面的子表达式一次或多次。要匹配 + 字符，请使用 `\+`。 | --- |
| `.` | 匹配除换行符 \n之外的任何单字符。要匹配` .`，请使用 `\.` | --- |
| `[ ]`| 标记一个中括号表达式的开始。要匹配` [`，请使用 `\[`。 | --- |
| `?` | 匹配前面的子表达式零次或一次，或指明一个非贪婪限定符。要匹配 ? 字符，请使用` \?`。 | --- |
| `\` | 将下一个字符标记为或特殊字符、或原义字符、或向后引用、或八进制转义符。例如， `n` 匹配字符`n`。`\n` 匹配换行符。序列 `\\` 匹配 `\`，而 `\(` 则匹配 `(`。 | --- |
| `^` | 匹配输入字符串的开始位置，除非在方括号表达式中使用，此时它表示不接受该字符集合。要匹配 `^` 字符本身，请使用 `\^`。 | --- |
| `{ }` | 标记限定符表达式的开始。要匹配 `{`，请使用 `\{`。 | --- |
| `|` | 指明两项之间的一个选择。要匹配`|`，请使用 `\|`。 | --- |

### 解释：

如果你在正则表达式中想匹配`[`,`\`和`[`。因为这几个字符在正则表达式中有特殊的含义，需要转义(need to be escaped)。即写成`\[`,`\\`,`\]`。

但因为它们又在Swif String里面，并且反斜杠`\`在swift中有特殊的意义，也需要在Swift语言中进行转义。所以在Swift中最终的是`\\[`,`\\\`,`\\]`。

如要匹配`[\]`，正则中的是`\[\\\]`, 在swift中最终的是`\\[\\\\\\]`

如: 
```
var passwordRegex = "^[A-Za-z0-9 !\"#$%&'()*+,-./:;<=>?@\\[\\\\\\]^_`{|}~].{8,}$"
```

## CSV文件中特殊字符的转义


如果字段中有逗号`,`，该字段使用双引号`"`括起来；

如果该字段中有双引号，该双引号前要再加一个双引号，然后把该字段使用双引号括起来。