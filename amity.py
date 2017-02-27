class Amity(object):
    def __init__(self):
        pass
    def add_person(self,firstname,lastname, role, wants_accomodation="No"):
        pass

    def create_room(self,type, name,*args):
        pass
    def allocate_office_room(self):
        #to be called by create person so office assignment is done when creating people
        pass
    def allocate_living_space(self):
        pass
    def reallocate_room(self, id, room_name):
        pass
    def load_people(self):
        pass
    def print_allocations(self):
        pass
    def print_unallocations(self):
        pass
    def print_room(self):
        pass
    def save_state(self):
        pass
    def load_state(self):
        pass

