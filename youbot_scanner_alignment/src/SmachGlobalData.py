#!/usr/bin/env python
"""SmachGlobalData module for youbot_scanner_alignment
Manages Global variables for the whole state machine
@Author: Philipp Wentscher
"""
import roslib; roslib.load_manifest('youbot_scanner_alignment')
import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from youbot_scanner_alignment.msg import *

class SmachGlobalData:
    """Shares data for the state machine. Use this class for threaded objects (e.g. publisher/subscriber)"""
    
    # pylint: disable=R0903
    def __init__(self):
        DRIVE_LEFT.linear
        pass
    
    pub_cmdvel = None
    pub_laser = None
    pub_marker = None
    sub_laser = None
    sub_marker = None
    sub_lines = None
    msgs_laser = None
    msg_laser = None
    msg_line = None
    #arrow_marker
    #msg_marker_arrow = None
    first_scan = False
    first_line = False
    laser_count = 0
    in_goal_tolerance = None
    in_goal_front_distance = None
    in_goal_side_difference = None
