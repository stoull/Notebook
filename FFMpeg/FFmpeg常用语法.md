FFmpeg常用语法

##视频压缩

### 1. 改变码率

`ffmpeg -i input.mp4 -b 800k output.mp4`

>
码率计算：想视频大小为1GB(为1GB字节gigabyte，8GB比特gigabits), 时长为2小时46分40秒，即10000秒。`8 000 000 000 bit / 10 000 s = 800 000 bit/s` 即为`800kbit/s`

### 2. 改变视频的CRF值（[Constant Rate Factor](https://slhck.info/video/2017/02/24/crf-guide.html))

`ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4`
`ffmpeg -i input.mp4 -vcodec libx264 -crf 20 output.mp4`

`H.265` CRF 一般为24-30，  `H.264` CRF 一般为20-26

>The range of the CRF scale is 0–51, where 0 is lossless (for 8 bit only, for 10 bit use -qp 0), 23 is the default, and 51 is worst quality possible. A lower value generally leads to higher quality, and a subjectively sane range is 17–28. Consider 17 or 18 to be visually lossless or nearly so; it should look the same or nearly the same as the input but it isn't technically lossless.
>
The range is exponential, so increasing the CRF value +6 results in roughly half the bitrate / file size, while -6 leads to roughly twice the bitrate.
>
ffmpeg -i RPReplay_Final1650625236.MP4 -vcodec libx264 -crf 20 output_sha.mp4

From [FFmpeg H.264 Video Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)

### 2. 改变视频的尺寸大小

原视频尺寸的二分之一：
`ffmpeg -i input.mkv -vf "scale=trunc(iw/4)*2:trunc(ih/4)*2" -c:v libx265 -crf 28 half_the_frame_size.mkv`

原视频尺寸的三分之一：
`ffmpeg -i input.mkv -vf "scale=trunc(iw/6)*2:trunc(ih/6)*2" -c:v libx265 -crf 28 a_third_the_frame_size.mkv`

原视频尺寸的四分之一：
`ffmpeg -i input.mkv -vf "scale=trunc(iw/8)*2:trunc(ih/8)*2" -c:v libx265 -crf 28 a_fourth_the_frame_size.mkv`

原视频尺寸的五分之一：
`ffmpeg -i input.mkv -vf "scale=trunc(iw/10)*2:trunc(ih/10)*2" -c:v libx265 -crf 28 a_fifth_the_frame_size.mkv`

##视频剪切

https://stackoverflow.com/questions/18444194/cutting-the-videos-based-on-start-and-end-time-using-ffmpeg

Re-encoding

ffmpeg -i movie.mp4 -ss 00:00:03 -t 00:00:08 -async 1 cut.mp4

NO Re-encoding

ffmpeg -i input.mp4 -ss 01:10:27 -to 02:18:51 -c:v copy -c:a copy output.mp4

##音频提取
Picking the 30 seconds fragment at an offset of 1 minute:

ffmpeg -i '12.Angry Men.mp4' -ss 0:01:00 -t 0:00:30 output.mp3

Picking the 30 seconds fragment from 01:00 to 01:30:

ffmpeg -i '12.Angry Men.mp4' -ss 0:01:00 -to 0:01:30 output.mp3

ffmpeg -i sample.avi -q:a 0 -map a sample.mp3

ffmpeg -i RPReplay_Final1649853524.MP4 -ss 00:00:00 -t 00:05:00.0 -q:a 0 -map a output_dd.mp3

##视频截图

