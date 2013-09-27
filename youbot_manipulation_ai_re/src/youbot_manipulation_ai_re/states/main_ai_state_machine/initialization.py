import smach
import copy
import rospy

#TODO: Replace constants by ROS Parameters
MARKER_INIT_ORIENTATION = "S"
MARKER_FIN_ORIENTATION = "N"

#FIXME ROS Const Hack
def const_hack(obj):
    while type(obj) == smach.user_data.Const:
        obj = obj._obj
    return obj

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done',],
                             input_keys=[],
                             output_keys=['task_specification_out',
                                          'dest_object_counter_out', 
                                          'alignment_out',
                                          'marker_init_out',
                                          'marker_src_out',
                                          'marker_dst_out',
                                          'marker_fin_out',
                                          'orientation_init_out',
                                          'orientation_src_out',
                                          'orientation_dst_out',
                                          'orientation_fin_out'],
                             io_keys=['task_specification_io'])
    def execute(self, userdata):
        service_areas = self.get_service_areas()
        userdata.task_specification_io = const_hack(userdata.task_specification_io)
        userdata.task_specification_out = userdata.task_specification_io
        userdata.dest_object_counter_out = 0
        init = userdata.task_specification_io.initial_place
        src = userdata.task_specification_io.source
        dst = userdata.task_specification_io.destination
        fin = userdata.task_specification_io.final_place
        form = userdata.task_specification_io.formation
        userdata.alignment_out = form
        userdata.marker_init_out = init
        userdata.marker_src_out = src
        userdata.marker_dst_out = dst
        userdata.marker_fin_out = fin
        print "[ManipulationAI] initial: %s, source: %s, dest: %s, formation: %s, final: %s" % (init, src, dst, form, fin)
        userdata.orientation_init_out = MARKER_INIT_ORIENTATION
        userdata.orientation_src_out = service_areas[src][0]
        userdata.orientation_dst_out = service_areas[dst][0]
        userdata.orientation_fin_out = MARKER_FIN_ORIENTATION
        return 'done'
    def get_service_areas(self):
        service_areas = {}
        try:
            service_area_count = int(rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area_count'))
        except ValueError:
            rospy.logerr("serviceAreaCount could not be parsed into an integer!")
            return None
        for i in range(service_area_count):
            try:
                name = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area%d/name' % (i+1))
                orientation = rospy.get_param('youbot_manipulation_ai_re/service_areas/service_area%d/orientation' % (i+1))
                service_areas[name] = (orientation,)
            except KeyError:
                rospy.logerr("Parameter for service_area %d was not found, but service_area_count is %d", i, service_area_count)
                continue
        return service_areas
