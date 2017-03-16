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

    #adds people as either staff or fellows to amity
    def add_person(self, firstname, lastname, role, wants_accomodation="N"):
        try:
            wants_accomodation_options = ["Yes", "N", "Y" "No", None]
            if isinstance(lastname, str) and isinstance(firstname, str):
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

                    if wants_accomodation.lower() in ["yes", "y"]:
                        return "Staff does not get living space. staff created with no living space."
                    elif wants_accomodation.lower() in ["no", "n"]:
                        pass
                    else:
                        print("invalid accomodation")
            else:
                print("please input valid names.")
        except():
            return "Please try again"

    #creates rooms in amity. a user can add one or more people.
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

    #allocates offices to people. called automatically by add_person()
    def allocate_office(self, id):
        error_message = "N/A"
        office =next((room for room in self.offices if room["no_of_members"]<room["max_members"]), error_message)
        if office != error_message:
            office["no_of_members"] = office["no_of_members"]+1
            return office["name"]
        else:
            print("No available office rooms.")
            return False

    #allocates living space to fellows.
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

    #gets person and tells whether person is staff or fellow.
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

    #gets persons current office.
    def get_current_office(self, person_id):
        person = self.get_person(person_id)["data"]
        all_assigned_people = []
        for room, people in self.office_allocations.items():
            for this_person in people:
                all_assigned_people.append(this_person)

        if person in all_assigned_people:
            for room, people in self.office_allocations.items():
                for p in people:
                    if p == person:
                        current_office = self.get_room(room)["data"]
                        break
        else:
            print("Person has no current office.")
            current_office = None
        return current_office

    #gets a persons current living space.
    def get_current_living_space(self, person_id):
        person = self.get_person(person_id)["data"]
        all_assigned_fellows =[]
        for room, people in self.living_space_allocations.items():
            for p in people:
                all_assigned_fellows.append(p)
        if person in all_assigned_fellows:
            for room, people in self.living_space_allocations.items():
                for this_person in people:
                    if this_person == person:
                        current_living_space = self.get_room(room)["data"]
                        break
            return current_living_space
        else:
             print("person has no current living space.")
             return None

    #reallocates person from one room to another.
    def reallocate_room(self, person_id, room_name):
        person = self.get_person(person_id)["data"]
        person_role = self.get_person(person_id)["role"]
        allocated_office_names = [room for room in self.office_allocations]
        allocated_living_space_names = [room for room in self.living_space_allocations]

        all_assigned_fellows =[]
        for room, people in self.living_space_allocations.items():
            for p in people:
                all_assigned_fellows.append(p)
        all_assigned_people = []
        for room, people in self.office_allocations.items():
            for this_person in people:
                all_assigned_people.append(this_person)
        allocated_people =  all_assigned_people + all_assigned_fellows
        new_room_type = self.get_room(room_name)["room_type"]
        new_room = self.get_room(room_name)["data"]
        if new_room_type == "office":
            if person in all_assigned_people:
                current_office = self.get_current_office(person_id)
                if new_room["max_members"] > new_room["no_of_members"]:
                    if new_room["name"] in allocated_office_names:
                        self.office_allocations[new_room["name"]].append(person)
                        self.office_allocations[current_office["name"]].remove(person)
                    else:
                        self.office_allocations[new_room["name"]] = [person]
                        self.office_allocations[current_office["name"]].remove(person)
                    
                    print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                else:
                    error_message = "N/A"
                    new_room=next((room for room in self.offices if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                    if new_room != error_message:
                        if new_room in allocated_office_names:
                            self.office_allocations[new_room].append(person)
                            self.office_allocations[current_room_name].remove(person)
                        else:
                            self.office_allocations[new_room] = [person]
                            self.office_allocations[current_room_name].remove(person)

                        print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                    else:
                        Print("No available rooms.")
            else:
                if new_room["max_members"]> new_room["no_of_members"]:
                    if new_room["name"] in allocated_office_names:
                        self.office_allocations[new_room["name"]].append(person)
                    else:
                        self.office_allocations[new_room["name"]] = [person]
                    print("{0}, allocated to {1}" .format(person["name"], new_room["name"]))
                else:
                    error_message = "N/A"
                    new_room=next((room for room in self.offices if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                    if new_room != error_message:
                        if new_room["name"] in allocated_office_names:
                            self.office_allocations[new_room["name"]].append(person)
                        else:
                            self.office_allocations[new_room["name"]] = [person]

                        print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                    else:
                        Print("No available rooms.")

        #if room is living space
        else:
            if person_role == "fellow":
                if person in all_assigned_fellows :
                    current_living_space= self.get_current_living_space(person_id)
                    if new_room["max_members"]> new_room["no_of_members"]:
                        if new_room["name"] in allocated_living_space_names:
                            self.living_space_allocations[new_room["name"]].append(person)
                        else:
                            self.living_space_allocations[new_room["name"]] = [person]
                        self.living_space_allocations[current_living_space["name"]].remove(person)
                        print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                    else:
                        error_message = "N/A"
                        new_room=next((room for room in self.living_spaces if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                        if new_room != error_message:
                            if new_room["name"] in allocated_living_space_names:
                                self.living_space_allocations[new_room["name"]].append(person)
                            else:
                                self.living_space_allocations[new_room["name"]] = [person]

                            self.living_space_allocations[current_living_space["name"]].remove(person)
                            print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                        else:
                            Print("No available rooms.")

                else:
                    if new_room["max_members"]> new_room["no_of_members"]:
                        if new_room["name"] in allocated_living_space_names:
                            self.living_space_allocations[new_room["name"]].append(person)
                        else:
                            self.living_space_allocations[new_room["name"]] = [person]
                        print("{0}, allocated to {1}" .format(person["name"], new_room["name"]))
                    else:
                        error_message = "N/A"
                        new_room=next((room for room in self.living_spaces if room["max_members"] > room["no_of_members"] and room["name"] != current_room_name), error_message)
                        if new_room != error_message:
                            if new_room["name"] in allocated_living_space_names:
                                self.living_space_allocations[new_room["name"]].append(person)
                            else:
                                self.living_space_allocations[new_room["name"]] = [person]

                            print("{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                        else:
                            Print("No available rooms.")
            else:
                print("You are trying to allocate staff living space. Staff cannot get living space.")


    #loads people from a txt file.
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

    #prints all allocated people and the rooms they have been allocated to.
    #specifying file name saves allocations to the specified file.
    def print_allocations(self, *args):
        #print office allocations
        args = list(args)
        if len(args)==0:
            print("OFFICE ALLOCATIONS")
            for room, people in self.office_allocations.items():
                print(room.upper())
                for person in people:
                    print(person["person_id"], person["name"])
            #print living space and people in the living space
            print("LIVING SPACES")
            for room, people in self.living_space_allocations.items():
                print(room.upper())
                for person in people:
                    print(person["person_id"], person["name"])
        elif len(args) == 1:
            for arg in args:
                textfile = str(arg)
            with open(textfile, "w") as f:
                f.write("OFFICE ALLOCATIONS\n")
                for room, people in self.office_allocations.items():
                    room = room.upper()
                    f.write("\t{0}\n" .format(room.upper()))
                    for person in people:
                        person_id = str(person["person_id"])
                        person_name = str(person["name"])
                        this_person = person_id + person_name
                        f.write("\t\t{0}, {1}\n".format(person_id, person_name))

                f.write("LIVING SPACES ALLOCATIONS\n")
                for room, people in self.living_space_allocations.items():
                    f.write("\t{0} \n" .format(room.upper()))
                    for person in people:
                        f.write("\t\t{0}, {1}\n" .format(person["person_id"], person["name"]))
                f.close()
                print("allocations saved into: {0}" .format (textfile))


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
        