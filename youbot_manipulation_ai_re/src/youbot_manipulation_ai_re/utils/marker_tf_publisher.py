#!/usr/bin/env python 
import roslib; roslib.load_manifest("youbot_manipulation_ai_re")
import rospy
import tf
from youbot_manipulation_ai_re.utils.service_area import service_area
from interactive_markers.interactive_marker_server import *

interactive_markers = []
to_update = {}
markers = None
areas = None
area_to_id = {}


def processFeedback(feedback):
    mname = feedback.marker_name.split("_")[0]
    m_id, typ = None, None
    sub_typ = None
    if feedback.marker_name.endswith("_nav"):
        typ = "nav"
        m_id = markers[mname][2]
    elif feedback.marker_name.endswith("_area"):
        typ = "area"
        m_id = area_to_id[mname]
        sub_typ = "l" if "left" in feedback.marker_name else "r"
    to_update[mname]={'name': mname, 'id': m_id, 'type': typ, 'x': feedback.pose.position.x, 'y': feedback.pose.position.y, 'sub_type':sub_typ}
    p = feedback.pose.position
    print feedback.marker_name + " is now at " + str(p.x) + ", " + str(p.y) + ", " + str(p.z)

def get_markers():
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
            num = i
            markers[name] = (x,y,i)
        except ValueError:
            rospy.logerr("marker %d position could not be parsed as float", i)
            continue
        except KeyError:
            rospy.logerr("Parameter for marker %d was not found, but markerCount is %d", i, marker_count)
            continue
    return markers

def get_service_areas():
    result = []
    s_count = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area_count')
    for i in range(1,s_count+1):
        try:
            n = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/name')
            h = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/height')
            x_pos = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/xpos')
            y_pos = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/ypos') 
            o = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/orientation')
            lpx = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/lPointX')
            lpy = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/lPointY')
            rpx = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/rPointX')
            rpy = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area'+str(i)+'/rPointY')
            area_to_id[n] = i
            s = service_area(n, h, x_pos, y_pos,(lpx, lpy), (rpx, rpy), o)
            result.append(s)
        except:
            print "Error while parsing %d" % i
    return result
    
def publish_coord_tf(tf_broadcaster, name, x, y):
    tf_broadcaster.sendTransform((x, y, 0), tf.transformations.quaternion_from_euler(0,0,0),
                                 rospy.Time.now(),
                                 name,
                                 "/map")

def create_interactive_marker(marker_server, name, x, y):
    marker = InteractiveMarker()
    marker.header.frame_id = "/map"
    marker.name = name
    marker.pose.position.x = x
    marker.pose.position.y = y
    box_marker = Marker()
    box_marker.type = Marker.CUBE
    box_marker.scale.x = 0.05
    box_marker.scale.y = 0.05
    box_marker.scale.z = 0.05
    box_marker.color.r = 1.0
    box_marker.color.g = 0.0
    box_marker.color.b = 1.0
    box_marker.color.a = 0.8
    box_control = InteractiveMarkerControl()
    box_control.always_visible = True
    box_control.markers.append( box_marker )
    marker.controls.append( box_control )
    move_control = InteractiveMarkerControl()
    move_control.orientation.w = 1.0
    move_control.orientation.x = 1.0
    move_control.orientation.y = 0.0
    move_control.orientation.z = 0.0
    move_control.name = "move_%s_x" % name
    move_control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
    marker.controls.append(move_control)
    move_control = InteractiveMarkerControl()
    move_control.orientation.w = 1.0
    move_control.orientation.x = 0.0
    move_control.orientation.y = 0.0
    move_control.orientation.z = 1.0
    move_control.name = "move_%s_z" % name
    move_control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
    marker.controls.append(move_control)
    marker_server.insert(marker, processFeedback)
    marker_server.applyChanges()

def publish_markers(tf_broadcaster, marker_server):
    markers = get_markers()
    for (marker_name, marker_coords) in markers.items():
        if not "%s_move_nav" % marker_name in interactive_markers:
            create_interactive_marker(marker_server, "%s_move_nav" % (marker_name), marker_coords[0], marker_coords[1])
            interactive_markers.append("%s_move_nav" % marker_name)
        publish_coord_tf(tf_broadcaster, marker_name, marker_coords[0], marker_coords[1])

def publish_service_areas(tf_broadcaster, marker_server):
    global interactive_markers
    areas = get_service_areas()
    for area in areas:
        if not "%s_move_area" % area.name in interactive_markers:
            create_interactive_marker(marker_server, "%s_left_area" % (area.name), area.left_point[0], area.left_point[1])
            create_interactive_marker(marker_server, "%s_right_area" % (area.name), area.right_point[0], area.right_point[1])
            interactive_markers.append("%s_move_area" % area.name)
        publish_coord_tf(tf_broadcaster, "%s_left" % (area.name), area.left_point[0], area.left_point[1])
        publish_coord_tf(tf_broadcaster, "%s_right" % (area.name), area.right_point[0], area.right_point[1])

def update():
    global to_update
    for m in to_update.values():
        print m
        if m["type"] == "nav":
            rospy.set_param('youbot_navigation_ai_re/markers/marker%d/x-pos' % m["id"], m["x"])
            rospy.set_param('youbot_navigation_ai_re/markers/marker%d/y-pos' % m["id"], m["y"])
        elif m["type"] == "area":
            sub_typ = m["sub_type"]
            rospy.set_param('youbot_manipulation_ai_re/service_areas/service_area%d/%sPointX' % (m["id"], sub_typ), m["x"])
            rospy.set_param('youbot_manipulation_ai_re/service_areas/service_area%d/%sPointY' % (m["id"], sub_typ), m["y"])
    to_update.clear()
    
if __name__ == "__main__":
    rospy.init_node("marker_publisher")
    markers = get_markers()
    areas = get_service_areas()
    marker_server = InteractiveMarkerServer("navigation_markers")
    br = tf.TransformBroadcaster()
    while not rospy.is_shutdown():
        publish_markers(br, marker_server)
        publish_service_areas(br, marker_server)
        update()
