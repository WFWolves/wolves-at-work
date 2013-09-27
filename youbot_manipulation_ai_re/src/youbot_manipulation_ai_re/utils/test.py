#!/usr/bin/python
'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@note: This class represents the task specification
'''
class task_specification:
    
    def __init__(self):
        self.__initial_place = ''
        self.__source = ''
        self.__destination = ''
        self.__final_place = ''
        self.__formation = ''
        self.__objects = ''
        self.__dictionary = {'Big alu profile' : 'M20'}
    
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
    
    def get_objects(self):
        return self.__objects
    
    def set_objects(self, objs):
        self.__objects = objs
        
    def get_final_place(self):
        return self.__final_places
    
    def set_final_place(self, fin):
        self.__final_place = fin
    '''
    @note: Uebersetzt die Namen der Objekte aus der Vision 
    '''
    def translate_object_names(self, name):
        return self.__dictionary.get(name)
t = task_specification()
print 'Hallo, ', t.translate_object_names(['Big alu profile'])