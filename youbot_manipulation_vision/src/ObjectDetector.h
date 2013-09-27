/*
 * ObjectDetector.h
 *
 *  Created on: 15.04.2013
 *      Author: cpupower
 */

#ifndef OBJECTDETECTOR_H_
#define OBJECTDETECTOR_H_

#include <string>
#include "youbot_manipulation_vision/DetectedObject.h"

namespace youbot_manipulation_vision {

class ObjectDetector {
public:
	ObjectDetector();
	virtual ~ObjectDetector();
	virtual std::string getObjectName() = 0;
	virtual float getObjectDetectedProbability(DetectedObject* object, VisionData* visionData) = 0;
};

} /* namespace youbot_manipulation_vision */
#endif /* OBJECTDETECTOR_H_ */
