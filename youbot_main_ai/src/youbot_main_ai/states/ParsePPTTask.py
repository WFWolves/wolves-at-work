import smach
import rospy
import copy
import traceback

from youbot_transportation_ai.utils.task_specification import transportation_task_specification, transportation_situation, transportation_place

#PPT<S1,(M20, S_40_40_G),S2>

class ParsePPTTask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['parsed', 'parseFailed'],
                                   input_keys=['refbox_message_in'],
                                   output_keys=['taskspec_out'])
    def parse_task(self, task):
        rospy.loginfo("PPT Taskspec: %s", task)
        tasktype = task.split("<",1)[0]
        assert tasktype == "PPT"
        task=task[4:-1] #remove 'PPT<' and '>'
        src = task.split(",",1)[0].strip()
        dst = "S1"#task.split(",")[-1].strip()
        objects_str = task.split("(",1)[1].split(")",1)[0]
        objects = objects_str.split(",")
        objects = [obj.strip() for obj in objects]
        for i in range(len(objects)):
            if objects[i] == "R20":
                objects[i] = "V20"
            
        situation_initial = transportation_situation(transportation_situation.SITUATION_INITIAL)
        situation_goal = transportation_situation(transportation_situation.SITUATION_GOAL)
        
        src_place = transportation_place(src, None, objects[:])
        dst_place = transportation_place(dst, "line", objects[:])
        situation_initial.add_place(src_place)
        situation_goal.add_place(dst_place)
        task_spec = transportation_task_specification(situation_initial, situation_goal)
        return task_spec
    def execute(self, userdata):
        msg = userdata.refbox_message_in
        try:
            userdata.taskspec_out = self.parse_task(msg)
            return 'parsed'
        except:
            rospy.logerr("Failed parsing PPT Taskspec: %s", traceback.format_exc())
            return 'parseFailed'
