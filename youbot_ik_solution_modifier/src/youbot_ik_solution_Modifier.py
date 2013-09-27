#!/usr/bin/env python
'''
@author: Jens Huebner j-k.huebner25@ostfalia.de
@note: Provides a Simple Filter for the inverse kinematic.
       This filter extends the IkControl class, so that you can change the joint angulars
       manual.
@version: 1.0 beta
'''
import roslib; roslib.load_manifest('youbot_ik_solution_modifier')
import rospy
import copy
import brics_actuator.msg
from youbot_manipulation_scripts.simple_ik_solver_console import IKControl

class youbot_ik_solution_modifier(IKControl):
    def __init__(self):
        self.__unit = 'rad'
        self.__joint_values = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.__joint_offset = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.__joint_uris = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
        self.__modifiedSolutionPublisher = rospy.Publisher('/arm_1/arm_controller/position_command', brics_actuator.msg.JointPositions)
        self.__ikSolutionSubscriber = rospy.Subscriber('ik_modifier_input', brics_actuator.msg.JointPositions, self.ik_modifier_input_callback)
        IKControl.__init__(self, False)
        self.armpub = rospy.Publisher('/ik_modifier_input', brics_actuator.msg.JointPositions)  
    
    def get_joint_values(self):
        return self.__add_Values()
    '''
    @param joint_number: number of the joint, whose angular you want to change.
    @param value: New value of the angular.
    '''
    def set_joint_offset(self, joint_number, value):
        self.__joint_offset[joint_number] = value
        self.__construct_new_brics_msg(self.__add_Values())
    
    '''
    @note: This Function changes the Angular of all Joints absolute.
    @param offset_array: Array with all joint angulars.
    '''
    def set_all_joint_offsets(self, offset_array):
        self.__joint_offset = copy.deepcopy(offset_array)
        self.__construct_new_brics_msg(self.__add_Values())
    
    '''
    @note: This Function changes the Angular of all Joints relative, it adds
           val to the current value to the current angular of the joint.
    @param joint_number: number of the joint, whose angular you want to change.
    @param val: 
    '''    
    def add_joint_offset(self, joint_number, val):
        self.__joint_offset[joint_number] += val
        self.__construct_new_brics_msg(self.__add_Values())
    
    '''
    @note: Changes all Angulars of all Joints absolute. Replaces the old values
           with the values in the offset_array.
    @param offset_array: Array with new Values for all Joints 
    '''
    def add_all_joint_offsets(self, offset_array):
        self.__joint_offset = copy.deepcopy(offset_array)
        self.__construct_new_brics_msg(self.__add_Values())
    
    '''
    @note: Callback function for the ik_modifier_input topic.
           Saves the data of the current message in __joint_values, adds
           self.__joint_offset to the angulars
    @param data: data 
    '''
    def ik_modifier_input_callback(self, data):
        for i in range(len(data.positions)):
            self.__joint_values[i] = data.positions[i].value
            data.positions[i].value += self.__joint_offset[i]
        self.__modifiedSolutionPublisher.publish(data)
        
    '''
    @note: This function adds the __joint_values and the __joint_offset array
    @return: result of the summation
    '''
    def __add_Values(self):
        result = [0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(len(self.__joint_offset)):
            result[i] = self.__joint_values[i] + self.__joint_offset[i]
        return result
    
    '''
    @note: creates a new brics_actuator message and publishes the created message
    @param values: Array with new angular of all joints.
    '''
    def __construct_new_brics_msg(self, values):
        msg = brics_actuator.msg.JointPositions()
        for i in range(len(self.__joint_uris)):
            pos = brics_actuator.msg.JointValue()
            pos.joint_uri = self.__joint_uris[i]
            pos.timeStamp = rospy.Time.now()
            pos.value = values[i]
            pos.unit = 'rad'
            msg.positions.append(pos)
        self.__modifiedSolutionPublisher.publish(msg)
        
if __name__ == '__main__':
    rospy.init_node('youbot_ik_solution_modifier')
    try:
        ik = youbot_ik_solution_modifier()
        ik.drive_to_front(10.0)
        ik.drive_to_front(10.0)
        while(1):
            num = int(raw_input("Enter LinkNumber: "))
            val = float(raw_input("Enter Value: "))
            ik.add_joint_offset(num, val)
    except rospy.ROSInterruptException:
        pass
