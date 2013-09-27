#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: This class represents the task specification
'''
class task_specification(object):
    
    def __init__(self):
        self.__initial_place = ''
        self.__source = ''
        self.__destination = ''
        self.__final_place = ''
        self.__formation = ''
        self.__objects = []
        self.__dictionary = {'Big alu profile' : 'S40_40_B',
                             'Thin alu profile': 'F20_20_B',
                            ## 'Rough small cylinder': 'R20',
                             'Rough small cylinder': 'V20',
                             'Smooth small cylinder': 'V20',
                             '': 'F_20_20_G',
                             '': 'S_40_40_G',
                             'Big Screw': 'M20_10',
                             '': 'M20_180'}
    
    def get_initial_place(self):
        return self.__initial_place
    
    def set_initial_place(self, init):
        self.__initial_place = init
    
    def get_source(self):
        return self.__source
    
    def set_source(self, src):
        self.__source = src
    
    def get_destination(self):
        return self.__destination
    
    def set_destination(self, dest):
        self.__destination = dest
    
    def get_formation(self):
        return self.__formation
    
    def set_formation(self, form):
        self.__formation = form
        
    def remove_object(self, obj):
	if obj in self.__objects:
            self.__objects.remove(obj)
            return True
        else:
            return False
        
    def add_object(self, obj):
        self.__objects.append(obj)
    
    def get_objects(self):
        return self.__objects
    
    def set_objects(self, objs):
        self.__objects = objs
        
    def get_final_place(self):
        return self.__final_place
    
    def set_final_place(self, fin):
        self.__final_place = fin
    '''
    @note: Uebersetzt die Namen der Objekte aus der Vision 
    '''
    def translate_object_names(self, name):
        return self.__dictionary.get(name)
    
    initial_place = property(get_initial_place, set_initial_place)
    source = property(get_source, set_source)
    destination = property(get_destination, set_destination)
    formation = property(get_formation, set_formation)
    objects = property(get_objects,set_objects)
    final_place = property(get_final_place, set_final_place)
    
