# Graphics Contexts上下文的状态存储及之间的切换

使用 Graphics Contexts 在绘图的过程中，经常会遇到一些context状态的存储和context之间的切挽，一般使用下面三对方法：
>1. CGContextSaveGState/CGContextRestoreGState
>2. UIGraphicsPushContext/UIGraphicsPopContext
>3. UIGraphicsBeginImageContext/UIGraphicsEndImageContext

###1. CGContextSaveGState/CGContextRestoreGState
     
     
CGContextSaveGState: Pushes a copy of the current graphics state onto the graphics state stack for the context.将当前的上下文状态保存到context的储存栈中。将上下文状态比作绘图软件的画布的话，上下文状态指其中画笔的颜色，大小，画的线条，还有‘坐标系统’啊，具体可见：[CGContext save state](https://developer.apple.com/documentation/coregraphics/1456156-cgcontextsavegstate)

CGContextRestoreGState: 将context的状态恢复到最近一次保存的状态，即将context恢复到context的储存栈顶那个状态，并把此状态从栈中移除。 Sets the current graphics state to the state most recently saved.

使用场景：

```
    public func exampleCGContextSaveGState() -> UIImage? {
        let imageSize: CGSize = CGSize.init(width: 200.0, height: 200.0)
        let scale = UIScreen.main.scale
        
        UIGraphicsBeginImageContextWithOptions(imageSize, false, scale)
        if let ctx = UIGraphicsGetCurrentContext() {
            ctx.move(to: CGPoint.init(x: 50.0, y: 50.0))
            ctx.addLine(to: CGPoint.init(x: 150.0, y: 50.0))
            ctx.setLineCap(CGLineCap.butt)
            ctx.setLineWidth(10.0)
            ctx.setStrokeColor(UIColor.black.cgColor)
            ctx.strokePath()
            
            ctx.saveGState()
            
            ctx.move(to: CGPoint.init(x: 50.0, y: 100.0))
            ctx.addLine(to: CGPoint.init(x: 150.0, y: 100.0))
            ctx.setLineCap(CGLineCap.round)
            ctx.setLineWidth(20.0)
            ctx.setStrokeColor(UIColor.red.cgColor)
            ctx.strokePath()
            
            // 可将此方法逐一打开，查看context的状态储存栈
//            ctx.saveGState()
//            ctx.restoreGState()
            
            ctx.restoreGState()
            
            ctx.move(to: CGPoint.init(x: 50.0, y: 150.0))
            ctx.addLine(to: CGPoint.init(x: 150.0, y: 150.0))
            ctx.strokePath()
        }
        
        let drawImage: UIImage? = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return drawImage
    }
```

### 2. UIGraphicsPushContext/UIGraphicsPopContext

UIGraphicsPopContext: 使用UIGraphicsPushContext存储以前的context并将ctx切换为当前上下文，和UIGraphicsPopContext一起使用
You can use this function to save the previous graphics state and make the specified context the current context. You must balance calls to this function with matching calls to the UIGraphicsPopContext function.

只能在当前上下文中绘图。 在方法UIGraphicsBeginImageContextWithOptions 和 drawRect：中系统已经将创建的上下文切换成前下下文了，所我们可以直接画图。当我们持有一个context参数的时候，必须将该上下文参数转化为当前上下文。如在CALayerDelegate代理方法func draw(_ layer: CALayer, in ctx: CGContext)里面，我们必需要调用 UIGraphicsPushContext 将当前layer的ctx切换为当前的上下文，才能绘到当前的layer上面。

UIGraphicsPopContext: 将存储栈顶的当前上下文件移除，并设置下一上下文ctx为当前上下文。。Removes the current graphics context from the top of the stack, restoring the previous context.

使用场景是：

当前正在使用CoreGraphics绘制图形A，想要使用UIKit绘制完全不同的图形B，此时就希望保存当前绘图context及已绘制内容。

使用UIGraphicsPushContext切换到一个全新的绘图context。

使用UIKit绘制图形B。

使用UIGraphicsPopContext恢复之前的绘图context，继续使用CoreGraphics绘制图形A。

```
 public func exampleUIGraphicsPushContext() -> UIImage? {
        let scale = UIScreen.main.scale
        let imageSize: CGSize = UIScreen.main.bounds.size
        
        UIGraphicsBeginImageContextWithOptions(imageSize, false, scale)
        if let ctx = UIGraphicsGetCurrentContext() {
            
            // 在使用UIGraphicsGetCurrentContext 创建的 ctx上绘制图片
            let photoDescribe: NSString = "我是 UIGraphicsGetCurrentContext 创建上下文 绘制的文字"
            let attributes: [String : Any] = [NSFontAttributeName : UIFont.boldSystemFont(ofSize: 20),
                                              NSForegroundColorAttributeName: UIColor.red]
            let textRect = CGRect.init(x: 10, y: 40, width: imageSize.width - 10, height: imageSize.height - 40)
            photoDescribe.draw(in: textRect, withAttributes: attributes)
            

            // 直接使用CoreGraphics的 CGContext.init 方法，创建一个新的Graphics Contexts（画布）
            let imageRect = CGRect.init(x: 10, y: 100.0, width: imageSize.width - 10, height: imageSize.height)
            let colorSpace:CGColorSpace = CGColorSpaceCreateDeviceRGB()
            let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)
            let screentContext = CGContext.init(data: nil, width: Int(imageRect.width), height: Int(imageRect.height), bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: bitmapInfo.rawValue)

            // 这个时候如果要在这个新建的画布上面绘图的话，就需要用到 UIGraphicsPushContext 方法了
            if let screenCTX = screentContext {
                
                UIGraphicsPushContext(screenCTX)
                
                // 这里是在 screenCTX 进行操作了
                screenCTX.scaleBy(x: scale, y: scale)
                let photoDescribe: NSString = "我是 CGContext.init 创建上下文 绘制的文字"
                let attributes: [String : Any] = [NSFontAttributeName : UIFont.boldSystemFont(ofSize: 20),
                                                  NSForegroundColorAttributeName: UIColor.blue]
                let textRect = CGRect.init(x: 10, y: 60, width: imageSize.width - 10, height: imageSize.height - 40)
                photoDescribe.draw(in: textRect, withAttributes: attributes)
                
                // 截取view的图像
                self.view.drawHierarchy(in: imageRect, afterScreenUpdates: false)
                
                
                // 虽然ctx不是当前上下文件，但这里还是可以通过 Graphics Contexts 进行离屏绘制的，但不能使用UIKit绘制,UIKit只能在当前上下文中绘图,所以使用UIKit会绘制到screenCTX上下文上
                ctx.move(to: CGPoint.init(x: 120.0, y: 80.0))
                ctx.addLine(to: CGPoint.init(x: imageSize.width - 120.0, y: 80.0))
                ctx.setLineWidth(2.0)
                ctx.setStrokeColor(UIColor.blue.cgColor)
                ctx.strokePath()

                UIGraphicsPopContext()
            }
            
            let drawImage = UIGraphicsGetImageFromCurrentImageContext()
            UIGraphicsEndImageContext()
            return drawImage;
        }else {
            return nil
        }
    }
```

### 3. UIGraphicsBeginImageContext/UIGraphicsEndImageContext
     
UIGraphicsBeginImageContext: 快捷创建Bitmap context上下文的方法，并将该新建的上下文存储并设置为当前上下文。它做了相当多的工作，像CGContext.init,将坐标系转换成UIKit的坐标系，以及UIGraphicsPushContext的工作。 Creates a bitmap-based graphics context with the specified options.

UIGraphicsEndImageContext: 将存储栈顶的Bitmap context上下文件移除，并设置下一上下文为当前上下文。  Removes the current bitmap-based graphics context from the top of the stack.

使用场景：

当前正在绘制图形A。

使用UIGraphicsBeginImageContext将旧的绘图context入栈，创建新的绘图context并使用。

绘制图形B。

结束绘制图形B之后，使用UIGraphicsEndImageContext恢复到之前的绘图context，继续绘制图形A。

```
public func exampleUIGraphicsBeginImageContext() -> UIImage? {
        let scale = UIScreen.main.scale
        let imageSize: CGSize = UIScreen.main.bounds.size
        
        UIGraphicsBeginImageContextWithOptions(imageSize, false, scale)
        if let ctx = UIGraphicsGetCurrentContext() {
            let photoDescribe: NSString = "当前的屏幕图像为(Current screen):"
            let attributes: [String : Any] = [NSFontAttributeName : UIFont.boldSystemFont(ofSize: 20),
                                              NSForegroundColorAttributeName: UIColor.darkGray]
            let textRect = CGRect.init(x: 10, y: 40, width: imageSize.width - 10, height: imageSize.height - 40)
            photoDescribe.draw(in: textRect, withAttributes: attributes)
            
            var screenShot: UIImage? = nil
            
            // 使用 UIGraphicsBeginImageContextWithOptions 创建新的上下文,这个方法会新建上文并push成当前上下文
            UIGraphicsBeginImageContextWithOptions(imageSize, false, scale)
            if let screenCTX = UIGraphicsGetCurrentContext() {
                
                // 将 self.view 的屏幕， 画在 UIGraphicsBeginImageContextWithOptions 新建的context上面
                self.view.layer.render(in: screenCTX)
                
                // i
                let sPath = UIBezierPath.init(rect: CGRect.init(x: 100, y: 80, width: 100, height: 100))
                sPath.lineWidth = 5.0
                UIColor.blue.setStroke()
                sPath.stroke()
                
                screenShot = UIGraphicsGetImageFromCurrentImageContext()
                
                UIGraphicsEndImageContext()
            }
            
            // UIGraphicsEndImageContext() 之后 ctx 又切换回当前的上下文
            let sPath = UIBezierPath.init(rect: CGRect.init(x: 20, y: 120, width: 100, height: 100))
            sPath.lineWidth = 20.0
            UIColor.yellow.setStroke()
            sPath.stroke()
            
            
            // 如果self.view的截图绘制成功
            if let screenShotImage = screenShot {
                let imageRect = CGRect.init(x: 10, y: 100.0, width: imageSize.width - 10, height: imageSize.height)
                screenShotImage.draw(in: imageRect, blendMode: .overlay, alpha: 1.0)
            }
            
            let drawImage = UIGraphicsGetImageFromCurrentImageContext()
            UIGraphicsEndImageContext()
            return drawImage;
        }else {
            return nil
        }
    }
```