# 记录 NSFileManager 对文件的增删改查操作

#### 获取Documents路径
```
- (NSString *)getDocumentsPath
{
    //获取Documents路径
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *path = [paths objectAtIndex:0];
    NSLog(@"path:%@", path);
    return path;
}
```

#### 创建文件夹
```
-(void)createDirectoryName:(NSString *)direcotryName{
    NSString *documentsPath =[self getDocumentsPath];
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *iOSDirectory = [documentsPath stringByAppendingPathComponent: direcotryName];
    BOOL isSuccess = [fileManager createDirectoryAtPath:iOSDirectory withIntermediateDirectories:YES attributes:nil error:nil];
    if (isSuccess) {
        NSLog(@"success");
    } else {
        NSLog(@"fail");
    }
}
```


#### 创建文件
```
-(void)createFile:(NSString *)fileName{
    NSString *documentsPath =[self getDocumentsPath];
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *iOSPath = [documentsPath stringByAppendingPathComponent: fileName];
    BOOL isSuccess = [fileManager createFileAtPath:iOSPath contents:nil attributes:nil];
    if (isSuccess) {
        NSLog(@"success");
    } else {
        NSLog(@"fail");
    }
}
```


#### 写文件
```
-(NSString *)writeFileContent:(NSString *)content fileName:(NSString *)fileName{
    NSString *documentsPath =[self getDocumentsPath];
    NSString *iOSPath = [documentsPath stringByAppendingPathComponent: fileName];
    NSString *content = content;
    BOOL isSuccess = [content writeToFile:iOSPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
    if (isSuccess) {
        NSLog(@"write success");
        return iOSPath;
    } else {
        NSLog(@"write fail");
        return nil;
    }
}
```


#### 读取文件内容
```
-(void)readFileContentWithFilePath:(NSString *)path{
    NSString *content = [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:nil];
    NSLog(@"read success: %@",content);
}
```


#### 判断文件是否存在
```
- (BOOL)isSxistAtPath:(NSString *)filePath{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    BOOL isExist = [fileManager fileExistsAtPath:filePath];
    return isExist;
}
```


#### 计算文件大小
```
- (unsigned long long)fileSizeAtPath:(NSString *)filePath{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    BOOL isExist = [fileManager fileExistsAtPath:filePath];
    if (isExist){
        unsigned long long fileSize = [[fileManager attributesOfItemAtPath:filePath error:nil] fileSize];
        return fileSize;
    } else {
        NSLog(@"file is not exist");
        return 0;
    }
}
```


#### 计算整个文件夹中所有文件大小
```
- (unsigned long long)folderSizeAtPath:(NSString*)folderPath{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    BOOL isExist = [fileManager fileExistsAtPath:folderPath];
    if (isExist){
        NSEnumerator *childFileEnumerator = [[fileManager subpathsAtPath:folderPath] objectEnumerator];
        unsigned long long folderSize = 0;
        NSString *fileName = @"";
        while ((fileName = [childFileEnumerator nextObject]) != nil){
            NSString* fileAbsolutePath = [folderPath stringByAppendingPathComponent:fileName];
            folderSize += [self fileSizeAtPath:fileAbsolutePath];
        }
        return folderSize / (1024.0 * 1024.0);
    } else {
        NSLog(@"file is not exist");
        return 0;
    }
}
```


#### 删除文件
```
-(void)deleteFile{
    NSString *documentsPath =[self getDocumentsPath];
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *iOSPath = [documentsPath stringByAppendingPathComponent:@"iOS.txt"];
    BOOL isSuccess = [fileManager removeItemAtPath:iOSPath error:nil];
    if (isSuccess) {
        NSLog(@"delete success");
    }else{
        NSLog(@"delete fail");
    }
}
```

#### 移动文件
```
- (BOOL)moveFile:(NSString *)filePath toTargetPath:(NSString *)targetPath
{
	 NSFileManager *fileManager = [NSFileManager defaultManager];
    BOOL isSuccess = [fileManager moveItemAtPath:filePath toPath:targetPath error:nil];
    if (isSuccess) {
        NSLog(@"rename success");
        return true;
    }else{
        NSLog(@"rename fail");
        return false;
    }
}
```


#### 重命名
```
- (BOOL)renameFileName:(NSString *)filePath rename:(NSString *)newfileName
{
    //通过移动该文件对文件重命名
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *moveToPath = [documentsPath stringByAppendingPathComponent:newfileName];
    BOOL isSuccess = [fileManager moveItemAtPath:filePath toPath:moveToPath error:nil];
    if (isSuccess) {
        NSLog(@"rename success");
        return true;
    }else{
        NSLog(@"rename fail");
        return false;
    }
}
```