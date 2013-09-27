# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:21:15 2013

@author: jens
"""

import smach
import rospy
from youbot_navigation_ai_re.utils.task_specification import * 
#TODO: Service Areas in Dict schreiben
class ConstructNavMsg(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['constructed'],
                             input_keys=['service_areas_in', 'destination_in'],
                             output_keys=['task_spec_nav_out'])
                             
    def execute(self, userdata):
        task_spec = task_specification_navigation()
        orientation = self.__get_service_area_orientation(userdata)
        assert orientation is not None
        target = navigation_target(userdata.destination_in, orientation, 0.0)
        task_spec.add_target(target)
        userdata.task_spec_nav_out = task_spec
        return 'constructed'
        
    def __get_service_area_orientation(self, userdata):
        rospy.loginfo("userdata.service_areas_in: %s", userdata.service_areas_in)
        rospy.loginfo("userdata.destinatioon_in: %s", userdata.destination_in)
        for service_area in userdata.service_areas_in:
            if service_area.name == userdata.destination_in:
                return service_area.orientation
