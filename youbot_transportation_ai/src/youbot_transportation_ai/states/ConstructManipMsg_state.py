# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:30:48 2013

@author: jens
"""


import smach
import copy
from youbot_manipulation_ai_re.utils.task_specification_man import TaskSpecificationMan
class ConstructManipMsg(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['constructed'],
                             input_keys=['task_spec_in', 'selected_src_in'],
                             output_keys=['task_specification_manip_out'])
                             
    def execute(self, userdata):
        service_area = userdata.selected_src_in
        objects = self.__get_objects(userdata)
        spec = TaskSpecificationMan(service_area, objects)
        userdata.task_specification_manip_out = spec
        return 'constructed'
        
    def __get_objects(self, userdata):
        task = copy.deepcopy(userdata.task_spec_in)
        for place in task.initialsituation.places:
            if place.name == userdata.selected_src_in:
                return place.objects
