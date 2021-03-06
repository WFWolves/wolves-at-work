import smach
import copy
import rospy
import tf
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

class rotate_in_place_recovery(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','failed'],
                             input_keys=['orientation_in', 'orientation_remapping_in'])
        self.__cmd_vel = rospy.Publisher('/cmd_vel', Twist)
        self.__tf_listener = tf.TransformListener()
    def correct_orientation(self, target_quat):
        current_tf = None
        try:
            current_tf = self.__tf_listener.lookupTransform('/map', '/base_footprint', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logerr("rotate_in_place_recovery: Failed to look up transform")
            return 'failed'
    
        euler_current = euler_from_quaternion(current_tf[1])
        euler_target = euler_from_quaternion(target_quat)
        
        rospy.loginfo("Euler Current: %s", str(euler_current))
        rospy.loginfo("Euler Target: %s", str(euler_target))
        yaw_correction = euler_target[2] - (euler_current[2] + 2*math.pi)
        if yaw_correction > math.pi:
            yaw_correction -= 2*math.pi
        elif yaw_correction < -math.pi:
            yaw_correction += 2*math.pi
        rospy.loginfo("YAW Correction: %f", yaw_correction)
        
        correction = Twist()
        speed = max(abs(yaw_correction) * 0.2, 0.1)
        if yaw_correction < 0:
            correction.angular.z = -speed
        else:
            correction.angular.z = speed
        self.__cmd_vel.publish(correction)
        rospy.sleep(abs(yaw_correction)/speed)
        correction.angular.z = 0.0
        self.__cmd_vel.publish(correction)
    def execute(self, userdata):
        if not userdata.orientation_remapping_in.has_key(userdata.orientation_in):
            rospy.logerr("rotate_in_place_recovery: Orientation '%s' is not mapped by orientation_remapping_in!", userdata.orientation_in)
            return 'failed'
        target_orientation = userdata.orientation_remapping_in[userdata.orientation_in]    
        
        precision = 5
        for i in range(precision):
            self.correct_orientation(target_orientation)
        return 'succeeded'
