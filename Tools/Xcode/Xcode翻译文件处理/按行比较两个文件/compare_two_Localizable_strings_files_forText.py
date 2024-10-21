import re

f = open("compare_result.txt", "w")
f.write("")
f.close()

with open('Localizable_cn.strings', 'r') as file1:
	existString = []
	noExistString = []
	with open('file_B', 'r') as file2:
		# same = set(file1).intersection(file2) // 取交集
		for line1 in file1:
			result2 = None
			result1 = re.match(r'"(.*)" *?= *?"(.*)";', line1)
			if result1:
				key1 = result1.group(1)
				value1 = result1.group(2)
				isExit = False
				file2.seek(0)
				for line2 in file2:
					result2 = str(line2)
					# 移除 xlsx 文件单元格中开始和结束误输入的空格及其它的特殊字符
					result2 = re.sub('^[ ]*|[ ]*$\n', '', result2)
					print(f"value1: {value1} {type(value1)} result2: {result2} {type(result2)}")
					if value1 == result2:
						isExit = True
						print(f"isExit {isExit}")
						# with open('compare_result.txt', 'a') as the_file:
						#     the_file.write(key1+'\n')
						break
				if isExit == False:
					noExistString.append(value1)
					# print(f"{value1}")
					# print(f"result1: {result1} result2: {result2}")
				else:
					existString.append(value1)
			else:
				continue
print("===并存的===:")
for eStr in existString:
	print(f"{eStr}")

print("===目标文件没有的===:")
for eStr in noExistString:
	print(f"{eStr}")