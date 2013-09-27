'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
import math
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data
class selecting(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Object selected', 'Object lost'],
                             input_keys=['camera_in'],
                             output_keys=['selected_object_name_out'])
        
    def execute(self, userdata):
        c_height = userdata.camera_in['height']
        c_width = userdata.camera_in['width']
        obj = copy.deepcopy(global_data.objects)
        closest_obj_to_center = None
        for i in range(len(obj)):
            if closest_obj_to_center == None:
                closest_obj_to_center = obj[i]

            distx_o = c_height - obj[i].rrect.height
            disty_o = c_width - obj[i].rrect.width
            
            distx_co = c_height -  closest_obj_to_center.rrect.height
            disty_co = c_width -  closest_obj_to_center.rrect.width
        
            distance_o = math.sqrt(distx_o**2 + disty_o**2)
            distance_co = math.sqrt(distx_co**2 + disty_co**2)
            
            if distance_o < distance_co:
                closest_obj_to_center = obj[i]
	if closest_obj_to_center == None:
		return 'Object lost'
        userdata.selected_object_name_out = closest_obj_to_center.object_name
        return 'Object selected'
