from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff
import sqlite3


class Amity(object):

    def __init__(self, offices=[], living_spaces=[], fellows=[], staff=[], office_allocations={}, living_space_allocations={}, people_counter=0):
        self.offices = offices
        self.living_spaces = living_spaces
        self.fellows = fellows
        self.staff = staff
        self.office_allocations = office_allocations
        self.living_space_allocations = living_space_allocations
        self.people_counter = people_counter

    def add_person(self, firstname, lastname, role, wants_accomodation = "N"):
        """Adds people as either staff or fellows to amity."""
        try:
            wants_accomodation_options = ["Yes", "N", "Y" "No", None]
            if isinstance(lastname, str) and isinstance(firstname, str):
                if role.lower() in ("fellow", "f"):
                    self.people_counter = self.people_counter + 1
                    Fellow.person_id = self.people_counter
                    Fellow.name = firstname + " " + lastname
                    fellow = Fellow(Fellow.person_id, Fellow.name)
                    office = self.allocate_office(Fellow.person_id)

                    allocated_room_names = []
                    for key in self.office_allocations:
                        allocated_room_names.append(key)
                    if office:
                        if office in allocated_room_names:
                            self.office_allocations[
                                office].append(fellow.__dict__)
                        else:
                            self.office_allocations[office] = [fellow.__dict__]

                    else:
                        pass
                    self.fellows.append(fellow.__dict__)
                    print("{0} created" .format(Fellow.name ))

                    if wants_accomodation.lower() in ("yes", "y"):
                        living_space = self.allocate_living_space(
                            Fellow.person_id)
                        allocated_room_names = []
                        for key in self.living_space_allocations:
                            allocated_room_names.append(key)
                        if living_space:
                            if living_space in allocated_room_names:
                                self.living_space_allocations[
                                    living_space].append(fellow.__dict__)
                            else:
                                self.living_space_allocations[
                                    living_space] = [fellow.__dict__]

                        else:
                            pass

                else:
                    Staff.name = firstname + " " + lastname
                    self.people_counter += 1
                    Staff.person_id = self.people_counter
                    staff = Staff(Staff.person_id, Staff.name)
                    print("{0} created" .format(Staff.name))
                    self.staff.append(staff.__dict__)
                    office = self.allocate_office(Staff.person_id)

                    allocated_room_names = []
                    for key in self.office_allocations:
                        allocated_room_names.append(key)
                    if office:
                        if office in allocated_room_names:
                            self.office_allocations[
                                office].append(staff.__dict__)
                        else:
                            self.office_allocations[office] = [staff.__dict__]

                    else:
                        pass

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

    def create_room(self, room_type, rooms):
        """Creates rooms in amity. A user can add one or more people."""
        all_rooms = self.offices + self.living_spaces
        all_room_names = []
        for r in all_rooms:
            all_room_names.append(r["name"].lower())
        if rooms == []:
            print ("please input room types")
        else:
            if isinstance(room_type, str):
                if room_type == "living_space":
                    for room in rooms:
                        if isinstance(room, str) and room.lower() not in all_room_names:
                            LivingSpace.living_space_name = room
                            living_space = LivingSpace(
                                LivingSpace.living_space_name)
                            self.living_spaces.append(
                                living_space.__dict__)
                            print("{0} created" .format(LivingSpace.living_space_name))
                        else:
                            print(
                                "one of your living room names is not a string or it already exists. please try again.")

                elif room_type == "office":
                    for room in rooms:
                        if isinstance(room, str) and room.lower() not in all_room_names:
                            Office.office_name = room
                            office = Office(Office.office_name)
                            self.offices.append(office.__dict__)
                            print("{0} created" .format(Office.office_name))
                            
                        else:
                            print(
                                "One of your office names is not a string or it already exists please retry.")
                else:
                    print("Please input a room type of either office or living space.")
            else:
                print("Room type should be a string.")

        print(self.offices)
        print(self.living_spaces)

    def allocate_office(self, id):
        """Allocates offices to people. called automatically by add_person()."""
        error_message = "N/A"
        office = next((room for room in self.offices if room[
                      "no_of_members"] < room["max_members"]), error_message)
        if office != error_message:
            office["no_of_members"] = office["no_of_members"]+1
            return office["name"]
        else:
            print("No available office rooms.")
            return False

    def allocate_living_space(self, person_id):
        """Allocates living space to fellows."""
        error_message = "N/A"
        living_space = next((room for room in self.living_spaces if room[
                            "no_of_members"] < room["max_members"]), error_message)
        if living_space != error_message:
            living_space["no_of_members"] = living_space["no_of_members"]+1
            return living_space["name"]
        else:
            print("No available living spaces")
            return False

    def get_room(self, room_name):
        """ Gets room given room name and tells whether the room is an office or a
    living space."""
        if isinstance(room_name, str):
            all_rooms = self.offices + self.living_spaces
            this_room = {}
            all_room_names = []
            for room in self.offices:
                all_room_names.append(room["name"])
            for room in self.living_spaces:
                all_room_names.append(room["name"])
            if room_name in all_room_names:
                for room in all_rooms:
                    if room["name"].lower() == room_name:
                        break
                        print("room does not exist.")
                if room["max_members"] == 4:
                    this_room["room_type"] = "living_space"
                    this_room["data"] = room
                else:
                    this_room["room_type"] = "office"
                    this_room["data"] = room
            else:
                print("Room does not exist.")
        else:
            print("Enter valid room name.")

        return this_room

    def get_person(self, person_id):
        """Gets person and tells whether person is staff or fellow."""
        fellow_ids = []
        staff_ids = []
        this_fellow = {}
        this_staff = {}
        person_id = int(person_id)

        for fellow in self.fellows:
            fellow_ids.append(fellow["person_id"])

        for staff in self.staff:
            staff_ids.append(staff["person_id"])

        if isinstance(person_id, int):
            if person_id in fellow_ids:
                for fellow in self.fellows:
                    if fellow["person_id"] == person_id:
                        break
                this_fellow["role"] = "fellow"
                this_fellow["data"] = fellow
                return this_fellow
            elif person_id in staff_ids:
                for staff in self.staff:
                    if staff["person_id"] == person_id:
                        break
                this_staff["role"] = "staff"
                this_staff["data"] = staff
                return this_staff
            else:
                return "The person ID does not exist please try again."
        else:
            return "Person id is an integer. refer to fellow or staff list."

    def get_current_office(self, person_id):
        """Gets persons current office."""
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

    def get_current_living_space(self, person_id):
        """Gets a persons current living space."""
        person = self.get_person(person_id)["data"]
        all_assigned_fellows = []
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

    def reallocate_room(self, person_id, room_name):
        """Reallocates person from one room to another."""
        person = self.get_person(int(person_id))["data"]
        person_role = self.get_person(person_id)["role"]
        allocated_office_names = [room for room in self.office_allocations]
        allocated_living_space_names = [
            room for room in self.living_space_allocations]

        all_assigned_fellows = []
        for room, people in self.living_space_allocations.items():
            for p in people:
                all_assigned_fellows.append(p)
        all_assigned_people = []
        for room, people in self.office_allocations.items():
            for this_person in people:
                all_assigned_people.append(this_person)
        allocated_people = all_assigned_people + all_assigned_fellows
        new_room_type = self.get_room(room_name)["room_type"]
        new_room = self.get_room(room_name)["data"]
        if new_room_type == "office":
            if person in all_assigned_people:
                current_office = self.get_current_office(person_id)
                if new_room["max_members"] > new_room["no_of_members"]:
                    if new_room["name"] in allocated_office_names:
                        self.office_allocations[
                            new_room["name"]].append(person)
                        self.office_allocations[
                            current_office["name"]].remove(person)
                    else:
                        self.office_allocations[new_room["name"]] = [person]
                        self.office_allocations[
                            current_office["name"]].remove(person)

                    print("{0}, reallocated to {1}" .format(
                        person["name"], new_room["name"]))
                else:
                    error_message = "N/A"
                    new_room = next((room for room in self.offices if room["max_members"] > room[
                                    "no_of_members"] and room["name"] != current_room_name), error_message)
                    if new_room != error_message:
                        if new_room in allocated_office_names:
                            self.office_allocations[new_room].append(person)
                            self.office_allocations[
                                current_room_name].remove(person)
                        else:
                            self.office_allocations[new_room] = [person]
                            self.office_allocations[
                                current_room_name].remove(person)

                        print("{0}, reallocated to {1}" .format(
                            person["name"], new_room["name"]))
                    else:
                        Print("No available rooms.")
            else:
                if new_room["max_members"] > new_room["no_of_members"]:
                    if new_room["name"] in allocated_office_names:
                        self.office_allocations[
                            new_room["name"]].append(person)
                    else:
                        self.office_allocations[new_room["name"]] = [person]
                    print("{0}, allocated to {1}" .format(
                        person["name"], new_room["name"]))
                else:
                    error_message = "N/A"
                    new_room = next((room for room in self.offices if room["max_members"] > room[
                                    "no_of_members"] and room["name"] != current_room_name), error_message)
                    if new_room != error_message:
                        if new_room["name"] in allocated_office_names:
                            self.office_allocations[
                                new_room["name"]].append(person)
                        else:
                            self.office_allocations[
                                new_room["name"]] = [person]

                        print("{0}, reallocated to {1}" .format(
                            person["name"], new_room["name"]))
                    else:
                        Print("No available rooms.")

        # if room is living space
        else:
            if person_role == "fellow":
                if person in all_assigned_fellows:
                    current_living_space = self.get_current_living_space(
                        person_id)
                    if new_room["max_members"] > new_room["no_of_members"]:
                        if new_room["name"] in allocated_living_space_names:
                            self.living_space_allocations[
                                new_room["name"]].append(person)
                        else:
                            self.living_space_allocations[
                                new_room["name"]] = [person]
                        self.living_space_allocations[
                            current_living_space["name"]].remove(person)
                        print("{0}, reallocated to {1}" .format(
                            person["name"], new_room["name"]))
                    else:
                        error_message = "N/A"
                        new_room = next((room for room in self.living_spaces if room["max_members"] > room[
                                        "no_of_members"] and room["name"] != current_room_name), error_message)
                        if new_room != error_message:
                            if new_room["name"] in allocated_living_space_names:
                                self.living_space_allocations[
                                    new_room["name"]].append(person)
                            else:
                                self.living_space_allocations[
                                    new_room["name"]] = [person]

                            self.living_space_allocations[
                                current_living_space["name"]].remove(person)
                            print(
                                "{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                        else:
                            Print("No available rooms.")

                else:
                    if new_room["max_members"] > new_room["no_of_members"]:
                        if new_room["name"] in allocated_living_space_names:
                            self.living_space_allocations[
                                new_room["name"]].append(person)
                        else:
                            self.living_space_allocations[
                                new_room["name"]] = [person]
                        print(
                            "{0}, allocated to {1}" .format(person["name"], new_room["name"]))
                    else:
                        error_message = "N/A"
                        new_room = next((room for room in self.living_spaces if room["max_members"] > room[
                                        "no_of_members"] and room["name"] != current_room_name), error_message)
                        if new_room != error_message:
                            if new_room["name"] in allocated_living_space_names:
                                self.living_space_allocations[
                                    new_room["name"]].append(person)
                            else:
                                self.living_space_allocations[
                                    new_room["name"]] = [person]

                            print(
                                "{0}, reallocated to {1}" .format(person["name"], new_room["name"]))
                        else:
                            Print("No available rooms.")
            else:
                print(
                    "You are trying to allocate staff living space. Staff cannot get living space.")

    def load_people(self, text_file):
        """Loads people from a txt file."""
        text_file = str(text_file)
        with open(text_file, "r") as f:
            people = f.read().splitlines()
            for person in people:
                person = person.split(" ")
                if len(person) == 4:
                    self.add_person(person[0], person[1], person[2], person[3])
                elif len(person) == 3:
                    self.add_person(person[0], person[1], person[2])
                else:
                    print(
                        "Please check the text file, some values are missing.")

  
    def print_allocations(self, *args):
        """Prints all allocated people and the rooms they have been allocated to.
            specifying file name saves allocations to the specified file."""
        args = list(args)
        if len(args) == 0:
            print("OFFICE ALLOCATIONS")
            for room, people in self.office_allocations.items():
                print(room.upper())
                for person in people:
                    print(person["person_id"], person["name"])
            # print living space and people in the living space
            print("LIVING SPACES")
            for room, people in self.living_space_allocations.items():
                print(room.upper())
                for person in people:
                    print(person["person_id"], person["name"])
        elif len(args) == 1:
            for arg in args:
                textfile = str(arg)+".txt"
                print (textfile)
            with open(textfile, "w") as f:
                f.write("OFFICE ALLOCATIONS\n")
                for room, people in self.office_allocations.items():
                    room = room.upper()
                    f.write("\t{0}\n" .format(room.upper()))
                    for person in people:
                        person_id = str(person["person_id"])
                        person_name = str(person["name"])
                        this_person = person_id + person_name
                        f.write(
                            "\t\t{0}, {1}\n".format(person_id, person_name))

                f.write("LIVING SPACES ALLOCATIONS\n")
                for room, people in self.living_space_allocations.items():
                    f.write("\t{0} \n" .format(room.upper()))
                    for person in people:
                        f.write(
                            "\t\t{0}, {1}\n" .format(person["person_id"], person["name"]))
                f.close()
                print("allocations saved into: {0}" .format(textfile))
        else:
            print("Please input corrent name of textfile eg: allocations")

    def print_unallocated(self, *args):
        """Prints people that have not been allocated to rooms.
            Specifying a text file saves the un allocated to the text file
            """
        # Find people with no offices
        args = list(args)
        all_people = self.fellows + self.staff
        allocated_people = []
        allocated_fellows = []
        if len(args) == 0:
            print("PEOPLE WITH NO OFFICES")
            for room, people in self.office_allocations.items():
                for person in people:
                    allocated_people.append(person)
            for person in all_people:
                if person not in allocated_people:
                    print(person["person_id"], person["name"])
            #Fellows with no living space

            print("FELLOWS WITH NO LIVING SPACE:")
            for room, people in self.living_space_allocations.items():
                for person in people:
                    allocated_fellows.append(person)
            for fellow in self.fellows:
                if fellow not in allocated_fellows:
                    print(fellow["person_id"], fellow["name"])

        elif len(args) == 1:
            for arg in args:
                text_file = str(arg)+".txt"
            with open(text_file, "w") as f:
                f.write("PEOPLE WITH NO OFFICES\n")
                for room, people in self.office_allocations.items():
                    for person in people:
                        allocated_people.append(person)
                for person in all_people:
                    if person not in allocated_people:
                        f.write(
                            "\t{0}, {1}\n".format(person["person_id"], person["name"]))

                f.write("FELLOWS WITH NO LIVING SPACE:\n")
                for room, people in self.living_space_allocations.items():
                    for person in people:
                        allocated_fellows.append(person)
                for fellow in self.fellows:
                    if fellow not in allocated_fellows:
                        f.write(
                            "\t{0}, {1}\n".format(fellow["person_id"], fellow["name"]))
            print("unallocated people saved to {0}" .format(text_file))
        else:
            print("Please input valid text file: eg unallocated")

    
    def print_room(self, room_name):
        """Prints a room and the occupants of the room."""
        if isinstance(room_name, str):
            all_rooms =[]
            allocated_office_names =[room for room in self.office_allocations]
            allocated_living_space_names =[room for room in self.living_space_allocations]
            for room in self.offices:
                all_rooms.append(room["name"])
            for room in self.living_spaces:
                all_rooms.append(room["name"])
            if room_name in all_rooms:
                if room_name in allocated_office_names:
                    print(room_name.upper())
                    occupants = self.office_allocations.get(room_name)
                    for occupant in occupants:
                        print(occupant["person_id"], occupant["name"])
                elif room_name in allocated_living_space_names:
                    print(room_name.upper())
                    occupants = self.living_space_allocations.get(room_name)
                    for occupant in occupants:
                        print(occupant["person_id"], occupant["name"])
                else:
                    print(room_name)
                    print("Room is currently vacant.")
            else:
                print("Room does not exist.")
        else:
            print("Please enter valid room name.")

    def save_state(self, args):
        """Saves the data generated by amity to an sqlite database. The database name is specified by the user. """
        dbfile = str(args)
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS person (person_id INTEGER PRIMARY KEY, name TEXT, role TEXT)WITHOUT ROWID')
        for fellow in self.fellows:
                this_person_id = fellow["person_id"]
                this_person_name = fellow["name"]
                this_person_role = "fellow"
                c.execute('INSERT OR IGNORE INTO person (person_id, name, role) VALUES(?, ?, ?)',(this_person_id, this_person_name, this_person_role))
        for staff in self.staff:
                this_person_id = staff["person_id"]
                this_person_name = staff["name"]
                this_person_role = "staff"
                c.execute('INSERT OR IGNORE INTO person (person_id, name, role) VALUES(?, ?, ?)',(this_person_id, this_person_name, this_person_role) 
                      )

        c.execute(
                  'CREATE TABLE IF NOT EXISTS room (name TEXT , no_of_members INTEGER, room_type TEXT)')
        all_rooms = self.offices +self.living_spaces
        for room in all_rooms:
            roomtype = self.get_room(room["name"])["room_type"]
            this_room_name = room["name"]
            this_room_no_of_members = room["no_of_members"]
            if roomtype == "office":
                this_room_type = "office"
            else:
                this_room_type = "living_space"

            c.execute('INSERT INTO room (name, no_of_members, room_type) VALUES(?, ?, ?)',(this_room_name, this_room_no_of_members, this_room_type) 
                      )

        c.execute(
                  'CREATE TABLE IF NOT EXISTS allocation (room_name TEXT , person_id INTEGER)')
        for room, people in self.office_allocations.items():
            for person in people:
                this_room_name = room
                this_person_id = person["person_id"]
                c.execute('INSERT INTO allocation (room_name, person_id) VALUES(?, ?)',(this_room_name, this_person_id) 
                      )
        for room, people in self.living_space_allocations.items():
            for person in people:
                this_room_name = room_name
                this_person_id = person["person_id"]
                c.execute('INSERT INTO allocation (room_name, person_id) VALUES(?, ?)',(this_room_name, this_person_id) 
                      )

        conn.commit()
        conn.close()

    def load_state(self, args):
        """Loads data from the database file specified into the respective lists."""

        dbname = str(args)
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="fellow"'.format(tn="person", cn="role", col1= "person_id", col2="name"))
        fellows = c.fetchall()
        for fellow in fellows:
            fellow = list(fellow)
            keys = ["person_id", "name"]
            fellowsdict = {}
            for k, v in zip(keys, fellow):
                fellowsdict[k] = v
            this_person_id = fellowsdict.get("person_id")
            fellowsdict["person_id"] = int(this_person_id)
            self.fellows.append(fellowsdict)

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="staff"'.format(tn="person", cn="role", col1= "person_id", col2="name"))
        all_staff = c.fetchall()
        for staff in all_staff:
            staff = list(staff)
            keys = ["person_id", "name"]
            staffdict = {}
            for k, v in zip(keys, staff):
                staffdict[k] = v
            this_person_id = staffdict.get("person_id")
            this_person_id = int(this_person_id)
            self.staff.append(staffdict)

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="office"'.format(tn="room", cn="room_type", col1= "name", col2="no_of_members"))
        offices = c.fetchall()
        for office in offices:
            office = list(office)
            office.append(6)
            keys = ["name", "no_of_members", "max_members"]
            officedict = {}
            for k, v in zip(keys, office):
                officedict[k] = v
            self.offices.append(officedict)

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="living_space"'.format(tn="room", cn="room_type", col1= "name", col2="no_of_members"))
        living_spaces = c.fetchall()
        for living_space in living_spaces:
            living_space = list(living_space)
            living_space.append(4)
            keys = ["name", "no_of_members", "max_members"]
            living_spacedict = {}
            for k, v in zip(keys, living_space):
                living_spacedict[k] = v
            self.living_spaces.append(living_spacedict)

        
        c.execute('SELECT {col1}, {col2} FROM {tn}'.format(tn="allocation", col1= "room_name", col2="person_id"))
        all_allocations = c.fetchall()
        allocated_office_names=[]
        allocated_living_space_names =[]
        for allocation in all_allocations:
            allocation = list(allocation)
            room_name = allocation[0]
            person_id =allocation[1] 
            room_type = self.get_room(room_name)["room_type"]
            person_data = self.get_person(int(person_id))["data"]
            if room_type == "office":
                if room_name not in allocated_office_names:
                    allocated_office_names.append("room_name")
                    self.office_allocations[room_name]=[person_data]
                    allocated_office_names.append(room_name)
                else:
                    self.office_allocations[room_name].append(person_data)

            else:
                if room_name not in allocated_living_space_names:
                    allocated_living_space_names.append("room_name")
                    self.living_space_allocations[room_name]=[person_data]
                    allocated_living_space_names.append(room_name)
                else:
                    self.living_space_allocations[room_name].append(person_data)
        all_ids = []
        all_people = self.fellows+self.staff
        for person in all_people:
            all_ids.append(person["person_id"])

        self.people_counter = max(all_ids)
        print("Data reloaded to Amity")

        conn.close()


    def list_fellows(self):
        """Prints all fellows"""
        print("person id     fellow")
        for person in self.fellows:
            print(person["person_id"], person["name"])

    def list_staff(self):
        """Prints all staff."""
        print("person id  staff")
        for person in self.staff:
            print(person["person_id"], person["name"])

    def list_offices(self):
        """Prints all offices"""
        for office in self.offices:
            print("office name : {0} , no_of_members: {1}" .format(office["name"], office["no_of_members"]))

    def list_living_spaces(self):
        """Prints all living spaces."""
        for room in self.living_spaces:
            print("Room name: {0} , No_of_members: {1}" .format(room["name"], room["no_of_members"]))

    def delete_person(self, person_id):
        """Deletes a person given their id."""
        person_role = self.get_person(person_id)["role"]
        person = self.get_person(person_id)["data"]
        if person_role == "fellow":
            self.fellows.remove(person)
            for room, people in self.office_allocations.items():
                if person in people:
                    people.remove(person)
            for room, people in self.living_space_allocations.items():
                if person in people:
                    people.remove(person)
        else:
            self.staff.remove(person)
            for room, people in self.office_allocations.items():
                if person in people:
                    people.remove(person)

    def delete_room(self, room_name):
        """Deletes a room given the room name."""
        room_type = self.get_room(room_name)["room_type"]
        this_room = self.get_room(room_name)["data"]
        all_allocated_offices = [room for room in self.office_allocations]
        all_allocated_living_spaces = [room for room in self.living_space_allocations]
        if room_type == "office":
            self.offices.remove(this_room)
            if room_name in all_allocated_offices:
                del self.office_allocations[room_name]
                print("Office was not vacant please reallocate people previously in office")
            else:
                print("Office was vacant")
        else:
            self.living_spaces.remove(this_room)
            if room_name in all_allocated_living_spaces:
                del self.living_space_allocations[room_name]
                print("Living space was not vacant please reallocate people previously in living space")
            else:
                print("Living Space was empty.")

