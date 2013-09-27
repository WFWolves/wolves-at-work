'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
from math import pi
from time import sleep
from youbot_conveyorbelt_ai.utils.global_data import global_data
class WaitForObject(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'failed'],
                             input_keys=[])
    def execute(self, userdata):
        down = [2.9543960221061782, 2.063130213965643, -1.7388872417252186, 3.1911944192894293, 1.4021458986377486]
        global_data.ik.set_all_joint_offsets(down)
        counter = 0
        objects = []
        while global_data.detected_objects_counter != 10:
            objects = global_data.objects
            sleep(0.0)
        rospy.loginfo("objects: %s", objects)
        return 'done'
