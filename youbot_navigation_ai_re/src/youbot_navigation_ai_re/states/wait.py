import smach
import copy
import rospy
from ..utils.global_data import global_data

class wait(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['completed'],
                             input_keys=['sleeptime_in'])
        
    def execute(self, userdata):
        rospy.sleep(userdata.sleeptime_in)
        return 'completed'
