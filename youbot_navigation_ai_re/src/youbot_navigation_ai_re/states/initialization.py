import smach
import copy
import rospy
import actionlib
import move_base_msgs
from ..utils.global_data import global_data
from ..utils.task_specification import task_specification_navigation, navigation_target

#FIXME ROS Const Hack
def const_hack(obj):
    while type(obj) == smach.user_data.Const:
        obj = obj._obj
    return obj

class initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done',],
                             io_keys=['task_specification_io'],
                             output_keys=['task_specification_out', 'markers_out', 'orientation_remapping_out'])
    def execute(self, userdata):
        global_data.move_base_client = actionlib.SimpleActionClient('move_base', move_base_msgs.msg.MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        global_data.move_base_client.wait_for_server()
        userdata.markers_out = self.get_markers()
        userdata.orientation_remapping_out = self.get_orientation()
        userdata.task_specification_out = const_hack(userdata.task_specification_io)
        return 'done'
    def get_markers(self):
        markers = {}
        try:
            marker_count = int(rospy.get_param('youbot_navigation_ai_re/markers/markerCount'))
        except ValueError:
            rospy.logerr("markerCount could not be parsed into an integer!")
            return None
        for i in range(marker_count):
            try:
                name = rospy.get_param('youbot_navigation_ai_re/markers/marker%d/name' % i)
                x = float(rospy.get_param('youbot_navigation_ai_re/markers/marker%d/x-pos' % i))
                y = float(rospy.get_param('youbot_navigation_ai_re/markers/marker%d/y-pos' % i))
                markers[name] = (x,y)
            except ValueError:
                rospy.logerr("marker %d position could not be parsed as float", i)
                continue
            except KeyError:
                rospy.logerr("Parameter for marker %d was not found, but markerCount is %d", i, marker_count)
                continue
        return markers
    
    def get_orientation(self):
        orientation = {}
        try:
            orientation_count = int(rospy.get_param('youbot_navigation_ai_re/orientation/orientationCount'))
        except ValueError:
            rospy.logerr("orientationCount could not be parsed into an integer!")
            return None
        for i in range(orientation_count):
            try:
                name = rospy.get_param('youbot_navigation_ai_re/orientation/o%d/name' % i)
                x = float(rospy.get_param('youbot_navigation_ai_re/orientation/o%d/x' % i))
                y = float(rospy.get_param('youbot_navigation_ai_re/orientation/o%d/y' % i))
                z = float(rospy.get_param('youbot_navigation_ai_re/orientation/o%d/z' % i))
                w = float(rospy.get_param('youbot_navigation_ai_re/orientation/o%d/w' % i))
                orientation[name] = (x,y,z,w)
            except ValueError:
                rospy.logerr("orientation %d could not be parsed as float", i)
                continue
            except KeyError:
                rospy.logerr("Parameter for orientation %d was not found, but orientationCount is %d", i, orientation_count)
                break
        return orientation
