from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff
import sqlite3


class Amity(object):
    

    def __init__(self, offices=[], living_spaces=[], fellows=[], staff=[],office_allocations = {},living_space_allocations = {}, people_counter=0):
        self.offices = offices
        self.living_spaces = living_spaces
        self.fellows = fellows
        self.staff = staff
        self.office_allocations = office_allocations
        self.living_space_allocations = living_space_allocations
        self.people_counter = people_counter

    def add_person(self, firstname, lastname, role, wants_accomodation="N"):
        try:
            wants_accomodation_options = ["Yes", "N", "Y" "No", None]
            if type(firstname) != str or type(lastname) != str:
                print("Please enter valid names.")
            else:
                if role.lower() in ("fellow", "f"):
                    self.people_counter = self.people_counter +1
                    Fellow.person_id = self.people_counter
                    Fellow.name = firstname + " " + lastname
                    fellow = Fellow( Fellow.person_id, Fellow.name)
                    office = self.allocate_office(Fellow.person_id)

                    allocated_room_names=[]
                    for key in self.office_allocations:
                        allocated_room_names.append(key)
                    if office:
                        if office in allocated_room_names:
                            self.office_allocations[office].append(fellow.__dict__)
                        else:
                            self.office_allocations[office] = [fellow.__dict__]
                        
                    else:
                        print("No available rooms.")
                    self.fellows.append(fellow.__dict__) 

                    if  wants_accomodation.lower() in ("yes", "y"):
                        living_space = self.allocate_living_space(Fellow.person_id)
                        allocated_room_names=[]
                        for key in self.living_space_allocations:
                            allocated_room_names.append(key)
                        if living_space:
                            if living_space in allocated_room_names:
                                self.living_space_allocations[living_space].append(fellow.__dict__)
                            else:
                                self.living_space_allocations[living_space] = [fellow.__dict__]
                            
                        else:
                            print("No available rooms.")



                    
                else:
                    Staff.name = firstname + " " + lastname
                    self.people_counter +=1
                    Staff.person_id = self.people_counter
                    staff = Staff(Staff.person_id, Staff.name)
                    self.staff.append(staff.__dict__)
                    office = self.allocate_office(Staff.person_id)
                    
                    allocated_room_names=[]
                    for key in self.office_allocations:
                        allocated_room_names.append(key)
                    if office:
                        if office in allocated_room_names:
                            self.office_allocations[office].append(staff.__dict__)
                        else:
                            self.office_allocations[office] = [staff.__dict__]
                        
                    else:
                        print("No available rooms.")

                    if wants_accomodation == "yes" or wants_accomodation == "Y":
                        return "Staff does not get living space. staff created with no living space."
                    elif wants_accomodation == "no" or wants_accomodation == "N":
                        pass
                    else:
                        print("invalid accomodation")

        except():
            return "Please try again"

    def create_room(self, room_type, name, *argv):
        try:
            argv = list(argv)
            all_rooms = self.offices + self.living_spaces
            all_room_names = []
            for r in all_rooms:
                all_room_names.append(r["name"].lower())
            if argv == []:
                if isinstance(room_type, str):
                    if isinstance(name, str) and name.lower() not in all_room_names:
                        if room_type == "living_space":
                            LivingSpace.living_space_name= name
                            living_space = LivingSpace(LivingSpace.living_space_name)
                            self.living_spaces.append(living_space.__dict__)
                        elif room_type == "office":
                            Office.office_name = name
                            office = Office(Office.office_name)
                            self.offices.append(office.__dict__)
                        else:
                            return "Please input a room type of either office or living space."
                    else:
                        return "room name should be a string."
                else:
                    print("Room type should be a string.")
            else:
                if isinstance(room_type, str):
                    if isinstance(name, str) and name.lower() not in all_room_names:
                        if room_type == "living_space":
                            LivingSpace.living_space_name= name
                            living_space=LivingSpace(LivingSpace.living_space_name)
                            self.living_spaces.append(living_space.__dict__)

                            for arg in argv:
                                if isinstance(arg, str) and arg.lower() not in all_room_names:
                                    LivingSpace.living_space_name= arg
                                    living_space = LivingSpace(LivingSpace.living_space_name)
                                    self.living_spaces.append(living_space.__dict__)
                                else:
                                    print(
                                        "one of your living room names is not a string. please change that.")

                        elif room_type == "office":
                            Office.office_name = name
                            office = Office(Office.office_name)
                            self.offices.append(office.__dict__)
                            for arg in argv:
                                if isinstance(arg, str) and arg.lower() not in all_room_names:
                                    Office.office_name = arg
                                    office = Office(Office.office_name)
                                    self.offices.append(office.__dict__)
                                else:
                                    print(
                                        "One of your office names is not a string please retry.")
                        else:
                            return "Please input a room type of either office or living space."
                    else:
                        return "room name should be a string."
                else:
                    print("Room type should be a string.")

        except():
            print("Failed.")

    def allocate_office(self, id):
        error_message = "N/A"
        office =next((room for room in self.offices if room["no_of_members"]<room["max_members"]), error_message)
        if office != error_message:
            office["no_of_members"] = office["no_of_members"]+1
            return office["name"]
        else:
            print("No available office rooms.")
            return False


    def allocate_living_space(self, person_id):
        error_message = "N/A"
        living_space =next((room for room in self.living_spaces if room["no_of_members"]<room["max_members"]), error_message)
        if living_space != error_message:
            living_space["no_of_members"] = living_space["no_of_members"]+1
            return living_space["name"]
        else:
            print("No available living spaces")
            return False

    #gets room given room name and tells whether the room is an office or a living space.
    def get_room(self, room_name):
        if isinstance(room_name, str):
            all_rooms = self.offices + self.living_spaces
            this_room ={}
            for room in all_rooms:
                if room["name"].lower()==room_name:
                    break
                    print ("room does not exist.")
            if room["max_members"] == 4:
                this_room["room_type"]="living_space"
                this_room["data"] = room
            else:
                this_room["room_type"]="office"
                this_room["data"] = room
        else:
            return ""
            
        return this_room

    def get_person(self, person_id):
        fellow_ids = []
        staff_ids = []
        this_fellow = {}
        this_staff = {}

        for fellow in self.fellows:
            fellow_ids.append(fellow["person_id"])

        for staff in self.staff:
            staff_ids.append(staff["person_id"])

        if isinstance(person_id, int):
            if person_id in fellow_ids:
                for fellow in self.fellows:
                    if fellow["person_id"]== person_id:
                        break
                this_fellow["role"] ="fellow"
                this_fellow["data"] = fellow
                return this_fellow
            elif person_id in staff_ids:
                for staff in self.staff:
                    if staff["person_id"]== person_id:
                        break
                this_staff["role"]= "staff"
                this_staff["data"]=staff
                return this_staff
            else:
                return "The person ID does not exist please try again."
        else:
            return "Person id is an integer. refer to fellow or staff list."




    def reallocate_room(self, person_id, room_name):
        office_names =[]
        living_space_names = []
        all_people_id = []
        allocated_office_names = [key for key in self.office_allocations]
        allocated_living_space_names = [key for key in self.living_space_allocations]
        for room in self.offices:
            office_names.append(room["name"])

        for room in self.living_spaces:
            living_space_names.append(room["name"])
        if str(room_name) in office_names:
            person = self.get_person(person_id)["data"]
            for key, value in self.office_allocations.items():
                for person in value:
                    if person["person_id"] == person_id:
                        current_room_name = key
                        break
            current_room = [room for room in self.offices if room["name"]== current_room_name]

            print("{0} is in office: {1}" .format(person["name"], current_room_name))
            new_room = self.get_room(room_name)["data"]
            if new_room["no_of_members"] < new_room["max_members"]:
                if new_room in allocated_office_names:
                    self.office_allocations[new_room].append(person)
                else:
                    self.office_allocations[new_room["name"]] = [person]
                self.office_allocations[current_room_name].remove(person)
                print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
            else:
                error_message = "N/A"
                new_room=next((room for room in self.offices if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                if new_room != error_message:
                    if new_room in allocated_office_names:
                        self.office_allocations[new_room].append(person)
                    else:
                        self.office_allocations[new_room] = [person]

                    self.office_allocations[current_room_name].remove(person)
                    print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                else:
                    Print("No available rooms.")


        elif str(room_name) in living_space_names:
            person = self.get_person(person_id)
            if person["role"].lower() in ("staff", "s"):
                print("Staff cannot have a living space.")
            else:
                person = person["data"]
                for key, value in self.living_space_allocations.items():
                    for person in value:
                        if person["person_id"] == person_id:
                            current_room_name = key
                            break
            current_room = [room for room in self.living_spaces if room["name"]== current_room_name]

            print("{0} is in living space: {1}" .format(person["name"], current_room_name))
            new_room = self.get_room(room_name)["data"]
            if new_room["no_of_members"] < new_room["max_members"]:
                if new_room in allocated_living_space_names:
                    self.living_space_allocations[new_room].append(person)
                else:
                    self.living_space_allocations[new_room["name"]] = [person]
                self.living_space_allocations[current_room_name].remove(person)
                print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
            else:
                error_message = "N/A"
                new_room=next((room for room in self.living_spaces if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                if new_room != error_message:
                    if new_room in allocated_living_space_names:
                        self.living_space_allocations[new_room].append(person)
                    else:
                        self.living_space_allocations[new_room] = [person]

                    self.living_space_allocations[current_room_name].remove(person)
                    print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                else:
                    Print("No available rooms.")




                





    def load_people(self, text_file):
        text_file = str(text_file)
        with open(text_file, "r") as f:
            people = f.read().splitlines()
            for person in people:
                person = person.split(" ")
                if len(person)==4:
                    self.add_person(person[0], person[1],person[2],person[3])
                elif len(person)==3:
                    self.add_person(person[0], person[1],person[2])
                else:
                    print("Please check the text file, some values are missing.")

    
        

    def print_allocations(self):
        pass

    def print_unallocations(self):
        pass

    def print_room(self):
        pass

    def save_state(self):
        conn = sqlite3.connect("my_db")
        c= conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS fellow (person_id TEXT PRIMARY KEY, name TEXT)WITHOUT ROWID')
        conn.commit()
        conn.close()

    def load_state(self):
        pass

a = Amity()
# a.create_room(1, "narnia")
# a.create_room("office", "platform")
# a.create_room("office", "hogwarts")
# # a.create_room("living_space", [])
# # a.create_room("living_space", "emerald", "diamond", "quartz", 4)
# # a.create_room("living_space", "topaz", "ruby", "platform")
# # a.create_room("sitting_room", "narnia")
# # a.create_room("office", "narnia", "hogwarts", "platform")
# a.create_room("living_space", "ruby")
# a.create_room("living_space", "topaz")


# a.add_person("maryanne", "Nganga", "fellow", "Y")
# a.add_person("jane", "Ngugi", "fellow")
# a.add_person("jake", "Kimani", "staff", "Y")
# a.add_person("joyce", "wangare", "staff")
# # a.add_person("moni", "wae", "staff")
# # a.add_person("njeri", "githinji", "staff")
# # a.add_person("gladys", "wamaitha", "staff")
# a.add_person("kagiri", "ma", "staff")
# a.add_person([], "Wambui", "F", 6)
# a.reallocate_room(1, "topaz")

# # a.reallocate_living_space("F1", "ruby")
# #a.save_state()

a.load_people("sample.txt")


# #print(a.get_room("topaz"))
# #print(a.get_person(1))
print("Staff: " , a.staff)
# print()
print("Fellows " , a.fellows)
# print()
# print("Living spaces " , a.living_spaces)
# print()
# print("Offices " , a.offices)
# print()
# print("Office allocations " , a.office_allocations)
# print()
# print("Living space allocations " , a.living_space_allocations)
