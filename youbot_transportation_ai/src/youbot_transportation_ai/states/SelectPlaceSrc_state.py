# -*- coding: utf-8 -*-
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import rospy
import copy
class SelectPlaceSrc(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['selected'],
                             input_keys=['task_spec_in'],
                             output_keys=['task_spec_out', 'selected_src_out'])
                             
    def execute(self, userdata):
        userdata.task_spec_out = copy.deepcopy(userdata.task_spec_in)
        places = userdata.task_spec_in.initialsituation.places
        for i in range(len(places)):
            if len(places[i].objects) > 0:
                userdata.selected_src_out = userdata.task_spec_in.initialsituation.places[i].name
                break
        return 'selected'
