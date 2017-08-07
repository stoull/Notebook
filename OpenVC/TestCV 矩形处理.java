package com.lk;

import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class TestCV {
	
	public static final Scalar FILL_COLOR = new Scalar(222,222,222); // 色块的 填充颜色
	public static final Scalar TEXT_COLOR = new Scalar(1,1,255); // 图片标记的字体的 颜色
	public static String PIC_BASE = "D:\\0clr\\"; // APP 的图片本地存储路径
	public static final String AWS_PREFIX = "aws_"; // 答案图片的 前缀

	static Scalar ffcolor = new Scalar(222, 222, 222);
	static int fontFace = 1;
	static int thickness = 1;

	private static int scale = 3;// 图像的 缩放比例

	public static final double MIN_AREA = 300*scale;// 色块的 最小面积

	// 当图片的大小是 550* 600 的时候， 行间距大概是10px， MAX_LINE_THICKNESS 为4或5 比较合适。 如果图像很大，则可以适当设置大一些
	public static int MAX_LINE_THICKNESS = 4*scale; // 行间距的最小值。
	
	static String imgSuffix = ".jpg";

	static  String fname = "";

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	public static void main(String[] args) {
//		testBUG();

		testSingle("D:\\0clr\\aa.jpg");
		testSingle("D:\\0clr\\bb.jpg");
		testSingle("D:\\0clr\\cc.jpg");
		testSingle("D:\\0clr\\dd.jpg");
	}

	private static void testBUG() {
		String imgPath = "D:\\0clr\\b.jpg";
		imgPath = "D:\\0clr\\c.jpg";
		String color = "orange";
		testXX(imgPath, color);
		color =  "cyan";
		testXX(imgPath, color);

		imgPath = "D:\\0clr\\d.jpg";
		color = "orange";
		testXX(imgPath, color);
		color =  "cyan";
		testXX(imgPath, color);
	}


	private static void testSingle(String imgPath) {
		// String imgPath = "D:\\0clr\\f.jpg";
		String color = "red";
		testXX(imgPath, color);
		color = "green";
		testXX(imgPath, color);
		color = "purple";
		testXX(imgPath, color);
		color = "yellow";
		testXX(imgPath, color);
		color = "orange";
		testXX(imgPath, color);
		color = "cyan";
		testXX(imgPath, color);
	}

	private static void testXX(String imgPath, String color) {
		System.out.println("imgPath = [" + imgPath + "], color = [" + color + "]");
		fname = "ret_"+color+ "_"+getImgName(imgPath);

		PIC_BASE = "D:\\0clr\\" + color + File.separator;
		File dir = new File(PIC_BASE);
		if (!dir.exists()) {
			dir.mkdir();
		} else {

		}

		Mat src = Imgcodecs.imread(imgPath, Imgcodecs.CV_LOAD_IMAGE_COLOR);

		Mat hsvImage = new Mat();
		Imgproc.cvtColor(src, hsvImage, Imgproc.COLOR_BGR2HSV);

		Mat mask = new Mat();
		Scalar[] hsvRange = getHSVRange(color);
		Scalar lowerb = hsvRange[0];
		Scalar upperb = hsvRange[1];

		// 获取范围
		Core.inRange(hsvImage, lowerb, upperb, mask);

		double thresh = 123.0;
		Mat thresholdOutput = new Mat();

		// 二值化
		Imgproc.threshold(mask, thresholdOutput, thresh, 255, 3);

		// 闭合图形
		Mat close_mask = close(MAX_LINE_THICKNESS, thresholdOutput);

		// 找到轮廓， 并挖出轮廓， 填充 轮廓。
		findcontour(close_mask, src);

		// 保存 被挖出色块的 原图。
		String destImg = PIC_BASE + fname;
		Imgcodecs.imwrite(destImg, src);
	}

	public static String getImgName(String imgPath) {
		return  imgPath.substring(imgPath.lastIndexOf(File.separator)+1);
	}

	
	public static void findcontour(Mat maskedImage, Mat frame) {
		List<MatOfPoint> contours = new ArrayList<>();
		Mat hierarchy = new Mat();
		// find contours
		Imgproc.findContours(maskedImage, contours, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		// if any contour exist...
		int contoursize = contours.size()-1;
		
		if (hierarchy.size().height > 0 && hierarchy.size().width > 0)
		{

			int cnt = 1;
			for (int idx = 0; idx >= 0; idx = (int) hierarchy.get(0, idx)[0])
			{
				MatOfPoint points = contours.get(contoursize - idx);
				Rect rect = Imgproc.boundingRect(points);
				double contourArea = Imgproc.contourArea(points);
				contourArea = rect.area();
				if (contourArea < MIN_AREA) {	
					continue;
				}
				
				// 单独 保存一个个的 色块
				Mat newMat = new Mat(frame, rect);
				String destImg = PIC_BASE + AWS_PREFIX + (cnt) + imgSuffix;
//				String destImg = PIC_BASE + fname + (cnt) + imgSuffix;;// 测试的时候， 可以把AWS_PREFIX 换成 fname
				Imgcodecs.imwrite(destImg, newMat);

				// 填充原图
				newMat.setTo(ffcolor);
				Point pos = new Point(rect.tl().x + 2, rect.tl().y + 11);

				// 色块 编号， 可选。
				Imgproc.putText(frame, ""+(cnt), pos, fontFace, scale, TEXT_COLOR, thickness);
				cnt++;
			}
		}
	}



	private static Mat close(double kenelSize, Mat src) {
		// TODO Auto-generated method stub
		Mat element = Imgproc.getStructuringElement(Imgproc.MORPH_RECT, new Size(kenelSize, kenelSize));
		Mat dst = new Mat(src.rows(), src.cols(), CvType.CV_8UC3);
		// Imgproc.dilate(src, dst, element);
		Imgproc.morphologyEx(src, dst, Imgproc.MORPH_CLOSE, element);
		return dst;
	}

	public static Scalar RGB2HSV(int rr,int gg,int bb) {
		float r = rr;
		float g =gg;
		float b = bb;
		float max = max(r, g, b);
		float min = min(r, g, b);
		float h = 0;
		if (max == min)
			h = 0;
		else if (r == max && g >= b)
			h = (g - b) / (max - min) * 60;
		else if (r == max && g < b)
			h = (g - b) / (max - min) + 360;
		else if (g == max)
			h = (b - r) / (max - min) * 60 + 120;
		else if (b == max)
			h = (r - g) / (max - min) * 60 + 240;

		float s = (max - min) / max;
		if (max == 0)
			s = 0;
		Scalar hsv = new Scalar(h, s,  max/255);
		return hsv;
	}


	private static float max(float r, float g, float b) {
		return Math.max(r, Math.max(g, b));
	}

	private static float min(float r, float g, float b) {
		return Math.min(r, Math.min(g, b));
	}

	private static Scalar[] getHSVRange(String color) {
		Scalar[] hsv = new Scalar[2];
		switch (color) {
		case "red":
			hsv[0] = new Scalar(165, 69, 66);
			hsv[1] = new Scalar(170, 255, 255);
			break;
		case "orange":
			hsv[0] = new Scalar(11, 43, 46);
			hsv[1] = new Scalar(25, 255, 255);
			break;
		case "yellow":
//			hsv[0] = new Scalar(26, 43, 46);
//			hsv[1] = new Scalar(34, 255, 255);

			hsv[0] = new Scalar(29, 105, 115);
			hsv[1] = new Scalar(38, 225, 225);
			break;
		case "green":
			hsv[0] = new Scalar(50, 43, 46);
			hsv[1] = new Scalar(70, 225, 225);
			break;
		case "cyan":
			hsv[0] = new Scalar(89, 43, 46);
			hsv[1] = new Scalar(95, 225, 225);

			break;
		case "blue":
			hsv[0] = new Scalar(100, 43, 46);
			hsv[1] = new Scalar(124, 225, 225);
			break;
		case "purple":
			hsv[0] = new Scalar(125, 43, 46);
			hsv[1] = new Scalar(155, 225, 225);

			break;
		default:
			break;
		}
		return hsv;
	}
}




