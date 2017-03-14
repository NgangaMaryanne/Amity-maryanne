class Person(object):
    # __metaclass__=ABCMeta
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name
