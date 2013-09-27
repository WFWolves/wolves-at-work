import smach
import copy
import rospy


class TaskSpecUpdate(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['nextObject','finished'],
                             input_keys=['current_object_in'],
                             io_keys=['task_specification_io'])
    def execute(self, userdata):
        print "CURRENT OBJECT by GraspAI: ", userdata.current_object_in
        current_object = userdata.task_specification_io.translate_object_names(userdata.current_object_in)
        print "CURRENT OBJECT translated: ", current_object
        #FIXME: The object name given by the GraspAI should be according to the specification of the refereebox.
        
        userdata.task_specification_io.remove_object(current_object)
        if len(userdata.task_specification_io.get_objects()) > 0:
            return 'nextObject'
        else:
            return 'finished'
