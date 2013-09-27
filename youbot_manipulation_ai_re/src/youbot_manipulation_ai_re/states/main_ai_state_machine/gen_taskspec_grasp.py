import smach
import copy
import rospy
from youbot_manipulation_ai_re.utils.task_specification_man import TaskSpecificationMan


class GenTaskspecGrasp(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['generated','failed'],
                             input_keys=['task_specification_in'],
                             output_keys=['task_spec_out'])
    def execute(self, userdata):
        try:
            service_area = userdata.task_specification_in.source
            objects = userdata.task_specification_in.objects
            spec = TaskSpecificationMan(service_area, objects)
            userdata.task_spec_out = spec
        except:
            return 'failed'
        return 'generated'
