'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: This States initializes the Vision.
'''
import rospy
import smach
import copy
import time
import math
from youbot_manipulation_ai_re.utils.global_data import global_data
from youbot_manipulation_ai_re.utils.task_specification import task_specification
from youbot_manipulation_vision import msg
from youbot_ik_solution_Modifier import youbot_ik_solution_modifier
from geometry_msgs.msg import Twist

class init_vision(smach.State):
    
    def __init__(self):
        smach.State.__init__(self, outcomes=['vision initialized'],
                          io_keys=['task_spec_io'],
                          output_keys=['camera_out'])
        self.__task_spec = None
        self.__last_objects = []
        self.__pt_dist_threshold = 30
    def execute(self, userdata):
        c_height = rospy.get_param('youbot_manipulation_ai_re/camera/height')
        c_width = rospy.get_param('youbot_manipulation_ai_re/camera/width')
        userdata.camera_out = {'height': c_height,
                            'width': c_width}
        self.__task_spec = userdata.task_spec_io
        global_data.subImage = rospy.Subscriber('/vision_objects', msg.DetectedObjects, self.object_callback)
        time.sleep(1)
        r = rospy.Rate(4)
        #         while(1):
        #             r.sleep()
        #             if len(global_data.objects) != 0:
        #                 break
        return 'vision initialized'
    def pointDist(self, point1, point2):
        return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)
    def isSimilarObject(self, object1, object2):
        ptDist = self.pointDist(object1.rrect.centerPoint, object2.rrect.centerPoint)
        if ptDist < self.__pt_dist_threshold:
            return True
        else:
            return False
    def getLastObjectMatch(self, obj):
        for last_obj in self.__last_objects:
            if self.isSimilarObject(obj, last_obj):
                return last_obj
        return None
    def object_callback(self, data):
        detectedObjects= []
        objectList = copy.deepcopy(data.objects)
        global_data.allObjects = copy.deepcopy(objectList)
        for i in range(len(objectList)):
            #if objectList[i].object_name == "???":
            #    lastMatch = self.getLastObjectMatch(objectList[i])
            #    if lastMatch is not None:
            #        objectList[i].object_name = lastMatch.object_name
            if self.__task_spec.translate_object_names(objectList[i].object_name) in self.__task_spec.get_objects():
                detectedObjects.append(objectList[i])
        global_data.objects = copy.deepcopy(detectedObjects)
        self.__last_objects = copy.deepcopy(detectedObjects)
