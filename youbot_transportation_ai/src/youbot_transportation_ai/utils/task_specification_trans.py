# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:56:00 2013

@author: jens
"""

class task_specification_trans:
    def __init__(self):
        self.initial_situation = []
        self.goal_situation = []
        
class place:
    def __init__(self, al, pl, objs):
        self.alignment = al
        self.place = pl
        self.obj = objs