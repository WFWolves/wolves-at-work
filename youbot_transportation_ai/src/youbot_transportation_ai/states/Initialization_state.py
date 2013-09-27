# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:32:22 2013

@author: jens
"""

import smach
import rospy
from youbot_manipulation_ai_re.utils.service_area import service_area

#FIXME ROS Const Hack
def const_hack(obj):
    while type(obj) == smach.user_data.Const:
        obj = obj._obj
    return obj

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['initialized'],
                             input_keys=['task_spec_in'],
                             output_keys=['service_areas_out', 'task_spec_out'])
                             
    def execute(self, userdata):
        userdata.task_spec_out = const_hack(userdata.task_spec_in)
        userdata.service_areas_out = self.get_service_areas()
        return 'initialized'
    def validate_service_areas(self, service_area_result):
        assert len(service_area_result) > 0
        for area in service_area_result:
            assert area.name is not None
            assert len(area.name) > 0
            assert area.height is not None
            assert area.x_pos is not None
            assert area.y_pos is not None
            assert area.orientation is not None
            assert isinstance(area.orientation,str)
            assert len(area.orientation) > 0
            assert area.left_point is not None
            assert area.right_point is not None
            assert area.left_point != area.right_point
        
    def get_service_areas(self):
         result = []
         s_count = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area_count')
         for i in range(1,s_count+1):
             try:
                 n = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/name')
                 h = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/height')
                 x_pos = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/xpos')
                 y_pos = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/ypos') 
                 o = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/orientation')
                 lpx = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/lPointX')
                 lpy = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/lPointY')
                 rpx = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/rPointX')
                 rpy = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/rPointY')
                 s = service_area(n, h, x_pos, y_pos,(lpx, lpy), (rpx, rpy), o)
                 print o
                 result.append(s)
             except Exception as ex:
                 rospy.logerr("Exception occured while parsing service_areas from rosparam: %s", str(ex))
                 break
         self.validate_service_areas(result)
         return result
