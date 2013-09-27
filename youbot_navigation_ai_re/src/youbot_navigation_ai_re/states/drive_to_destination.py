import smach
import copy
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from ..utils.global_data import global_data

class drive_to_destination(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['goal reached','cant reach goal'],
                             input_keys=['destination_in', 'orientation_in', 'coord_remapping_in', 'orientation_remapping_in'])
        self.goal_counter = 0
    def execute(self, userdata):
        if not userdata.coord_remapping_in.has_key(userdata.destination_in):
            rospy.logerr("drive_to_destination: Destination '%s' is not mapped by coord_remapping_in!", userdata.destination_in)
            return 'cant reach goal'
        if not userdata.orientation_remapping_in.has_key(userdata.orientation_in):
            rospy.logerr("drive_to_destination: Orientation '%s' is not mapped by orientation_remapping_in!", userdata.orientation_in)
            return 'cant reach goal'
        target_pos = userdata.coord_remapping_in[userdata.destination_in]
        target_orientation = userdata.orientation_remapping_in[userdata.orientation_in]
        print "Driving to %s" % userdata.destination_in
        self.move_to_coord(target_pos[0], target_pos[1], target_orientation)
        global_data.move_base_client.wait_for_result()
        result = global_data.move_base_client.get_result()
        state = global_data.move_base_client.get_state()
        if state == 3: #SUCCEEDED
            return 'goal reached'
        else:
            return 'cant reach goal'
    def move_to_coord(self, x, y, quaternion):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "/map"
        goal.target_pose.header.stamp = rospy.get_rostime()
        self.goal_counter += 1
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]
        print "Publishing..."
        global_data.move_base_client.send_goal(goal)
        print "Published"
