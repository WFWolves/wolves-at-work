'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
from youbot_conveyorbelt_ai.utils.global_data import global_data
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class DriveToConveyorbelt(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done', 'failed'],
                             input_keys=[])
    
    def execute(self, userdata): 
        self.move_robot(2.587, -0.515, (0.000, 0.000, 0.927, 0.374))
        global_data.move_base_client.wait_for_result()
        result = global_data.move_base_client.get_result()
        state = global_data.move_base_client.get_state()
        if state == 3:
            return 'done'
        else:
            return 'failed'

    def move_robot(self, x, y, quaternion):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "/map"
        goal.target_pose.header.stamp = rospy.get_rostime()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]
        global_data.move_base_client.send_goal(goal)
