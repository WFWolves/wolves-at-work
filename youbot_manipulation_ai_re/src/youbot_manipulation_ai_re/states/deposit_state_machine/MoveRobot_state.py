'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
import actionlib
from time import sleep
from math import pi
import copy
from youbot_manipulation_ai_re.utils.global_data import global_data
from geometry_msgs.msg import Twist
from youbot_scanner_alignment.msg import AlignedDrivingAction, AlignedDrivingGoal
class MoveRobot(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'],
                             input_keys=['joint_position_in', 'line_in', 'zick_zack_in', 
                                         'circle_in', 'alignment_in', 'object_counter_in',
                                         'service_area_height_in'])
        self.align_client = actionlib.SimpleActionClient('aligned_driving', AlignedDrivingAction)        
    	self.align_client.wait_for_server()
    def execute(self, userdata):
        alignment = self.__get_alignment(userdata)
        self.__move_base(alignment, userdata.object_counter_in)
#        if userdata.alignment_in == 'zigzag':
#            global_data.ik.set_joint_offset(4, pi/2.0)
        self.__move_arm(alignment, userdata.object_counter_in, userdata.joint_position_in, userdata.service_area_height_in)
        return 'done'
        
    def __get_alignment(self, us):
        al = copy.deepcopy(us.alignment_in)
        if al == 'circle':
            return copy.deepcopy(us.circle_in)
        elif al == 'line':
            return copy.deepcopy(us.line_in)
        elif al == 'zigzag':
            return copy.deepcopy(us.zick_zack_in)
    
    def __move_base(self, al, counter):
        coords = al[counter]
        #goal = AlignedDrivingGoal()
        #goal.front_distance = 0.05
        #goal.tolerance = 0.008
        #goal.side_difference = coords[1]
	    #self.align_client.send_goal(goal)
	    #self.align_client.wait_for_result(rospy.Duration.from_sec(0.0))

        if coords[1] > 0.0:
            msg_vel = Twist()
            msg_vel.linear.y += coords[1]
            global_data.pubVel.publish(msg_vel)
            sleep(3)
            global_data.pubVel.publish(Twist())
        goal = AlignedDrivingGoal()
        goal.front_distance = 0.05
        goal.tolerance = 0.008
        goal.side_difference = 0.0
        self.align_client.send_goal(goal)
        self.align_client.wait_for_result(rospy.Duration.from_sec(0.0))
            
    def __move_arm(self, al, counter, pos, z):
        pos['x'] += 0.04
        coords = al[counter]
        print '\n\n ' + str(coords)
        pos['x'] += coords[0]
        pos['z'] = z
        global_data.ik.change_pos(pos)
        sleep(3)
        global_data.ik.set_joint_offset(4, 0.0)
