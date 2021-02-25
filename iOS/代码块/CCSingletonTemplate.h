
#ifndef CCSingleton_h
#define CCSingleton_h

#define singleton_interface(className)\
+ (className *)share##className;

#define singleton_implementation(className) \
static className *_instance;\
+ (className *)shared##className\
{\
    __block className *strongRef = _instance;\
    if (strongRef == nil) {\
        static dispatch_semaphore_t lock;\
        static dispatch_once_t onceToken;\
        dispatch_once(&onceToken, ^{\
            lock = dispatch_semaphore_create(1);\
        });\
        dispatch_semaphore_wait(lock, DISPATCH_TIME_FOREVER);\
        if (_instance == nil) {\
            strongRef = [[super allocWithZone:NULL] init];\
            SEL sel = NSSelectorFromString(@"singletonInit");\
            if ([strongRef respondsToSelector:sel]) {\
                [strongRef performSelector:@selector(singletonInit)];\
            }\
            _instance = strongRef;\
        } else {\
            strongRef = _instance;\
        }\
        dispatch_semaphore_signal(lock);\
    }\
    return strongRef;\
}\
- (instancetype)init {\
    static dispatch_semaphore_t semaphore;\
    static dispatch_once_t onceToken;\
    dispatch_once(&onceToken, ^{\
        semaphore = dispatch_semaphore_create(1);\
    });\
    className *strongRef = _instance;\
    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);\
    if (strongRef.class != self.class) {\
        self = [super init];\
        if (self.class == _instance.class) {\
            SEL sel = NSSelectorFromString(@"singletonInit");\
            if ([self respondsToSelector:sel]) {\
                [self performSelector:@selector(singletonInit)];\
            }\
            _instance = self;\
        }\
    }\
    dispatch_semaphore_signal(semaphore);\
    return self;\
}\
- (void)singletonInit {\
    NSLog(@"caller: %@; SingletonClass customic init", self);\
}\
+ (id)allocWithZone:(NSZone *)zone {\
    if (self == className.class) {\
        return [className share##className];\
    }\
    return [super allocWithZone:zone];\
}\
- (id)copyWithZone:(NSZone *)zone {\
    return self;\
}\

#endif
