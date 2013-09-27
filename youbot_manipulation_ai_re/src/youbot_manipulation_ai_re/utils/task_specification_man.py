#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: This class represents the task specification
'''
class TaskSpecificationMan(object):
    
    def __init__(self, c_s_a, objs):
        self.__current_service_area = c_s_a
        self.__objects = objs
        self.__dictionary = {'Big alu profile' : 'S40_40_B',
                             'Thin alu profile': 'F20_20_B',
                             'Rough small cylinder': 'V20',
                             'Smooth small cylinder': 'V20',
                             #'Rough small cylinder': 'R20',
                             '': 'F_20_20_G',
                             '': 'S_40_40_G',
                             'Big Screw': 'M20_10',
                             '': 'M20_180'}
    
    def get_current_service_area(self):
        return self.__current_service_area
    
    def set_current_service_area(self, c_s_a):
        self.__current_service_area = c_s_a
    
    def get_objects(self):
        return self.__objects
    
    def set_objects(self, objs):
        self.__objects = objs
        
    '''
    @note: Uebersetzt die Namen der Objekte aus der Vision 
    '''
    def translate_object_names(self, name):
        return self.__dictionary.get(name)
        
    current_service_area = property(get_current_service_area, set_current_service_area)
    
