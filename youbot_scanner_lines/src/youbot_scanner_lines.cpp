/*
 * youbot_scanner_lines.cpp
 *
 *  Created on: 29.09.2012
 *      Author: cpupower
 */


#include <vector>
#include <queue>
#include <ros/ros.h>
#include <ros/console.h>
#include <tf/transform_listener.h>
#include <laser_geometry/laser_geometry.h>
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/ros/conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/crop_box.h>
#include <pcl/io/pcd_io.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/sample_consensus/ransac.h>
#include <pcl/sample_consensus/sac_model_line.h>
#include <pcl/sample_consensus/sac_model_parallel_line.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <visualization_msgs/Marker.h>
#include <dynamic_reconfigure/server.h>

#include "youbot_scanner_lines/DetectedLaserLine.h"
#include "youbot_scanner_lines/DetectedLaserLines.h"
#include "youbot_scanner_lines/ScannerLinesConfig.h"

using namespace std;


namespace youbot_scanner_lines {
	class DetectedLaserLineComparator {
	public:
		bool operator() (DetectedLaserLine a, DetectedLaserLine b);
	};

    typedef pcl::PointCloud<pcl::PointXYZ> PointCloud;

    /*struct LineInformation {
	    float pointX;
	    float pointY;
	    float pointZ;
	    float directionX;
	    float directionY;
	    float directionZ;
	    int pointCount;
    };*/

    class YoubotScannerLines {
    public:
	    YoubotScannerLines();
	    void cb_laserscan(const sensor_msgs::LaserScan::ConstPtr& scan);
	    bool getPointCloudFromLaserScan(const sensor_msgs::LaserScan::ConstPtr& scan, sensor_msgs::PointCloud2& outCloud);
	    void publishVisualization(ros::Publisher pub_marker, std_msgs::Header header, vector<DetectedLaserLine> lineinfo, float r=1.0, float g=0.0, float b=0.0);
    private:
	    ros::NodeHandle nh;
	    laser_geometry::LaserProjection projector;
	    tf::TransformListener tfListener;
	    ros::Subscriber sub_scanner;
	    ros::Publisher pub_cloud;
	    ros::Publisher pub_cloud_best;
	    ros::Publisher pub_marker;
	    ros::Publisher pub_marker_best;
	    ros::Publisher pub_lines;
	    dynamic_reconfigure::Server<youbot_scanner_lines::ScannerLinesConfig> dsrv;
	    template<class Comparator, class Allocator>
	    void extractLines(PointCloud::Ptr pcloud, double cloudFraction, double sacDistance, std::priority_queue<DetectedLaserLine, Comparator, Allocator>& lineInfo);
	    void extractPointCloudByIndices(const PointCloud::ConstPtr input_cloud, const pcl::IndicesPtr& indices, PointCloud::Ptr out_cloud, bool negative=false);
	    void cb_reconfigure(youbot_scanner_lines::ScannerLinesConfig &config, uint32_t level);
    };

    bool DetectedLaserLineComparator::operator() (DetectedLaserLine a, DetectedLaserLine b) {
    	return a.pointCount < b.pointCount;
    }

    void YoubotScannerLines::extractPointCloudByIndices(const PointCloud::ConstPtr input_cloud, const pcl::IndicesPtr& indices, PointCloud::Ptr out_cloud, bool negative) {
        pcl::ExtractIndices<pcl::PointXYZ> extract;
	    extract.setInputCloud(input_cloud);
	    extract.setIndices(indices);
	    extract.setNegative(negative);
	    extract.filter(*out_cloud);
    }

    YoubotScannerLines::YoubotScannerLines() {
	    sub_scanner = nh.subscribe<sensor_msgs::LaserScan>("/base_scan", 100, &YoubotScannerLines::cb_laserscan, this);
	    tfListener.setExtrapolationLimit(ros::Duration(3.0));
	    pub_cloud = nh.advertise<sensor_msgs::PointCloud2>("scanner_lines_filtered_cloud", 100, false);
	    pub_cloud_best = nh.advertise<sensor_msgs::PointCloud2>("scanner_lines_best_cloud", 100, false);
	    pub_marker = nh.advertise<visualization_msgs::Marker>("scanner_lines_marker", 0);
	    pub_marker_best = nh.advertise<visualization_msgs::Marker>("scanner_lines_marker_best", 0);
	    pub_lines = nh.advertise<youbot_scanner_lines::DetectedLaserLines>("detected_laser_lines", 0);

	    dynamic_reconfigure::Server<youbot_scanner_lines::ScannerLinesConfig>::CallbackType cb;
	    cb = boost::bind(&youbot_scanner_lines::YoubotScannerLines::cb_reconfigure, this, _1, _2);
	    dsrv.setCallback(cb);
    }

    void YoubotScannerLines::cb_reconfigure(youbot_scanner_lines::ScannerLinesConfig &config, uint32_t level) {
    	nh.setParam("/scanner_lines_clusterMinSize", config.scanner_lines_clusterMinSize);
    	nh.setParam("/scanner_lines_clusterMaxSize", config.scanner_lines_clusterMaxSize);
    	nh.setParam("/scanner_lines_clusterTolerance", config.scanner_lines_clusterTolerance);
    	nh.setParam("/scanner_lines_clusterCloud", config.scanner_lines_clusterCloud);
	    nh.setParam("/scanner_lines_keepCloudFraction", config.scanner_lines_keepCloudFraction);
	    nh.setParam("/scanner_lines_cropMinX", config.scanner_lines_cropMinX);
	    nh.setParam("/scanner_lines_cropMinY", config.scanner_lines_cropMinY);
	    nh.setParam("/scanner_lines_cropMaxX", config.scanner_lines_cropMaxX);
	    nh.setParam("/scanner_lines_cropMaxY", config.scanner_lines_cropMaxY);
	    nh.setParam("/scanner_lines_sacModelDistance", config.scanner_lines_sacModelDistance);
	}

    bool YoubotScannerLines::getPointCloudFromLaserScan(const sensor_msgs::LaserScan::ConstPtr& scan, sensor_msgs::PointCloud2& outCloud) {
	    //tfListener.waitForTransform("/laser", "/base_link", ros::Time::now(), ros::Duration(10.0));
	    try {
	        projector.transformLaserScanToPointCloud("/base_link", *scan, outCloud, tfListener);
	        return true;
	    }
	    catch (tf::LookupException ex) {
	        ROS_WARN("LookupException");
	    }
	    catch (tf::ExtrapolationException ex) {
	        ROS_WARN("ExtrapolationException");
	    }
	    return false;
    }

    void YoubotScannerLines::publishVisualization(ros::Publisher pub_marker, std_msgs::Header header, vector<DetectedLaserLine> lineinfo, float r, float g, float b) {
	    static size_t maxmarkers = 0;
	    maxmarkers = max(maxmarkers, lineinfo.size());
	    /*for (size_t i = 0; i < maxmarkers; i++)
	    {
		    visualization_msgs::Marker marker_clear;
		    marker_clear.header.frame_id = "/base_link";
		    marker_clear.header.stamp = ros::Time::now();
		    marker_clear.ns = "youbot_scanner_lines";
		    marker_clear.id = i;
		    marker_clear.action = visualization_msgs::Marker::DELETE;
		    pub_marker.publish(marker_clear);
	    }*/
	    for (size_t i = 0; i < lineinfo.size(); i++) {
		    /*Eigen::Vector3f vec1(lineinfo[i].directionX, lineinfo[i].directionY, lineinfo[i].directionZ);
		    Eigen::Vector3f vec2(1.0, 0.5, 0.0);
		    Eigen::Quaternionf dirquat;
		    dirquat.setFromTwoVectors(vec1, vec2);*/
		    tf::Vector3 axis_vector(lineinfo[i].directionX, lineinfo[i].directionY, lineinfo[i].directionZ);
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
		    marker_line.ns = "youbot_scanner_lines";
		    marker_line.id = i;
		    marker_line.type = visualization_msgs::Marker::ARROW;
		    marker_line.action = visualization_msgs::Marker::ADD;
		    marker_line.pose.position.x = lineinfo[i].pointX;
		    marker_line.pose.position.y = lineinfo[i].pointY;
		    marker_line.pose.position.z = lineinfo[i].pointZ;
		    marker_line.scale.x = 1;
		    marker_line.scale.y = 1;
		    marker_line.scale.z = 1;
		    marker_line.color.r = r;
		    marker_line.color.g = g;
		    marker_line.color.b = b;
		    marker_line.color.a = 0.5;
		    marker_line.lifetime = ros::Duration(0.5);
		    marker_line.pose.orientation = orientation;
		    pub_marker.publish(marker_line);
	    }
    }

    template<class Comparator, class Allocator>
    void YoubotScannerLines::extractLines(PointCloud::Ptr pcloud, double cloudFraction, double sacDistance, std::priority_queue<DetectedLaserLine, Comparator, Allocator>& lineInfo) {
    	ROS_DEBUG("Cluster size: %lu", pcloud->size());
    	PointCloud::Ptr pcloud_tmp(new PointCloud);
    	int nr_points = (int) pcloud->points.size ();
    	while (pcloud->points.size () > cloudFraction * nr_points && nr_points > 2) {
			pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
			pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
			pcl::SACSegmentation<pcl::PointXYZ> seg;
			seg.setOptimizeCoefficients(true);
			seg.setModelType(pcl::SACMODEL_LINE);
			seg.setDistanceThreshold(sacDistance);
			seg.setInputCloud(pcloud);
			seg.segment(*inliers, *coefficients);
			if (coefficients->values.size() < 6) {
				break;
			}

			pcl::ExtractIndices<pcl::PointXYZ> extract;
			extract.setInputCloud(pcloud);
			extract.setIndices(inliers);
			extract.setNegative(false);
			extract.filter(*pcloud_tmp);

			DetectedLaserLine* linfo = new DetectedLaserLine;
			linfo->pointX = coefficients->values[0];
			linfo->pointY = coefficients->values[1];
			linfo->pointZ = coefficients->values[2];
			linfo->directionX = coefficients->values[3];
			linfo->directionY = coefficients->values[4];
			linfo->directionZ = coefficients->values[5];
			linfo->pointCount = inliers->indices.size();
			sensor_msgs::PointCloud2 tmpcloud_msg;
			pcl::toROSMsg(*pcloud_tmp, tmpcloud_msg);
			linfo->cloud = tmpcloud_msg;

			lineInfo.push(*linfo);

		   extract.setNegative(true);
		   extract.filter(*pcloud_tmp);
		   pcloud.swap(pcloud_tmp);
		   delete linfo;
		}
    }


    void YoubotScannerLines::cb_laserscan(const sensor_msgs::LaserScan::ConstPtr& scan) {
        double cropMinX, cropMinY;
        double cropMaxX, cropMaxY;
        double sacDistance;
        double cloudFraction;
        bool clusterCloud;
        int clusterMinSize, clusterMaxSize;
        double clusterTolerance;
        ros::param::param<bool>("/scanner_lines_clusterCloud", clusterCloud, false);
        ros::param::param<int>("/scanner_lines_clusterMinSize", clusterMinSize, 5);
        ros::param::param<int>("/scanner_lines_clusterMaxSize", clusterMaxSize, 25000);
        ros::param::param<double>("/scanner_lines_clusterTolerance", clusterTolerance, 0.10);
        ros::param::param<double>("/scanner_lines_keepCloudFraction", cloudFraction, 0.1);
        ros::param::param<double>("/scanner_lines_cropMinX", cropMinX, 0);
        ros::param::param<double>("/scanner_lines_cropMinY", cropMinY, -0.1);
        ros::param::param<double>("/scanner_lines_cropMaxX", cropMaxX, 0.5);
        ros::param::param<double>("/scanner_lines_cropMaxY", cropMaxY, 0.1);
        ros::param::param<double>("/scanner_lines_sacModelDistance", sacDistance, 0.01);
        ROS_DEBUG("SAC: %f", sacDistance);
	    sensor_msgs::PointCloud2 cloud_msg;
	    ROS_DEBUG("Scan recieved");
	    if (!getPointCloudFromLaserScan(scan, cloud_msg)) {
	        ROS_ERROR("Error transforming to point cloud.");
	        return;
	    }

	    PointCloud cloud;
	    pcl::fromROSMsg(cloud_msg, cloud);
	    PointCloud::ConstPtr pcloud = cloud.makeShared();

	    PointCloud::Ptr pcloud_filtered_crop (new PointCloud(cloud));

	    pcl::CropBox<pcl::PointXYZ> cropBoxFilter;
	    pcl::IndicesPtr crop_indices(boost::shared_ptr<std::vector<int> >(new std::vector<int>));
	    cropBoxFilter.setInputCloud(pcloud);
	    cropBoxFilter.setMin(Eigen::Vector4f(cropMinX,cropMinY,-0.03,0));
	    cropBoxFilter.setMax(Eigen::Vector4f(cropMaxX,cropMaxY,-0.03,0));
	    cropBoxFilter.filter(*crop_indices);
	    extractPointCloudByIndices(pcloud, crop_indices, pcloud_filtered_crop, true);


        PointCloud::Ptr pcloud_filtered (new PointCloud(*pcloud_filtered_crop));

	    PointCloud::Ptr pcloud_filtered_tmp (new PointCloud);

	    vector<DetectedLaserLine> lineInfo;
	    vector<pcl::PointIndices> cluster_indices;
	    priority_queue<DetectedLaserLine, vector<DetectedLaserLine>, youbot_scanner_lines::DetectedLaserLineComparator> lineInfoQueue;


	    if (clusterCloud) {
	        pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
            tree->setInputCloud (pcloud_filtered);

            pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
            ec.setClusterTolerance (clusterTolerance);
            ec.setMinClusterSize (clusterMinSize);
            ec.setMaxClusterSize (clusterMaxSize);
            ec.setSearchMethod (tree);
            ec.setInputCloud (pcloud_filtered);
            ec.extract (cluster_indices);
	    }

	    int nr_points = (int) pcloud_filtered->points.size ();
	    ROS_DEBUG("Number of points: %d", nr_points);

	    if (clusterCloud) {

			for (vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin (); it != cluster_indices.end (); ++it)
			{
				PointCloud::Ptr cloud_cluster(new PointCloud);
				pcl::copyPointCloud(*pcloud_filtered, it->indices, *cloud_cluster);
				extractLines(cloud_cluster, cloudFraction, sacDistance, lineInfoQueue);
			}
	    } else {
	    	extractLines(pcloud_filtered, cloudFraction, sacDistance, lineInfoQueue);
	    }

	    for (int i=0; lineInfoQueue.size() > 0; i++) {
	    	DetectedLaserLine linfo = lineInfoQueue.top();
	    	lineInfoQueue.pop();
	    	lineInfo.push_back(linfo);
	    	if (i==0) {
				publishVisualization(pub_marker_best, scan->header, lineInfo, 1.0, 0.0, 1.0);
				pub_cloud_best.publish(linfo.cloud);
	    	}

	    	ROS_DEBUG("Line %d - Point [%f, %f, %f]; Direction [%f, %f, %f]; PCount [%d]",
	    	    				        i,
	    	    				        linfo.pointX,
	    	    				        linfo.pointY,
	    	    				        linfo.pointZ,
	    	    				        linfo.directionX,
	    	    				        linfo.directionY,
	    	    				        linfo.directionZ,
	    	    				        linfo.pointCount);
	    }

	    publishVisualization(pub_marker, scan->header, lineInfo);
	    DetectedLaserLines detectedLines;
	    detectedLines.detectedLines = lineInfo;
	    pub_lines.publish(detectedLines);



	    //pcl::copyPointCloud(cloud, inliers->indices, filteredCloud);
	    sensor_msgs::PointCloud2 filteredCloud_msg;
	    pcl::toROSMsg(*pcloud_filtered_crop, filteredCloud_msg);
	    pub_cloud.publish(filteredCloud_msg);
    }
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "youbot_scanner_lines");

    youbot_scanner_lines::YoubotScannerLines yscanlines;
    ros::spin();
    return EXIT_SUCCESS;
}
