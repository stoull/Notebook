//
//  PhotoEidter.h
//  KaoTiBi
//
//  Created by Stoull Hut on 26/02/2017.
//  Copyright © 2017 CCApril. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
#import "penTableViewCell.h"

@interface PhotoEidter : NSObject

// 分离色块
-(void)distinguishColorBlockSeparate:(NSString *)picPath colorType:(ColorType)colorType;

// 整个块图片进行色块识别
- (void)distinguishColorBlockWithWholePic:(NSString *)path colorType:(ColorType)colorType;
@end
