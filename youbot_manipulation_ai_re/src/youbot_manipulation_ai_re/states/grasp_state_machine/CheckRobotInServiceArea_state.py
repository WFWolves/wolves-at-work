'''
@author: Alex
@version: 0.0.1 prealpha
@note:
'''
import rospy
import smach
import tf
import numpy
from numpy.linalg import norm

class CheckRobotInServiceArea(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['determined', 'tfFailed'],
                             input_keys=['in_service_areas', 'in_task_spec'],
                             output_keys=['out_status', 'out_left_angle', 'out_right_angle'])
        self.__tf_listener = tf.TransformListener()
    def angle_between_vectors(self, vec1, vec2):
        cos_angle = numpy.dot(vec1,vec2) / (norm(vec1)*norm(vec2))
        return numpy.arccos(cos_angle)
    def check_robot_in_service_area(self, base_point, left_point, right_point):
        lp = numpy.array(left_point[:2])
        rp = numpy.array(right_point[:2])
        bp = numpy.array(base_point[:2])
        left_right_vec = rp - lp
        right_left_vec = lp - rp
        left_base_vec = bp - lp
        right_base_vec = bp - rp
        angle_left = self.angle_between_vectors(left_right_vec, left_base_vec)
        angle_right = self.angle_between_vectors(right_left_vec, right_base_vec)
        
        angle_thresh = 83.0
        
        in_left_range = numpy.degrees(angle_left) < angle_thresh
        in_right_range = numpy.degrees(angle_right) < angle_thresh
        
        assert not (not in_right_range and not in_left_range)
        
        if not in_left_range:
            state = "OutOfLeft"
            rospy.loginfo("CheckRobotServiceArea State: %s, left: %f, right: %f", state, angle_left, angle_right)
            return (state, angle_left, angle_right)
        elif not in_right_range:
            state = "OutOfRight"
            rospy.loginfo("CheckRobotServiceArea State: %s, left: %f, right: %f", state, angle_left, angle_right)
            return (state, angle_left, angle_right)
        else:
            state = "InBounds"
            rospy.loginfo("CheckRobotServiceArea State: %s, left: %f, right: %f", state, angle_left, angle_right)
            return (state, angle_left, angle_right)
        
    def execute(self, userdata):
        base_tf = None
        service_area_name = userdata.in_task_spec.current_service_area
        service_area = None
        for s_area in userdata.in_service_areas:
            if s_area.name == service_area_name:
                service_area = s_area
        assert service_area is not None
        left_point = service_area.left_point
        right_point = service_area.right_point
        try:
            base_tf = self.__tf_listener.lookupTransform('/map', '/base_footprint', rospy.Time(0))
            service_area_status = self.check_robot_in_service_area(base_tf[0], left_point, right_point)
            userdata.out_status = service_area_status[0]
            userdata.out_left_angle = service_area_status[1]
            userdata.out_right_angle = service_area_status[2]
            return 'determined'
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logerr("CheckRobotInServiceArea: Failed to look up transform")
            return 'tfFailed'
