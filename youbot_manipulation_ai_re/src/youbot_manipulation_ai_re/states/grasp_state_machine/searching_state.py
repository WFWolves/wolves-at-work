'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: If no Object was detected, this state looks for Objects on the Service Area.
'''
import smach
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data
class searching(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['object found', 'no object found'],
                             input_keys=['joint_position_in'])
        
    def execute(self, userdata):
        global_data.ik.set_joint_offset(4,0.0)
        global_data.ik.change_pos(userdata.joint_position_in)
        if len(global_data.objects) != 0:
            return 'object found'
        return 'no object found'
