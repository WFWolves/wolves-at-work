'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: If no Object was detected, this state lookes for Objects on the Service Area.
'''
import smach
from time import sleep

class SelectShape(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'])
        
    def execute(self, userdata):
        return 'done'
