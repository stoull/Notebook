
#ifdef DEBUG
    #define CCLog(fmt, ...) NSLog((@"\n:%s log: " fmt), __FUNCTION__, ##__VA_ARGS__)
    #define DLog(fmt, ...) NSLog((@"\n文件:%s\n" "函数名:%s\n" "行号:%d \n" fmt), __FILE__, __FUNCTION__, __LINE__, ##__VA_ARGS__)
    #define DeBugLog(fmt, ...) NSLog((@"%s [Line %d] " fmt), __PRETTY_FUNCTION__, __LINE__, ##__VA_ARGS__)
    #define NSLog(...) NSLog(__VA_ARGS__)
    #define MyNSLog(FORMAT, ...) fprintf(stderr,"[%s]:[line %d行] %s\n",[[[NSString stringWithUTF8String:__FILE__] lastPathComponent] UTF8String], __LINE__, [[NSString stringWithFormat:FORMAT, ##__VA_ARGS__] UTF8String])
#else
    #define CCLog(...)
    #define DLog(...)
    #define DeBugLog(...)
    #define NSLog(...)
    #define MyNSLog(FORMAT, ...)
#endif
