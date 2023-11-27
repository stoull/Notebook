import re

f = open("compare_result.txt", "w")
f.write("")
f.close()

with open('Localizable_cn.strings', 'r') as file1:
	with open('Localizable_zn.strings', 'r') as file2:
		# same = set(file1).intersection(file2) // 取交集
		for line1 in file1:
			result2 = None
			result1 = re.match(r'(".*") *?= *?".*";', line1)
			if result1:
				key1 = result1.group(1)
				isExit = False
				file2.seek(0)
				for line2 in file2:
					result2 = re.match(r'(".*") *?= *?".*";', line2)
					if result2:
						key2 = result2.group(1)
						if key1 == key2:
							isExit = True
							# with open('compare_result.txt', 'a') as the_file:
							#     the_file.write(key1+'\n')
							break
				if isExit == False:
					print(f"{key1}")
					# print(f"result1: {result1} result2: {result2}")
			else:
				continue
				
			

				





					
				