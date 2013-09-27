#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Main file, contains the statemachine
'''
import roslib; roslib.load_manifest('youbot_conveyorbelt_ai')
import rospy
import smach
import smach_ros
import zmq

from youbot_conveyorbelt_ai.states.adjust_robot_state import AdjustRobot
from youbot_conveyorbelt_ai.states.adjust_robot_to_object_state import AdjustRobotToObject
from youbot_conveyorbelt_ai.states.drive_to_conveyorbelt_state import DriveToConveyorbelt
from youbot_conveyorbelt_ai.states.grasp_object import GraspObject
from youbot_conveyorbelt_ai.states.initialization_state import Initialization
from youbot_conveyorbelt_ai.states.leave_arena_state import LeaveArena
from youbot_conveyorbelt_ai.states.wait_for_object_state import WaitForObject
from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg._Quaternion import Quaternion

class YoubotConveyorBeltAI():
    def __init__(self):
        self.__sis = None
        self.setup_statemachine()
        #self.setup_introspection()
    def run(self):
        server_ip = rospy.get_param('youbot_main_ai/refbox/server_ip')
        server_port = rospy.get_param('youbot_main_ai/refbox/server_port')
        team_name = "WF Wolves"
        message = None
        connection_address = "tcp://" + server_ip + ":" + server_port
        rospy.loginfo("Start connection to %s", connection_address)
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(connection_address)
        except:
            print "connect failed"
        rospy.loginfo("Connected.")
        try:
            socket.send(team_name)
        except:
            print "send Failed"
        try:
            message = socket.recv()
        except:
            print "recieve failed"
        try:
            socket.send("ACK")
            socket.close()
        except:
            print "sendFailed"
        self.__sm.execute()
        if self.__sis is not None:
            self.__sis.stop()
    def get_statemachine(self):
        return self.__sm
       
    def setup_introspection(self):
        self.__sis = smach_ros.IntrospectionServer('debug', self.__sm, '/youbot_conveyorbelt_ai')
        self.__sis.start()
        
    def cb_dynamic_reconfigure(self, config, level):
        rospy.set_param("youbot_transportation_ai_re/misc/arm_step_range", config.arm_step_range)
        return config
    
    def setup_dynamic_reconfigure(self):
        srv = dynamic_reconfigure.server.Server(ManipulationAI_ReConfig, cb_dynamic_reconfigure)

    def setup_statemachine(self):
        
       # setup_dynamic_reconfigure()
        
        self.__sm = smach.StateMachine(outcomes=['succeeded', 'failed'],
                                input_keys=[],
                                output_keys=[])
                                
        with self.__sm:
                
                smach.StateMachine.add('Initialization', Initialization(),
                                       transitions={'done': 'DriveToConveyorbelt',
                                                    'failed': 'failed'})  
                                     
                smach.StateMachine.add('DriveToConveyorbelt', DriveToConveyorbelt(),
                                       transitions={'done': 'AdjustRobotToConveyorBelt',
                                                    'failed': 'AdjustRobotToConveyorBelt'})
                
                smach.StateMachine.add('AdjustRobotToConveyorBelt', AdjustRobot(),
                                       transitions={'done': 'WaitForObject',
                                                    'failed': 'DriveToConveyorbelt'})
                
                smach.StateMachine.add('WaitForObject', WaitForObject(),
                                       transitions={'done': 'AdjustRobotToObject',
                                                    'failed': 'AdjustRobotToConveyorBelt'})
                
                smach.StateMachine.add('AdjustRobotToObject', AdjustRobotToObject(),
                                       transitions={'done': 'GraspObject',
                                                    'failed': 'failed'})
                
                smach.StateMachine.add('GraspObject', GraspObject(),
                                       transitions={'done': 'LeaveArena',
                                                    'failed': 'failed'})
                
                smach.StateMachine.add('LeaveArena', LeaveArena(),
                                       transitions={'done': 'succeeded',
                                                    'failed': 'failed'})
                                             
                
    
if __name__ == '__main__':
    rospy.init_node("youbot_conveyorbelt_ai")
    you = YoubotConveyorBeltAI()
    you.setup_introspection()
    you.run()
