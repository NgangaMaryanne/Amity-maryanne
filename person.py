from abc import ABCMeta, abstractmethod
class Person(metaclass=ABCMeta):
    def __init__(self, person_id, name, role):
        self.person_id = person_id
        self.name = name
        self.role = role

    @abstractmethod   
    def __str__ (self):
        pass