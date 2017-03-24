from abc import ABCMeta, abstractmethod
class Room(metaclass=ABCMeta):
    def __init__(self, name, max_members, no_of_members = 0 ):
        self.name = name
        self.max_members=max_members
        self.no_of_members=no_of_members

    @abstractmethod
    def __str__(self):
        pass

        