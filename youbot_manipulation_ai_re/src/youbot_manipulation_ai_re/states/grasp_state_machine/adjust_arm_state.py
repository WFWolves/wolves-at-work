'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import time
import copy
import rospy
from time import sleep
from math import sin
from math import cos
from math import pi
from youbot_manipulation_ai_re.utils.global_data import global_data

class adjust_arm(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['arm adjusted', 'object lost'],
                             input_keys=['joint_position_in', 'selected_object_name_in',
                                         'camera_params_in'],
                             io_keys=['object_lengths_io'],
			     output_keys=['joint_position_out'])
        self.__offset = 0.0
        self.__adjust_arm_threshold = 0.0
        self.__image_timeout = 0.0
        self.__wait_for_image_loop_rate = 0.0
    def execute(self, userdata):
        self.__offset = rospy.get_param('youbot_manipulation_ai_re/misc/angle_offset')
        self.__adjust_arm_threshold = rospy.get_param('youbot_manipulation_ai_re/misc/adjust_arm_threshold')
        self.__image_timeout = rospy.get_param('youbot_manipulation_ai_re/misc/image_timeout')
        self.__wait_for_image_loop_rate = rospy.get_param('youbot_manipulation_ai_re/misc/wait_for_image_loop_rate')
        c_height = userdata.camera_params_in['height']
        msg_joint = copy.deepcopy(userdata.joint_position_in)
        
        while(1):
            t1 = rospy.Time.now().to_sec()
            obj = None
            r = rospy.Rate(self.__wait_for_image_loop_rate)
            while(1):
                obj = self.get_object(userdata.selected_object_name_in)
                t2 = rospy.Time.now().to_sec()
                if t2 - t1 > self.__image_timeout:
                    return 'object lost'  
                if obj != None:
                    break
                r.sleep()
            
            if abs(obj.rrect.centerPoint.y + obj.rrect.height/2.0 - c_height) < self.__adjust_arm_threshold:
                userdata.joint_position_out = copy.deepcopy(msg_joint)
                break
            time.sleep(0.5)
            angle = global_data.ik.get_joint_values()[4] - self.__offset
            #x = -0.001 * (cos(angle) - sin(angle))
            #y = -0.001 * (sin(angle) + cos(angle))
            x = 0.001 * cos(angle)
            y = 0.001 * sin(angle)
            msg_joint['x'] += x
            msg_joint['y'] += y
            global_data.ik.change_pos(msg_joint)
        return 'arm adjusted'
    
    def get_object(self, obj_name):
        obj = None
        object_list = copy.deepcopy(global_data.objects)
        for i in range(len(object_list)):
            if object_list[i].object_name == obj_name:
                obj = object_list[i]
        return obj
    
