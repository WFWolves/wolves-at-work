#!/usr/bin/env python
'''
Created on 08.10.2012

@author: cpupower
'''

import roslib; roslib.load_manifest('youbot_manipulation_scripts')
import rospy
import sensor_msgs.msg
import brics_actuator.msg

MIN_ANGLE_STEP = 0.001
JOINT_MAX = [ 5.8400,  2.6178,  -0.0158,  3.4291,  5.6414]
JOINT_MIN = [0.0101, 0.0101, -5.0264, 0.0222, 0.1107]

class ArmChanger():
    """Allows to change joint angles by using 
    absolute or relative changes for one or multiple joints."""
    def __init__(self, use_saved_jointstate = False, check_reached = True):
        """@param use_saved_jointstate: whether to use last saved joint state
        saved by self.save_joint_state() or the last sensor reading as reference
        for the joint angles.
        @param check_reached: Whether to wait until the joint goal is reported as reached or not"""
        self.joint_names = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
        self.received_state = False
        self.updated_since_last_cmd = False
        self.joint_state = [0, 0, 0, 0, 0]
        self.check_reached = check_reached
        self.use_saved_jointstate = use_saved_jointstate
        self.saved_joint_state = self.joint_state[:]
        self.last_joint_state = self.joint_state[:]
        self.sub_jointstate = rospy.Subscriber('/joint_states', sensor_msgs.msg.JointState, self.cb_jointstate)
        self.pub_arm = rospy.Publisher("/arm_1/arm_controller/position_command", brics_actuator.msg.JointPositions)
    def save_joint_state(self):
        """Saves the current joint state sensor reading, which can be used as reference point"""
        self.saved_joint_state = self.joint_state[:]
    def cb_jointstate(self, msg):
        """Callback method for joint state sensor reading topic.
        @param msg: the message received by the subscriber"""
        self.last_joint_state = self.joint_state[:]
        for k in range(5):
            for i in range(len(msg.name)):
                joint_name = self.joint_names[k]
                if(msg.name[i] == joint_name):
                    self.joint_state[k] = msg.position[i]
                    if self.last_joint_state[k] != self.joint_state[k]:
                        self.updated_since_last_cmd = True
        self.received_state = True
    def is_goal_reached(self, goal, conf):
        """Checks whether the joint goal is reached.
        @param goal: The joint goal which is tested whether it is reached.
        @param conf: The current joint state which is compared to the goal.
        By default it checks whether each absolute angle difference
        is smaller or equal to the MIN_ANGLE_STEP. 
        This method might be overriden to accomplish a different behaviour."""
        for i in range(len(self.joint_names)):
            if (abs(goal[i] - conf[i]) > MIN_ANGLE_STEP):
                return False
        return True
    def get_joint_state(self):
        """Returns the reference joint state which is used to calculate relative angle values.
        @return self.saved_joint_state clone if self.use_saved_jointstate 
        else the last sensor joint state reading"""
        if self.use_saved_jointstate:
            return self.saved_joint_state[:]
        else:
            return self.joint_state
    def change_absolute(self, joint_id, value):
        """Changes one joint identified by its id to an absolute value in radians.
        @param joint_id: The joint id for which the absolute value is given.
        @param value: The absolute angle in radians to which the joint should be set."""
        values = self.get_joint_state()
        values[joint_id] = value
        self.change_absolute_all(values)
    def change_absolute_all(self, joint_values):
        """Sets all joint angles absolute to the values given in joint_values.
        @param joint_values: list of absolute angle values for each joint (in radians)."""
        goal = [0 for i in range(len(self.joint_names))]
        if not self.received_state:
            rospy.logerr("Error: ArmChanger has not recieved a JointState message yet!")
            return
        if not len(joint_values) == len(self.joint_names):
            rospy.logerr("Error: Joint Values given do not have length %d" % len(self.joint_names))
            return
        jpos = brics_actuator.msg.JointPositions()
        for i in range(len(self.joint_names)):
            jval = brics_actuator.msg.JointValue()
            jval.joint_uri = self.joint_names[i]
            if joint_values[i] is not None:
                jval.value = joint_values[i]
            else:
                jval.value = self.get_joint_state()[i]
            jval.value = max(min(jval.value, JOINT_MAX[i]), JOINT_MIN[i])
            if self.use_saved_jointstate:
                self.saved_joint_state[i] = jval.value
            goal[i] = jval.value
            jval.unit = "rad"
            jpos.positions.append(jval)
        self.pub_arm.publish(jpos)
        self.updated_since_last_cmd = False
        if self.check_reached:
            while not self.is_goal_reached(goal, self.joint_state):
                self.pub_arm.publish(jpos)
                rospy.sleep(0.05)
        else:
            self.pub_arm.publish(jpos)
    def change_relative(self, joint_id, value):
        """Changes one joint identified by its id to a relative value in radians.
        @param joint_id: The joint id for which the relative value is given.
        @param value: The relative angle in radians to which the joint should be set."""
        values = [0 for i in range(len(self.joint_names))]
        values[joint_id] = value
        self.change_relative_all(values)
    def change_relative_all(self, joint_values):
        """Sets all joint angles relative to the values given in joint_values.
        @param joint_values: list of relative angle values for each joint (in radians)."""
        assert len(joint_values) == len(self.joint_names)
        values = [joint_values[i] + self.get_joint_state()[i]
                   if joint_values[i] is not None
                   else None 
                  for i in range(len(self.joint_names))]
        self.change_absolute_all(values)

if __name__ == "__main__":
    def main():
        """Main method if the script is directly launched."""
        rospy.init_node("youbot_arm_change", disable_signals = True)
        armc = ArmChanger()
        rospy.loginfo("Waiting for initial joint_state...")
        while not armc.received_state:
            rospy.sleep(.1)
        rospy.loginfo("Initial joint_state recieved!")
        rospy.sleep(.5)
        
        while 1:
            change = float(raw_input("Relative Joint 0: "))
            print "Updated since last cmd:", str(armc.updated_since_last_cmd)
            armc.change_relative(0, change)
    main()
    
