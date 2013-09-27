'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: 
'''
import smach
from time import sleep

class store_object(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['Object stored', 'failed'])
        
    def execute(self, userdata):
        return 'Object stored'