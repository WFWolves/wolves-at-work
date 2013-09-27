#!/usr/bin/python

class task_specification_navigation(object):
    TASK_ID = "BNT"
    def __init__(self):
        self.__targets = []
    def __str__(self):
        targets = ""
        for target in self.__targets:
            targets += str(target)
        return "%s<%s>" % (task_specification_navigation.TASK_ID, targets)
    def get_target_count(self):
        return len(self.__targets)
    def get_targets(self):
        return tuple(self.__targets)
    def get_target(self, num):
        return self.__targets[num]
    def add_target(self, target):
        self.__targets.append(target)
    def remove_target_at(self, num):
        return self.__targets.pop(num)
    targets = property(get_targets)
        
class navigation_target(object):
    def __init__(self, marker = None, orientation = None, sleeptime = None):
        self.__marker = marker
        self.__orientation = orientation
        self.__sleeptime = sleeptime
    def __str__(self):
        return "(%s,%s,%d)" % (self.__marker, self.__orientation, self.__sleeptime)
    def get_orientation(self):
        return self.__orientation
    def get_marker(self):
        return self.__marker
    def get_sleeptime(self):
        return self.__sleeptime
    def set_orientation(self, orientation):
        self.__orientation = orientation
    def set_marker(self, marker):
        self.__marker = marker
    def set_sleeptime(self, sleeptime):
        self.__sleeptime = sleeptime
    orientation = property(get_orientation, set_orientation)
    marker = property(get_marker, set_marker)
    sleeptime = property(get_sleeptime, set_sleeptime)
    
