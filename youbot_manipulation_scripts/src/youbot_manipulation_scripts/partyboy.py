#!/usr/bin/env python
"""Youbot Partyboy script - Moves the arm for the partyboy theme song
@Author: Alexander Gabel
"""
from time import sleep
import roslib; roslib.load_manifest('youbot_manipulation_scripts')
import rospy
from youbot_manipulation_scripts.simple_ik_solver_console import IKControl

if __name__ == "__main__":
    def main():
        """Main method - Starts the ros node and runs the main loop"""
        rospy.init_node("partyboy")
        ikc = IKControl()
        while 1:
            ikc.drive_to_top(False)
            sleep(2)
            ikc.change_pos({'yaw': 0.378, 'pitch': 1.387, 'y': -0.0459, 'x': 0.029, 'z': 0.378, 'roll': 0.29})
            sleep(2)
    main()