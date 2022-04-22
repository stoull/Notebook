FFmpeg常用语法

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

