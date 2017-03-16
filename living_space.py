from room import Room
class LivingSpace(Room):
    def __init__(self, name, no_of_members=0 , max_members=4 ):
        super(LivingSpace, self).__init__(name, max_members, no_of_members=0)