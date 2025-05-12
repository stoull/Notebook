# Mac上常用软件


### markdown编辑器

[MacDown](https://macdown.uranusjr.com)

### 视频播放器：

* [IINA - The modern media player for macOS.](https://iina.io)
	IINA is born to be a modern macOS application, from its framework to the user interface. It adopts the post-Yosemite design language of macOS and keeps up the pace of new technologies like Force Touch, Touch Bar, and Picture-in-Picture.
	
* [VLC media player](https://www.videolan.org)

	VLC is a free and open source cross-platform multimedia player and framework that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and various streaming protocols.

### 开源视频转换工具： 

* [HandBrake - The open source video transcoder](https://handbrake.fr)

	HandBrake is a open-source tool, built by volunteers, for converting video from nearly any format to a selection of modern, widely supported codecs.

### 音频文件工具： 

给mp3文件添加封面：

```
ffmpeg -i in.mp3 -i test.jpeg -map 0:0 -map 1:0 -codec copy -id3v2_version 3 \ 
-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3
```

### 开源图片处理

* [GIMP](https://www.gimp.org): This is the official website of the GNU Image Manipulation Program (GIMP).

* [GIMP - downloads](https://www.gimp.org/downloads/)
* [RawTherapee](https://rawtherapee.com/downloads/5.11/): 相机照片原始RAW文件处理

### 电子书编辑：

* [calibre - E-book management](https://calibre-ebook.com)

	calibre is a powerful and easy to use e-book manager. Users say it’s outstanding and a must-have. It’ll allow you to do nearly everything and it takes things a step beyond normal e-book software. It’s also completely free and open source and great for both casual users and computer experts.
	
	
	mp3tag
### 系统清理

* [OnlyX](https://www.titanium-software.fr/en/applications.html)

	OnyX is the main application. The Maintenance, Deeper, and CalHash applications are parts of OnyX. Thus, if you use OnyX, the Maintenance, Deeper and CalHash applications are redundant!
	
	
	
	
	
	
