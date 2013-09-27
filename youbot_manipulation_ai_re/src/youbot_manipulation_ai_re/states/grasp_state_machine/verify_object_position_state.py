'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data
from geometry_msgs.msg import Twist
class verify_object_position(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['move robot', 'robot adjusted'],
                             input_keys=['selected_object_name_in',
                                         'camera_height_in', 'camera_width_in'],
                             output_keys=['object_data_out'])
        self.__tollerance = 2.0
        
    def execute(self, userdata):
        obj = None
        object_list = copy.deepcopy(global_data.objects)
        for i in range(len(global_data.objects)):
            if object_list[i].object_name == userdata.selected_object_name_in:
                obj = object_list[i]
        if obj != None:
            distance_to_center_x = obj.rrect.centerPoint.x - userdata.camera_width_in/2
            distance_to_center_y = obj.rrect.centerPoint.y - userdata.camera_height_in/2
            angel = obj.rrect.angle
            userdata.object_data_out = [distance_to_center_x, distance_to_center_y, angel]
            sleep(0.1)
            if self.is_object_in_center(distance_to_center_x, distance_to_center_y, angel, obj.rrect.width, obj.rrect.height):
                global_data.pubVel.publish(Twist())
                return 'robot adjusted'
            else:
                if obj.rrect.width > obj.rrect.height:
                    userdata.object_data_out = [distance_to_center_x, distance_to_center_y, angel, 1]
                else:
                    userdata.object_data_out = [distance_to_center_x, distance_to_center_y, angel, 0]
                return 'move robot'
        
    def is_object_in_center(self, dx, dy, a, width, height):
        return abs(dx) < self.__tollerance and \
               abs(dy) < self.__tollerance and \
               abs(a) < self.__tollerance and height > width
