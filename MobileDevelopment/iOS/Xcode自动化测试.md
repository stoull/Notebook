# Xcode自动化测试


## XCtest

### 定义测试用例及测试方法

* 创建一个继承`XCTestCase`的类为测试用例。使用`Command+N`下拉选择XCtest Unit或者UI test。
* 在创建的类中创建测试方法，测试方法以小写的`test`开头，XCTest framework会自动识别。

### 测试断言

* Bool断言
	- XCTAssert()
	- XCTAssertTrue()
	- XCTAssertFalse()
* Nil断言
	- XCTAssertNil(expression, message)
	- XCTAssertNotNil(expression, message)
* 相等断言
	- XCTAssertEqual(expression1, expression1, message): 比较值是否相等
	- XCTAssertNotEqual(expression1, expression1, message)
	- XCTAssertIdentical(expression1, expression1, message): 比较是否相同的实例
	- XCTAssertNotIdentical(expression1, expression1, message)
* 对比断言
	- XCTAssertGreaterThan(searchField.frame.size.width, 100, "测试一般会通过，因为searchField的宽度一般会大于100")
	- XCTAssertGreaterThanOrEqual(searchField.frame.size.width, 100, "测试一般会通过，因为searchField的宽度一般会大于100")
	- XCTAssertLessThanOrEqual(valueIcon.frame.size.width, 60, "测试一般会通过，因为valueIcon的宽度就是60")
	- XCTAssertLessThan(valueIcon.frame.size.width, 40, "测试应该不通过，因为valueIcon的宽度就是60")
* 错误断言
	- XCTAssertThrowsError(_:_:file:line:_:)
	- XCTAssertNoThrow(_:_:file:line:)
* 不符合条件断言
	- XCTFail("用户名输入框没有输入用户名")

[Defining Test Cases and Test Methods](https://developer.apple.com/documentation/xctest/defining_test_cases_and_test_methods)


### UI元素 XCUIElement

XCUIElement (XCUIElementTouchEvents)

#### 定位

`XCUIElementTypeQueryProvider`: A type that provides ready-made queries for locating descendant UI elements.

示例：

* `app.tabBars.button["Discover"].tap()`
* `app.staticTexts["San francisco"].isHittable`
* `app.images["vault120"].swipeLeft()`

系统提供的有如下等：

* buttons
* images
* textViews
* textFields
* tabBars
* textFields
* staticTexts
* ...

* `- (BOOL)waitForExistenceWithTimeout:(NSTimeInterval)timeout;`: 以对应的超时时间等待其出现
* `- (BOOL)waitForNonExistenceWithTimeout:(NSTimeInterval)timeout;`: 以对应的超时时间等待其没有出现
* `- (XCUIElementQuery *)descendantsMatchingType (XCUIElementType)type;`: 倒序
* `- (XCUIElementQuery *)childrenMatchingType:(XCUIElementType)type;`: 类型

#### 属性 XCUIElementAttributes

* `exists`
* `hittable`
* `debugDescription`

#### 动作: 划，点，缩放，长按.....

示例：
* `app.tabBars.button["Discover"].tap()`: 点击一下名为Discover的tabBars
* `app.images[vault120].swipeLeft()`: 左划一下`vault120`图片

XCUIElementTouchEvents

* `- (void)swipeUp;`
* `- (void)swipeDown;`
* `- (void)swipeLeft;`
* `- (void)swipeRight;`
* `- (void)tap`
* `- (void)focus`
* `- (void)tapWithNumberOfTaps:(NSUInteger)numberOfTaps numberOfTouches:(NSUInteger)numberOfTouches;`
* ...


参考资料：

[Set Up and Tear Down State in Your Tests](https://developer.apple.com/documentation/xctest/xctestcase/set_up_and_tear_down_state_in_your_tests)

[XCUIElement](https://developer.apple.com/documentation/xctest/xcuielement)

[User Interface Testing: A Complete Guide](https://www.headspin.io/blog/ui-testing-a-complete-guide-with-checklists-and-examples)

[XCTest: A Complete Guide](https://www.headspin.io/blog/xctest-a-complete-guide)