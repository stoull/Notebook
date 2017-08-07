//
//  PhotoEidter.m
//  KaoTiBi
//
//  Created by Stoull Hut on 26/02/2017.
//  Copyright © 2017 CCApril. All rights reserved.
//

#import <opencv2/opencv.hpp>

#include <math.h>
#import "PhotoEidter.h"
#import "DocumentMgr.h"
#import "KTDefine.h"
#import "UIDevice+deviceModel.h"

static cv::Scalar FILL_COLOR = cv::Scalar(222,222,222); // 色块的填充颜色
static cv::Scalar TEXT_COLOR = cv::Scalar(1.0,1.0,255.0);// 图片标记的字体的颜色

double scale = 1.0;          // 图像的缩放比例

static int fontFace = 1;
static int thickness = 1;

double MIN_AREA = 600 * scale * scale;   // 色块的最小面积
//static double MIN_WIDTH = 100;
//static double MIN_HEIGHT = 50;

// 当图片的大小是 550* 600 的时候， 行间距大概是10px， MAX_LINE_THICKNESS 为4或5 比较合适。 如果图像很大，则可以适当设置大一些
double MAX_LINE_THICKNESS = 4*scale; // 笔的线条的最大宽度。

cv::Mat processClose (double kenelSize, cv::Mat src);
cv::Mat Mask(double threshod, cv::Mat src, cv::Mat mask, int type);
cv::Mat ScanImageAndReduceIterator(cv::Mat I, const uchar* const table);
float getMax (float r, float g, float b);
float getMin (float r, float g, float b);
void GetHSVRangWithColor(cv::Scalar Scalars[2], ColorType color);
cv::Mat getMask(double threshod, cv::Mat src, cv::Mat mask);
cv::Mat getUnMask(double threshod, cv::Mat src, cv::Mat mask);

@implementation PhotoEidter

-(void)distinguishColorBlockSeparate:(NSString *)picPath colorType:(ColorType)colorType{
    NSString *curentScreenSize = [[UIDevice currentDevice] iPhoneScreenSize];
    if ([curentScreenSize isEqualToString:iPhone_3_5_Inch]) {// 3.5英寸 640/480
        scale = 1.0;
    }else if ([curentScreenSize isEqualToString:iPhone_4_0_Inch]) {// 4.0英寸 640/480
        scale = 1.0;
    }else if ([curentScreenSize isEqualToString:iPhone_4_7_Inch]) {// 4.7英寸 1280/720
        scale = 2.0;
    }else if ([curentScreenSize isEqualToString:iPhone_5_5_Inch]) {// 5.5英寸 1920/1080
        scale = 3.0;
    }else{
        
    }
    
    MIN_AREA = 600 * scale * scale;
    MAX_LINE_THICKNESS = 4 * scale;
    
    cv::String filePath = [picPath UTF8String];
    cv::Mat CVImage = cv::imread(filePath, CV_LOAD_IMAGE_COLOR);
    if (!CVImage.empty()) {
        cv::Mat hsvImage;
        cv::cvtColor(CVImage, hsvImage, cv::COLOR_BGR2HSV);
        
        cv::Mat mask = cv::Mat();
        cv::Scalar hsvRange[2];
        GetHSVRangWithColor(hsvRange, colorType);
        cv::Scalar lowerb = hsvRange[0];
        cv::Scalar uperb = hsvRange[1];
        
        // 获取范围
        cv::inRange(hsvImage, lowerb, uperb, mask);
        
        double thresh = 123.0;
        cv::Mat thresholdOutput = cv::Mat();
        
        // 二值化
        cv::threshold(mask, thresholdOutput, thresh, 255, 3);
        
        // 闭合图形
        cv::Mat close_mask = processClose(MAX_LINE_THICKNESS, thresholdOutput);
        
//        NSString *closeSTring = @"/Users/stoull/Desktop/closePic.jpg";
//        cv::String closeS = [closeSTring UTF8String];
//        cv::imwrite(closeS, close_mask);
        
        // 保存被挖出色块的原图
        NSString *lastcom = [picPath lastPathComponent];
        NSString *docPath = [picPath stringByReplacingOccurrencesOfString:lastcom withString:@""];
        cv::String dPath = [docPath UTF8String];
        
        // 找到轮廓，并挖出轮廓，填充轮廓。
        findContour(close_mask, CVImage,dPath);
        
        NSString *umaskString = [NSString stringWithFormat:@"%@%@.jpg",docPath,kNoAnswerPicName];
        cv::String umaskImg = [umaskString UTF8String];
        cv::imwrite(umaskImg, CVImage);
    }
}

- (void)distinguishColorBlockWithWholePic:(NSString *)path colorType:(ColorType)colorType{
    cv::String filePath = [path UTF8String];
    cv::Mat CVImage = cv::imread(filePath, CV_LOAD_IMAGE_COLOR);
    if (!CVImage.empty()) {
        cv::Mat hsvImage;
        cv::cvtColor(CVImage, hsvImage, cv::COLOR_BGR2HSV);
        
        cv::Mat mask = cv::Mat();
        cv::Scalar hsvRange[2];
        GetHSVRangWithColor(hsvRange, colorType);
        cv::Scalar lowerb = hsvRange[0];
        cv::Scalar uperb = hsvRange[1];
        
        cv::inRange(hsvImage, lowerb, uperb, mask);
        
        double thresh = 123.0;
        cv::Mat thresholdOutput = cv::Mat();
        cv::threshold(mask, thresholdOutput, thresh, 255, 3);
        
        cv::Mat clone = CVImage.clone();
        cv::Mat close_mask = processClose(MAX_LINE_THICKNESS, thresholdOutput);
        
        CVImage = getMask(125, CVImage, close_mask);
        NSString *destString = @"/Users/stoull/Desktop/exampleCVI2.jpg";
        cv::String desS = [destString UTF8String];
        cv::imwrite(desS, CVImage);
        
        clone = getUnMask(125, clone, close_mask);
        NSString *umaskString = @"/Users/stoull/Desktop/exampleumask.jpg";
        cv::String umaskImg = [umaskString UTF8String];
        cv::imwrite(umaskImg, clone);
    }
}


void findContour(cv::Mat maskedImage, cv::Mat frame, cv::String dPath){
    std::vector<std::vector<cv::Point>> contours ;
    cv::Mat hierarchy = cv::Mat();
    cv::findContours(maskedImage, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_TC89_KCOS);
    
    unsigned long contoursize = contours.size() - 1;
    if (hierarchy.size().height > 0 && hierarchy.size().width > 0) {
        int labelIndex = 1;
        for (int idx=0; idx >= 0; idx = (int)hierarchy.at<cv::Vec4i>(0,idx)[0]){
            cv::Rect rect = cv::boundingRect(contours.at(contoursize - idx));
            double contourArea = rect.area();
            int realWidth = rect.width;
            int realHeigth = rect.height;
            if (contourArea < MIN_AREA) {
                continue;
            }
            
//            contours.at(contoursize - idx) =
//            if (realWidth < MIN_WIDTH || realHeigth < MIN_HEIGHT) {
//                continue;
//            }
            
            cv::Point pos = rect.tl();
            // 色块 编号， 可选。
            NSString *indexString = [NSString stringWithFormat:@"%d",labelIndex++];
            cv::String idxString = [indexString UTF8String];
            cv::putText(frame, idxString, pos, fontFace, scale, TEXT_COLOR, thickness);
            
            // 单独 保存一个个的 色块
            cv::Mat newMat = cv::Mat(frame,rect);
            NSString *sepString = [NSString stringWithFormat:@"%s%@%d.jpg",dPath.c_str(),kSeparateBlock,idx+1];
            cv::String sepStr = [sepString UTF8String];
            cv::imwrite(sepStr, newMat);
            
            newMat.setTo(FILL_COLOR);
        }
        // 填充原图
//        cv::fillPoly(frame, contours, FILL_COLOR);
    }
}


cv::Mat getMask(double threshod, cv::Mat src, cv::Mat mask){
    return Mask(threshod, src, mask, 1);
}

cv::Mat getUnMask(double threshod, cv::Mat src, cv::Mat mask){
    return Mask(threshod, src, mask, 2);
}

cv::Mat processClose (double kenelSize, cv::Mat src){
    cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(kenelSize,kenelSize));
    cv::Mat dst = cv::Mat(src.rows, src.cols,CV_8UC3);
    cv::morphologyEx(src, dst, cv::MORPH_CLOSE, element);
    return dst;
}

cv::Mat Mask(double threshod, cv::Mat src, cv::Mat mask, int type)
{
    
    uint8_t *myData = src.data;
    long width = src.cols;
    long height = src.rows;
    long _stride = src.step;//in case cols != strides
    
    
    
    
    uint8_t *maskData = mask.data;
    long mW = mask.cols;
    long mH = mask.rows;
    long _maskStride = mask.step;

    NSLog(@" src : %ld %ld    mask : %ld %ld",width, height, mW, mH);
    
    for(int i=0; i<height; i++){
        for(int j=0; j<width; j++){
            
            uint8_t ds = maskData[ i * _maskStride + j];
            if (type == 1) {
                if (ds < threshod) {
                    src.data[src.step[0]*i + src.step[1]* j + 0] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 1] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 2] = ds;
                }
            }else if (type == 2){
                if (ds > threshod) {
                    src.data[src.step[0]*i + src.step[1]* j + 0] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 1] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 2] = ds;
                }
            }else if (type == 3){
                if (ds < threshod) {
                    ds = 0;
                    src.data[src.step[0]*i + src.step[1]* j + 0] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 1] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 2] = ds;
                }
            }else if (type == 4){
                if (ds > threshod) {
                    ds = 0;
                    src.data[src.step[0]*i + src.step[1]* j + 0] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 1] = ds;
                    src.data[src.step[0]*i + src.step[1]* j + 2] = ds;
                }
            }
        }
    }
    return src;

//    uint8_t *myData = src.data;
//    int width = src.cols;
//    int height = src.rows;
//    long _stride = src.step;//in case cols != strides
//    for(int i = 0; i < height; i++)
//    {
//        for(int j = 0; j < width; j++)
//        {
//            uint8_t ds = myData[ i * _stride + j];
////            LBLog(@" th: %f  ds : %hhu",threshod,ds);
//            if (type == 1) {
//                if (ds < threshod) {
//                    //                    double dsx[3] = {ds,ds,ds};
////                    ds = 0;
//                    mask.at<uint8_t>(i,j) = ds;
//                    LBLog(@" xx: %f  ?? : %hhu type: %d",threshod,ds,type);
//                }
//            }else if (type == 2){
//                if (ds > threshod) {
//                    mask.at<uint8_t>(i,j) = ds;
//                    LBLog(@" xx: %f  ?? : %hhu type: %d",threshod,ds,type);
//                }
//            }else if (type == 3){
//                if (ds < threshod) {
//                    ds = 0;
//                    mask.at<uint8_t>(i,j) = ds;
//                    LBLog(@" xx: %f  ?? : %hhu type: %d",threshod,ds,type);
//                }
//            }else if (type == 4){
//                if (ds > threshod) {
//                    ds = 0;
//                    mask.at<uint8_t>(i,j) = ds;
//                    LBLog(@" xx: %f  ?? : %hhu type: %d",threshod,ds,type);
//                }
//            }
//        }
//    }
    
//    cv::Size size = src.size();
//    double hh = size.height;
//    double ww = size.width;
//    long h = round(hh) -1;
//    long w = round(ww) - 1;
//    for (int i = 0; i < h ; i++){
//        for (int j = 0; j < w; j++){
//            double ds = mask.at<double>(i,j);
//#warning Here no clear
//            if (type == 1) {
//                if (ds < threshod) {
////                    double dsx[3] = {ds,ds,ds};
//                    mask.at<double>(i,j) = ds;
//                }
//            }else if (type == 2){
//                if (ds < threshod) {
//                    mask.at<double>(i,j) = ds;
//                }
//            }else if (type == 3){
//                if (ds < threshod) {
//                    ds = 0;
//                    mask.at<double>(i,j) = ds;
//                }
//            }else if (type == 4){
//                if (ds < threshod) {
//                    ds = 0;
//                    mask.at<double>(i,j) = ds;
//                }
//            }
//        }
//    }
//    return src;
}

cv::Mat ScanImageAndReduceIterator(cv::Mat I, const uchar* const table)
{
    // accept only char type matrices
    CV_Assert(I.depth() != sizeof(uchar));
    const int channels = I.channels();
    switch(channels)
    {
        case 1:
        {
            cv::MatIterator_<uchar> it, end;
            for( it = I.begin<uchar>(), end = I.end<uchar>(); it != end; ++it)
                *it = table[*it];
            break;
        }
        case 3:
        {
            cv::MatIterator_<cv::Vec3b> it, end;
            for( it = I.begin<cv::Vec3b>(), end = I.end<cv::Vec3b>(); it != end; ++it)
            {
                (*it)[0] = table[(*it)[0]];
                (*it)[1] = table[(*it)[1]];
                (*it)[2] = table[(*it)[2]];
            }
        }
    }
    return I;
}

cv::Mat ScanImageAndReduceRandomAccess(cv::Mat I, const uchar* const table)
{
    // accept only char type matrices
    CV_Assert(I.depth() != sizeof(uchar));
    const int channels = I.channels();
    switch(channels)
    {
        case 1:
        {
            for( int i = 0; i < I.rows; ++i)
                for( int j = 0; j < I.cols; ++j )
                    I.at<uchar>(i,j) = table[I.at<uchar>(i,j)];
            break;
        }
        case 3:
        {
            cv::Mat_<cv::Vec3b> _I = I;
            
            for( int i = 0; i < I.rows; ++i)
                for( int j = 0; j < I.cols; ++j )
                {
                    _I(i,j)[0] = table[_I(i,j)[0]];
                    _I(i,j)[1] = table[_I(i,j)[1]];
                    _I(i,j)[2] = table[_I(i,j)[2]];
                }
            I = _I;
            break;
        }
    }
    return I;
}

float getMax (float r, float g, float b){
    return MAX(r, MAX(g, b));
}

float getMin (float r, float g, float b){
    return MIN(r, MIN(g, b));
}

void GetHSVRangWithColor(cv::Scalar Scalars[2], ColorType color){
    switch (color) {
        case ColorTypeRed:
        {
            cv::Scalar low = cv::Scalar(165,69,66);
            cv::Scalar up = cv::Scalar(180,255,255);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case ColorTypeYellow:
        {
            cv::Scalar low = cv::Scalar(27, 105, 115);
            cv::Scalar up = cv::Scalar(40, 225, 225);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case ColorTypeOrange:
        {
            cv::Scalar low = cv::Scalar(11, 43, 46);
            cv::Scalar up = cv::Scalar(25, 255, 255);
            Scalars[0] = low;
            Scalars[1] = up;
        }

            break;
        case ColorTypeCyan:
        {
            cv::Scalar low = cv::Scalar(29, 105, 135);
            cv::Scalar up = cv::Scalar(41, 251, 211);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case ColorTypeGreen:
        {
            cv::Scalar low = cv::Scalar(50, 43, 46);
            cv::Scalar up = cv::Scalar(70, 225, 225);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case ColorTypeBlue:
        {
            cv::Scalar low = cv::Scalar(89, 43, 46);
            cv::Scalar up = cv::Scalar(120, 225, 225);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case ColorTypePink:
        {
            cv::Scalar low = cv::Scalar(29, 105, 135);
            cv::Scalar up = cv::Scalar(41, 251, 211);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        case 7:
        {
            cv::Scalar low = cv::Scalar(29, 105, 135);
            cv::Scalar up = cv::Scalar(41, 251, 211);
            Scalars[0] = low;
            Scalars[1] = up;
        }
        case ColorTypePurple:
        {
            cv::Scalar low = cv::Scalar(125, 43, 46);
            cv::Scalar up = cv::Scalar(155, 255, 255);
            Scalars[0] = low;
            Scalars[1] = up;
        }
            break;
        default:
            break;
    }
}

@end
