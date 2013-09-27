'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
import rospy
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data
from geometry_msgs.msg import Twist

class move_robot_vert(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'],
                             input_keys=['object_data_in'],
                             io_keys=['joint_position_io'])
        self.__max_center_point_dist = 0.0
        self.__arm_step_range = 0.0
        self.__base_step_range = 0.0
        self.__angle_step_range = 0.0

    def execute(self, userdata):
        self.__arm_step_range = rospy.get_param('youbot_manipulation_ai_re/misc/arm_step_range')
        self.__base_step_range = rospy.get_param('youbot_manipulation_ai_re/misc/base_step_range')
        self.__angle_step_range = rospy.get_param('youbot_manipulation_ai_re/misc/angle_step_range')
        self.__max_center_point_dist = rospy.get_param('youbot_manipulation_ai_re/misc/max_center_point_dist')
        
        msg_joint = copy.deepcopy(userdata.joint_position_io)
        dx = userdata.object_data_in.distance_to_center_x
        dy = userdata.object_data_in.distance_to_center_y
        a = userdata.object_data_in.angle
        height = userdata.object_data_in.height
        width = userdata.object_data_in.width
        msg_vel = Twist()
        msg_vel.linear.y = 0
        if dy > 0 and abs(dy) > self.__max_center_point_dist:
            msg_joint["x"] -= self.__arm_step_range
                
        if dy < 0 and abs(dy) > self.__max_center_point_dist:
            msg_joint["x"] += self.__arm_step_range

        if dx > 0 and abs(dx) > self.__max_center_point_dist:
            msg_vel.linear.y  = -self.__base_step_range
            
        if dx < 0 and abs(dx) > self.__max_center_point_dist:
            msg_vel.linear.y  = self.__base_step_range
        
        if a > -89.9 and height > width:
            global_data.ik.add_joint_offset(4, self.__angle_step_range)
            
        if a < -0.0 and width > height:
            global_data.ik.add_joint_offset(4, -self.__angle_step_range)
            
        global_data.ik.change_pos(msg_joint)
        if msg_vel.linear.y != 0:
            global_data.pubVel.publish(msg_vel)
            sleep(0.5)
            global_data.pubVel.publish(Twist())
            global_data.pubVel.publish(Twist())
            global_data.pubVel.publish(Twist())
        userdata.joint_position_io = copy.deepcopy(msg_joint)
        return 'done'
