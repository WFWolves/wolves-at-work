#!/usr/bin/python
import roslib; roslib.load_manifest('youbot_manipulation_ai_re')
import rospy
import smach
import smach_ros
import tf
import os

from youbot_navigation_ai_re.main.navigation_ai_re import YoubotNavigationAI
from youbot_manipulation_ai_re.main.grasp_ai import YoubotGraspAI
from youbot_manipulation_ai_re.main.DepositObject import DepositObject
from youbot_manipulation_ai_re.utils.task_specification import task_specification
from youbot_manipulation_ai_re.states.main_ai_state_machine.initialization import Initialization 
from youbot_manipulation_ai_re.states.main_ai_state_machine.gen_taskspec_navigation import GenTaskspecNavigation
from youbot_manipulation_ai_re.states.main_ai_state_machine.gen_taskspec_grasp import GenTaskspecGrasp
from youbot_manipulation_ai_re.states.main_ai_state_machine.align_robot import AlignRobot
from youbot_manipulation_ai_re.states.main_ai_state_machine.task_spec_update import TaskSpecUpdate   

class YoubotManipulationAI():
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
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_manipulation_ai_re')
        self.__sis.start()
    def setup_statemachine(self):
        self.__nav_ai = YoubotNavigationAI()
        self.__nav_sm = self.__nav_ai.get_statemachine()
        self.__grasp_ai = YoubotGraspAI()
        self.__grasp_sm = self.__grasp_ai.get_statemachine()
        self.__deposit_ai = DepositObject()
        self.__deposit_sm = self.__deposit_ai.get_statemachine()
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                            input_keys=['task_specification_manip_in'])
        with self.__sm:
            self.__sm.userdata.task_specification = None
            self.__sm.userdata.task_spec_tmp = None
            self.__sm.userdata.current_object = None
            self.__sm.userdata.dest_object_counter = 0
            self.__sm.userdata.alignment = None
            self.__sm.userdata.marker_init = None
            self.__sm.userdata.marker_src = None
            self.__sm.userdata.marker_dst = None
            self.__sm.userdata.marker_fin = None
            self.__sm.userdata.orientation_init = None
            self.__sm.userdata.orientation_src = None
            self.__sm.userdata.orientation_dst = None
            self.__sm.userdata.orientation_fin = None
            
            smach.StateMachine.add('initialization', Initialization(), 
                                   transitions={'done': 'gen_taskspec_nav_initial'}, 
                                   remapping={'task_specification_io': 'task_specification_manip_in',
                                              'task_specification_out': 'task_specification',
                                              'dest_object_counter_out': 'dest_object_counter',
                                              'alignment_out': 'alignment',
                                              'marker_init_out': 'marker_init',
                                              'marker_src_out': 'marker_src',
                                              'marker_dst_out': 'marker_dst',
                                              'marker_fin_out': 'marker_fin',
                                              'orientation_init_out': 'orientation_init',
                                              'orientation_src_out': 'orientation_src',
                                              'orientation_dst_out': 'orientation_dst',
                                              'orientation_fin_out': 'orientation_fin'})
                                              
            smach.StateMachine.add('gen_taskspec_nav_initial', GenTaskspecNavigation(),
                                   transitions={'generated': 'drive_to_initial_place',
                                                'failed': 'failed'},
                                   remapping={'marker_in': 'marker_init',
                                              'orientation_in': 'orientation_init',
                                              'task_spec_out': 'task_spec_tmp'})
            
            smach.StateMachine.add('drive_to_initial_place', self.__nav_sm,
                                   transitions={'succeeded': 'gen_taskspec_nav_source',
                                                'failed': 'gen_taskspec_nav_source'},
                                   remapping={'task_specification_nav_in': 'task_spec_tmp'})
                                   
            smach.StateMachine.add('gen_taskspec_nav_source', GenTaskspecNavigation(),
                                   transitions={'generated': 'drive_to_source_place',
                                                'failed': 'failed'},
                                   remapping={'marker_in': 'marker_src',
                                              'orientation_in': 'orientation_src',
                                              'task_spec_out': 'task_spec_tmp'})
            
            smach.StateMachine.add('drive_to_source_place', self.__nav_sm,
                                   transitions={'succeeded': 'align_robot_source',
                                                'failed': 'gen_taskspec_nav_source'},
                                   remapping={'task_specification_nav_in': 'task_spec_tmp'})
                                   
            smach.StateMachine.add('align_robot_source', AlignRobot(),
                                   transitions={'succeeded': 'gen_taskspec_grasp',
                                                'failed': 'gen_taskspec_grasp'},
                                   remapping={})
                                   
            smach.StateMachine.add('gen_taskspec_grasp', GenTaskspecGrasp(),
                                   transitions={'generated': 'grasp_object',
                                                'failed': 'failed'},
                                   remapping={'task_specification_in': 'task_specification',
                                              'task_spec_out': 'task_spec_tmp'}) 
                                   
            smach.StateMachine.add('grasp_object', self.__grasp_sm,
                                   transitions={'succeeded': 'gen_taskspec_nav_dest',
                                                'failed': 'gen_taskspec_nav_dest'},
                                   remapping={'task_spec_in': 'task_spec_tmp',
                                              'selected_object_name_out_sm': 'current_object'}) 
           
            smach.StateMachine.add('gen_taskspec_nav_dest', GenTaskspecNavigation(),
                                   transitions={'generated': 'drive_to_dest_place',
                                                'failed': 'failed'},
                                   remapping={'marker_in': 'marker_dst',
                                              'orientation_in': 'orientation_dst',
                                              'task_spec_out': 'task_spec_tmp'}) 
           
            smach.StateMachine.add('drive_to_dest_place', self.__nav_sm,
                                   transitions={'succeeded': 'align_robot_dest',
                                                'failed': 'align_robot_dest'},
                                   remapping={'task_specification_nav_in': 'task_spec_tmp'})
           
            smach.StateMachine.add('align_robot_dest', AlignRobot(),
                                   transitions={'succeeded': 'deposit_object',
                                                'failed': 'deposit_object'},
                                   remapping={})
           
            smach.StateMachine.add('deposit_object', self.__deposit_sm,
                                   transitions={'succeeded': 'task_spec_update',
                                                'failed': 'task_spec_update'},
                                   remapping={'object_counter_in_sm': 'dest_object_counter',
                                              'alignment_in_sm': 'alignment',
                                              'service_area_name_in_sm': 'marker_dst'})
                                              
            smach.StateMachine.add('task_spec_update', TaskSpecUpdate(),
                                   transitions={'nextObject': 'gen_taskspec_nav_source',
                                                'finished': 'gen_taskspec_nav_final'},
                                   remapping={'task_specification_io': 'task_specification',
                                              'current_object_in': 'current_object'})
                                              
            smach.StateMachine.add('gen_taskspec_nav_final', GenTaskspecNavigation(),
                                   transitions={'generated': 'drive_to_final_place',
                                                'failed': 'failed'},
                                   remapping={'marker_in': 'marker_fin',
                                              'orientation_in': 'orientation_fin',
                                              'task_spec_out': 'task_spec_tmp'})
            
            smach.StateMachine.add('drive_to_final_place', self.__nav_sm,
                                   transitions={'succeeded': 'succeeded',
                                                'failed': 'failed'},
                                   remapping={'task_specification_nav_in': 'task_spec_tmp'})
           

def main():
    rospy.init_node("youbot_manipulation_ai_re")
    manip_ai = YoubotManipulationAI()
    manip_ai.setup_introspection()
    #Example Task Spec
    spec = task_specification()
    spec.set_initial_place("T4")
    spec.set_source("S5")
    spec.set_destination("D2")
    spec.set_final_place("T4")
    spec.set_formation("line")
    spec.set_objects(["R20", "V20", "F20_20_B"])
    manip_ai.get_statemachine().userdata.task_specification_manip_in = spec
    manip_ai.run()
    
if __name__ == '__main__':
    main()
