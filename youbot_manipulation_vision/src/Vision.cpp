//
//  main.cpp
//  Histofilter
//
//  Created by Jan Carstensen on 21.06.12.
//  ROS connection by Alexander Gabel
//  Copyright (c) 2012 WF Wolves. All rights reserved.
//
#include "ros/ros.h"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <image_transport/image_transport.h>
#include <geometry_msgs/Polygon.h>
#include <geometry_msgs/Point32.h>
#include <dynamic_reconfigure/server.h>
#include <cassert>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <list>

#include "DetectedObject.hpp"
#include "youbot_manipulation_vision/BoundingBox.h"
#include "youbot_manipulation_vision/RotatedRect.h"
#include "youbot_manipulation_vision/DetectedObject.h"
#include "youbot_manipulation_vision/DetectedObjects.h"

#include "youbot_manipulation_vision/ManipulationVisionConfig.h"

#define IMAGE_IN_TOPIC  "/usb_cam/image_raw" //"/usb_cam/image_rect_color"
#define IMAGE_THRESH_TOPIC "/vision_thresholded"
#define IMAGE_DEBUG_TOPIC "/vision_debug"
#define IMAGE_DEBUG_EXTRACTED_TOPIC "/vision_extracted"
#define OBJECTS_TOPIC "/vision_objects"

//#define SHOW_IMAGE_COUNT

using namespace cv;
using namespace std;

#define PI 3.1415926535

image_transport::Publisher pub_thresholded;
image_transport::Publisher pub_debug;
image_transport::Publisher pub_extracted;
image_transport::Subscriber sub_camera;
ros::Publisher pub_objects;

ros::NodeHandle* nh;



float getRotatedArea(RotatedRect rect) {
	return rect.size.height * rect.size.width;
}

Mat* extractRotatedRegion(Mat& image, RotatedRect rect) {
	Point2f center = rect.center;
	double angle = rect.angle;
	Mat* dst_buf = new Mat( rect.size.width, rect.size.height, image.type());

	Mat rotmat = getRotationMatrix2D(center,angle+90,1);

	rotmat.at<double>(0, 2) += dst_buf->cols*0.5 - center.x;
	rotmat.at<double>(1, 2) += dst_buf->rows*0.5 - center.y;

	warpAffine(image, *dst_buf, rotmat, dst_buf->size());

	return dst_buf;
}

bool sortBoundingBoxes(Rect one, Rect two){
    if (one.area() > two.area()){
        return true;
    } else {
        return false;
    }
}

bool sortRotatedBoxes(RotatedRect one, RotatedRect two){
    if (getRotatedArea(one) > getRotatedArea(two)){
        return true;
    } else {
        return false;
    }
}

void drawShadowText(Mat image, string text, Point org,
		int fontFace, double fontScale, Scalar color,
		int thickness=1, int linetype=8, bool bottomLeftOrigin = false,
		Scalar shadowColor = Scalar(0,0,0), int shadowOffsetX = 2, int shadowOffsetY = 2) {
	Point2f shadowPoint = org;
	shadowPoint.x += shadowOffsetX;
	shadowPoint.y += shadowOffsetY;
	putText(image, text, shadowPoint, fontFace, fontScale, shadowColor, thickness, linetype, bottomLeftOrigin);
	putText(image, text, org, fontFace, fontScale, color, thickness, linetype, bottomLeftOrigin);
}

void deleteDetectedObjectList(list<DetectedObject*> detectedObjects) {
	for (list<DetectedObject*>::const_iterator iterator = detectedObjects.begin(), end = detectedObjects.end(); iterator != end; ++iterator) {
		delete (*iterator);
	}
}

void drawDetectedObjects(list<DetectedObject*> detectedObjects, Mat& drawing) {
	for (list<DetectedObject*>::const_iterator iterator = detectedObjects.begin(), end = detectedObjects.end(); iterator != end; ++iterator) {
    	DetectedObject* obj = *iterator;
		RotatedRect rect = obj->getRotatedRect();
		float ratio = obj->getAspectRatio();
		string objectname = obj->getName();

        Scalar color = Scalar( 0,0,0 );
        Point2f* points = new Point2f[4];
        rect.points(points);

        for(int j = 0; j < 4; ++j) {
            line(drawing, points[j], points[(j + 1) % 4], color, 1, CV_AA);
        }

        float angle = rect.angle;

        //angle lines
        Point2f topPoint = rect.center;
        topPoint.y-=50;
        line(drawing, rect.center, topPoint, Scalar(0,255,0), 1, CV_AA);
        Point2f degPoint = rect.center;
        degPoint.x+=50*cos((angle-90)*PI/180.0);
        degPoint.y+=50*sin((angle-90)*PI/180.0);
        line(drawing, rect.center, degPoint, Scalar(0,255,0), 1, CV_AA);

        //angle arc
        Point2f lastPoint(topPoint);
        lastPoint.y+=25;
        float tmpangle = angle-90;
        for (int j=-90; j>tmpangle; j--) {
        	Point2f nowPoint(rect.center);
        	nowPoint.x+=25*cos((j)*PI/180.0);
        	nowPoint.y+=25*sin((j)*PI/180.0);
        	line(drawing, lastPoint, nowPoint, Scalar(0,255,255), 1, CV_AA);
        	lastPoint = nowPoint;
        }

        //angle text
        stringstream sangle;
        sangle << setprecision(1) << fixed << angle << " deg";
        drawShadowText(drawing, sangle.str(), rect.center, 1, 1, Scalar(0,0,255), 2, 1, false);

        //aspect ratio text
        Point2f ratiop(rect.center);
        ratiop.y += 20;
        stringstream sratio;
        sratio << "Aspect Ratio: " << setprecision(2) << fixed << ratio;
        drawShadowText(drawing, sratio.str(), ratiop, 1, 1, Scalar(255,0,255), 2, 1, false);

        Point2f objp(ratiop);
        objp.y += 20;
        stringstream objdetected;
        objdetected << "Detected: " << objectname;

        drawShadowText(drawing, objdetected.str(), objp, 1, 1, Scalar(0,255,255), 2, 1, false);


        delete[] points;

    }
}

void drawBoundingBoxes(vector<Rect> rects, Mat& drawing) {
    for( size_t i = 0; i < rects.size(); i++ ){
        Scalar color = Scalar( 0,0,0 );
        rectangle( drawing, rects[i].tl(), rects[i].br(), color, 2, 8, 0 );
    }
}

list<DetectedObject*> getDetectedObjects(vector<RotatedRect> rrects) {
	list<DetectedObject*> objects;
	for (size_t i=0; i<rrects.size(); i++) {
		DetectedObject* obj = new DetectedObject(rrects[i], "???");

		float ratio = obj->getAspectRatio();
		string name = "???";

        if (ratio >= 0.16 && ratio <= 0.32) {
        	name = "Thin alu profile";
        	//width: 0.02m
        	//height: 0.10m
        	//ratio: 0.2
        }/* else if (ratio >= 0.25 && ratio <= 0.32) {
        	name = "Big Screw";
			//width: 0.02m .. 0.034m
			//height: 0.112m
			//ratio: 0.179..0.304
        }*/ else if (ratio >= 0.38 && ratio <= 0.50) {
        	name = "Big alu profile";
        	//width: 0.04m
        	//height: 0.10m
        	//ratio: 0.4
        } else if (ratio >= 0.55 && ratio <= 0.69) {
        	name = "Small cylinder";
        	//width: 0.03m
        	//height: 0.045m
        	//ratio: 0.666
        }
        obj->setName(name);

        objects.push_back(obj);
	}
	return objects;
}

void filterDetectedObjects(std_msgs::Header currentHeader, Mat& grey, Mat& thresholded, double canny_threshold, int cornerThreshold, list<DetectedObject*>& detectedObjects) {
    for (list<DetectedObject*>::const_iterator iterator = detectedObjects.begin(), end = detectedObjects.end(); iterator != end; ++iterator) {
    	DetectedObject* obj = *iterator;
    	/*if (obj->getName() == "Thin alu profile") {
    		Mat* region = extractRotatedRegion(thresholded, obj->getRotatedRect());
    		cv_bridge::CvImagePtr cv_pextracted(new cv_bridge::CvImage);
    		sensor_msgs::ImagePtr msg_extracted;

    		vector<vector<Point> > contours;
    		vector<Vec4i> hierarchy;
    		vector<int> cvxHullIndices;
    		vector<Vec4i> cvxDefects;
    		vector<vector<Point> > contours_poly(1);
    		findContours(*region, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

    		if (contours.size() <= 0) {
    			continue;
    		}

    		cout << "Contour size: " << contours[0].size() << endl;

    		//approxPolyDP( Mat(contours[0]), contours_poly[0], approxPolyEpsilon, true );

    		//convexHull(contours_poly[0], cvxHullIndices, true, true);
    		//if (cvxHullIndices.size() < 4) {
    		//	continue;
    		//}
    		//convexityDefects(contours_poly[0], cvxHullIndices, cvxDefects);

    		//if (cvxDefects.size() > 2) {
    		//	obj->setName("Big screw");
    		//}

    		Mat regionColored;
    		cvtColor(*region, regionColored, CV_GRAY2BGR);
    		Scalar color (0, 255, 0);
    		drawContours(regionColored, contours_poly, 0, color);


    		cv_pextracted->image = regionColored;

			cv_pextracted->header = currentHeader;
			cv_pextracted->encoding = sensor_msgs::image_encodings::BGR8;
			msg_extracted = cv_pextracted->toImageMsg();

			pub_extracted.publish(msg_extracted);

			cv_pextracted->image.release();


    		delete region;
    	}else */if (obj->getName() == "Small cylinder") {
    		Mat* region = extractRotatedRegion(grey, obj->getRotatedRect());

    		Mat regCanny;
    		GaussianBlur(*region, regCanny, Size(3,3), 10, 10);

    		Canny(regCanny, regCanny, canny_threshold, canny_threshold);

    		cv_bridge::CvImagePtr cv_pextracted(new cv_bridge::CvImage);
    		sensor_msgs::ImagePtr msg_extracted;

    		//cout << "NonZeroCount: " << countNonZero(regCanny) << endl;
    		vector<Point2f> corners;
    		goodFeaturesToTrack(regCanny, corners, 100, 0.3, 10);

    		Mat cannyColored;

    		cvtColor(regCanny, cannyColored, CV_GRAY2BGR);

    		for (size_t i=0; i<corners.size(); i++) {
    			int x = corners[i].x;
    			int y = corners[i].y;
    			cannyColored.at<Vec3b>(y,x)[0] = 0;
    			cannyColored.at<Vec3b>(y,x)[1] = 0;
    			cannyColored.at<Vec3b>(y,x)[2] = 255;
    		}

    		//cout << "CornersCount: " << corners.size() << endl;

    		if (corners.size() > cornerThreshold) {
    			obj->setName("Rough small cylinder");
    		} else {
    			obj->setName("Smooth small cylinder");
    		}

    		cv_pextracted->image = cannyColored;

    		cv_pextracted->header = currentHeader;
    		cv_pextracted->encoding = sensor_msgs::image_encodings::BGR8;
            msg_extracted = cv_pextracted->toImageMsg();

            pub_extracted.publish(msg_extracted);

            cv_pextracted->image.release();
    		delete region;
    	}
    }

}

void image_cb (const sensor_msgs::ImageConstPtr& image) {
    int threshold_value;
    ros::param::param<int>("/vision_threshold_binary", threshold_value, 95);
    int min_objekt_size;
    ros::param::param<int>("/vision_min_objekt_size", min_objekt_size, 4000);
    int keep_object_count;
    ros::param::param<int>("/vision_keep_object_count", keep_object_count, 4);
    int canny_threshold;
    ros::param::param<int>("/vision_canny_threshold", canny_threshold, 40);
    int corner_threshold;
    ros::param::param<int>("/vision_corner_threshold", corner_threshold, 25);
    int const max_BINARY_value = 255;
    Mat grey, thresholded, filtered;
#ifdef SHOW_IMAGE_COUNT
    static long imcount = 0;
    cout << "Image "<< ++imcount <<" recieved" << endl;
#endif
    cv_bridge::CvImagePtr cv_ptr;
    cv_bridge::CvImagePtr cv_pthresholded(new cv_bridge::CvImage());
    cv_bridge::CvImagePtr cv_pdebug(new cv_bridge::CvImage());
    sensor_msgs::ImagePtr msg_thresholded;
    sensor_msgs::ImagePtr msg_debug;
    try
    {
        cv_ptr = cv_bridge::toCvCopy(image, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }
    Mat frame = cv_ptr->image.clone();
    
    cvtColor( frame, grey, CV_RGB2GRAY );  
    
    int dilate_size = 3;
    Mat dilate_element = getStructuringElement( MORPH_RECT,
                                           Size( 2*dilate_size + 1, 2*dilate_size+1 ),
                                           Point( dilate_size, dilate_size ) );

    threshold( grey, thresholded, threshold_value, max_BINARY_value, 1 ); //Binary Inverted
    dilate(thresholded, filtered, dilate_element);
    erode(filtered, filtered, dilate_element);
    
    try
    {
        cv_pthresholded->image = filtered;
        cv_pthresholded->header = cv_ptr->header;
        cv_pthresholded->encoding = sensor_msgs::image_encodings::MONO8;
        msg_thresholded = cv_pthresholded->toImageMsg();
    }
    catch (cv_bridge::Exception& e)
    {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }
    pub_thresholded.publish(msg_thresholded);
    
    
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    
    findContours(filtered, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    
    /// Approximate contours to polygons + get bounding rects and circles
    vector<vector<Point> > contours_poly( contours.size() );
    vector<Rect> boundRect( contours.size() );
    vector<RotatedRect> minRect( contours.size() );
    
    for( size_t i = 0; i < contours.size(); i++ )
    { 
        approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true );
        boundRect[i] = boundingRect( Mat(contours_poly[i]) );
        minRect[i] = minAreaRect( Mat(contours_poly[i]) );
    }
    
    size_t filteredOutBound = 0;
    size_t filteredOutRot = 0;
    vector<Rect> bigBoundRecs(boundRect.size());
    vector<RotatedRect> bigRotRecs(minRect.size());
    
    for( size_t i = 0; i < boundRect.size(); ++i ){ 
        if (boundRect[i].area() > static_cast<size_t>(min_objekt_size)) {
            bigBoundRecs[i-filteredOutBound] = boundRect[i];
        } else {
            ++filteredOutBound;
        }
    }

    for( size_t i = 0; i < minRect.size(); ++i ){
        if (getRotatedArea(minRect[i]) > min_objekt_size) {
            bigRotRecs[i-filteredOutRot] = minRect[i];
        } else {
            ++filteredOutRot;
        }
    }
    

    /// Filter the x Largest Objects (BoundRects)
    long filteredSizeBound;
    if (boundRect.size()-filteredOutBound >= static_cast<size_t>(keep_object_count)){
        filteredSizeBound = keep_object_count;
    } else {
        filteredSizeBound = boundRect.size()-filteredOutBound;
    }

    /// Filter the x Largest Objects (RotatedRects)
    long filteredSizeRot;
    if (minRect.size()-filteredOutRot >= static_cast<size_t>(keep_object_count)){
        filteredSizeRot = keep_object_count;
    } else {
        filteredSizeRot = minRect.size()-filteredOutRot;
    }

    
    
    vector<Rect> filteredRectBound(filteredSizeBound);
    for( size_t i = 0; i < bigBoundRecs.size()-filteredOutBound; ++i ){
        if( i < filteredRectBound.size()){
            filteredRectBound[i] = bigBoundRecs[i];
        } else {
            for(size_t z = 0; z < filteredRectBound.size(); ++z){
                if (sortBoundingBoxes(bigBoundRecs[i], filteredRectBound[z])){
                    filteredRectBound[z] = bigBoundRecs[i];
                    break;
                }
            }
        }
    }

    vector<RotatedRect> filteredRectRot(filteredSizeRot);
        for( size_t i = 0; i < bigRotRecs.size()-filteredOutRot; ++i ){
            if( i < filteredRectRot.size()){
                filteredRectRot[i] = bigRotRecs[i];
            } else {
                for(size_t z = 0; z < filteredRectRot.size(); ++z){
                    if (sortRotatedBoxes(bigRotRecs[i], filteredRectRot[z])){
                        filteredRectRot[z] = bigRotRecs[i];
                        break;
                    }
                }
            }
        }

    Rect bestBound;
    int bestRatioBound = 0;

	for( size_t i = 0; i < filteredRectBound.size(); ++i ){
		if (bestRatioBound < filteredRectBound[i].height/filteredRectBound[i].width){
			bestRatioBound = filteredRectBound[i].height/filteredRectBound[i].width;
			bestBound = filteredRectBound[i];
		}
	}

    RotatedRect bestRotated;
    int bestRatioRot = 0;

	for( size_t i = 0; i < filteredRectRot.size(); ++i ){
			if (bestRatioRot < filteredRectRot[i].size.height/filteredRectRot[i].size.width){
				bestRatioRot = filteredRectRot[i].size.height/filteredRectRot[i].size.width;
				bestRotated = filteredRectRot[i];
			}
		}

	list<DetectedObject*> detectedObjects = getDetectedObjects(filteredRectRot);
    
	filterDetectedObjects(cv_ptr->header, grey, filtered, canny_threshold, corner_threshold, detectedObjects);

    /// Draw polygonal contour + bounding rects + circles
    Mat drawing = frame.clone();
    drawBoundingBoxes(filteredRectBound, drawing);
    drawDetectedObjects(detectedObjects, drawing);

	youbot_manipulation_vision::DetectedObjects objects;
	objects.header = cv_ptr->header;
	for (list<DetectedObject*>::const_iterator iterator = detectedObjects.begin(), end = detectedObjects.end(); iterator != end; ++iterator) {
		DetectedObject* obj = *iterator;
		RotatedRect rrect = obj->getRotatedRect();
		Rect bbox = obj->getBoundingBox();
		youbot_manipulation_vision::DetectedObject obj_msg;
		youbot_manipulation_vision::RotatedRect rrect_msg;
		youbot_manipulation_vision::BoundingBox bbox_msg;

		geometry_msgs::Point pCenter;
		pCenter.x = rrect.center.x;
		pCenter.y = rrect.center.y;

		geometry_msgs::Point pPosition;
		pPosition.x = bbox.x;
		pPosition.y = bbox.y;

		rrect_msg.centerPoint = pCenter;
		rrect_msg.width = rrect.size.width;
		rrect_msg.height = rrect.size.height;
		rrect_msg.angle = rrect.angle;

		bbox_msg.position = pPosition;
		bbox_msg.width = bbox.width;
		bbox_msg.height = bbox.height;

		obj_msg.rrect = rrect_msg;
		obj_msg.bbox = bbox_msg;
		obj_msg.object_name = obj->getName();

		objects.objects.push_back(obj_msg);
	}

	pub_objects.publish(objects);

    try
    {
        cv_pdebug->image = drawing;
        cv_pdebug->header = cv_ptr->header;
        cv_pdebug->encoding = sensor_msgs::image_encodings::BGR8;
        msg_debug = cv_pdebug->toImageMsg();
    }
    catch (cv_bridge::Exception& e)
    {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }
    pub_debug.publish(msg_debug);
    
    
    cv_pthresholded->image.release();
    cv_pdebug->image.release();
    
    deleteDetectedObjectList(detectedObjects);
}

void cb_reconfigure(youbot_manipulation_vision::ManipulationVisionConfig &config, uint32_t level) {
	nh->setParam("/vision_threshold_binary", config.vision_threshold_binary);
	nh->setParam("/vision_canny_threshold", config.vision_canny_threshold);
	nh->setParam("/vision_min_objekt_size", config.vision_min_objekt_size);
	nh->setParam("/vision_keep_object_count", config.vision_keep_object_count);
	nh->setParam("/vision_corner_threshold", config.vision_corner_threshold);
}

int main (int argc, char** argv)
{
    //Init ROS node
    ros::init(argc, argv, "youbot_manipulation_vision");
    
    nh = new ros::NodeHandle();

    image_transport::ImageTransport it(*nh);
    pub_thresholded = it.advertise(IMAGE_THRESH_TOPIC, 1);
    pub_debug = it.advertise(IMAGE_DEBUG_TOPIC, 1);
    pub_objects = nh->advertise<youbot_manipulation_vision::DetectedObjects>(OBJECTS_TOPIC, 1);
    pub_extracted = it.advertise(IMAGE_DEBUG_EXTRACTED_TOPIC, 1);
    
    sub_camera = it.subscribe(IMAGE_IN_TOPIC, 1, &image_cb);//nh.subscribe<const sensor_msgs::ImagePtr&>(IMAGE_IN_TOPIC, 1, &image_cb);

    dynamic_reconfigure::Server<youbot_manipulation_vision::ManipulationVisionConfig> dsrv;
    dynamic_reconfigure::Server<youbot_manipulation_vision::ManipulationVisionConfig>::CallbackType cbt_dynre;
    cbt_dynre = boost::bind(&cb_reconfigure, _1, _2);
    dsrv.setCallback(cbt_dynre);

    ros::spin();

    delete nh;
    nh = NULL;

    return 0;
}
