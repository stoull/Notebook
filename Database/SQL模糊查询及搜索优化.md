# SQL模糊查询及搜索优化


SQL实现查询主要有两种方法一是`LIKE`二是正则表达式函数。



### 使用LIKE 

`LIKE`是写在 where 查询子句中进行条件匹配的，一般使用通配符`%`及`_`或者`[]`:

`%`: 匹配零个或多个任意字符。
`_`: 匹配一个任意字符。

#### 示例
```
SELECT id,name FROM movie WHERE name LIKE '我%'
```
`LIKE '我%'` : 匹配以`我`开头的字符串，如`我的父亲母亲`,`我脑中的橡皮擦`和`我和我的祖国`, 而`何处是我朋友的`则不会匹配
`LIKE '%我%'` : 匹配含`我`的字符串，如`我的父亲母亲`,`我脑中的橡皮擦`和`我和我的祖国`, 及`何处是我朋友的`则不会匹配
`LIKE '秋日_'` : 匹配以`秋日`开头，并且后面只有一个字符的字符串，如`秋日和`,但`秋日`的早晨就不会匹配
`LIKE '_十_'` : 匹配中间为`十`的三个字符的的字符串，如`狗十三`,`二十二`。
`LIKE '我的____'` : 匹配含`我的`的后连四个字符的字符串，如`我的父亲母亲`,但`我的舅舅`不会匹配。

#### 转义字符

转义字符可以将通配符`%`和`_`进行转义，将它们当作普通字符使用。默认的转义字符为反斜杠`\`。如：

`LIKE '50%%'` :  这里匹配`50%`的字符
`LIKE '%_我%'` :  这里匹配以下划画`_我`开头的字符串

#### 大小写匹配
在使用 LIKE 查找数据时，还需要注意的一个问题就是大小写。

* Oracle 和 PostgreSQL 默认区分 LIKE 中的大小写，PostgreSQL 提供了不区分大小写的 ILIKE 运算符；
* MySQL 和 SQL Server 默认不区分 LIKE 中的大小写。

### 使用正则表达式函数

Oracle 和 MySQL 支持类似的正则表达式函数：

```REGEXP_LIKE(source_str, pattern [, match_type]) ```

`[]`: 表示匹配[]中的任意一个字符
`[^]`: 表示匹配不在[]中的任意一个字符

及其它.....

[QL 模糊条件查询](https://deepinout.com/sql/sql-dql/sql-fuzzy-condition-queries.html)


[SQL Grammar](https://forcedotcom.github.io/phoenix/)

[SQL模糊查询的四种匹配模式](https://cloud.tencent.com/developer/article/1492397)

[SQL 模糊查询](https://www.cnblogs.com/GT_Andy/archive/2009/12/25/1921914.html)