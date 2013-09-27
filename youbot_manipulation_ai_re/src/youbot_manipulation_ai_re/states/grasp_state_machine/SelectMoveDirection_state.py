'''
@author:
@version: 0.0.1 prealpha
@note:
'''
import smach
class SelectMoveDirection(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['move robot'],
                             input_keys=['status_in', 'left_angle_in', 'right_angle_in'],
                             output_keys=['direction_out'])
        self.__direction = 'L'
    def execute(self, userdata):
        if userdata.status_in == 'InBounds':
            userdata.direction_out = self.__direction
        elif userdata.status_in == 'OutOfRight':
            self.__direction = 'L'
            userdata.direction_out = self.__direction
        elif userdata.status_in == 'OutOfLeft':
            self.__direction = 'R'
            userdata.direction_out = self.__direction
        return 'move robot'
