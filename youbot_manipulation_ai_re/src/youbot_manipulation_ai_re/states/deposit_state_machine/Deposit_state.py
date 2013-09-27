'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: If no Object was detected, this state lookes for Objects on the Service Area.
'''
import smach
from time import sleep
from youbot_manipulation_ai_re.utils.global_data import global_data

class Deposit(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'])
        
    def execute(self, userdata):
        global_data.ik.open_gripper()
        sleep(3)
        global_data.ik.drive_to_back()
        sleep(3)
        return 'done'
