from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff


class Amity(object):

    def __init__(self, offices=[], living_spaces=[], fellows=[], staff=[], staff_counter=0, fellow_counter=0):
        self.offices = offices
        self.living_spaces = living_spaces
        self.fellows = fellows
        self.staff = staff
        self.fellow_counter = fellow_counter
        self.staff_counter = staff_counter

    def add_person(self, firstname, lastname, role, wants_accomodation="N"):
        try:
            fellow = {}
            staff = {}
            roles = ["fellow", "staff", "F", "S"]
            wants_accomodation_options = ["Yes", "N", "Y" "No", None]
            if type(firstname) != str or type(lastname) != str:
                print("Please enter valid names.")
            else:
                if role not in roles:
                    return "Please enter valid role."
                else:
                    if role == "fellow" or role == "F":
                        fellow_name = firstname + " " + lastname
                        self.fellow_counter = self.fellow_counter+1
                        fellow_id = "F"+str(self.fellow_counter)
                        fellow["id"] = fellow_id
                        fellow["name"] = fellow_name
                        fellow["office"] = self.allocate_office(fellow_id)
                        if wants_accomodation == "Yes" or wants_accomodation == "Y":
                            fellow["living_space"] = self.allocate_living_space(
                                fellow_id, "topaz")

                        elif wants_accomodation == "no" or wants_accomodation == "N":
                            pass
                        else:
                            print(
                                "invalid accomodation option, fellow created but not assigned living space.")
                        self.fellows.append(fellow)
                        fellow = Fellow()
                    else:
                        self.staff_counter = self.staff_counter + 1
                        staff_id = "S" + str(self.staff_counter)
                        staff["id"] = staff_id
                        staff["name"] = firstname + " " + lastname
                        staff["office"] = self.allocate_office(staff_id)
                        self.staff.append(staff)
                        staff = Staff()
                        if wants_accomodation == "yes" or wants_accomodation == "Y":
                            print(
                                "Staff does not get living space. staff created with no living space.")
                        elif wants_accomodation == "no" or wants_accomodation == "N":
                            pass
                        else:
                            print("invalid accomodation")

        except():
            return "Please try again"

    def create_room(self, room_type, name, *argv):
        try:
            count =0
            argv = list(argv)
            all_rooms = self.offices + self.living_spaces
            office_dict={}
            living_dict = {}
            if argv ==[]:
                if isinstance(room_type, str):
                    if isinstance(name, str):
                        if room_type == "living_space":
                            living_dict["name"]=name
                            living_dict["max_numbers"]=4
                            living_dict["no_of_members"]=0
                            self.living_spaces.append(living_dict)
                        elif room_type =="office":
                            office_dict["name"]=name
                            office_dict["max_numbers"]=6
                            office_dict["no_of_members"]=0
                            self.offices.append(office_dict)
                        else:
                            print("Please input a room type of either office or living space.")
                    else:
                        print("room name should be a string.")
                else:
                    print("Room type should be a string.")
            else:
                if isinstance(room_type, str):
                    if isinstance(name, str):
                        if room_type == "living_space":
                            living_dict["name"]=name
                            living_dict["max_numbers"]=4
                            living_dict["no_of_members"]=0
                            self.living_spaces.append(living_dict)
                            for arg in argv:
                                if isinstance(arg, str):
                                    living_dict={}
                                    living_dict["name"]=arg
                                    living_dict["max_numbers"]=4
                                    living_dict["no_of_members"]=0
                                    self.living_spaces.append(living_dict)
                                else:
                                    print("one of your living room names is not a string. please change that.")

                        elif room_type =="office":
                            office_dict["name"]=name
                            office_dict["max_numbers"]=6
                            office_dict["no_of_members"]=0
                            self.offices.append(office_dict)
                            for arg in argv:
                                if isinstance(arg, str):
                                    office_dict={}
                                    office_dict["name"]=arg
                                    office_dict["max_numbers"]=6
                                    office_dict["no_of_members"]=0
                                    self.offices.append(office_dict)
                                else:
                                    print("One of your office names is not a string please retry.")
                        else:
                            print("Please input a room type of either office or living space.")
                    else:
                        print("room name should be a string.")
                else:
                    print("Room type should be a string.")
                    
        except():
            print("Failed.")
        

    def allocate_office(self, id):
        # to be called by create person so office assignment is done when
        # creating people
        return "camelot"

    def allocate_living_space(self, fellow_id, room_name):
        return "topaz"

    def reallocate_living_space(self, fellow_id, room_name):
        pass

    def reallocate_office(self, id, room_name):
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

a = Amity()
a.add_person("maryanne", "Nganga", "fellow", "Y")
a.add_person("jane", "Ngugi", "fellow", "N")
a.add_person("jake", "Kimani", "staff", "Y")
a.add_person("joyce", "wangare", "staff")
a.add_person([], "Wambui", "F", 6)


a.create_room("sitting_room", "narnia")
a.create_room("office", "narnia", "hogwarts","platform", 8)
a.create_room("living_space", "ruby")

a.create_room(1, "narnia")
a.create_room("office", 1)
a.create_room("living_space", [])
a.create_room("living_space", "emerald", "diamond", "quartz", 4)
a.create_room("living_space", "topaz")
print(a.staff)
print(a.fellows)
print(a.living_spaces)
print(a.offices)
