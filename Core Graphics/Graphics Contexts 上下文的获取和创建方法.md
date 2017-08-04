# Graphics Contexts 上下文的获取和创建方法
主要是 Graphics Contexts 的理解。Graphics Contexts 是一个你要开始做图像处理的环境。如在PhotoShop中如果你要开始用画笔画一张图画，你就要新建一个画布（其实你看到的是画布上面的一张透明的图像），你需要指定画布的大小,颜色模式,分辨率等等。新建好之后就有一个空白的图像，这个时候工具栏的工具都可以用了（如矩形选框，画笔，文字等）。Graphics Contexts 就是这个新建的的空白图像，所有对图片的处理动作都是在这个新建的画布中。而所有的Core Craphics都在Graphics Contexts上进行处理，所以对Graphics Contexts学习主要有。

1. 如何创建或获得Graphics Contexts（画布）是需要我们好好学习的，不然一切Core Craphics功能都无从开始。

2. 这些Graphics Contexts（画布）的状态如何存储，画布之间如何切换，这些在绘图中也是必需要的技巧。

2. 还有就是如存存储画布以及不画布中导出不同类型的格式（PDF文件，Bitmap图像，屏幕显示等）



## Graphics Contexts 的获取,创建的七种方式

### 1. UIView 中的 `draw(_ rect: CGRect)` 方法

UIKit在UIView中提供一个获取当前Graphics Contexts的入口，  `draw(_ rect: CGRect)` 方法，在这个方法中可以很方便的使用UIKit的绘图方式绘图。 UIKit做了所有事情，获取Graphics Contexts，并将该上下文件切换为当前上下文，转换对应的坐标，将我们用UIKit做操作转成CoreGraphics的接口绘制上去等。
下面在UIView上画一个矩形，填充并描边，根本就不要`import CoreGraphics`，直接用UIKit就可以。
    
```
override func draw(_ rect: CGRect) {
        
        let viewFrame: CGRect = self.bounds
        let fileRect = CGRect.init(x: 10, y: 10, width: viewFrame.size.width - 20, height: viewFrame.size.height - 20)
        
        let fillPath: UIBezierPath = UIBezierPath.init(rect: fileRect)
        fillPath.lineWidth = 8.0
        
        UIColor.green.setFill()
        UIColor.red.setStroke()
        
        // 调用UIBezierPath 的 fill , stroke方法
        fillPath.fill()
        fillPath.stroke()
    }
```

### 2. UIGraphicsGetCurrentContext()
获取当前上下文的工具：UIGraphicsGetCurrentContext()。使用这个方法特别方便的获取当前的上下文。只要你或系统通过任何方式设置过当前上下文，像在UIView的draw(_ rect: CGRect)方法中，UIGraphicsBeginImageContextWithOptions方法后，或UIGraphicsPushContext(screenCTX)后，可以特别方便的获取当前的context。获取到context之后，就不仅可以使用UIKit进行绘图，还可以直接调用Quartz的绘图方法了。
当前上下文的默认值为nil。如果先前没有使用UIView进行绘制动作，或没有UIGraphicsPushContext，即context的存储栈里面压入任何的context，调用此方法将返回nil。

```

if  let ctx = UIGraphicsGetCurrentContext() {
            
            let viewFrame = self.bounds
            let rect = CGRect.init(x: 10, y: 10, width: viewFrame.size.width - 20, height: viewFrame.size.height - 20)
            let path = CGPath.init(rect: rect, transform: nil)
            
            ctx.addPath(path)
            
            ctx.setFillColor(UIColor.green.cgColor)
            
            ctx.fillPath()

            ctx.setStrokeColor(UIColor.red.cgColor)
            ctx.setLineWidth(8.0)
            ctx.stroke(rect)
        }

```
### 3. CALayerDelegate 的代理方法：`draw(_ layer: CALayer, in ctx: CGContext)`
使用这方法需要注意的是ctx并不是当前的上下文，而UIKit只能在当前上下文中绘图，所以如果在这个方法里面需要使用UIKit的绘图接口，定要先调用UIGraphicsPushContext存储以前的context并将ctx切换到当前上下文，绘制完后调用UIGraphicsPopContext退出当前上下文。
>对应的Layer需要`myLayer.setNeedsDisplay()`才会调用这个代理方法

```
    // CALayerDelegate
    func draw(_ layer: CALayer, in ctx: CGContext) {
        /*
         UIKit只能在当前上下文中绘图。 在方法UIGraphicsBeginImageContextWithOptions 和 drawRect：中系统已经将创建的上下文切换成前下下文了，所我们可以直接画图。当我们持有一个context参数的时候，必须将该上下文参数转化为当前上下文，就像当前这个方法里面，我们必需要调用 UIGraphicsPushContext 将当前layer的ctx切换为当前的上下文，才能使下面的UIBezierPath绘到当前的layer上面，如果使用Core graphics进行离屏绘制则不需要
         */
        UIGraphicsPushContext(ctx)
        
        let fillPath: UIBezierPath = UIBezierPath.init(rect: CGRect.init(x: 10, y: 10, width: 160, height: 60))
        fillPath.lineWidth = 8.0
        
        UIColor.green.setFill()
        UIColor.red.setStroke()
        
        // 调用UIBezierPath 的 fill , stroke方法
        fillPath.fill()
        fillPath.stroke()
        

        // 离开ctx 切换回到使用以前的Context
        // Removes the current graphics context from the top of the stack, restoring the previous context.
        UIGraphicsPopContext()
    }
```

### 4. CALayer的 `draw(in ctx: CGContext)`方法
```
override func draw(in ctx: CGContext) {
        
        let layerRect: CGRect = self.bounds;

        let padding: CGFloat = 20.0
        ctx.move(to: CGPoint.init(x: layerRect.origin.x + padding, y: layerRect.origin.y + padding))
        ctx.addLine(to: CGPoint.init(x: layerRect.size.width - padding, y: layerRect.origin.y + padding))
        ctx.addLine(to: CGPoint.init(x: layerRect.size.width - padding, y: layerRect.size.height - padding))
        ctx.addLine(to: CGPoint.init(x: layerRect.origin.x + padding, y: layerRect.size.height - padding))
        ctx.closePath()
        
        ctx.setStrokeColor(UIColor.red.cgColor)
        ctx.setFillColor(UIColor.blue.cgColor)
        ctx.setLineWidth(6.0)

        ctx.strokePath()
    }
```


### 5. 使用 UIGraphicsBeginImageContextWithOptions() 创建上下文
快捷创建Bitmap context上下文的方法，并将该新建的上下文存储并设置为当前上下文。它做了相当多的工作，首先是CGContext.init,然后将坐标系转换成UIKit的坐标系，以及将创建的context压入栈并设置为当前上下文的工作。

>注意:
>UIGraphicsGetImageFromCurrentImageContext用来获取使用UIGraphicsBeginImageContext方法创建的bitmap图片的上下文绘制的图形。如果当前上下文用`UIGraphicsBeginImageContext`创建的bitmap图形，使用此方法将获取不到对应的图形，返回的为nil
>
>You should call this function only when a bitmap-based graphics context is the current graphics context. If the current context is nil or was not created by a call to UIGraphicsBeginImageContext, this function returns nil.

```
public func drawImage() -> UIImage? {
        
        let imageSize: CGSize = CGSize.init(width: 200.0, height: 200.0)
        let scale = UIScreen.main.scale
        
        // 创建一个画布，并将该上下文件切换为当前上下文
        UIGraphicsBeginImageContextWithOptions(imageSize, false, scale)
//        UIGraphicsBeginImageContext(<#T##size: CGSize##CGSize#>)
        
        // 获取创建的画布
        let ctx = UIGraphicsGetCurrentContext()
        
        let path = UIBezierPath.init(ovalIn:CGRect.init(x: 0.0, y: 0.0, width: imageSize.width, height: imageSize.height))
        UIColor.red.setFill()
        ctx?.setFillColor(UIColor.red.cgColor)
        path.fill()
        
        // 把画导出为 UIImage 格式，怎么导出为纸质的！
        let drawImage: UIImage? = UIGraphicsGetImageFromCurrentImageContext()
        
        UIGraphicsEndImageContext()
        
        return drawImage
    }
```

### 6. 直接使用Quartz的方法创建Graphics Contexts
使用用Graphics Contexts的方法创建Bitmap graphics contexts，这是一种更为底层的方法，需要指定存储空间，颜色空间等信息。注意：使用这种方法创建的context不像其它通过UIKit获得的context，这个context的坐标系还是Quartz的坐标系，这个context也没有存储及切换为当前上下文。
这种方法可以用来进行离屏绘图，就是都不用将Context渲染屏幕显示，直接导出绘制好的图形。不过在使用这个方式进行离屏绘图前，优先考虑使用CGLayer进行离屏绘图。

```
func getDrawImage() -> UIImage? {
        let imageSize: CGSize = CGSize.init(width: 200.0, height: 200.0)

        let bitmapBytesPerRow: Int = Int(imageSize.width) * 4
        let bitmapByteCount: Int = bitmapBytesPerRow * Int(imageSize.height)
        let imageData: UnsafeMutableRawPointer! = calloc(bitmapByteCount, bitmapBytesPerRow)
        
        let colorSpace:CGColorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue)
        let screentContext = CGContext.init(data: imageData,
                                            width: Int(imageSize.width),
                                            height: Int(imageSize.height),
                                            bitsPerComponent: 8,
                                            bytesPerRow: bitmapBytesPerRow,
                                            space: colorSpace,
                                            bitmapInfo: bitmapInfo.rawValue)

        if let screenCTX = screentContext {
            
            // 将 screenCTX 设置为当前上下文, UIKit只能在当前上下文中绘图,所以下面使用的 UIBezierPath 的绘制方法才能将图形绘制到screenCTX上下文中
            UIGraphicsPushContext(screenCTX)
            
            let bPath = UIBezierPath.init(ovalIn:CGRect.init(x: 0.0, y: 0.0, width: imageSize.width, height: imageSize.height))
            UIColor.red.setFill()
            bPath.fill()
            
            guard let drawImageRef = screenCTX.makeImage() else {
                return nil
            }
            
            let drawImage = UIImage.init(cgImage: drawImageRef)
            
            /*
            let drawImage = UIGraphicsGetImageFromCurrentImageContext()
            
             UIGraphicsGetImageFromCurrentImageContext用来获取使用UIGraphicsBeginImageContext方法创建的bitmap图片的上下文绘制的图形。 因为 screenCTX 不是用 UIGraphicsBeginImageContext 创建的bitmap图形，所以获取不到对应的图形，返回的为nil
             You should call this function only when a bitmap-based graphics context is the current graphics context. If the current context is nil or was not created by a call to UIGraphicsBeginImageContext, this function returns nil.
            */
            UIGraphicsPopContext()
            free(imageData)
            return drawImage
        }else {
            return nil
        }
    }
```

### 7. iOS10+的新方法`UIGraphicsImageRenderer`
UIGraphicsImageRenderer: A graphics renderer for creating Core Graphics-backed images iOS 10+

[Apple document](https://developer.apple.com/documentation/uikit/uigraphicsimagerenderer)

[Drawing into a Core Graphics context with UIGraphicsImageRenderer](https://www.hackingwithswift.com/read/27/3/drawing-into-a-core-graphics-context-with-uigraphicsimagerenderer)

```
class DrawRectSeven: NSObject {
    func getDrawImage() -> UIImage? {
        
        let imageSize = CGSize.init(width: 200, height: 200)
        let renderFormat = UIGraphicsImageRendererFormat.default() // *
        renderFormat.opaque = false
        
        let render = UIGraphicsImageRenderer.init(size: imageSize, format: renderFormat)
        
        // 这里的 ctx 是 UIGraphicsImageRendererContext 类, 这个类有一个CGContext属性，这个就有点像UIKit对CGContext类更高的封装，获取图片和导出图片数据也更方便.
        let drawImage = render.image { (ctx) in
            UIColor.darkGray.setStroke()
            ctx.stroke(render.format.bounds)
            UIColor(colorLiteralRed: 158/255, green: 215/255, blue: 245/255, alpha: 1).setFill()
            ctx.fill(CGRect(x: 1, y: 1, width: 140, height: 140))
        }
        
        return drawImage
    }
```