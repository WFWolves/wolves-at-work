import smach
import rospy
import copy

class SelectTask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['taskBNT', 'taskBMT', 'taskBTT', 'taskPPT', 'taskUnknown'],
                                   input_keys=['refbox_message_in'])
    def execute(self, userdata):
        msg = userdata.refbox_message_in
        if msg.startswith("BNT"):
            return "taskBNT"
        elif msg.startswith("BMT"):
            return "taskBMT"
        elif msg.startswith("BTT"):
            return "taskBTT"
        elif msg.startswith("PPT"):
            return "taskPPT"
        else:
            return "taskUnknown"
