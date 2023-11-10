
# 遍历目录下所有的文件

import os,re

# with os.scandir('Crawl-Example-Code') as entries:
#     for entry in entries:
#         print(entry.name)


def recursionAllFiles(base_dir):
	for root, ds, fs in os.walk(base_dir):
		for f in fs:
			# 匹配所有文件
			if re.match(r'\w+.\w+', f):
				fullname = os.path.join(root, f)
				yield fullname

def main():
	base_dir = "/Users/kevin/Documents/Notebook/Python"
	for i in recursionAllFiles(base_dir):
		print(i)


if __name__ == '__main__':
	main()