#!/usr/bin/env python
"""Youbot scanner alignment states module
States for the scanner alignment statemachine.
@Author: Philip Wentscher
"""
import roslib; roslib.load_manifest('youbot_scanner_alignment')
import rospy
import smach
import smach_ros
import math
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from SmachGlobalData import SmachGlobalData
from scanner_alignment_utils import Utils
GOAL_TOLERANCE = 0.005
GOAL_ANGLE_TOLERANCE = 0.05
BOT_OFFSET = 0.33
TIME_TO_STOP = 0.2
#Borders:
LEFT_LEFT_BORDER = 0.22
LEFT_RIGHT_BORDER = 0.14
RIGHT_LEFT_BORDER = -0.14
RIGHT_RIGHT_BORDER = -0.22
SIDE_BACK_BORDER = -0.01
SIDE_FRONT_BORDER = 0.02
#Speed:
ROTATION_MAX = 1.0
DRIVING_MAX = 0.04
#Destination Distance
GOAL_FRONT_DISTANCE = 0.05
#DEBUG
DEBUG = True

class Localisation(smach.State):
    """Localisation state
    This state localised the youBot.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["aligned", "locate",
                                               "driveLeft", "driveRight",
                                               "driveForward", "driveBackward",
                                               "turnLeft", "turnRight"],
                             output_keys = ["out_drive_time", "out_turn_speed",
                                            "out_drive_speed"])
        self.rate = rospy.Rate(30)
        self.set_atribute_none()
        self.goal_tolerance = SmachGlobalData.goal_tolerance
        self.goal_front_distance = SmachGlobalData.goal_front_distance
        self.goal_side_difference = SmachGlobalData.goal_side_difference
        self.goal_side_distance = None
    
    def set_atribute_none(self):
        self.front_left_point = None
        self.front_right_point = None
        self.msg_laser = None
        SmachGlobalData.laser_count = 0
    
    def get_goal_side_distance(self):
        if self.goal_side_distance == None:
            
            side_point =  self.get_side_average_point(SIDE_FRONT_BORDER, SIDE_BACK_BORDER)
            side_distance = abs(side_point[1])
            if DEBUG:
                rospy.logdebug("side_distance= %s :: goal_side_difference= %s :: ++= %s", side_distance, self.goal_side_difference, (side_distance + self.goal_side_difference))
            self.goal_side_distance = side_distance + self.goal_side_difference
        return self.goal_side_distance
    
    def get_attribute_value(self, value, default_value):
        return default_value if value == None else value
    
    def get_msg_laser(self):
        if self.msg_laser == None:
            self.wait_for_laser_msgs(Utils.BUFFERSIZE)
            self.msg_laser = Utils.laser_average()
        return self.msg_laser
    
    def get_side_average_point(self, back_border, front_border):
        array = Utils.get_carts_in_range(back_border, front_border, self.get_msg_laser(), Utils.SIDE)
        if DEBUG:
            #rospy.logdebug("side_array: =%s", array)
            pass
        return Utils.array_average_point(array)
    
    def get_front_average_point(self, left_border, right_border):
        array = Utils.get_carts_in_range(left_border, right_border, self.get_msg_laser(), Utils.FRONT)
        return Utils.array_average_point(array)
    
    def get_front_left_point(self):
        if self.front_left_point == None:
            self.front_left_point = self.get_front_average_point(LEFT_LEFT_BORDER, LEFT_RIGHT_BORDER)
        return self.front_left_point
    
    def get_front_right_point(self):
        if self.front_right_point == None:
            self.front_right_point = self.get_front_average_point(RIGHT_LEFT_BORDER, RIGHT_RIGHT_BORDER)
        return self.front_right_point
    
    def get_x_dif_fl_fr(self):
        return self.get_front_left_point()[0] - self.get_front_right_point()[0]
    
    def get_x_dif_fl_fgd(self):
        return self.get_front_left_point()[0] - self.goal_front_distance
    
    def get_side_y_dif_ls_sgd(self):
        side_distance = abs(self.get_side_average_point(SIDE_FRONT_BORDER, SIDE_BACK_BORDER)[1])
        if DEBUG:
            rospy.logdebug("side_distance: %s | goal: %s || --:= %s", side_distance, self.get_goal_side_distance(), side_distance - self.get_goal_side_distance())
        return side_distance - self.get_goal_side_distance()
    
    def get_return_state(self, dif_angle_or_distance, lower_state, higher_state):
        return lower_state if (dif_angle_or_distance < 0) else higher_state
    
    def get_speed_and_time(self, dif_angle_or_distance, max_angle_or_distance):
        """Returns a tupel of: (result_state, result_speed, driving_time)
        """
        result_speed = 0.0
        result_time = 0.0
        if abs(dif_angle_or_distance) <= max_angle_or_distance:
            result_speed = abs(dif_angle_or_distance)
            result_time = self.norm_drive_time(1.0)
        else: 
            result_speed = max_angle_or_distance
            result_time = self.norm_drive_time(abs(dif_angle_or_distance) / max_angle_or_distance)
        # We work closed loop, so reduce time to sample again before reacing goal
        result_time /= 10;
        if DEBUG:
            rospy.logdebug("(dif_angle_or_distance= %f, max_angle_or_distance= %f)",dif_angle_or_distance, max_angle_or_distance)
            rospy.loginfo("(result_speed= %f, result_time= %f)",result_speed, result_time)
        return (result_speed, result_time)
    
    def get_turn_params(self):
        """Returns a tupel of: (rotation_state, rotation_speed, driving_time)
        """
        angle = Utils.get_wall_angle(SmachGlobalData.msg_line)
        #angle = math.copysign(angle, self.get_x_dif_fl_fr())
        (return_speed, return_time) = self.get_speed_and_time(angle, ROTATION_MAX)
        return_state = self.get_return_state(angle, "turnLeft", "turnRight")
        return (return_state, return_speed, return_time)
    
    def get_drive_front_params(self):
        """Returns a tupel of: (driving_state, driving_speed, driving_time)
        """
        x_dif = (SmachGlobalData.msg_line.pointX- BOT_OFFSET) - self.goal_tolerance
        return_state = self.get_return_state(x_dif, "driveBackward", "driveForward")
        (return_speed, return_time) = self.get_speed_and_time(x_dif, DRIVING_MAX)
        return (return_state, return_speed, return_time)
    
    def get_drive_side_params(self):
        """Returns a tupel of: (driving_state, driving_speed, driving_time)
        """
        if DEBUG:
            rospy.logdebug("++++++++++++self.goal_side_distance:= %s",self.goal_side_distance)
        
        return_state = self.get_return_state(self.get_side_y_dif_ls_sgd(), "driveRight", "driveLeft")
        (return_speed, return_time) = self.get_speed_and_time(self.get_side_y_dif_ls_sgd(), DRIVING_MAX)
        return (return_state, return_speed, return_time)
    
    def norm_drive_time(self, time):
        return max(time -TIME_TO_STOP, TIME_TO_STOP)
    
    def wait_for_laser_msgs(self, number_of_msgs):
        print "+++++++++Wait for msgs"
        while SmachGlobalData.laser_count <= number_of_msgs:
            self.rate.sleep()
        SmachGlobalData.laser_count = 0
    
    def is_located(self):
        result = self.is_not_collimated() == False
        result = result and self.is_not_in_front_distance() == False
        return result and self.is_not_in_side_distance() == False
    
    def is_not_collimated(self):
        angle = Utils.get_wall_angle(SmachGlobalData.msg_line)
        print "wall_angle", angle
        return abs(angle) > GOAL_ANGLE_TOLERANCE
        #return abs(self.get_x_dif_fl_fr()) > self.goal_tolerance
    
    def is_not_in_front_distance(self):
        rospy.loginfo("x:%f, dif:%f", (SmachGlobalData.msg_line.pointX- BOT_OFFSET), ((SmachGlobalData.msg_line.pointX- BOT_OFFSET)- self.goal_front_distance))
        return ((SmachGlobalData.msg_line.pointX- BOT_OFFSET)- self.goal_front_distance)> self.goal_tolerance
        #return self.get_x_dif_fl_fgd() > self.goal_tolerance
    
    def is_not_in_side_distance(self):
         dif = abs(self.get_side_y_dif_ls_sgd())
         if DEBUG:
            rospy.logdebug("dif: %s :: goal_tolerance: %s ## %s", dif, self.goal_tolerance, dif > self.goal_tolerance)
         return dif > self.goal_tolerance
    
    def execute(self, userdata):
        """localeState
        Deciding where and how to move next
        """
        userdata.out_drive_time = None
        userdata.out_turn_speed = None
        userdata.out_drive_speed = None
        return_state = "locate"
        
        if self.is_located():
            pass
            return_state = "aligned"
        elif self.is_not_collimated():
            pass
            print "turn"
            (return_state, userdata.out_turn_speed, userdata.out_drive_time) = self.get_turn_params()
        elif self.is_not_in_front_distance():
            pass
            print "forward"
            (return_state, userdata.out_drive_speed, userdata.out_drive_time) = self.get_drive_front_params()
        elif self.is_not_in_side_distance():
            pass
            #(return_state, userdata.out_drive_speed, userdata.out_drive_time) = self.get_drive_side_params()
        #angle = Utils.angle_wall_robo(self.get_front_left_point(), self.get_front_right_point())
        #rospy.logdebug("Angle: %f", angle)
        
        self.set_atribute_none()
        return return_state

class DriveLeft(smach.State):
    """DriveLeftstate
    This state drives the youBot to the left side.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """DriveLeft state
        Driving to the left for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(linear=Vector3(x = 0.0, y = userdata.in_drive_speed , z = 0.0)))
        print "###Driving for:", userdata.in_drive_time
        print "###Driving with:", userdata.in_turn_speed
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state

class DriveRight(smach.State):
    """DriveRight state
    This state drives the youBot to the right side.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """DriveRight state
        Driving to the right for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(linear=Vector3(x = 0.0, y = -userdata.in_drive_speed , z = 0.0)))
        print "###Driving for:", userdata.in_drive_time
        print "###Driving with:", userdata.in_turn_speed
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state

class DriveForward(smach.State):
    """DriveForward state
    This state drives the youBot forward.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """DriveForward state
        Driving forwards for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(linear=Vector3(x = userdata.in_drive_speed, y = 0.0 , z = 0.0)))
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state
    
class DriveBackward(smach.State):
    """DriveBackward state
    This state drives the youBot backwards.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """DriveBackward state
        Driving backwards for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(linear=Vector3(x = -userdata.in_drive_speed, y = 0.0 , z = 0.0)))
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state
    
class TurnLeft(smach.State):
    """TurnLeft state
    This state turns the youBot to the right.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """TurnLeft state
        Turning to the left for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(angular=Vector3(x = 0.0, y = 0.0 , z = userdata.in_turn_speed)))
        #Utils.drive(Utils.TURN_LEFT)
        print "###Driving for:", userdata.in_drive_time
        print "###Driving with:", userdata.in_turn_speed
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state

class TurnRight(smach.State):
    """TurnRight state
    This state drives the youBot backwards.
    """
    def __init__(self):
        smach.State.__init__(self, outcomes = ["locate"],
                             input_keys = ["in_drive_time", "in_drive_speed", "in_turn_speed"])
    
    def execute(self, userdata):
        """TurnRight state
        Turning to the right for a given time.
        """
        return_state = "locate"
        Utils.drive(Twist(angular=Vector3(x = 0.0, y = 0.0 , z = -userdata.in_turn_speed)))
        print "###Driving for:", userdata.in_drive_time
        print "###Driving with:", userdata.in_turn_speed
        rospy.sleep(userdata.in_drive_time)
        Utils.drive(Utils.STOP)
        return return_state
