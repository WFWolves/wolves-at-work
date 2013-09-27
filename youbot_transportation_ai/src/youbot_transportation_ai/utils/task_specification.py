class transportation_task_specification(object):
    def __init__(self, initialsituation, goalsituation):
        self.__initialsituation = initialsituation
        self.__goalsituation = goalsituation
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<%s: Initial: %s, Goal: %s>" % (self.__class__.__name__,
                                                str(self.initialsituation),
                                                str(self.goalsituation) )
    def get_initialsituation(self):
        return self.__initialsituation
    def get_goalsituation(self):
        return self.__goalsituation
    initialsituation = property(get_initialsituation)
    goalsituation = property(get_goalsituation)

class transportation_situation(object):
    SITUATION_INITIAL = 1
    SITUATION_GOAL = 2
    def __init__(self, situationtype):
        assert situationtype == transportation_situation.SITUATION_INITIAL or \
               situationtype == transportation_situation.SITUATION_GOAL
        self.__situationtype = situationtype
        self.__places = []
    def __str__(self):
        return repr(self)
    def __repr__(self):
        sittype = None
        if self.situationtype == transportation_situation.SITUATION_INITIAL:
            sittype = "SITUATION_INITIAL"
        elif self.situationtype == transportation_situation.SITUATION_GOAL:
            sittype = "SITUATION_GOAL"
        return "<%s: %s, %s>" % (self.__class__.__name__,
                                 sittype,
                                 str(tuple(self.places)))
    def get_situationtype(self):
        return self.__situationtype
    def get_places(self):
        return tuple(self.__places) #immutable
    def add_place(self, place):
        self.__places.append(place)
    def remove_place(self, place):
        self.__places.remove(place)
    def pop_place(self, index):
        return self.__places.pop(index)
    situationtype = property(get_situationtype)
    places = property(get_places)

class transportation_place(object):
    def __init__(self, name, alignment = None, objects = None):
        self.__name = name
        self.__alignment = alignment
        self.__objects = objects
        if objects is None:
            self.__objects = []
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<%s: %s, %s, %s>" % (self.__class__.__name__,
                                     self.name,
                                     self.alignment,
                                     str(tuple(self.objects)))
    def get_name(self):
        return self.__name
    def get_alignment(self):
        return self.__alignment
    def get_objects(self):
        return tuple(self.__objects) #immutable
    def add_object(self, obj):
        self.__objects.append(obj)
    def remove_object(self, obj):
        self.__objects.remove(obj)
    def pop_object(self, index):
        return self.__objects.pop(index)
    name = property(get_name)
    alignment = property(get_alignment)
    objects = property(get_objects)
