# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:39:39 2013

@author: jens
"""

import smach
import rospy
import copy
from youbot_manipulation_ai_re.utils.task_specification_man import TaskSpecificationMan

#FIXME ROS Const Hack
def const_hack(obj):
    while type(obj) == smach.user_data.Const:
        obj = obj._obj
    return obj

class UpdateTaskSpec(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Object remaining', 'finished'],
                             input_keys=['grasped_objects_in', 'task_spec_trans_in'],
                             io_keys=['task_spec_trans_io'])
                             
    def execute(self, userdata):
        task = const_hack(userdata.task_spec_trans_io)
        ts = TaskSpecificationMan('', [])
        name = ts.translate_object_names(userdata.grasped_objects_in)

        for place in task.initialsituation.places:
            print 'name in place.objects: %s in %s' % (name, place.objects)
            if name in place.objects:
                place.remove_object(name)
                print "Removed %s: %s" % (name, place.objects)
                break
        
        for place in task.goalsituation.places:
            print 'name in place.objects: %s in %s' % (name, place.objects)
            if name in place.objects:
                place.remove_object(name)
                print "Removed %s: %s" % (name, place.objects)
                break
        
        for place in task.initialsituation.places:
            if len(place.objects) == 0:
                task.initialsituation.remove_place(place) 
                print "Removed %s: %s" % (place.name, place.objects)      
        
        for place in task.goalsituation.places:
            if len(place.objects) == 0:
                task.goalsituation.remove_place(place)  
                print "Removed %s: %s" % (place.name, place.objects)
                
        userdata.task_spec_trans_io = task
        if len(task.goalsituation.places) == 0:
            return 'finished'
        else:                
            return 'Object remaining'
