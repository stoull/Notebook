#!/bin/bash

#使用FFMpeg将本目录下所有的wav文件转换成双声道320k的mp3文件

function loopToConvert() {

	# 移除文件名中的空格(用_替代空格)
	for f in *\ *; do mv "$f" "${f// /_}"; done

	#进行操作
	find . -name "*.wav" -type f -print0 | while read -d $'\0' wavFileName
	do
	    mp3FileName=`echo "$wavFileName" | sed 's/\.\/\([0-9 ._]\)*\(.*\).wav/\.\/\2.mp3/'`
	    echo "Converting ${wavFileName} to ${mp3FileName}"
		ffmpeg -i "${wavFileName}" -ac 2 -ab 320000 "${mp3FileName}"
	done
}

function main() {
    loopToConvert "$1"
}

main "$1"