# Core Graphics

##主要概念：

#### Opaque data types
Wiki: In computer science, an opaque data type is a data type whose concrete data structure is not defined in an interface. 
IBM： An opaque data type is a user-defined data structure.

```
The opaque data types available in Quartz 2D include the following:

CGPathRef, used for vector graphics to create paths that you fill or stroke. See Paths.
CGImageRef, used to represent bitmap images and bitmap image masks based on sample data that you supply. See Bitmap Images and Image Masks.
CGLayerRef, used to represent a drawing layer that can be used for repeated drawing (such as for backgrounds or patterns) and for offscreen drawing. See Core Graphics Layer Drawing
CGPatternRef, used for repeated drawing. See Patterns.
CGShadingRef and CGGradientRef, used to paint gradients. See Gradients.
CGFunctionRef, used to define callback functions that take an arbitrary number of floating-point arguments. You use this data type when you create gradients for a shading. See Gradients.
CGColorRef and CGColorSpaceRef, used to inform Quartz how to interpret color. See Color and Color Spaces.
CGImageSourceRef and CGImageDestinationRef, which you use to move data into and out of Quartz. See Data Management in Quartz 2D and Image I/O Programming Guide.
CGFontRef, used to draw text. See Text.
CGPDFDictionaryRef, CGPDFObjectRef, CGPDFPageRef, CGPDFStream, CGPDFStringRef, and CGPDFArrayRef, which provide access to PDF metadata. See PDF Document Creation, Viewing, and Transforming.
CGPDFScannerRef and CGPDFContentStreamRef, which parse PDF metadata. See PDF Document Parsing.
CGPSConverterRef, used to convert PostScript to PDF. It is not available in iOS. See PostScript Conversion.
```

"Opaque" is defined, in English, as "not able to be seen through; not transparent". In Computer Science, this means a value which reveals no details other then the type of the value itself.

An example for an Opaque Value is FILE (from the C library):

```
int main()
{
    FILE * fh = fopen( "foo", "r" );
    if ( fh != NULL )
    {
        fprintf( fh, "Hello" );
        fclose( fh );
    }
    return 0;
}
```
You get a FILE pointer from fopen(), and use it as a parameter for other functions, but you never bother with what it actually points to.

##学习资料

####简书

主要讲了些Quartz 2D 基础：

[iOS开发-Quartz 2D基础篇](http://www.jianshu.com/p/a2d07e437b58)

主要讲了些Core Graphics绘图的入口：

[iOS绘图](http://www.jianshu.com/p/72b386d755f5)

[iOS绘图教程](http://www.cocoachina.com/industry/20140115/7703.html)

很棒的讲Core Graphics特性
[Drawing into a Core Graphics context with UIGraphicsImageRenderer](https://www.hackingwithswift.com/read/27/3/drawing-into-a-core-graphics-context-with-uigraphicsimagerenderer)

####raywenderlich.com

[Core Graphics Tutorial Part 1: Getting Started](https://www.raywenderlich.com/90690/modern-core-graphics-with-swift-part-1
)

#### 关于Cocoa Drawing的博客
[Cocoa Drawing Guide学习](http://blog.noark9.com/2014/01/07/cocoa-drawing-guide-study-part-2/)