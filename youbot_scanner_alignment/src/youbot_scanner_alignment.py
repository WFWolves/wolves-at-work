#!/usr/bin/env python
"""This is a program to perform an autoalignment of te youBot base to a wall or 
box.
@Author: p-th.wentscher@ostfalia.de (philipp)
"""

import roslib; roslib.load_manifest('youbot_scanner_alignment')
import rospy
import actionlib
import smach
import smach_ros
from youbot_scanner_alignment.msg import *
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from youbot_scanner_lines.msg import *
from scanner_alignment_states import Localisation
from scanner_alignment_states import DriveBackward, DriveForward, DriveLeft, DriveRight
from scanner_alignment_states import TurnLeft, TurnRight
from SmachGlobalData import SmachGlobalData
from scanner_alignment_utils import Utils

class ActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('aligned_driving', AlignedDrivingAction, self.execute, False)
        print "actionServer init"
        self.is_running = False
        self.server.start()
        
    def execute(self, goal):
        print "goal: ", goal
        if not self.is_running:
            self.is_running = True
            SmachGlobalData.goal_side_difference = goal.side_difference
            SmachGlobalData.goal_tolerance = goal.tolerance
            SmachGlobalData.goal_front_distance = goal.front_distance
            print "start main"
            self.main()
            self.server.set_succeeded()
            self.is_running = False
        
        
    
    def main(self):
        SmachGlobalData.pub_cmdvel = rospy.Publisher('cmd_vel', Twist)
        SmachGlobalData.pub_marker = rospy.Publisher('visualization_marker', Marker)
        SmachGlobalData.pub_laser = rospy.Publisher('merged_scan', LaserScan)
        SmachGlobalData.sub_laser = rospy.Subscriber('base_scan', LaserScan, Utils.laser_callback)
        SmachGlobalData.sub_lines = rospy.Subscriber('detected_best_laser_line_filtered', DetectedLaserLine, Utils.lines_callback) 
        #arrow marker
        #SmachGlobalData.sub_marker = rospy.Subscriber('visualization_marker', Marker, Utils.marker_callback)
        SmachGlobalData.msg_laser = LaserScan()
        SmachGlobalData.msgs_laser = [LaserScan()]
        #SmachGlobalData.msg_marker_arrow = Marker()
        SmachGlobalData.first_scan = False
        SmachGlobalData.first_line = False
        SmachGlobalData.laser_count = 0
        print "wait for scan"
        while not SmachGlobalData.first_scan :
            rospy.sleep(0.1)
        print "wait for line"
        while not SmachGlobalData.first_line:
            rospy.sleep(0.1)
        sma = smach.StateMachine(outcomes=["Aligned"])
        
        sma.userdata.sm_drive_time = 0.0
        sma.userdata.sm_turn_speed = 0.0
        sma.userdata.sm_drive_speed = 0.0
        
        sis = smach_ros.IntrospectionServer("introspection_youbot_scanner_alignment", sma, "/Youbot_Scanner_Alignment")
        sis.start()
        
        with sma:
            smach.StateMachine.add("Localisation", Localisation(),
                                    transitions = {"locate" : "Localisation",
                                                   "driveLeft": "DriveLeft",
                                                   "driveRight": "DriveRight",
                                                   "driveForward": "DriveForward",
                                                   "driveBackward": "DriveBackward",
                                                   "turnLeft": "TurnLeft",
                                                   "turnRight": "TurnRight",
                                                   "aligned": "Aligned"},
                                    remapping = {"out_drive_time": "sm_drive_time",
                                                 "out_turn_speed": "sm_turn_speed",
                                                 "out_drive_speed": "sm_drive_speed"})
            smach.StateMachine.add("DriveLeft", DriveLeft(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
            smach.StateMachine.add("DriveRight", DriveRight(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
            smach.StateMachine.add("DriveForward", DriveForward(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
            smach.StateMachine.add("DriveBackward", DriveBackward(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
            smach.StateMachine.add("TurnLeft", TurnLeft(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
            smach.StateMachine.add("TurnRight", TurnRight(),
                                    transitions = {"locate": "Localisation"},
                                    remapping = {"in_drive_time":"sm_drive_time",
                                                 "in_drive_speed": "sm_drive_speed",
                                                 "in_turn_speed": "sm_turn_speed"})
        
        sma_result = sma.execute()
        
        rospy.loginfo("State machine finished with: %s" % str(sma_result))
        
        sis.stop()

if __name__ == "__main__":
    print "init... node"
    rospy.init_node("youbot_scanner_alignment", disable_signals=True)
    print "node init"
    sate_server = ActionServer()
    rospy.spin()
    

