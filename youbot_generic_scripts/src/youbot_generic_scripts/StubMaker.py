#!/usr/bin/env python
"""Youbot Generic Script: StubMaker
Creates stub versions of instance methods
@Author: Alexander Gabel
"""

def create_methods_stub(instance, debug = False):
    """Creates automatically stub versions of all methods of the first baseclass of the given instance"""
    import new #for creating new methods
    import inspect #to check whether the attribute is a method
    def make_override_method(methodname):
        """This creates a method that overrides a method from a base class"""
        def override_method(*args, **kwargs):
            """This method overrides a method from a base class and was generated by create_methods_stub"""
            instance.method_wrapper(methodname, args, kwargs)
        return override_method
    def add_method(method, name = None):
        """Adds a method to the instance"""
        if name is None:
            name = method.func_name
        setattr(instance.__class__, name, method)
    baseclass = instance.__class__.__bases__[0]
    for prop in dir(instance.__class__): #go through all attributes of the class
        if prop in dir(baseclass): #check if the property is inherited by base class
            attr = getattr(instance.__class__, prop)
            if inspect.ismethod(attr): #check if property is a method
                basemethod = getattr(baseclass, prop)
                origmethod = attr
                if origmethod.im_func is basemethod.im_func: #check if the method is not already overriden
                    if debug:
                        print "Method override: %s" % origmethod.im_func.func_name
                    override_method = make_override_method(prop)
                    add_method(override_method, prop)