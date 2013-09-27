#!/usr/bin/env python
"""SmachGlobalData module for youbot_scanner_alignment
Manages Global variables for the whole state machine
@Author: Philipp Wentscher
"""
import roslib; roslib.load_manifest('youbot_scanner_alignment')
import rospy
import math
import numpy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from SmachGlobalData import SmachGlobalData
from visualization_msgs.msg import Marker

import scanner_alignment_states

DEBUG = True

class Utils:
    SPEED = 0.01
    BUFFERSIZE = 20
    WALL_MIN_DISTANCE = 1
    KALMAN_RANGE = 5
    
    FRONT = True
    SIDE = False
    
    DRIVE_LEFT = Twist(linear=Vector3(x = 0.0, y = SPEED , z = 0.0))
    DRIVE_RIGHT = Twist(linear=Vector3(x = 0.0, y = -SPEED , z = 0.0))
    DRIVE_FORWARD = Twist(linear=Vector3(x = SPEED, y = 0.0 , z = 0.0))
    DRIVE_BACKWARD = Twist(linear=Vector3(x = -SPEED, y = 0.0 , z = 0.0))
    TURN_LEFT = Twist(angular=Vector3(x = 0.0, y = -0.2 , z = 0.025))
    TURN_RIGHT = Twist(angular=Vector3(x = 0.0, y = 0.2 , z = -0.025))
    STOP = Twist(angular=Vector3(x = 0.0, y = 0.0 , z = 0.0), 
                 linear=Vector3(x = 0.0, y = 0.0 , z = 0.0))
    
    @classmethod
    def get_wall_angle(cls, msg_line):
        return numpy.arctan(msg_line.directionX/msg_line.directionY)
    
    @classmethod
    def angle_wall_robo(cls, cart_point_a, cart_point_b):
        vec_of_wall = numpy.array([cart_point_a[0]-cart_point_b[0], cart_point_a[1]-cart_point_b[1]])
        vec_of_y_axis = numpy.array([0, 1])
        cos_of_angle = numpy.dot(vec_of_wall,vec_of_y_axis)/numpy.linalg.norm(vec_of_wall)/numpy.linalg.norm(vec_of_y_axis)
        return numpy.arccos(cos_of_angle)
    
    @classmethod
    def publish_marker(cls, x_cord, y_cord, mid):
        new_marker = Marker(type = Marker.CUBE, action=Marker.ADD)
        new_marker.header.frame_id = "/base_laser_front_link"
        new_marker.header.stamp = rospy.Time.now()
        new_marker.ns = "basic_shapes"
        new_marker.id = mid
        new_marker.pose.position.x = x_cord
        new_marker.pose.position.y = y_cord
        new_marker.pose.position.z = 0.0
        #pointxyz
        new_marker.pose.orientation.x = 0
        new_marker.pose.orientation.y = 0
        new_marker.pose.orientation.z = 0.0
        new_marker.pose.orientation.w = 1
        new_marker.scale.x = 0.005
        new_marker.scale.y = 0.005
        new_marker.scale.z = 0.005
        if mid == 0:
            new_marker.color.r = 1
        elif mid == 5:
            new_marker.color.g = 1
        elif mid == 10:
            new_marker.color.b = 1
        
        new_marker.color.a = 1
        new_marker.text = "marker"
        
        new_marker.lifetime = rospy.Duration(1)
        SmachGlobalData.pub_marker.publish(new_marker)
    
    @classmethod
    def array_average_point(cls, cart_array):
        (average_x, average_y) = (0, 0)
        for i in range(len(cart_array)):
            # x:=[0]
            average_x += cart_array[i][0]
            # y:=[1]
            average_y += cart_array[i][1]
        if len(cart_array) > 0: #prevent division by zero
            return (average_x / len(cart_array), average_y / len(cart_array))
        else:
            return (0, 0)
        
    
    @classmethod
    def points_average(cls, mid_id, edge_id, msg_laser):
        if mid_id > edge_id: #swap
            mid_id ^=  edge_id
            edge_id ^= mid_id
            mid_id ^= edge_id
        point_distance = 0
        for i in range(mid_id, edge_id):
            point_distance += msg_laser.ranges[i]
        point_distance /=  edge_id - mid_id
        return point_distance
    
    @classmethod
    def get_cart_from_id(cls, polar_id, msg_laser):
        angle = msg_laser.angle_min + msg_laser.angle_increment * polar_id
        return (math.cos(angle) * msg_laser.ranges[polar_id], math.sin(angle) * msg_laser.ranges[polar_id])
    
    @classmethod
    def get_carts_in_range(cls, border_a, border_b, msg_laser, front_side):
        start_id = 0
        carts_in_range = []
        x_or_y = 1 if front_side else 0
        #if border_a >= 0:
        #    start_id = len(msg_laser.ranges)/2
        for i in range(start_id, len(msg_laser.ranges)):
            #if front_side == False:
            cart_coordinate = Utils.get_cart_from_id(i, msg_laser)
            if front_side == False and cart_coordinate[1] < 0.0 and DEBUG:
                pass
                #rospy.logdebug("x:=%s (>= border_b): %s :: (<= border_a:) %s :: cart_coordinate= %s", cart_coordinate[x_or_y], cart_coordinate[x_or_y] >= border_b, cart_coordinate[x_or_y] <= border_a, cart_coordinate)
            if cart_coordinate[x_or_y] >= border_b and cart_coordinate[x_or_y] <= border_a: #cart_coordinate[1] := y distance
                if front_side:
                    carts_in_range.append(cart_coordinate)
                else:
                    if cart_coordinate[1] > 0.0:
                        carts_in_range.append(cart_coordinate)
            #if cart_coordinate[x_or_y] >= border_a:
            #    break
        if front_side == False and DEBUG:
            Utils.publish_marker(carts_in_range[0][0],carts_in_range[0][1], 0)
            last_id = len(carts_in_range) -1
            Utils.publish_marker(carts_in_range[last_id][0],carts_in_range[last_id][1], 5)
            rospy.logdebug("border_a= %f, border_b= %f, front_side= %s,x_or_y = %i",border_a, border_b, front_side, x_or_y)
            rospy.logdebug("carts_in_range= %s", carts_in_range)
        return carts_in_range
    
    """Changed the
    """
    @classmethod
    def __laser_kalman_index_filter(cls, index, kal_range, array_len):
        dif = index + kal_range/2 - array_len
        dif = dif if dif < 0 else 0
        index = index + dif
        dif = index - kal_range/2
        dif = abs(dif) if dif < 0 else 0
        index = index + dif
    
    @classmethod
    def __laser_kalman_norm(cls, msgs_array, index, kal_range):
        if len(msgs_array) <= kal_range:
            return
        Utils.__laser_kalman_index_filter(index, kal_range, len(msgs_array))
        average_slope = index - kal_range/2
        average_distance = 0
        for i in range(kal_range-1):
            if i != kal_range/2:
                average_slope +=msgs_range[i + index - kal_range/2] - msgs_range[i + index - kal_range/2 + 1]
                average_slope = average/2
                average_distance += msgs_range[i + index - kal_range/2]
        average_distance = average_distance / kal_range-1
        dif = abs(msgs_range[i] - average_distance)
        return average_distance if dif > average_slope else msgs_range[i]
        
    
    @classmethod
    def laser_kalman(cls, msg_laser):
        for i in range(len(msg_laser.ranges)):
            msg_laser.ranges[i] = __laser_kalman_index_filter(msg_laser.ranges, i, KALMAN_RANGE)
    
    @classmethod
    def laser_average(cls):
        print "Buffer:", len(SmachGlobalData.msgs_laser)
        result_laser = SmachGlobalData.msgs_laser[0]
        result_laser.ranges = list(result_laser.ranges)
        if len(SmachGlobalData.msgs_laser) > 1:
            for i in range(len(SmachGlobalData.msgs_laser[0].ranges)):
                for j in range(1, len(SmachGlobalData.msgs_laser)):
                    result_laser.ranges[i] += SmachGlobalData.msgs_laser[j].ranges[i]
                result_laser.ranges[i] = result_laser.ranges[i]/len(SmachGlobalData.msgs_laser)
        #Utils.laser_kalman(result_laser)
        if DEBUG :
            SmachGlobalData.pub_laser.publish(result_laser)
        return result_laser
    
    @classmethod
    def drive(cls, msg_twist):
        SmachGlobalData.pub_cmdvel.publish(msg_twist)
    
    @classmethod
    def lines_callback(cls, msg_line):
        if not SmachGlobalData.first_line:
            SmachGlobalData.first_line = True
        SmachGlobalData.msg_line = msg_line
        
    
    @classmethod
    def laser_callback(cls, msg_scan):
        if not SmachGlobalData.first_scan: 
            SmachGlobalData.first_scan = True
            SmachGlobalData.msgs_laser = []
        if len(SmachGlobalData.msgs_laser)  == Utils.BUFFERSIZE:
            SmachGlobalData.msgs_laser = SmachGlobalData.msgs_laser[1:] + [msg_scan]
        else:
            SmachGlobalData.msgs_laser.append(msg_scan)
        SmachGlobalData.laser_count += 1
        #Commented to reduse cpu load; princpe is just in time cumputation
        #SmachGlobalData.msg_laser = Utils.laser_average()
        
    @classmethod
    def marker_callback(cls, msg_marker):
        if (msg_marker.type == Marker.ARROW and msg_marker.pose.position.y >= self.WALL_MIN_DISTANCE):
            SmachGlobalData.msg_marker_arrow = msg_marker
