'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: Global data of the state machine
'''
from youbot_manipulation_vision import msg
class global_data():
    def __init__(self):
        pass
    ik = None
    pubVel = None
    subImage = None
    objects = []
    allObjects = []