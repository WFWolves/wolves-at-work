#!/usr/bin/env python
import roslib; roslib.load_manifest('youbot_main_ai')
import rospy
import brics_actuator.msg
from geometry_msgs.msg import Twist

def cb_position_cmd(msg):
    try:
        intercept = rospy.get_param('youbot_main_ai/intercept_actuator')
    except:
        rospy.logerr("param intercept_actuator not found")
    if not intercept:
        pub_poscmd.publish(msg)
    
    
def cb_cmd_vel(msg):
    try:
        intercept = rospy.get_param('youbot_main_ai/intercept_actuator')
    except:
        rospy.logerr("param intercept_actuator not found")
    if not intercept:
        pub_cmdvel.publish(msg)
    else:
        pub_cmdvel.publish(Twist())
    
rospy.init_node("actuator_interceptor")
sub_poscmd = rospy.Subscriber('position_command_in', brics_actuator.msg.JointPositions, cb_position_cmd)
sub_cmdvel = rospy.Subscriber('cmd_vel_in', Twist, cb_cmd_vel)
pub_cmdvel = rospy.Publisher('/cmd_vel', Twist)
pub_poscmd = rospy.Publisher('/arm_1/arm_controller/position_command', brics_actuator.msg.JointPositions)
rospy.spin()
