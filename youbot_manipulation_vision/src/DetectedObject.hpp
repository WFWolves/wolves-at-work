/*
 * DetectedObject.hpp
 *
 *  Created on: 15.08.2012
 *      Author: cpupower
 */

#ifndef DETECTEDOBJECT_HPP_
#define DETECTEDOBJECT_HPP_

#include <string>
#include <limits>
#include "opencv2/core/core.hpp"

class DetectedObject {
public:
	DetectedObject(cv::RotatedRect rrect, std::string name);
	cv::RotatedRect getRotatedRect();
	cv::Rect getBoundingBox();
	std::string getName();
	void setName(std::string name);
	float getAspectRatio();
	virtual ~DetectedObject();
private:
	cv::Rect bbox;
	cv::RotatedRect rect;
	std::string name;
};


#endif /* DETECTEDOBJECT_HPP_ */
