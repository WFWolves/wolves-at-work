'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
import copy
import rospy
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data
from geometry_msgs.msg import Twist
class verify_object_orientation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'object lost'],
                             input_keys=['selected_object_name_in', 'joint_position_in'],
                             output_keys=['object_orientation_out', 'joint_position_out'])
        self.__image_timeout = 0.0
        self.__wait_for_image_loop_rate = 0.0
    def execute(self, userdata):
        self.__image_timeout = rospy.get_param('youbot_manipulation_ai_re/misc/image_timeout')
        self.__wait_for_image_loop_rate = rospy.get_param('youbot_manipulation_ai_re/misc/wait_for_image_loop_rate')
        userdata.joint_position_out = copy.deepcopy(userdata.joint_position_in)

        t1 = rospy.Time.now().to_sec()
        obj = None
        r = rospy.Rate(self.__wait_for_image_loop_rate)
        while(1):
            obj = self.get_object(userdata.selected_object_name_in)
            t2 = rospy.Time.now().to_sec()
            if t2 - t1 > self.__image_timeout:
                return 'object lost'
            if obj != None:
                break
            global_data.pubVel.publish(Twist())
            r.sleep()
                
#        if obj.bbox.width > obj.bbox.height and abs(obj.rrect.angle) < 5.0:
#            global_data.ik.add_joint_offset(4, 0.6)     
#            sleep(2)
        userdata.object_orientation_out = self.orientation(obj)
        print '\n\n\n\n\n'+str(self.orientation(obj))
        return 'done'
    
    def get_object(self, obj_name):
        obj = None
        object_list = copy.deepcopy(global_data.objects)
        for i in range(len(object_list)):
            if object_list[i].object_name == obj_name:
                obj = object_list[i]
        return obj
    
    def orientation(self, obj):
        angle = obj.rrect.angle
        height = obj.bbox.height
        width = obj.bbox.width
        if (width > height) and (angle < -70 or angle > -20):
            return 'horizontal'
        else:
            return 'vertical' 
        #if (height > width and angle > -70.0) or (width > height and angle < -20.0):
        #    return 'vertical'
        #else:
        #    return 'horizontal'
