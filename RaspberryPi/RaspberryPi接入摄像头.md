# RaspberryPi接入摄像头

### raspberrypi-guide.github.io

[Working with USB webcams on your Raspberry Pi](https://raspberrypi-guide.github.io/electronics/using-usb-webcams)

[Secure Webcam streaming with MJPG-Streamer on a Raspberry Pi](https://www.sigmdel.ca/michel/ha/rpi/streaming_en.html)

`fswebcam -r 1280x720 --no-banner /home/pi/Shared/image2023-0928-1.jpg`


`ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 mage2023-0928-2.jpg`