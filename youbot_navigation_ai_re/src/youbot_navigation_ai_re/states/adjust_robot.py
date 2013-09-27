import smach
import copy
import rospy
from ..utils.global_data import global_data

class adjust_robot(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['robot adjusted',],
                             input_keys=['orientation_in', 'task_specification_in'])
        
    def execute(self, userdata):
        return 'robot adjusted'
