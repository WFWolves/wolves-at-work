'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
from copy import deepcopy
import copy
from time import sleep
from youbot_conveyorbelt_ai.utils.global_data import global_data
class GraspObject(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'failed'])
        self.__threshold = 10.0
    def execute(self, userdata):
        object = self.selectObject()
        #self.moveArm(object.rrect.centerPoint, deepcopy(userdata.joint_position_in))
        self.graspObject()
        return 'done'
    
    def moveArm(self, centerPoint, joint_position):
        msg_joint = None
        if abs(centerPoint.x - 320) > self.__threshold:
            if centerPoint.x - 320 < 0.0:
                global_data.ik.change_pos(joint_position["y"])
            elif centerPoint.x -320 > 0.0:
                global_data.ik.change_pos()
                
    def selectObject(self):
        objects = deepcopy(global_data.objects)
        result = None
        for obj in objects:
            if result == None or (self.calcDistance(obj.rrect.centerPoint) < self.calcDistance(result.rrect.centerPoint)):
                result = deepcopy(obj)
        return result
    
    def graspObject(self):
        up = [2.9542953300339474, 1.9365904867936465, -1.6723168933956507, 3.206282913583431, 1.4021458986377486]
        sleep(3)
        global_data.ik.close_gripper()
        sleep(3)
        global_data.ik.set_all_joint_offsets(up)
        sleep(3)
        global_data.ik.drive_to_back()
