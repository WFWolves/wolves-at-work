'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import smach
import rospy
from time import sleep
import copy

from youbot_manipulation_ai_re.utils.global_data import global_data
from youbot_ik_solution_Modifier import youbot_ik_solution_modifier
from geometry_msgs.msg import Twist

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'],
                                   input_keys=['object_counter_in', 'alignment_in', 'service_area_name_in'],
                                   output_keys=['object_counter_out', 'alignment_out', 'service_area_height_out',
                                                'std_joint_position_out', 'zick_zack_out',
                                                'line_out', 'circle_out'])
        self.__service_area_names = {'S1': 'service_area1',
                                     'S2': 'service_area2',
                                     'S3': 'service_area3'}
    def execute(self, userdata):
        global_data.ik = youbot_ik_solution_modifier()
        global_data.pubVel = rospy.Publisher('/cmd_vel', Twist)
        userdata.object_counter_out = copy.deepcopy(userdata.object_counter_in)
        userdata.alignment_out = copy.deepcopy(userdata.alignment_in)
        userdata.service_area_height_out = self.__get_service_area_height(userdata.service_area_name_in)
        userdata.std_joint_position_out = self.__get_joint_start_position()
        userdata.zick_zack_out = self.__get_zick_zack_positions()
        userdata.line_out = self.__get_line_positions()
        userdata.circle_out = self.__get_circle_positions()
        return 'done'
        
#    def __get_service_area_height(self, name):
#        real_name = self.__service_area_names[name]
#        try:
#            return rospy.get_param('youbot_manipulation_ai_re/service_areas/'+real_name+'/height')
#        except:
#            pass
    def __get_service_area_height(self, name):
         s_count = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area_count')
         for i in range(1,s_count+1):
             try:
                 n = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/name')
		 if n == name:
                 	return rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/height')
		 else:
			continue	
             except:
                 break

    def __get_circle_positions(self):
        circle = []
        for i in range(4):
            x = rospy.get_param('youbot_manipulation_ai_re/circle/pos'+str(i)+'/x')
            y = rospy.get_param('youbot_manipulation_ai_re/circle/pos'+str(i)+'/y')
            circle.append((x,y))
        return circle
            
    def __get_zick_zack_positions(self):
        zick_zack = []
        for i in range(8):
            x = rospy.get_param('youbot_manipulation_ai_re/zick_zack/pos'+str(i)+'/x')
            y = rospy.get_param('youbot_manipulation_ai_re/zick_zack/pos'+str(i)+'/y')
            zick_zack.append((x,y))
        return zick_zack
    
    def __get_line_positions(self):
        line = []
        for i in range(8):
            x = rospy.get_param('youbot_manipulation_ai_re/line/pos'+str(i)+'/x')
            y = rospy.get_param('youbot_manipulation_ai_re/line/pos'+str(i)+'/y')
            line.append((x,y))
        return line
    
    def __get_joint_start_position(self):
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
