#!/usr/bin/python
import roslib; roslib.load_manifest('youbot_main_ai')
import rospy
import smach
import smach_ros
import tf
import os

from youbot_main_ai.states.GetTaskspecFromRefbox import GetTaskspecFromRefbox
from youbot_main_ai.states.SelectTask import SelectTask
from youbot_main_ai.states.ParseBNTTask import ParseBNTTask
from youbot_main_ai.states.ParseBMTTask import ParseBMTTask
from youbot_main_ai.states.ParseBTTTask import ParseBTTTask
from youbot_main_ai.states.ParsePPTTask import ParsePPTTask
from youbot_main_ai.states.GenTaskspecNavigation import GenTaskspecNavigation
from youbot_navigation_ai_re.main.navigation_ai_re import YoubotNavigationAI
from youbot_manipulation_ai_re.main.manipulation_ai import YoubotManipulationAI
from youbot_transportation_ai.main.transportation_ai import YoubotTransportationAI

class YoubotMainAI():
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
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_main_ai')
        self.__sis.start()
    def setup_statemachine(self):
        self.__nav_ai = YoubotNavigationAI()
        self.__nav_sm = self.__nav_ai.get_statemachine()
        self.__manip_ai = YoubotManipulationAI()
        self.__manip_sm = self.__manip_ai.get_statemachine()
        self.__trans_ai = YoubotTransportationAI()
        self.__trans_sm = self.__trans_ai.get_statemachine()
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'])
        
        with self.__sm:
            self.__sm.userdata.refbox_message = None
            self.__sm.userdata.taskspec = None
            self.__sm.userdata.taskspec_tmp = None
            self.__sm.userdata.marker_leave = "MAP_ZERO"
            self.__sm.userdata.orientation_leave = "N"
            
            smach.StateMachine.add('get_taskspec_from_refbox', GetTaskspecFromRefbox(), 
                                   transitions={'succeeded': 'select_task',
                                                'sendFailed': 'failed', 
                                                'recieveFailed': 'failed',
                                                'connectFailed': 'failed'}, 
                                   remapping={'recieved_message_out': 'refbox_message'})
            smach.StateMachine.add('select_task', SelectTask(),
                                   transitions={'taskBNT': 'parse_bnt_task',
                                                'taskBMT': 'parse_bmt_task',
                                                'taskBTT': 'parse_btt_task',
                                                'taskPPT': 'parse_ppt_task',
                                                'taskUnknown': 'failed'},
                                   remapping={'refbox_message_in': 'refbox_message'})
            smach.StateMachine.add('parse_bnt_task', ParseBNTTask(),
                                   transitions={'parsed': 'BNT',
                                                'parseFailed': 'failed'},
                                   remapping={'refbox_message_in': 'refbox_message',
                                              'taskspec_out': 'taskspec'})
            smach.StateMachine.add('parse_bmt_task', ParseBMTTask(),
                                   transitions={'parsed': 'BMT',
                                                'parseFailed': 'failed'},
                                   remapping={'refbox_message_in': 'refbox_message',
                                              'taskspec_out': 'taskspec'})
            smach.StateMachine.add('parse_btt_task', ParseBTTTask(),
                                   transitions={'parsed': 'BTT',
                                                'parseFailed': 'failed'},
                                   remapping={'refbox_message_in': 'refbox_message',
                                              'taskspec_out': 'taskspec'})
            smach.StateMachine.add('parse_ppt_task', ParsePPTTask(),
                                   transitions={'parsed': 'BTT',
                                                'parseFailed': 'failed'},
                                   remapping={'refbox_message_in': 'refbox_message',
                                              'taskspec_out': 'taskspec'})
            smach.StateMachine.add('BNT', self.__nav_sm,
                                   transitions={'succeeded': 'LeaveArenaGenerateTaskspec',
                                                'failed': 'failed'},
                                   remapping={'task_specification_nav_in': 'taskspec'})
            smach.StateMachine.add('BMT', self.__manip_sm,
                                   transitions={'succeeded': 'LeaveArenaGenerateTaskspec',
                                                'failed': 'failed'},
                                   remapping={'task_specification_manip_in': 'taskspec'})
            smach.StateMachine.add('BTT', self.__trans_sm,
                                   transitions={'succeeded': 'LeaveArenaGenerateTaskspec',
                                                'failed': 'failed'},
                                   remapping={'task_spec_in_sm': 'taskspec'})
            smach.StateMachine.add('LeaveArenaGenerateTaskspec', GenTaskspecNavigation(),
                                   transitions={'generated': 'LeaveArena',
                                                'failed': 'failed'},
                                   remapping={'marker_in': 'marker_leave',
                                              'orientation_in': 'orientation_leave',
                                              'task_spec_out': 'taskspec_tmp'})
            smach.StateMachine.add('LeaveArena', self.__nav_sm,
                                   transitions={'succeeded': 'succeeded',
                                                'failed': 'failed'},
                                   remapping={'task_specification_nav_in': 'taskspec_tmp'})
                                             
           

def main():
    rospy.init_node("youbot_main_ai")
    rospy.logdebug("DEBUG ENABLED")
    main_ai = YoubotMainAI()
    main_ai.setup_introspection()
    main_ai.run()
    
if __name__ == '__main__':
    main()
