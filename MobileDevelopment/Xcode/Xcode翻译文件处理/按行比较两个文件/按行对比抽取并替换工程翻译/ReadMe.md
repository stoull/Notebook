* `compare_and_replace.py`会在A目录下，按目录结构循环每一个.strings文件，然后在B目录下查找对应的文件。如果在B文件找到文件，则会对文件进行逐行比对。将在B中找到的value值替换到A文件中，并写入到Result中。

* Result中的目录结构与A中一致。