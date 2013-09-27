#!/usr/bin/env python
"""Youbot Open Gripper
@Author: Alexander Gabel
"""
from time import sleep
import roslib; roslib.load_manifest('youbot_manipulation_scripts')
import rospy
from youbot_manipulation_scripts.simple_ik_solver_console import IKControl

if __name__ == "__main__":
    def main():
        """Main method - Starts the ros node and opens the gripper"""
        rospy.init_node("open_gripper")
        ikc = IKControl(False)
        rospy.sleep(2.0)
        ikc.open_gripper()
    main()
