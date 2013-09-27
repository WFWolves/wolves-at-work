'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
from youbot_manipulation_ai_re.utils.global_data import global_data

class count_grasped_objects(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['One or more objects found',
                                             'No object found',
                                             'All objects grasped'],
                             input_keys=['counter_in', 'task_spec_in'])
        
    def execute(self, userdata):
        if userdata.counter_in == 3:
            return 'All objects grasped'
        if len(global_data.objects) > 0 and userdata.counter_in != 3:
            return 'One or more objects found'
        if len(global_data.objects) == 0:
            return 'No object found'
