/*
 * youbot_scanner_lines_filter.cpp
 *
 *  Created on: 25.06.2013
 *      Author: p-th.wentscher@ostfalia.de
 */
 
#include <deque>

#include <ros/ros.h>
#include <ros/console.h>
#include <tf/transform_listener.h>
#include <dynamic_reconfigure/server.h>

#include <visualization_msgs/Marker.h>
#include "youbot_scanner_lines/DetectedLaserLine.h"
#include "youbot_scanner_lines/DetectedLaserLines.h"
#include "youbot_scanner_lines/ScannerLinesFilterConfig.h"

namespace youbot_scanner_lines_filter {
	
	/*struct LineInformation {
	    float pointX;
	    float pointY;
	    float pointZ;
	    float directionX;
	    float directionY;
	    float directionZ;
	    int pointCount;
    };*/
	
	class YoubotScannerLinesFilter {
	public:
		YoubotScannerLinesFilter();
		void cb_scannerLine(const youbot_scanner_lines::DetectedLaserLines::ConstPtr& lines);
	private:
		ros::NodeHandle nh;
		tf::TransformListener tfListener;
		ros::Subscriber sub_lines;
		ros::Publisher pub_line;
		ros::Publisher pub_marker;
		std::deque<youbot_scanner_lines::DetectedLaserLine> merged_lines;
		int deque_size;
		dynamic_reconfigure::Server<youbot_scanner_lines::ScannerLinesFilterConfig> dsrv;
		
		void add_line(const youbot_scanner_lines::DetectedLaserLine line);
		youbot_scanner_lines::DetectedLaserLine merge_lines();
		void publish_line_marker(const youbot_scanner_lines::DetectedLaserLine& line);
		void cb_reconfigure(youbot_scanner_lines::ScannerLinesFilterConfig &config, uint32_t level);
	};
	
	YoubotScannerLinesFilter::YoubotScannerLinesFilter() {
		sub_lines = nh.subscribe<youbot_scanner_lines::DetectedLaserLines>("/detected_laser_lines", 100, &YoubotScannerLinesFilter::cb_scannerLine, this);
	    pub_line = nh.advertise<youbot_scanner_lines::DetectedLaserLine>("detected_best_laser_line_filtered", 0);
	    pub_marker = nh.advertise<visualization_msgs::Marker>("scanner_lines_marker_best_filtered", 0);
	    tfListener.setExtrapolationLimit(ros::Duration(3.0));
	    nh.setParam("/scanner_lines_filter_dequeSize", 10);
	    
	    dynamic_reconfigure::Server<youbot_scanner_lines::ScannerLinesFilterConfig>::CallbackType cb;
	    cb = boost::bind(&youbot_scanner_lines_filter::YoubotScannerLinesFilter::cb_reconfigure, this, _1, _2);
	    dsrv.setCallback(cb);
    }
    
    void YoubotScannerLinesFilter::cb_reconfigure(youbot_scanner_lines::ScannerLinesFilterConfig &config, uint32_t level) {
	    nh.setParam("/scanner_lines_filter_dequeSize", config.scanner_lines_filter_dequeSize);
	}
    
    void YoubotScannerLinesFilter::add_line(const youbot_scanner_lines::DetectedLaserLine line) {
		nh.getParam("/scanner_lines_filter_dequeSize", deque_size);
		while (merged_lines.size() >= deque_size) {
			merged_lines.pop_front();
		}

		merged_lines.push_back(line);	
	}
	
	youbot_scanner_lines::DetectedLaserLine YoubotScannerLinesFilter::merge_lines() {
		youbot_scanner_lines::DetectedLaserLine merged_line;
		if (merged_lines.empty()) {
			return merged_line;
		}
		std::deque<youbot_scanner_lines::DetectedLaserLine>::iterator it = merged_lines.begin();
		std::deque<youbot_scanner_lines::DetectedLaserLine>::iterator ite = merged_lines.end();
		for(it, ite; it != ite; ++it) {
			merged_line.pointX += it->pointX;
			merged_line.pointY += it->pointY;
			merged_line.pointZ += it->pointZ;
			merged_line.directionX += it->directionX;
			merged_line.directionY += it->directionY;
			merged_line.directionZ += it->directionZ;
		}
		merged_line.pointX /= merged_lines.size();
		merged_line.pointY /= merged_lines.size();
		merged_line.pointZ /= merged_lines.size();
		merged_line.directionX /= merged_lines.size();
		merged_line.directionY /= merged_lines.size();
		merged_line.directionZ /= merged_lines.size();
		return merged_line;
	}
	
	void YoubotScannerLinesFilter::publish_line_marker(const youbot_scanner_lines::DetectedLaserLine& line) {
		tf::Vector3 axis_vector(line.directionX, line.directionY, line.directionZ);
		tf::Vector3 v2(1.0, 0.0, 0.0);
		tf::Vector3 right_vector = axis_vector.cross(v2);
		right_vector.normalized();
		tf::Quaternion q(right_vector, -1.0*acos(axis_vector.dot(v2)));
		q.normalize();
		geometry_msgs::Quaternion orientation;
		tf::quaternionTFToMsg(q, orientation);
		
		visualization_msgs::Marker marker_line;
		marker_line.header.frame_id = "/base_link";
		marker_line.header.stamp = ros::Time();
		marker_line.ns = "youbot_scanner_lines_filter";
		marker_line.id = 0;
		marker_line.type = visualization_msgs::Marker::ARROW;
		marker_line.action = visualization_msgs::Marker::ADD;
		marker_line.pose.position.x = line.pointX;
		marker_line.pose.position.y = line.pointY;
		marker_line.pose.position.z = line.pointZ;
		marker_line.scale.x = 1;
		marker_line.scale.y = 1;
		marker_line.scale.z = 1;
		marker_line.color.r = 0;
		marker_line.color.g = 1;
		marker_line.color.b = 0;
		marker_line.color.a = 1;
		marker_line.lifetime = ros::Duration(0.5);
		marker_line.pose.orientation = orientation;
		pub_marker.publish(marker_line);
	}

    
    void YoubotScannerLinesFilter::cb_scannerLine(const youbot_scanner_lines::DetectedLaserLines::ConstPtr& lines) {
		if (lines->detectedLines.size() == 0) {
			return;
		}
		add_line(lines->detectedLines[0]);
		youbot_scanner_lines::DetectedLaserLine merged_line = merge_lines();
		publish_line_marker(merged_line);
		pub_line.publish(merged_line);
	}
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "youbot_scanner_lines_filter");

    youbot_scanner_lines_filter::YoubotScannerLinesFilter fscanlines;

    ros::spin();
    return EXIT_SUCCESS;
}
