'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
import rospy
import math
import tf
from time import sleep
from math import sin
from math import cos
from math import pi
from tf.transformations import euler_from_quaternion
from youbot_manipulation_ai_re.utils.global_data import global_data
from tarfile import calc_chksums
from geometry_msgs.msg import Twist

class grasp_object(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Object grasped'],
                             input_keys=['joint_position_in', 'selected_object_name_in',
                                         'service_areas_in', 'overview_position_in',
                                         'camera_params_in',
                                         'object_orientation_in'],
                             output_keys=['joint_position_out', 'selected_object_name_out'],
                             io_keys=['object_lengths_io', 'task_spec_io'])
        self.__offset = 0.0
        self.__tf_listener = tf.TransformListener()
    def execute(self, userdata):
        self.threshold = 10.0
        self.__object_orientation = copy.deepcopy(userdata.object_orientation_in)
        self.__camera_params = copy.deepcopy(userdata.camera_params_in)
        self.__offset = rospy.get_param('youbot_manipulation_ai_re/misc/angle_offset')
        self.__adjust_arm_threshold = rospy.get_param('youbot_manipulation_ai_re/misc/adjust_arm_threshold')
        self.__image_timeout = rospy.get_param('youbot_manipulation_ai_re/misc/image_timeout')
        self.__wait_for_image_loop_rate = rospy.get_param('youbot_manipulation_ai_re/misc/wait_for_image_loop_rate')
        msg_joint = copy.deepcopy(userdata.joint_position_in)
        userdata.selected_object_name_out = copy.deepcopy(userdata.selected_object_name_in)        
        current_tf = None
        while current_tf == None:
    	    try:
            	current_tf = self.__tf_listener.lookupTransform('/arm_link_0', '/arm_link_4', rospy.Time(0))
            	euler_current = euler_from_quaternion(current_tf[1])
            	print euler_current
    	    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        	    rospy.logerr("grasp_object_state: Failed to look up transform")
        	    
        euler_current = euler_from_quaternion(current_tf[1])
        pitch = euler_current[1]
        ak = msg_joint['z'] - 0.06 #0.045
        hyp = ak/cos(euler_current[1])
        gk = sin(euler_current[1]) * hyp
        dest = copy.deepcopy(msg_joint)
        dest['x'] = msg_joint['x'] + gk
#        global_data.ik.change_pos(dest)
#        sleep(2)
        dest['z'] = msg_joint['z'] - ak
        msg_joint['x'] += gk
        while msg_joint['z'] > 0.055:
            msg_joint['z'] -= 0.01
            global_data.ik.change_pos(msg_joint)
            sleep(1)
            msg_joint = self.align_robot(msg_joint)
            
        #global_data.ik.change_pos(dest)
        sleep(2)
        global_data.ik.close_gripper()
        sleep(2)
        global_data.ik.drive_to_back()
        sleep(2)
        global_data.ik.set_joint_offset(4, 0.00)
        return 'Object grasped'
    
    def align_robot(self, msg_joint):
        while 1:
            current_object = self.get_object()
            angle = current_object.rrect.angle
            height = current_object.rrect.height
            width = current_object.rrect.width
            self.threshold += 2.0
            print self.threshold
            if abs(self.calc_distance(current_object)[0]) > self.threshold:
                print abs(self.calc_distance(current_object)[0])
                if self.__object_orientation == 'horizontal': #self.is_object_horizontal(angle, height, width):
                    msg_joint = self.move_robot_hor(current_object, msg_joint)
                else:
                    self.move_robot_vert(current_object)
            else:
                return msg_joint
    
    def move_robot_vert(self, obj):
        msg_vel = Twist()
        if self.__camera_params['width'] / 2.0 - obj.rrect.centerPoint.x < 0.0:
            msg_vel.linear.y -= 0.02
        else:
            msg_vel.linear.y += 0.02
        global_data.pubVel.publish(msg_vel)
        sleep(1)
        global_data.pubVel.publish(Twist())
     
    def calc_threshold(self, diff):
        return 
        
    def move_robot_hor(self, obj, msg_joint):
        if self.__camera_params['width'] / 2.0 - obj.rrect.centerPoint.x < 0.0:
            msg_joint['x'] += 0.003
        else:
            msg_joint['x'] -= 0.003
        global_data.ik.change_pos(msg_joint)
        sleep(1)
        return msg_joint
        
    def calc_distance(self, obj):
        return (self.__camera_params['width'] / 2.0 - obj.rrect.centerPoint.x, \
                         self.__camera_params['height'] / 2.0 - obj.rrect.centerPoint.y)
        
    def calc_distance_to_center(self, obj):
        print 'Camera Parameter: %s' %self.__camera_params
        return math.sqrt((self.__camera_params['width'] / 2.0 - obj.rrect.centerPoint.x)**2 + \
                         (self.__camera_params['height'] / 2.0 - obj.rrect.centerPoint.y)**2)
    
    def get_object(self):
        nearest_object = None
        for obj in global_data.allObjects:
           print 'Distanz: %s' %self.calc_distance_to_center(obj)
           if nearest_object != None:
              print 'Naechstes Objekt: %s' %self.calc_distance_to_center(nearest_object)
           print 'Objekt: %s' %self.calc_distance_to_center(obj)
           if nearest_object == None or self.calc_distance_to_center(obj) <= self.calc_distance_to_center(nearest_object):
                 nearest_object = obj
                 print 'Mittelpunkt: %s' %obj.rrect.centerPoint
        return nearest_object
 
    def is_object_horizontal(self, a, h, w):
        return ((a > -30.0 and h > w) or (a < -60.0 and w > h)) and self.__object_orientation == 'horizontal' and self.__counter > 40   
              
    def get_service_area_height(self, service_areas, task_spec_in):
        for i in range(len(service_areas)):
            if service_areas[i].name == task_spec_in.get_current_service_area():
                return service_areas[i].height
            
