import smach
import rospy
import copy
import traceback

from youbot_navigation_ai_re.utils.task_specification import task_specification_navigation, navigation_target

#BNT<(D1,N,3)(S1,W,3)(T1,E,3)>

class ParseBNTTask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['parsed', 'parseFailed'],
                                   input_keys=['refbox_message_in'],
                                   output_keys=['taskspec_out'])
    def parse_place(self, place_str):
        place = place_str.strip()[1:] #remove heading '('
        print place
        marker, orientation, sleeptime = place.split(",")
        sleeptime = int(sleeptime)
        return navigation_target(marker, orientation, sleeptime)
    def parse_task(self, task_str):
        rospy.loginfo("BNT Taskspec: %s", task_str)
        test, spec = task_str.split("<")
        assert test == "BNT"
        spec = spec.strip()[:-1] #remove trailing '>'
        places = spec.split(")")[:-1] #remove last (empty) element
        
        taskspec = task_specification_navigation()
        for place in places:
            taskspec.add_target(self.parse_place(place))
        return taskspec
    def execute(self, userdata):
        msg = userdata.refbox_message_in
        try:
            userdata.taskspec_out = self.parse_task(msg)
            return 'parsed'
        except:
            rospy.logerr("Failed parsing BNT Taskspec: %s", traceback.format_exc())
            return 'parseFailed'
