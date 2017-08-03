# Graphics Contexts 的获取,创建及不同上下文之间状态存储与切换

主要是 Graphics Contexts 的理解。Graphics Contexts 是一个你要开始做图像处理的环境。如在PhotoShop中如果你要开始用画笔画一张图画，你就要新建一个画布（其实你看到的是画布上面的一张透明的图像），你需要指定画布的大小,颜色模式,分辨率等等。新建好之后就有一个空白的图像，这个时候工具栏的工具都可以用了（如矩形选框，画笔，文字等）。Graphics Contexts 就是这个新建的的空白图像，所有对图片的处理动作都是在这个新建的画布中。而所有的Core Craphics都在Graphics Contexts上进行处理，所以对Graphics Contexts学习主要有。

1. 如何创建或获得Graphics Contexts（画布）是需要我们好好学习的，不然一切Core Craphics功能都无从开始。

2. 这些Graphics Contexts（画布）的状态如何存储，画布之间如何切换，这些在绘图中也是必需要的技巧。

2. 还有就是如存存储画布以及不画布中导出不同类型的格式（PDF文件，Bitmap图像，屏幕显示等）



