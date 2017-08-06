# Graphics Contexts导出图像


导出画布（Graphics Contexts）的图像：

* UIKit: `UIGraphicsGetImageFromCurrentImageContext `



`UIGraphicsGetImageFromCurrentImageContext`用来获取使用`UIGraphicsBeginImageContext`方法创建的bitmap图片的上下文绘制的图形。如果不是用 `UIGraphicsBeginImageContext` 创建的bitmap图形，使用此方法就会获取不到对应的图形，返回的为nil

>You should call this function only when a bitmap-based graphics context is the current graphics context. If the current context is nil or was not created by a call to UIGraphicsBeginImageContext, this function returns nil.


* UIView: `setNeedsDisplay()` `setNeedsDisplayInRect()`


>
You should use this method to request that a view be redrawn only when the content or appearance of the view change. If you simply change the geometry of the view, the view is typically not redrawn.


* CALayer: `setNeedsDisplay()`

>
Calling this method causes the layer to recache its content. This results in the layer potentially calling either the displayLayer: or drawLayer:inContext: method of its delegate. The existing content in the layer’s contents property is removed to make way for the new content.

* Core Graphics: `CGContext: makeImage()`方法