'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note:
'''

class service_area:
    def __init__(self, name, h, x_pos, y_pos, lp, rp, o):
        self.name = name
        self.height = h
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.orientation = o
        self.left_point = lp
        self.right_point= rp