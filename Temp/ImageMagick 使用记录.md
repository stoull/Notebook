# ImageMagick 使用记录

## 1. 压缩文件下所有的文件 可更改hash值

> `find . -iname "*.png" -exec echo {} \; -exec convert {} {} \;`


## 2. 批量更改图片尺寸

> `find . -iname "*2x.png" -exec echo {} \; -exec convert {} -resize 54x54 {} \;`

将当前文件夹的所有以`2x.png`结尾的图片，更改大小为54*54



[ImageMagick 图片处理常用实例简介](https://www.starky.ltd/2019/04/11/examples-about-processing-images-by-imagemagick/)