'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
from copy import deepcopy
from youbot_conveyorbelt_ai.utils.global_data import global_data
from geometry_msgs.msg import Twist
from math import sqrt

class AdjustRobotToObject(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'failed'],
                             input_keys=[])
    def execute(self, userdata):
        #selected_obj = self.selectObject()
        #self.move_base()
        return 'done'
    
    def selectObject(self):
        objects = deepcopy(global_data.objects)
        result = None
        for obj in objects:
            if result == None or (self.calcDistance(obj.rrect.centerPoint) < self.calcDistance(result.rrect.centerPoint)):
                result = deepcopy(obj)
        return result    
    
    def calcDistance(self, centerPoint):
        return sqrt(centerPoint.x**2 + centerPoint.y**2)
        
    def move_base(self):
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.04
        global_data.pub_vel.publish(cmd_vel)
        
        