'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''

class object_data:
    def __init__(self, dist_x, dist_y, a, h, w, rOl ):
        self.distance_to_center_x = dist_x
        self.distance_to_center_y = dist_y
        self.height = h
        self.width = w
        self.angle = a
        self.right_or_left_rotation = rOl