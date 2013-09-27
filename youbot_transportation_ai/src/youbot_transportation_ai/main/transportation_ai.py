#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Main file, contains the statemachine
'''
import roslib; roslib.load_manifest('youbot_transportation_ai')
import rospy
import smach
import smach_ros

from youbot_transportation_ai.states.SelectPlaceSrc_state import SelectPlaceSrc
from youbot_transportation_ai.states.SelectPlaceDst_state import SelectPlaceDst
from youbot_navigation_ai_re.main.navigation_ai_re import YoubotNavigationAI
from youbot_manipulation_ai_re.main.DepositObject import DepositObject
from youbot_transportation_ai.states.ConstructNavMsg_state import ConstructNavMsg
from youbot_transportation_ai.states.ConstructManipMsg_state import ConstructManipMsg
from youbot_transportation_ai.states.Initialization_state import Initialization
from youbot_transportation_ai.states.Align_state import Align
from youbot_transportation_ai.states.UpdateTaskSpec_state import UpdateTaskSpec
from youbot_manipulation_ai_re.main.grasp_ai import YoubotGraspAI
class YoubotTransportationAI():
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
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_transportation_ai')
        self.__sis.start()
        
    def cb_dynamic_reconfigure(self, config, level):
        rospy.set_param("youbot_transportation_ai_re/misc/arm_step_range", config.arm_step_range)
        return config
    
    def setup_dynamic_reconfigure(self):
        srv = dynamic_reconfigure.server.Server(ManipulationAI_ReConfig, cb_dynamic_reconfigure)

    def setup_statemachine(self):
        
       # setup_dynamic_reconfigure()
        
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                                input_keys=['task_spec_in_sm'],
                                output_keys=[])
        self.__grasp_ai = YoubotGraspAI()
        self.__grasp_sm = self.__grasp_ai.get_statemachine()
        self.__deposit_ai = DepositObject()
        self.__deposit_sm = self.__deposit_ai.get_statemachine()
        self.__nav_ai = YoubotNavigationAI()
        self.__nav_sm = self.__nav_ai.get_statemachine()
                                
        with self.__sm:
            self.__sm.userdata.task_spec_nav = None
            self.__sm.userdata.task_spec_manip = None
            self.__sm.userdata.task_spec_trans = None
            self.__sm.userdata.selected_service_area = None
            self.__sm.userdata.destination = None
            self.__sm.userdata.service_areas = None
            self.__sm.userdata.grasped_objects = None
            self.__sm.userdata.object_counter = 0
            self.__sm.userdata.alignment = 'line'
            #self.__sm.userdata.task_spec = TaskSpecificationMan('S1',['S40_40_B','F20_20_B','R20','R20','M20_100'])

            with self.__sm:
                
                smach.StateMachine.add('Initialization', Initialization(),
                                       transitions={'initialized': 'SelectPlaceSrc'},
                                        remapping={'service_areas_out': 'service_areas',
                                                   'task_spec_in': 'task_spec_in_sm',
                                                   'task_spec_out': 'task_spec_trans'})
                                       
                smach.StateMachine.add('SelectPlaceSrc', SelectPlaceSrc(), 
                                       transitions={'selected':'ConstructSrcNavMsg'},
                                       remapping={'task_spec_in': 'task_spec_trans',
                                                  'task_spec_out': 'task_spec_trans',
                                                  'selected_src_out': 'selected_service_area'})
                                       
                smach.StateMachine.add('ConstructSrcNavMsg', ConstructNavMsg(),
                                       transitions={'constructed': 'DriveToSrc'},
                                        remapping= {'destination_in': 'selected_service_area',
                                                    'service_areas_in': 'service_areas',
                                                    'task_spec_nav_out': 'task_spec_nav'})
                
                smach.StateMachine.add('DriveToSrc', self.__nav_sm,
                                       transitions={'succeeded': 'AlignToSrcServiceArea'},
                                        remapping={'task_specification_nav_in': 'task_spec_nav'})
                
                smach.StateMachine.add('AlignToSrcServiceArea', Align(),
                                       transitions={'succeeded': 'ConstructManipMsg',
                                                    'failed': 'ConstructManipMsg'})
            
                smach.StateMachine.add('ConstructManipMsg', ConstructManipMsg(),
                                       transitions={'constructed': 'GraspObject'},
                                        remapping={'task_specification_manip_out': 'task_spec_manip',
                                                   'selected_src_in': 'selected_service_area',
                                                   'task_spec_in': 'task_spec_trans'})                
                
                smach.StateMachine.add('GraspObject', self.__grasp_sm,
                                       transitions={'succeeded': 'SelectPlaceDst'},
                                        remapping={'task_spec_in': 'task_spec_manip',
                                                   'selected_object_name_out_sm': 'grasped_objects'})              

                smach.StateMachine.add('SelectPlaceDst', SelectPlaceDst(),
                                       transitions={'selected': 'ConstructDstNavMsg'},
                                       remapping={'grasped_object_in': 'grasped_objects',
                                                  'task_spec_trans_in': 'task_spec_trans',
                                                  'selected_service_area_out': 'destination'})

                smach.StateMachine.add('ConstructDstNavMsg', ConstructNavMsg(),
                                       transitions={'constructed': 'DriveToDst'},
                                        remapping= {'service_areas_in': 'service_areas',
                                                    'task_spec_nav_out': 'task_spec_nav',
                                                    'destination_in': 'destination'})
                
                smach.StateMachine.add('DriveToDst', self.__nav_sm,
                                       transitions={'succeeded': 'AlignToDstServiceArea'},
                                        remapping={'task_specification_nav_in': 'task_spec_nav'})
                                        
                smach.StateMachine.add('AlignToDstServiceArea', Align(),
                                       transitions={'succeeded': 'DepositObject',
                                                    'failed': 'DepositObject'})
                
                smach.StateMachine.add('DepositObject', self.__deposit_sm,
                                       transitions={'succeeded': 'UpdateTaskSpec'},
                                        remapping={'object_counter_in_sm': 'object_counter',
                                                   'alignment_in_sm': 'alignment',
                                                   'service_area_name_in_sm': 'destination'})
                                       
                smach.StateMachine.add('UpdateTaskSpec', UpdateTaskSpec(),
                                       transitions={'Object remaining': 'SelectPlaceSrc',
                                                    'finished': 'succeeded'},
                                        remapping={'grasped_objects_in': 'grasped_objects',
                                                   'task_spec_trans_io': 'task_spec_trans'})                       
                
             
                                             
                
    
if __name__ == '__main__':
    rospy.init_node("youbot_manipulation_ai_re")
    you = YoubotTransportationAI()
    you.run()
