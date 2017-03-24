from room import Room
class Office(Room):

    def __init__(self, name, no_of_members = 0 , max_members =6):
        super(Office, self).__init__(name, max_members, no_of_members=0)

    def __str__(self):
        pass