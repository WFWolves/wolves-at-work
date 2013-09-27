#!/usr/bin/env python
"""Youbot Close Gripper
@Author: Alexander Gabel
"""
from time import sleep
import roslib; roslib.load_manifest('youbot_manipulation_scripts')
import rospy
from youbot_manipulation_scripts.simple_ik_solver_console import IKControl

if __name__ == "__main__":
    def main():
        """Main method - Starts the ros node and closes the gripper"""
        rospy.init_node("close_gripper")
        ikc = IKControl(False)
        rospy.sleep(2.0)
        ikc.close_gripper()
    main()
