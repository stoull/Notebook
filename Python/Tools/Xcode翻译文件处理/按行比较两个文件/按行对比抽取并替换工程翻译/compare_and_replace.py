import os, re

def compare_and_replace(afile, bfile, tfile):
	with open(afile, 'rt') as file1:
		with open(bfile, 'rt') as file2:
			with open(tfile, 'wt') as file3:
				for line1 in file1:
					result2 = None
					result1 = re.match(r'(".*") *?= *?(".*");', line1)
					if result1:
						key1 = result1.group(1)
						isExit = False
						file2.seek(0)
						for line2 in file2:
							result2 = re.match(r'(".*") *?= *?(".*");', line2)
							if result2:
								key2 = result2.group(1)
								value2 = result2.group(2)
								if key1 == key2:
									new_value_line = f"{key1} = {value2};\n"
									file3.write(new_value_line)
									isExit = True
									break
						if isExit == False:
							file3.write(line1)
					else:
						file3.write(line1)
						continue

def recursionAllFiles(base_dir):
	files = []
	for root, ds, fs in os.walk(base_dir):
		for f in fs:
			if re.match(r'\w+[.](strings)$', f):
				fullname = os.path.join(root, f)
				files.append(fullname)
	return files

def create_dir_on_result_dir(a_dir, result_dir):
	with os.scandir(a_dir) as entries:
	    for entry in entries:
	        dir_path = os.path.join(result_dir, entry.name)
	        if not os.path.exists(dir_path):
	        	os.mkdir(dir_path)


def main():
	print(f'处理Result文件目录')
	create_dir_on_result_dir("A", "Result")
	a_dir_files = recursionAllFiles("A")
	b_dir_files = recursionAllFiles("B")
	print(f'开始处理文件')
	for a_f in a_dir_files:
		a_file_name = os.path.basename(a_f)
		a_file_dir = os.path.basename(os.path.dirname(a_f))
		is_found = False
		for b_f in b_dir_files:
			b_file_dir = os.path.basename(os.path.dirname(b_f))
			if a_file_dir == b_file_dir:
				result_f = os.path.join("Result", b_file_dir, a_file_name)
				print(f'处理文件中: 从 {a_f} 到 {result_f}')
				is_found = True
				compare_and_replace(a_f, b_f, result_f)
		if is_found == False:
			print(f"没有找到文件: {a_f}")

if __name__ == '__main__':
	main()
