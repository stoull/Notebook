# Color and Color Spaces 颜色和颜色空间
## 缘起

## 什么是颜色
### 光
一切都始于光。所要明白颜色是什么，我们先得明白光是什么东西。

### 人的睛眼

### 原色以及增减色原理

### 颜色的亮度

### 光谱功率分布

### 什么是白色？

### 光的强度

## 什么是颜色空间
### CIE XYZ 颜色空间

### CIE Yxy颜色空间

### 灰度颜色空间

### RGB 颜色空间

### CMYK 颜色空间

## 颜色管理系统（Color Management Systems）
### 颜色空间转换
### 设备颜色Profiles文件
### 颜色管理组件（CMM）




相关资料：

[颜色空间总结](http://blog.csdn.net/lg1259156776/article/details/48317339)

[Color space](https://en.wikipedia.org/wiki/Color_space 'en.wikipedia.org')

专业介绍颜色：
[Introduction to Light, Color and Color Space](http://www.scratchapixel.com/lessons/digital-imaging/colors/color-space?url=digital-imaging/colors/color-space)

苹果官方文档: [Introduction to Color Management Overview](https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/csintro/csintro_intro/csintro_intro.html)

[Cocoa Drawing Guide学习part3——颜色AND透明](http://blog.noark9.com/2014/01/28/cocoa-drawing-guide-study-part-3/)

One of the best guides to code-level color management I've ever seen, especially online... You guys are awesome!!":
[Learn Computer Graphics From Scratch](http://www.scratchapixel.com/index.php?redirect)

#### 相关机构
[CIE 国际照明委员会(International Commission on Illumination)](http://www.cie.co.at/index.php/Research+Strategy?service=restart)

国际色彩联盟（International Color Consortium）的色彩管理的标准——ICC规范：
[国际色彩联盟](http://www.color.org/index.xalter)
#### HSV 和 HLS 颜色空间的描述：

这两个颜色空间使用三个变量描述颜色，分别是：色相（Hue）, 饱和度（Saturation）, 和亮度（Brightness）

* 色相：代表色谱中一种颜色，每一个色相都是标准的，独一无二的。比如蓝色，只有一种色相代表蓝色，区别于其它的颜色。
* 饱和度：即颜色的纯度（或浓淡）。如灰色即为0饱和度。
* 亮度：颜色的亮度。可理解为这种颜色物体反射或发出光的强度。如在夜里拿白色手电照射对应颜色，对应手电光的强度。


### 上下文件中如果使用 不同颜色空间图片 的渲染问题

```
void CGContextSetRenderingIntent ( CGContextRef context, CGColorRenderingIntent intent );

参数： intent：渲染意图的常量：kCGRenderingIntentDefault, kCGRenderingIntentAbsoluteColorimetric, kCGRenderingIntentRelativeColorimetric, kCGRenderingIntentPerceptual, or kCGRenderingIntentSaturation.
```
**Discussion：**渲染意图指明了Quartz应该如何去处理上下文中那些不在目的源颜色空间得颜色。如果你没有明确的设置渲染意图，Quartz使用 kCGRenderingIntentPerceptual,的渲染意图去绘制图片，kCGRenderingIntentRelativeColorimetric去进行其他的绘制。