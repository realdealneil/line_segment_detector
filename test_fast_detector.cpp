#include <iostream>
#include <opencv2/opencv_modules.hpp>

#ifdef HAVE_OPENCV_FEATURES2D

#include <opencv2/line_descriptor.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/highgui.hpp>

#include <cstdio>

using namespace cv;
using namespace cv::line_descriptor;
using namespace std;

int main( int argc, char** argv)
{
	if (argc !=2)
	{
		cout << "Usage: " << argv[0] << " <ImageFileName>\n";
		return -1;
	}
	
	Mat image;
	image = imread(argv[1], CV_LOAD_IMAGE_COLOR);
	
	if (!image.data)
	{
		cout << "Coult not open the image: " << argv[1] << "\n";
		return -1;
	}
	
	//! Try to detect lines in image using LSD line detector:
	Ptr<LSDDetector> lineDetector = LSDDetector::createLSDDetector();
	
	vector<KeyLine> lineSegments;
	
	Mat output = image.clone();
	lineDetector->detect(image, lineSegments, 2, 1);
	
	/* Draw lines on output image */
	if (output.channels() == 1)
	{
		cvtColor(output, output, COLOR_GRAY2BGR);
	}
	
	for (int i=0; i<lineSegments.size(); ++i)
	{
		const KeyLine& kl = lineSegments.at(i);
		if (kl.octave == 0) {
			Scalar myCol(128, 128, 200);
			Point p0 = Point2f(kl.startPointX, kl.startPointY);
			Point p1 = Point2f(kl.endPointX, kl.endPointY);
			
			line(output, p0, p1, myCol, 3);
			
		}
	}
	
	
	
	namedWindow("Output", WINDOW_AUTOSIZE);
	imshow("Output", output);
	
	waitKey(0);
	return 0;
}
#else
int main()
{
	std::cerr << " OpenCV was built without features2d module!  Rebuild!\n";
	return 0;
}

#endif // HAVE_OPENCV_FEATURES2D
