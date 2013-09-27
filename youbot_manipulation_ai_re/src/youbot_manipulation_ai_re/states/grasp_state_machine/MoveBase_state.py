'''
@author: 
@version: 0.0.1 prealpha
@note:
'''
import smach
from youbot_manipulation_ai_re.utils.global_data import global_data
from geometry_msgs.msg import Twist
from time import sleep
class MoveBase(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['base moved'],
                             input_keys=['direction_in'])
        
    def execute(self, userdata):
        msg_vel = Twist()
        if userdata.direction_in == 'L':
            msg_vel.linear.y = 0.01
        elif userdata.direction_in == 'R':
            msg_vel.linear.y = -0.01
        global_data.pubVel.publish(msg_vel)
        sleep(2)
        global_data.pubVel.publish(Twist())
        return 'base moved'
