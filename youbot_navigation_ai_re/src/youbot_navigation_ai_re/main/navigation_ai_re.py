#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Main file, contains the statemachine
'''
import roslib; roslib.load_manifest('youbot_navigation_ai_re')
import rospy
import smach
import smach_ros
import tf
import nav_msgs
import move_base_msgs

from youbot_navigation_ai_re.utils.task_specification import navigation_target, task_specification_navigation
from youbot_navigation_ai_re.states.initialization import initialization
from youbot_navigation_ai_re.states.drive_to_destination import drive_to_destination
from youbot_navigation_ai_re.states.rotate_in_place_recovery import rotate_in_place_recovery
from youbot_navigation_ai_re.states.adjust_robot import adjust_robot
from youbot_navigation_ai_re.states.select_destination import select_destination
from youbot_navigation_ai_re.states.wait import wait

class YoubotNavigationAI():
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
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_navigation_ai_re')
        self.__sis.start()
    def setup_statemachine(self):
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                            input_keys=['task_specification_nav_in'])
        with self.__sm:
            self.__sm.userdata.task_specification = None
            self.__sm.userdata.destination = None
            self.__sm.userdata.orientation = None
            self.__sm.userdata.sleeptime = None
            self.__sm.userdata.orientation_remapping = None
            self.__sm.userdata.coord_remapping = None
            
            smach.StateMachine.add('initialization', initialization(), 
                                   transitions={'done': 'select_destination'}, 
                                   remapping={'task_specification_io':  'task_specification_nav_in',
                                              'task_specification_out': 'task_specification',
                                              'orientation_remapping_out': 'orientation_remapping',
                                              'markers_out': 'coord_remapping',})
            
            smach.StateMachine.add('select_destination', select_destination(),
                                   transitions={'selected': 'drive_to_destination',
                                                'finished': 'succeeded'},
                                   remapping={'task_specification_io': 'task_specification',
                                              'destination_out': 'destination',
                                              'orientation_out': 'orientation',
                                              'sleeptime_out': 'sleeptime'})
            
            smach.StateMachine.add('drive_to_destination', drive_to_destination(), 
                                   transitions={'goal reached': 'adjust_robot',
                                                'cant reach goal': 'rotate_in_place_recovery'}, 
                                   remapping={'destination_in': 'destination',
                                              'orientation_in': 'orientation',
                                              'coord_remapping_in': 'coord_remapping',
                                              'orientation_remapping_in': 'orientation_remapping'})
            
            smach.StateMachine.add('rotate_in_place_recovery', rotate_in_place_recovery(), 
                                   transitions={'succeeded': 'adjust_robot',
                                                'failed': 'failed'}, 
                                   remapping={'orientation_in': 'orientation',
                                              'orientation_remapping_in': 'orientation_remapping'})
                    
            smach.StateMachine.add('adjust_robot', adjust_robot(), 
                                   transitions={'robot adjusted': 'wait'}, 
                                   remapping={'orientation_in': 'orientation',
                                              'task_specification_in': 'task_specification'})
                                              
            smach.StateMachine.add('wait', wait(),
                                   transitions={'completed': 'select_destination'},
                                   remapping={'sleeptime_in': 'sleeptime'})

def main():
    rospy.init_node("youbot_navigation_ai_re")
    nav_ai = YoubotNavigationAI()
    nav_ai.setup_introspection()
    #Example Task Spec
    spec = task_specification_navigation()
    spec.add_target(navigation_target("D1", "S", 2.0))
    spec.add_target(navigation_target("T4", "W", 2.0))
    spec.add_target(navigation_target("S1", "N", 2.0))
    spec.add_target(navigation_target("S5", "N", 2.0))
    nav_ai.get_statemachine().userdata.task_specification_nav_in = spec
    nav_ai.run()
    
    
if __name__ == '__main__':
    main()
