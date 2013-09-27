'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
import copy
import actionlib
from copy import deepcopy
from time import sleep
import move_base_msgs
import move_base_msgs.msg
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from youbot_conveyorbelt_ai.utils.global_data import global_data
from youbot_manipulation_vision.msg import DetectedObjects
from youbot_ik_solution_Modifier import youbot_ik_solution_modifier

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'failed'],
                             input_keys=[])
        self.__leftBorder = rospy.get_param('/youbot_manipulation_ai/misc/leftImageBorder')
        self.__rightBorder = rospy.get_param('/youbot_manipulation_ai/misc/rightImageBorder')
    def execute(self, userdata):
        global_data.sub_image = rospy.Subscriber('/vision_objects', DetectedObjects, self.object_callback)
        global_data.move_base_client = actionlib.SimpleActionClient('move_base', move_base_msgs.msg.MoveBaseAction)
        global_data.pub_vel = rospy.Publisher('/cmd_vel', Twist)
        global_data.ik = youbot_ik_solution_modifier()
        global_data.detected_objects_counter = 0
        sleep(2)
        global_data.ik.open_gripper()
        global_data.ik.open_gripper()
        global_data.ik.open_gripper()
        return 'done'

    def object_callback(self, data):
        global_data.detected_objects_counter +=1
        objects = copy.deepcopy(data.objects)
        result = []
        for obj in objects:
            if obj.rrect.centerPoint.x > self.__leftBorder and obj.rrect.centerPoint.x < self.__rightBorder:
                result.append(obj)
        global_data.objects = deepcopy(result)
