#!/usr/bin/env python

import roslib; roslib.load_manifest('youbot_scanner_alignment')
import rospy
import actionlib
from youbot_scanner_alignment.msg import *
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

if __name__ == '__main__':
    rospy.init_node('align_client')
    client = actionlib.SimpleActionClient('aligned_driving', AlignedDrivingAction)
    print "connected"
    client.wait_for_server()
    print "waiting for server"
    
    goal = AlignedDrivingGoal()
    goal.front_distance = 0.02
    goal.side_difference = 0
    
    client.send_goal(goal)
    print "goal sent"
    client.wait_for_result(rospy.Duration.from_sec(0.0))
    print goal
