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
from youbot_manipulation_ai_re.utils.object_data import object_data
from geometry_msgs.msg import Twist
class verify_object_position(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['vertical','horizontal', 'robot adjusted', 'object lost'],
                             input_keys=['selected_object_name_in',
                                         'camera_in',
                                         'object_orientation_in',
                                         'joint_position_in'],
                             output_keys=['object_data_out', 'joint_position_out', 'object_orientation_out'])
        self.__max_center_point_dist = 0.0
        self.__image_timeout = 0.0
        self.__object_orientation = ''
        self.__counter = 0
        self.__rOl = ''
        self.__wait_for_image_loop_rate = 0.0
    def execute(self, userdata):
        self.__max_center_point_dist = rospy.get_param('youbot_manipulation_ai_re/misc/max_center_point_dist')
        self.__image_timeout = rospy.get_param('youbot_manipulation_ai_re/misc/image_timeout')
        self.__wait_for_image_loop_rate = rospy.get_param('youbot_manipulation_ai_re/misc/wait_for_image_loop_rate')
        sleep(0.5)       
        c_height = userdata.camera_in['height']
        c_width = userdata.camera_in['width']
        self.__counter+= 1
        userdata.joint_position_out = copy.deepcopy(userdata.joint_position_in)
        self.__object_orientation = copy.deepcopy(userdata.object_orientation_in)
        t1 = rospy.Time.now().to_sec()
        obj = None
        r = rospy.Rate(2)
        while(1):
            obj = self.get_object(userdata.selected_object_name_in)
            t2 = rospy.Time.now().to_sec()
            if t2 - t1 > self.__image_timeout:
                return 'object lost'  
            if obj != None:
                break
            global_data.pubVel.publish(Twist())
            r.sleep()
            
        if obj != None:
            distance_to_center_x = obj.rrect.centerPoint.x - c_width/2
            distance_to_center_y = obj.rrect.centerPoint.y - c_height/2
            angle = obj.rrect.angle
            height = obj.rrect.height
            width = obj.rrect.width
            bwidth = obj.bbox.width
            bheight = obj.bbox.height
            rOl = ''
            if height >= width:
                self.__rOl = 'left'
            elif width > height:
                self.__rOl = 'right'
            if self.is_object_in_center(distance_to_center_x, distance_to_center_y, angle, bwidth, bheight):
                global_data.pubVel.publish(Twist())
                userdata.object_orientation_out = copy.deepcopy(self.__object_orientation)
                return 'robot adjusted'
            else:
                userdata.object_data_out = object_data(distance_to_center_x, distance_to_center_y, angle, height, width, self.__rOl)
                if self.is_object_horizontal(angle, height, width):
                    return 'horizontal'
                    
                return 'vertical'
        
    def get_object(self, obj_name):
        obj = None
        object_list = copy.deepcopy(global_data.objects)
        for i in range(len(object_list)):
            if object_list[i].object_name == obj_name:
                obj = object_list[i]
        return obj
    
    def is_object_horizontal(self, a, h, w):
        return ((a > -30.0 and h > w) or (a < -60.0 and w > h)) and self.__object_orientation == 'horizontal' and self.__counter > 40   
    
    def is_object_in_center(self, dx, dy, a, width, height):
	#abs(dy) < self.__max_center_point_dist and
	return abs(dx) < self.__max_center_point_dist and \
               abs(a) < self.__max_center_point_dist and height > width	\
               and (abs(a) > 85 or abs(a) < 5)	
