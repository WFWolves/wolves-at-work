import smach
import copy
import rospy
from ..utils.global_data import global_data

class select_destination(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['selected','finished'],
                             io_keys=['task_specification_io'],
                             output_keys=['destination_out', 'orientation_out', 'sleeptime_out'])
        
    def execute(self, userdata):
        if len(userdata.task_specification_io.targets) > 0:
            target = userdata.task_specification_io.remove_target_at(0)
            userdata.destination_out = target.marker
            userdata.orientation_out = target.orientation
            userdata.sleeptime_out = target.sleeptime
            return 'selected'
        else:
            return 'finished'
