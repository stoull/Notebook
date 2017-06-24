## 记录Shell的常用命令用法 

### :ls 排序

由大到小排序

	ls -Sl

从小到大排序

	ls -Slr
	
	
`-h`，表示`–human-readable`，单位是k或者M ，比较容易看清楚结果。

显示子目录结构

	ls -R

ls按时间排序

从新到旧

	ls -lt
	
从旧到新

	ls -lrt
	
ls对当前目录和文件大小排序

	du -s * | sort -nr
	
只对当前目录排序，并用直观的大小显示出来

	for i in $(ls -l |grep '^d' |du -s * |sort -nr|awk '{print $2}');do du -sh $i;done
