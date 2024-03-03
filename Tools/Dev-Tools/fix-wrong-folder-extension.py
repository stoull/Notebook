import os
import sys, getopt

def commandHelp():
	print('\nfix-wrong-folder-extension.py')
	print('说明：查找当前目录下，所有有后缀名（extension）的目录, 有后缀名的目录会导致在某些系上会按文件打开，而导致文件夹打开失败')
	print('使用格式：')
	print('fix-wrong-folder-extension.py [-d <directory>]')
	print('-d --directory 需要检测的目录')
	print('--withfix 自动移除对应的目录后缀')
	print('\n')

def main(argv):
	root_path = '' # 根目录
	withfix = False

	try:
		opts, args = getopt.getopt(argv, "d:", ["directory=", "withfix"])
		pass
	except getopt.GetoptError:
		commandHelp()
		sys.exit(2)

	print(f"opt: {opts} arg: {args}")

	for opt, arg in opts:
		if opt == '-d':
			root_path = arg
		elif opt == '--withfix':
			withfix = True

	if isinstance(root_path, str) and len(root_path) == 0:
		commandHelp()
		sys.exit(3)
	# else:
		# print('--dir', root_path, withfix)
	findAllInvalidDirName(root_path, withfix)

def findAllInvalidDirName(dir_path, is_fix):
	print(f'检测中...')
	all_invalid_files = []
	for dirpath, dirnames, filenames in os.walk(dir_path):
	# print('目录', dirpath, dirnames, filenames)
		for dirname in dirnames:
			ext = os.path.splitext(dirname)[1]
			if dirname.endswith('.mp4') or dirname.endswith('.mkv') or dirname.endswith('.avi') or dirname.endswith('.rmvb'):
				invalid_file = dirpath + '/' + dirname
				all_invalid_files.append(invalid_file)
				# print(f'问题目录: {dirpath}/{dirname} ext: {ext}')
				if is_fix:
					fixTheWorngDirName(invalid_file)

	print(f'不正确的文件夹有：{len(all_invalid_files)}')
	print('\n'.join(all_invalid_files))
	print('\n')

	with open('./invalid-dir.txt', mode='wt', encoding='utf-8') as logFile:
		logFile.write(f'不正确的文件夹有：{len(all_invalid_files)}\n')
		logFile.write('\n'.join(all_invalid_files))
	print('已写入文件：./invalid-dir.txt')

	if is_fix:
		print('以上目录名已作更改！')

def fixTheWorngDirName(dir_path):
	new_dir_name = os.path.splitext(dir_path)[0]
	try:
		os.rename(dir_path, new_dir_name)
	except Exception as e:
		print(f'更名失败: {dir_path} -> {new_dir_name}')
		raise
	print(f'更名成功: {dir_path} -> {new_dir_name}')

if __name__ == "__main__":
    main(sys.argv[1:])