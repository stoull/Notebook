
# 匹配在项目中没有写成NSLocalizedString，定成 label.text = "电量"的文本


import os,re

# with os.scandir('Crawl-Example-Code') as entries:
#     for entry in entries:
#         print(entry.name)


def recursionAllFiles(base_dir):
	for root, ds, fs in os.walk(base_dir):
		for f in fs:
			if re.match(r'\w+[.]swift$', f):
				fullname = os.path.join(root, f)
				yield fullname

def getStringFromOldStringFile():
	old_lan_path = "./Localizable.strings"
	if os.path.isfile(old_lan_path):
		keyValueDic={}
		with open(old_lan_path, 'r') as f:
			for line in f:
				result = re.match(r'"(.*)" *?= *?"(.*)";', line)
				if result:
					key = result.group(1)
					value = result.group(2)
					keyValueDic[key]=value
		return keyValueDic
	else:
		return False

def handleAllFiles():
	base_dir = "/Users/kevin/Desktop/Python_Script/遍历目录所有文件/ProjectEV"
	totalNumber = 0
	totalLineNumber = 0
	tDic = getStringFromOldStringFile()
	no_value_lines = []
	for filepath in recursionAllFiles(base_dir):
		totalNumber += 1
		with open(filepath, 'r') as f:
			for line in f:
				totalLineNumber += 1
				re_result = re.match(r'.*NSLocalizedString\("(\w+)", comment: "(\w+)"\).*', line)
				# re_result = re.match(r'.*"(.*)".*', line)
				if re_result:
					pass
					# value_str = tDic.get(key_str)
					# if value_str is None:
					# 	# print(f"{key_str} 没有翻译！")
					# 	no_value_lines.append(key_str)
				else:
					# 中文匹配
					re_result = re.match(r'.*= "([\u4e00-\u9fa5]+)".*', line)
					if re_result:
						key_str = re_result.group(1)
						no_value_lines.append(key_str)
		f.close()

	print(totalNumber)
	print(totalLineNumber)
	with open("./result.strings", mode='wt', encoding='utf-8') as the_file:
		the_file.write("// ==== 没有翻译 \n")
		the_file.write('\n'.join(no_value_lines))
		the_file.close()

def main():
	handleAllFiles()


if __name__ == '__main__':
	main()