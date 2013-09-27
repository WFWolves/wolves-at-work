'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: This States initializes the Robot.
'''
import rospy
import smach
import copy
import time
from youbot_manipulation_ai_re.utils.global_data import global_data
from youbot_manipulation_ai_re.utils.service_area import service_area
from youbot_manipulation_vision import msg
from youbot_ik_solution_Modifier import youbot_ik_solution_modifier
from geometry_msgs.msg import Twist

#FIXME ROS Const Hack
def const_hack(obj):
    while type(obj) == smach.user_data.Const:
        obj = obj._obj
    return obj

class initialization(smach.State):
    
     def __init__(self):
         smach.State.__init__(self, outcomes=['initialized'],
                              output_keys=['service_areas_out',
                                           'joint_start_position_out',
                                           'object_lengths_out',
                                           'overview_position_out',
                                           'task_spec_out'],
                              input_keys=['task_spec_iin'])
         
     def execute(self, userdata):
         userdata.task_spec_out = const_hack(userdata.task_spec_iin)
         global_data.pubVel = rospy.Publisher('/cmd_vel', Twist)
         global_data.pubVel.publish(Twist())
         global_data.ik = youbot_ik_solution_modifier()
         time.sleep(2)
         global_data.ik.open_gripper() #test
         pos = self.get_joint_start_position()
         userdata.joint_start_position_out = pos
         global_data.ik.change_pos(pos)
         time.sleep(2)
         userdata.object_lengths_out = self.get_object_lengths()
         userdata.service_areas_out = self.get_service_areas()
         userdata.joint_start_position_out = pos
         userdata.overview_position_out = pos
         return 'initialized'
     
     def get_joint_start_position(self):
         x =  rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/x')
         y =  rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/y')
         z = rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/z')
         roll = rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/roll')
         pitch = rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/pitch')
         yaw = rospy.get_param('youbot_manipulation_ai_re/misc/joint_start_position/yaw')
         return {"x": x,
                 "y": y,
                 "z": z,
                 "roll": roll,
                 "pitch": pitch,
                 "yaw": yaw}         
     
     def get_object_lengths(self):
         result= {}
         for i in range(10):
             n = ''
             l = 0.0
             try:
                 n = rospy.get_param('youbot_manipulation_ai_re/objects/object'+str(i)+'/name')
                 l = rospy.get_param('youbot_manipulation_ai_re/objects/object'+str(i)+'/length')
                 result[n] = l
             except:
                 break
         return result

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
                 result.append(s)
             except:
                 break
         return result
