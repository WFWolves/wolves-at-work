import smach
import rospy
import copy
import traceback

from youbot_manipulation_ai_re.utils.task_specification import task_specification

#BMT<Initial,Source,Dest,align(Part1,Part2),Final>
#BMT<S3,S1,S2,line(M20_100,F20_20_B),T4>

class ParseBMTTask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['parsed', 'parseFailed'],
                                   input_keys=['refbox_message_in'],
                                   output_keys=['taskspec_out'])
    def parse_task(self, task_str):
        rospy.loginfo("BMT Taskspec: %s", task_str)
        test, spec = task_str.split("<")
        assert test == "BMT"
        spec = spec.strip()[:-1] #remove trailing '>'
        initial, source, dest, remaining_spec = spec.split(",", 3)
        place_str, final = remaining_spec.split(")")
        final = final.replace(",", "").strip()
        align, obj_str = place_str.split("(")
        objects = obj_str.split(",")
        
        taskspec = task_specification()
        print "[ParseBMTTask] initial: %s, source: %s, dest: %s, formation: %s, objects: %s, final: %s" % (initial, source, dest, align, objects, final)
        taskspec.initial_place = initial
        taskspec.source = source
        taskspec.destination = dest
        taskspec.formation = align
        taskspec.objects = objects
        taskspec.final_place = final
        
        return taskspec
    def execute(self, userdata):
        msg = userdata.refbox_message_in
        try:
            spec = self.parse_task(msg)
            userdata.taskspec_out = spec
            return 'parsed'
        except:
            rospy.logerr("Failed parsing BMT Taskspec: %s", traceback.format_exc())
            return 'parseFailed'
