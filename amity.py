class Amity(object):
    def __init__(self, offices=[], living_spaces=[], fellows=[], staff=[]):
        self.offices=offices
        self.living_spaces=living_spaces
        self.fellows = fellows
        self.staff = staff
    def add_person(self,firstname,lastname, role, wants_accomodation="No"):
        pass
        # try:
        #     fellow={}
        #     staff={}
        #     fellow_counter=0
        #     names =[]
        #     roles=["fellow", "staff", "F","S"]
        #     names.append(firstname)
        #     names.append(lastname)
        #     wants_accomodation_options=["Y", "N"]
        #     if role not in roles:
        #         print("please enter a valid role.")
        #     else:
        #         if wants_accomodation not in wants_accomodation_options:
        #             print("please input a Y or N for wants accomodation")
        #         else:
        #             for name in names:
        #                 if not isinstance(name, str):
        #                     print("please input valid names")
        #                 else:
        #                     if role=="fellow":
        #                         if wants_accomodation= "Y"
        #                             fellow_id = "F"+str(fellow_counter+1)
        #                             fellow["id"]=fellow_id
        #                             fellow["name"]=firstname + " "+ lastname
        #                             fellow["office"]=self.allocate_office(fellow_id)
        #                             fellow["living_space"]=self.allocate_living_space(fellow_id)
        #                             self.fellows.append(Fellow)
# 




    def create_room(self,type, name,*args):
        pass
    def allocate_office(self, id):
        #to be called by create person so office assignment is done when creating people
        pass
    def allocate_living_space(self, fellow_id, room_name):
        pass
    def reallocate_living_space(self, fellow_id, room_name):
        pass
    def reallocate_office(self, id, room_name ):
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

