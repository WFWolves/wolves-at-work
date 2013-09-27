#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Main file, contains the statemachine
'''
import roslib; roslib.load_manifest('youbot_manipulation_ai_re')
import rospy
import smach
import smach_ros

from youbot_manipulation_ai_re.utils.global_data import global_data
from youbot_ik_solution_Modifier import youbot_ik_solution_modifier
from geometry_msgs.msg import Twist

import time
from youbot_manipulation_ai_re.utils.global_data import global_data

from youbot_manipulation_ai_re.states.deposit_state_machine.Initialization_state import Initialization
from youbot_manipulation_ai_re.states.deposit_state_machine.Deposit_state import Deposit
from youbot_manipulation_ai_re.states.deposit_state_machine.SelectShape_state import SelectShape
from youbot_manipulation_ai_re.states.deposit_state_machine.MoveRobot_state import MoveRobot
class DepositObject():
    def __init__(self):
        self.__sis = None
        self.setup_statemachine()
        #self.setup_introspection()
    def run(self):
        self.__sm.execute()
        if self.__sis is not None:
            self.__sis.stop()
    def get_statemachine(self):
        return self.__sm
    def setup_introspection(self):
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/DepositObject')
        self.__sis.start()
    def setup_statemachine(self):
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                            input_keys=['object_counter_in_sm', 'alignment_in_sm', 'service_area_name_in_sm'])
        with self.__sm:
            self.__sm.userdata.object_counter = 0
            self.__sm.userdata.alignment = ''
            self.__sm.userdata.service_area_height = 0.0
            self.__sm.userdata.std_joint_position = None
            self.__sm.userdata.cirlce = None
            self.__sm.userdata.line = None
            self.__sm.userdata.zick_zack = None
            
            smach.StateMachine.add('Initialization', Initialization(),
                                   transitions={'done': 'MoveRobot'}, 
                                   remapping={'alignment_in': 'alignment_in_sm',
                                              'object_counter_in': 'object_counter_in_sm',
                                              'service_area_name_in': 'service_area_name_in_sm',
                                              'service_area_height_out': 'service_area_height',
                                              'object_counter_out': 'object_counter',
                                              'std_joint_position_out': 'std_joint_position',
                                              'circle_out': 'circle',
                                              'line_out': 'line',
                                              'zick_zack_out': 'zick_zack',
                                              'alignment_out': 'alignment'})
                                              
            smach.StateMachine.add('MoveRobot', MoveRobot(),
                                   transitions={'done': 'Deposit'}, 
                                   remapping={'joint_position_in': 'std_joint_position',
                                              'circle_in': 'circle',
                                              'line_in': 'line',
                                              'zick_zack_in': 'zick_zack',
                                              'alignment_in': 'alignment',
                                              'object_counter_in': 'object_counter',
                                              'service_area_height_in': 'service_area_height'})

            smach.StateMachine.add('Deposit', Deposit(),
                                   transitions={'done': 'succeeded'})                      
def main():
    rospy.init_node("youbot_deposit_object")
    for i in range(0,8):
    	depot = DepositObject()
    	depot.get_statemachine().userdata.alignment_in_sm = 'zigzag'
    	depot.get_statemachine().userdata.object_counter_in_sm = i
    	depot.get_statemachine().userdata.service_area_name_in_sm = 'S1'
    	depot.run()
	global_data.ik.open_gripper()
	raw_input('test')
	global_data.ik.close_gripper()
	time.sleep(4)    
if __name__ == '__main__':
    main()
