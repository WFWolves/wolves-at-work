import smach
import rospy
import copy
import traceback

from youbot_transportation_ai.utils.task_specification import transportation_task_specification, transportation_situation, transportation_place

#BTT<initialsituation(<D1,line(R20)><D2,line(F20_20_G)>);goalsituation(<S2,circle(F20_20_G)><S2,zigzag(R20)>)>

SIT_INIT = "initialsituation"
SIT_GOAL = "goalsituation"

class ParseBTTTask(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['parsed', 'parseFailed'],
                                   input_keys=['refbox_message_in'],
                                   output_keys=['taskspec_out'])
    def parse_task(self, task):
        rospy.loginfo("BTT Taskspec: %s", task)
        tasktype = task.split("<",1)[0]
        assert tasktype == "BTT"
        task=task[4:-1] #remove 'BTT<' and '>'
        situations = task.split(";")
        init_sit = None
        goal_sit = None
        for sit in situations:
            sit = sit.strip()
            sit = sit[:-1] #remove ')'
            sit_name, places_str = sit.split("(",1)
            sit_type = 0
            assert sit_name == SIT_INIT or sit_name == SIT_GOAL
            if sit_name == SIT_INIT:
                sit_type = transportation_situation.SITUATION_INITIAL
            elif sit_name == SIT_GOAL:
                sit_type = transportation_situation.SITUATION_GOAL
            situation = transportation_situation(sit_type)
            for place_str in places_str.split("<")[1:]:
                place_str = place_str.strip()[:-1] #remove '>'
                assert len(place_str) > 0
                place_name, place_info = place_str.split(",",1)
                place_name = place_name.strip()
                assert len(place_name) > 0
                place_alignment, objects_str = place_info.split("(",1)
                place_alignment = place_alignment.strip()
                if place_alignment == "":
                    place_alignment = None
                objects_str = objects_str.strip()[:-1].strip() #remove ')'
                objects_str = objects_str.replace("R20", "V20")
                objects = [obj.strip() for obj in objects_str.split(",")]
                for i in range(len(objects)):
                    if objects[i] == "R20":
                        objects[i] = "V20"
                place = transportation_place(place_name, place_alignment, objects)
                rospy.logdebug("Place: %s", str(place))
                situation.add_place(place)
            if situation.situationtype == transportation_situation.SITUATION_INITIAL:
                init_sit = situation
            elif situation.situationtype == transportation_situation.SITUATION_GOAL:
                goal_sit = situation
        assert init_sit is not None
        assert goal_sit is not None
        task_spec = transportation_task_specification(init_sit, goal_sit)
        rospy.loginfo("BTT parsed Taskspec: %s", str(task_spec))
        return task_spec  
    def execute(self, userdata):
        msg = userdata.refbox_message_in
        try:
            userdata.taskspec_out = self.parse_task(msg)
            return 'parsed'
        except:
            rospy.logerr("Failed parsing BTT Taskspec: %s", traceback.format_exc())
            return 'parseFailed'
