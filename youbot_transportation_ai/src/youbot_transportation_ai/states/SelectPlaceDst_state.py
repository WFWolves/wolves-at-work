# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:33:20 2013

@author: jens
"""
import smach
import smach_ros
import copy
from youbot_manipulation_ai_re.utils.task_specification_man import TaskSpecificationMan
class SelectPlaceDst(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['selected'],
                             input_keys=['grasped_object_in', 'task_spec_trans_in'],
                             output_keys=['selected_service_area_out'])
                             
    def execute(self, userdata):
        service_area_name = self.__get_service_area(userdata)
        userdata.selected_service_area_out = service_area_name
        return 'selected'
    
    def __get_service_area(self, userdata):
        task = copy.deepcopy(userdata.task_spec_trans_in)
        name = copy.deepcopy(userdata.grasped_object_in)
        task_man = TaskSpecificationMan(None,None)
        for place in task.goalsituation.places:
            if task_man.translate_object_names(name) in place.objects:
                return place.name
            
