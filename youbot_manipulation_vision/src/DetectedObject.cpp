/*
 * DetectedObject.cpp
 *
 *  Created on: 15.08.2012
 *      Author: cpupower
 */

#include "DetectedObject.hpp"

using namespace cv;

DetectedObject::DetectedObject(RotatedRect rrect, string name) {
		this->rect = rrect;
		this->name = name;
}
RotatedRect DetectedObject::getRotatedRect() {
	return this->rect;
}
Rect DetectedObject::getBoundingBox() {
	Point2f pts[4];
	this->rect.points(pts);
	float minX = std::numeric_limits<float>::max();
	float minY = std::numeric_limits<float>::max();
	float maxX = std::numeric_limits<float>::min();
	float maxY = std::numeric_limits<float>::min();
	for (int i=0; i<4; i++) {
		if (pts[i].x < minX) {
			minX = pts[i].x;
		}
		if (pts[i].x > maxX) {
			maxX = pts[i].x;
		}
		if (pts[i].y < minY) {
			minY = pts[i].y;
		}
		if (pts[i].y > maxY) {
			maxY = pts[i].y;
		}
	}
	float width = maxX - minX;
	float height = maxY - minY;
	bbox.width = width;
	bbox.height = height;
	bbox.x = minX;
	bbox.y = minY;

	return this->bbox;
}
string DetectedObject::getName() {
	return this->name;
}
void DetectedObject::setName(string name) {
	this->name = name;
}
float DetectedObject::getAspectRatio() {
	float ratio;
	float ratioWH = this->rect.size.width / this->rect.size.height;
	float ratioHW = this->rect.size.height / this->rect.size.width;
	if (ratioWH < ratioHW) {
		ratio = ratioWH;
	} else {
		ratio = ratioHW;
	}
	return ratio;
}

DetectedObject::~DetectedObject() {
	// TODO Auto-generated destructor stub
}

