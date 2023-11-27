import re

with open('Localizable_A.strings', 'rt') as file1:
	with open('Localizable_B.strings', 'rt') as file2:
		with open('Localizable_C.strings', 'wt') as file3:
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
			

				





					
				