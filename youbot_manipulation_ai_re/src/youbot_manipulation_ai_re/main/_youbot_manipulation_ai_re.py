#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Main file, contains the two statemachines
'''
import roslib; roslib.load_manifest('youbot_manipulation_ai_re')
import rospy
import smach
import smach_ros
#import dynamic_reconfigure.server
#from youbot_manipulation_ai_re.cfg import ManipulationAI_ReConfig
#from utils.task_specification_man import TaskSpecificationMan
from states.grasp_state_machine.talking_to_referee_box_state import talking_to_referee_box
from states.grasp_state_machine.count_grasped_objects_state import count_grasped_objects
from states.grasp_state_machine.searching_state import searching
from states.grasp_state_machine.selecting_state import selecting
from states.grasp_state_machine.initialization_state import initialization
from states.grasp_state_machine.verify_object_position_state import verify_object_position
from states.grasp_state_machine.grasp_object_state import grasp_object
from states.grasp_state_machine.init_vision_state import init_vision
from states.grasp_state_machine.adjust_arm_state import adjust_arm

from states.adjust_robot_to_object_state_machine.verify_object_orientation_state import verify_object_orientation
from states.adjust_robot_to_object_state_machine.verify_object_position_state import verify_object_position
from states.adjust_robot_to_object_state_machine.move_robot_vert_state import move_robot_vert
from states.adjust_robot_to_object_state_machine.move_robot_hor_state import move_robot_hor

class YoubotGraspAI():
    def __init__(self):
        self.setup_statemachine()

    def run(self):
        self.__sm.execute()
        self.__sis.stop()

    def get_statemachine(self):
        return self.__sm
       
    def setup_introspection(self):
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_navigation_ai_re')
        self.__sis.start()
        
    def cb_dynamic_reconfigure(self, config, level):
        rospy.set_param("youbot_manipulation_ai_re/misc/arm_step_range", config.arm_step_range)
        return config
    
    def setup_dynamic_reconfigure(self):
        srv = dynamic_reconfigure.server.Server(ManipulationAI_ReConfig, cb_dynamic_reconfigure)

    def setup_statemachine(self):
        
       # setup_dynamic_reconfigure()
        
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                                input_keys=['task_spec_in'],
                                output_keys=['selected_object_name_out_sm'])
                                
        self.__adjust_sm = smach.StateMachine(outcomes=['succeeded', 'object lost'],
                                       input_keys=['selected_object_name_in_ad',
                                                   'joint_position_in_ad',
                                                   'camera_in_ad',
                                                   'overview_position_in_ad'],
                                       output_keys=['joint_position_out_ad'])
        
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/SM_ROOT')
        self.__sis.start()
        with self.__adjust_sm:
            self.__sis_ad = smach_ros.IntrospectionServer('debug', self.__adjust_sm, '/SM_ROOT/adjust_sm')
            self.__sis_ad.start()
            self.__adjust_sm.userdata.object_orientation_ad = ''
            self.__adjust_sm.userdata.joint_position_out_ad = None
            self.__adjust_sm.userdata.object_data_ad = None
            self.__adjust_sm.userdata.joint_position = None
            smach.StateMachine.add('verify_object_orientation', verify_object_orientation(),
                                   transitions={'done': 'verify_object_position',
                                                'object lost': 'object lost'},
                                   remapping={'selected_object_name_in': 'selected_object_name_in_ad',
                                              'object_orientation_out': 'object_orientation_ad',
                                              'joint_position_in': 'joint_position_in_ad',
                                              'joint_position_out': 'joint_position'})
            
            smach.StateMachine.add('verify_object_position', verify_object_position(),
                                   transitions={'vertical': 'move_robot_vert',
                                                'horizontal': 'move_robot_hor',
                                                'robot adjusted': 'succeeded',
                                                'object lost': 'object lost'},
                                   remapping={'selected_object_name_in': 'selected_object_name_in_ad',
                                             'camera_in': 'camera_in_ad',
                                             'object_orientation_in': 'object_orientation_ad',
                                             'object_data_out': 'object_data_ad',
                                             'joint_position_in': 'joint_position',
                                             'joint_position_out': 'joint_position_out_ad'})
            
            smach.StateMachine.add('move_robot_vert', move_robot_vert(),
                                   transitions={'done': 'verify_object_position'},
                                   remapping={'object_data_in': 'object_data_ad',
                                              'joint_position_io': 'joint_position'})
            
            smach.StateMachine.add('move_robot_hor', move_robot_hor(),
                                   transitions={'done': 'verify_object_position'},
                                   remapping={'object_data_in': 'object_data_ad',
                                              'joint_position_io': 'joint_position'})
            
        with self.__sm:
            self.__sm.userdata.object_counter = 0
            self.__sm.userdata.task_spec = None
            #self.__sm.userdata.task_spec = TaskSpecificationMan('S1',['S40_40_B','F20_20_B','R20','R20','M20_100'])
            self.__sm.userdata.camera_params = None
            self.__sm.userdata.selected_object_name = ''
            self.__sm.userdata.object_data = []
            self.__sm.userdata.service_areas = []
            self.__sm.userdata.current_joint_position =  None
            self.__sm.userdata.overview_position = None
            self.__sm.userdata.object_lengths = {}

            with self.__sm:
                smach.StateMachine.add('Initialization', initialization(), 
                                       transitions={'initialized':'init_vision'},
                                       remapping={'service_areas_out': 'service_areas',
                                                  'joint_start_position_out': 'current_joint_position',
                                                  'object_lengths_out': 'object_lengths',
                                                  'overview_position_out': 'overview_position',
                                                  'task_spec_iin': 'task_spec_in',
                                                  'task_spec_out': 'task_spec'})
    #            smach.StateMachine.add('talking_to_referee_box', talking_to_referee_box(),
    #                                   transitions={'message received': 'init_vision',
    #                                                'Error, retry': 'talking_to_referee_box'},
    #                                   remapping={'task_specification_out':'task_spec'})
                smach.StateMachine.add('init_vision', init_vision(),
                                       transitions={'vision initialized': 'selecting'},
                         
                                       remapping={'task_spec_io': 'task_spec',
                                                  'camera_out': 'camera_params'})
     #           smach.StateMachine.add('count_grasped_objects', count_grasped_objects(),
     #                                  transitions={'One or more objects found': 'selecting',
     #                                               'No object found': 'searching',
     #                                               'All objects grasped': 'succeeded'},
     #                                  remapping={'counter_in':'object_counter'})
                smach.StateMachine.add('searching', searching(),
                                       transitions={'finished': 'selecting'})

                smach.StateMachine.add('selecting',selecting(),
                                       transitions={'Object selected': 'adjust_state_machine',
						    'Object lost': 'searching'},
                                       remapping={'selected_object_name_out':'selected_object_name',
                                                 'camera_in': 'camera_params'})

                smach.StateMachine.add('adjust_state_machine', self.__adjust_sm,
                                      transitions={'succeeded': 'adjust_arm',
                                                   'object lost': 'searching'},
                                      remapping={'selected_object_name_in_ad': 'selected_object_name',
                                                   'joint_position_in_ad': 'current_joint_position',
                                                   'camera_in_ad': 'camera_params',
                                                   'overview_position_in_ad': 'overview_position',
                                                   'joint_position_out_ad': 'current_joint_position'})
                
                smach.StateMachine.add('grasp_object', grasp_object(),
                                       transitions={'Object grasped': 'succeeded'},
                                       remapping={'joint_position_in': 'current_joint_position',
                                                  'selected_object_name_in': 'selected_object_name',
                                                  'service_areas_in': 'service_areas',
                                                  'object_lengths_io': 'object_lengths',
                                                  'task_spec_io': 'task_spec',
                                                  'joint_position_out': 'current_joint_position',
                                                  'overview_position_in': 'overview_position',
                                                  'selected_object_name_out': 'selected_object_name_out_sm'})
                
                smach.StateMachine.add('adjust_arm', adjust_arm(),
                                       transitions={'arm adjusted': 'grasp_object',
                                                    'object lost': 'searching'},
                                       remapping={'joint_position_in': 'current_joint_position',
                                                  'selected_object_name_in': 'selected_object_name',
                                                  'object_lengths_io': 'object_lengths',
                                                  'camera_params_in': 'camera_params'})
    
if __name__ == '__main__':
    rospy.init_node("youbot_manipulation_ai_re")
    you = YoubotGraspAI()
    you.run()
