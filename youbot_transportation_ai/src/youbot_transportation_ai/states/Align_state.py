# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:24:19 2013

@author: jens
"""

import smach
import rospy
import actionlib

from youbot_scanner_alignment.msg import AlignedDrivingAction, AlignedDrivingGoal


class Align(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','failed'],
                             input_keys=[],
                             output_keys=[])
        self.align_client = actionlib.SimpleActionClient('aligned_driving', AlignedDrivingAction)
        rospy.loginfo("Waiting for aligned_driving action server...")
        self.align_client.wait_for_server()
    def execute(self, userdata):
        rospy.loginfo("Waiting for aligned_driving action server...")
        self.align_client.wait_for_server()
        goal = AlignedDrivingGoal()
        goal.front_distance = 0.05
        goal.tolerance = 0.005
        goal.side_difference = 0.0
        rospy.loginfo("Sending aligned_driving goal...")
        self.align_client.send_goal(goal)
        rospy.loginfo("Waiting for aligned_driving to finish...")
        self.align_client.wait_for_result(rospy.Duration.from_sec(0.0))
        #TODO check action result/status
        return 'succeeded'
