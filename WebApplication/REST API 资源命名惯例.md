# REST API 资源命名惯例

REST即是`REpresentational State Transfer`, 中文是表述性状态传递，由计算机科学家 Roy Fielding 于2000年创建。

REST并不像协议(如HTTP)一样是一个标准，它是一个架构规范或者一个风格约定，并且建立于HTTP之上，用于REST API设计。主要通用的原则有：

* 服务与客户端(Client-server)分离，之间的资源通过HTTP请求管理。
* 无状态客户端-服务器通信，即在请求期间，不会存客户端信息，每一个请求都是独立,互不关联的。
* HTTP接口传递的资源都使用URIs进行定位，即使用资源定位符(Resource identifiers)使用接口统一，信息以标准形式传输。
* 各类型服务器会对不同功能有分层系统，及对请求有缓存策略，但对客户端请求不可见。

很多API也不采用REST标准设计API,像会使用SOAP(简单对象访问协议),但相比之下，REST 则是一组可按需实施的准则，使 REST API 速度更快、更轻，可扩展性更高，非常适合物联网（IoT）和移动应用开发。 

实现了REST的API即是RESTful API，RESTful是形容词。

## REST资源命名规则

* 什么是资源

服务器与客户端之间的传递的就是资源。

>
The key abstraction of information in REST is a resource. Any information that can be named can be a resource: a document or image, a temporal service (e.g. “today’s weather in Los Angeles”), a collection of other resources, a non-virtual object (e.g., a person), and so on.
>
— Roy Fielding’s dissertation


### 单个资源与群组资源区分

**使用单复数据对单个资源与群组资源进行区分**

一个资源可能是单个或多个数据实体，像一本书`book`是单个资料，而一个书单`books`就是群组资源包含多个数据实体。

这里可以使用URI`/books`标识一个书单，而单个一本书可以使用`/books/{book-id}`进行标识。



### 群组资源与子群组资源
群组资源中的实体可能包含子群组资源

如一个书单里的书有有目录，可以使用`/books/{book-id}/contents`标识，如果要指定某个目录，则使用`/books/{bookId}/contents/{content-id}`进行标识

### URL
REST 使用[统一资源标识符-Uniform Resource Identifiers](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)对各资源进行引用。如果命名不好则会在使用和理解上造成困扰。


>
The constraint of a uniform interface is partially addressed by the combination of URIs and HTTP verbs and using them in line with the standards and conventions.

#### 使用名词标识资源

RESTful风格的URIs是用来标识资源的，所有的资源都应该是名词。URIs中不应该出现任何 CRUD (Create, Read, Update, Delete)等动作的标识的词，也不应该出现动名词组合的词，如连词: `get-book`, 蛇形: `delete_book`, 或者驼峰: `updateBook`。

不好的示例：
>
http://api.example.com/v1/store/CreateItems/{item-id}❌
http://api.example.com/v1/store/getEmployees/{emp-id}❌
http://api.example.com/v1/store/update-prices/{price-id}❌
http://api.example.com/v1/store/deleteOrders/{order-id}❌

好的示例：
>
http://api.example.com/v1/store/items/{item-id}✅
http://api.example.com/v1/store/employees/{emp-id}✅
http://api.example.com/v1/store/prices/{price-id}✅
http://api.example.com/v1/store/orders/{order-id}✅

#### 使用复数标识群组资源
>
http://api.example.com/v1/books/{book-id}/contents/{content-id}✅

>
http://api.example.com/v1/book/{book-id}/contents/{content-id}❌

#### 使用HTTP中的Methods表示资源的操作动作
常见的HTTP操作类型：

* GET(SELECT)：从服务器检索特定资源，或资源列表。
* POST(CREATE)：在服务器上创建一个新的资源。
* PUT(UPDATE)：更新服务器上的资源，提供整个资源。
* PATCH(UPDATE)：更新服务器上的资源，仅提供更改的属性。
* DELETE(DELETE)：从服务器删除资源。

正确示例 :

> 出自[RESTful风格规范](https://www.cnblogs.com/MTRD/p/12153561.html) :

```
单资源( singular-resourceX )
url样例：order/ (order即指那个单独的资源X)
GET – 返回一个新的order
POST- 创建一个新的order，从post请求携带的内容获取值。

单资源带id(singular-resourceX/{id} )
URL样例：order/1 ( order即指那个单独的资源X )
GET – 返回id是1的order
DELETE – 删除id是1的order
PUT – 更新id是1的order，order的值从请求的内容体中获取。


复数资源(plural-resourceX/)
URL样例:orders/
GET – 返回所有orders

复数资源查找(plural-resourceX/search)
URL样例：orders/search?name=123
GET – 返回所有满足查询条件的order资源。(实例查询，无关联) – order名字等于123的。

 复数资源查找(plural-resourceX/searchByXXX)
URL样例：orders/searchByItems?name=ipad
GET – 将返回所有满足自定义查询的orders – 获取所有与items名字是ipad相关联的orders。

单数资源(singular-resourceX/{id}/pluralY)
URL样例：order/1/items/ (这里order即为资源X，items是复数资源Y)
GET – 将返回所有与order id 是1关联的items。

singular-resourceX/{id}/singular-resourceY/
URL样例：order/1/item/
GET – 返回一个瞬时的新的与order id是1关联的item实例。
POST – 创建一个与order id 是1关联的item实例。Item的值从post请求体中获取。

singular-resourceX/{id}/singular-resourceY/{id}/singular-resourceZ/
URL样例：order/1/item/2/package/
GET – 返回一个瞬时的新的与item2和order1关联的package实例。
POST – 创建一个新的与item 2和order1关联的package实例，package的值从post请求体中获得。


以上规范是以查询为主，下面重点说一下patch

patch主要用来更改部分字段，比如重命名，或者更改实体的状态。这个时候两个方法都要写，，不能都写成Patch /order/{id},这样区分不出来。这个时候可以这样做

/order/{id}/name (用来重命名)

/order/{id}/status(用来更改用户状态)

这样就可以通过url和 method的两种方式完美的区分开了两个方法。

此处特殊说明一下，有的博客中使用/order/name/{id}这样的命名规范，将id放在字段的后面，我不确定那种正确，但是根据查询的相关规则，我选择id还是直接跟在order后面合适。
```

#### 使用连字符`-`增加URIs的可读性

```
http://api.example.com/devicemanagement/manageddevices/
http://api.example.com/device-management/managed-devices 	/*This is much better version*/
```

在URIs中不要使用下划线`_`，下划线`_`有可能在某些浏览器上不兼容。


其他规范

**一些其他规范：**

* 规则1：URI结尾不应包含（/）
* 规则2：正斜杠分隔符（/）必须用来指示层级关系
* 规则3：应使用连字符（ - ）来提高URI的可读性
* 规则4：不得在URI中使用下划线（_）
* 规则5：URI路径中全都使用小写字母

[REST API Tutorial](https://restfulapi.net)


[RESTful风格的接口命名规范 ](https://www.cnblogs.com/MTRD/p/12153561.html)

[REST Resource Naming Guide](https://restfulapi.net/resource-naming/)

[REST API Naming Conventions and Best Practices](https://medium.com/@nadinCodeHat/rest-api-naming-conventions-and-best-practices-1c4e781eb6a5)