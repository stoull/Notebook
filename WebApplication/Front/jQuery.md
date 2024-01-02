# jQuery

## jQuery

### 常用查找选取

	$("button")				// 按tag类型选取
	$(".well")				// 按类名选取
	$("#author")			// 按id选取
	$('.well.author')		// 多类名选取(无空格) 即`<div class="well author ...">`都能匹配
	$('[name= author]')		// 按属性查找 即 找出<??? name="author">的元素 多个即 $('[items="A B"]')
	$('[class^=prefix]')	// 按前缀查找，即查找对应属性开头匹配为`prefix`的元素
	$('[class$=suffix]')	// 按后缀查找，即查找对应属性结尾匹配为`suffix`的元素
	var tr = $('tr.red');	// 组合tag及类查找， 找出<tr class="red ...">...</tr>
	$('p,div'); 			// 把<p>和<div>都选出来
	$('p.red,p.green'); 	// 把<p class="red">和<p class="green">都选出来


### 元素DOM操作

* 使用＄进行选择body元素

	`$("body").addClass("animated fadeOut");` // 给body增加hinge动画
	
* 使用＄进行选择，并增加或移除css类

	`$("button").addClass("animated bounce");` // 选择标签的元素
   `$(".well").removeClass("animated shake");`.  // 选择特定类的元素
   `$("#target3").addClass("animated fadeOut");` // 选择特定的id元素

* 更改元素的css

	`$("button").css("color", "red");`
	`$("#left-well").parent().css("background-color", "blue")`
	`$("#right-well").children().css("color", "orange")`
	
* 更改元素的属性prop

>
	aTag.hide(); // 隐藏
	aTag.show(); // 显示
	div.width(); // 600
	div.height(); // 300
>
	div.attr('name'); // 获取属性name的值
	div.attr('name', 'Hello'); // div的name属性变为'Hello'
	div.removeAttr('name'); // 删除name属性
>
	$("#target1").prop("disabled", true);	// 	使用prop
>
	input.val();	对于表单元素，jQuery对象统一提供val()方法获取和设置对应的value属性
	
* 更改元素的html

	`$(".target4").html("<em>#target4</em>");`
	
* 移除元素

	`$("#target4").remove();`
	
* 选择并移动元素

	`$("#target2").appendTo("#right-well");`
	`$("#target2").clone().appendTo("#right-well");`		// 复制并移动

* 使用CSS Selectors

	`$(".target:nth-child(2)").addClass("animated bounce");` // target 下的第二个元素都增加animated和bounce
	`$(".target:odd").addClass("animated shake");`	// 选择位置为奇数的元素`:even`为偶数

### 动画

### AJAX

### 扩展

## jQuery UI

[jQuery UI](https://jqueryui.com)

[廖雪峰的官方网站-JavaScript教程](https://www.liaoxuefeng.com/wiki/1022910821149312)