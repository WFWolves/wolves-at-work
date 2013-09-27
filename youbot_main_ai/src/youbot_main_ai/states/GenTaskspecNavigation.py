import smach
import copy
import rospy
from youbot_navigation_ai_re.utils.task_specification import task_specification_navigation, navigation_target


class GenTaskspecNavigation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['generated','failed'],
                             input_keys=['marker_in', 'orientation_in'],
                             output_keys=['task_spec_out'])
    def execute(self, userdata):
        try:
            task_spec = task_specification_navigation()
            target = navigation_target(userdata.marker_in, userdata.orientation_in, 0.0)
            task_spec.add_target(target)
            userdata.task_spec_out = task_spec
        except:
            return 'failed'
        return 'generated'
