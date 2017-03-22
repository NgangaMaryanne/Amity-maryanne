from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff
import sqlite3
from termcolor import cprint
import random


class Amity(object):

    def __init__(self, offices=[], living_spaces=[], people = [], \
                    office_allocations={}, living_space_allocations={}, \
                    people_counter=0):
        self.offices = offices
        self.living_spaces = living_spaces
        self.people = people
        self.office_allocations = office_allocations
        self.living_space_allocations = living_space_allocations
        self.people_counter = people_counter

    def add_person(self, firstname, lastname, role, wants_accomodation="N"):
        """Adds people as either staff or fellows to amity."""
        try:
            wants_accomodation_options = ["Yes", "N", "Y" "No", None]
            all_people_names = [person["name"] for person in self.people]
            if firstname.isalpha() and lastname.isalpha():
                name = firstname + " " + lastname
                if name in all_people_names:
                    cprint("Person exists. please try again.", 'red')
                else:
                    self.people_counter = self.people_counter + 1
                    person_id = self.people_counter
                    if role in ("fellow", "f", "F", "Fellow"):
                        fellow = Fellow(person_id, name)
                        self.people.append(fellow.__dict__)
                        cprint("{0} created" .format(fellow.name), 'blue')
                        self.allocate_office(fellow.person_id)

                        if wants_accomodation in ("yes", "y", "Yes", "Y"):
                            self.allocate_living_space(fellow.person_id)
                            
                    elif role in ['staff', 's', 'Staff', 'S']:
                        staff = Staff(person_id, name)
                        cprint("{0} created" .format(name), 'blue')
                        self.people.append(staff.__dict__)
                        self.allocate_office(staff.person_id)
                        if wants_accomodation.lower() in ["yes", "y"]:
                            message = "Staff does not get living space. staff \
                            created with no living space."
                            cprint(message, 'red')
                            return message
                    else:
                        cprint(
                            "Specify whether person is fellow or \
                            staff.", 'red')
                        return "Please specify whether person is fellow or \
                        staff."
            else:
                cprint("Please input valid names.", 'red')
                return "Please input valid names."
        except():
            return "Please try again"

    def create_room(self, room_type, rooms):
        """Creates rooms in amity. A user can add one or more people."""
        all_rooms = self.offices + self.living_spaces
        all_room_names = []
        for r in all_rooms:
            all_room_names.append(r["name"].lower())
        if rooms == []:
            cprint("please input room types", 'red')
        else:
            if isinstance(room_type, str):
                if room_type == "living_space":
                    for room in rooms:
                        if room.isalpha():
                            if room.lower() not in all_room_names:
                                living_space_name = room
                                living_space = LivingSpace(
                                    living_space_name)
                                self.living_spaces.append(
                                    living_space.__dict__)
                                cprint(
                                    "{0} created" .format(living_space_name), \
                                'blue')
                            else:
                                cprint("Room already exists", 'red')
                        else:
                            cprint("Room name is not valid.")

                elif room_type == "office":
                    for room in rooms:
                        if room.isalpha():
                            if room.lower() not in all_room_names:
                                office_name = room
                                office = Office(office_name)
                                self.offices.append(office.__dict__)
                                cprint(
                                    "{0} created" .format(office_name), 'blue')
                            else:

                                cprint("Office exists please retry.", 'red')
                        else:
                            cprint(
                                "Office name is not valid.", 'red')
                            return "Office name is not valid."

                else:
                    return "Room type is either office or living space."
            else:
                cprint("Room type should be a string.", 'red')

    def allocate_office(self, person_id):
        """Allocates offices to people. called automatically by add_person()."""
        person = self.get_person(person_id)
        available_offices = [office["name"] for office in self.offices if \
        office["max_members"]>office["no_of_members"]]
        if available_offices != []:
            office_name = random.choice(available_offices)
            office = self.get_room(office_name)["data"]
            allocated_room_names = [room for room in self.office_allocations]
            if office_name in allocated_room_names:
                self.office_allocations[
                    office_name].append(person)

            else:
                self.office_allocations[
                    office_name] = [person]
            office["no_of_members"]+=1 
            cprint("{0} allocated to office {1}" .format(person["name"], office["name"]), 'blue')
        else:
            cprint("No available offices", 'red')

    def allocate_living_space(self, person_id):
        """Allocates living space to fellows."""
        person = self.get_person(person_id)
        available_living_spaces = [room["name"] for room in self.living_spaces \
        if room["max_members"]> room["no_of_members"]]
        allocated_living_spaces_names = [room["name"] for \
        room in self.living_space_allocations]

        if available_living_spaces !=[]:
            living_space_name = random.choice(available_living_spaces)
            living_space = self.get_room(living_space_name)["data"]
            if living_space_name in allocated_living_spaces_names:
                self.living_space_allocations[
                    living_space].append(person)
            else:
                self.living_space_allocations[
                    living_space_name] = [person]
            living_space["no_of_members"] +=1
            cprint("{0} allocated living space: {1}" .format(person["name"], \
                   living_space_name))
        else:
            cprint("No available living_spaces.", 'red')


        

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
                        cprint("room does not exist.", 'red')
                if room["max_members"] == 4:
                    this_room["room_type"] = "living_space"
                    this_room["data"] = room
                else:
                    this_room["room_type"] = "office"
                    this_room["data"] = room
                return this_room
            else:
                cprint("Room does not exist.", 'red')
        else:
            cprint("Enter valid room name.", 'red')

    def get_person(self, person_id):
        """Gets person and tells whether person is staff or fellow."""
        all_ids = [person["person_id"] for person in self.people]
        if isinstance(person_id, int):
            if person_id in all_ids:
                for person in self.people:
                    if person["person_id"] == person_id:
                        break
                this_person= person
                return this_person
            
            else:
                cprint("The person ID does not exist please try again.", 'red')
        else:
            cprint(
                "Person id is an integer. refer to fellow or staff list.",'red')

    def get_current_office(self, person_id):
        """Gets persons current office."""
        person = self.get_person(person_id)
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
            return current_office

        else:
            cprint("Person has no current office.")

    def get_current_living_space(self, person_id):
        """Gets a persons current living space."""
        person = self.get_person(person_id)
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
            cprint("person has no current living space.", 'red')


    def reallocate_room(self, person_id, room_name, \
                        current_room,room_allocations, \
                        allocated_room_names, available_rooms):   
        person = self.get_person(person_id)
        new_room = self.get_room(room_name)["data"]
        if new_room["no_of_members"] < new_room["max_members"]:
            if room_name in allocated_room_names:
                room_allocations[room_name].append(person)
            else:
                room_allocations[room_name] = [person]
            if current_room:
                room_allocations[current_room["name"]].remove(person)
            cprint("{0} reallocated to {1}".format(person["name"], room_name), 'blue')

        else:
            cprint("{0} is full.", 'red')

            if available_rooms != []:
                room_name = random.choice(available_rooms)
                new_room = self.get_room(room_name)
                if room_name in allocated_room_names:
                    room_allocations[room_name].append(person)
                else:
                    room_allocations[room_name] = [person]
                cprint("{0} reallocated to {1}".format(person["name"], \
                       room_name), 'blue')
                if current_room:
                    room_allocations[current_room["name"]].remove(person)
            else:
                cprint("No available rooms.")

    def reallocate_person(self, person_id, room_name):
        """Reallocates person from one room to another."""
        all_people_ids = [person["person_id"] for person in self.people]
        all_office_names = [room["name"] for room in self.offices]
        all_living_space_names = [room["name"] for room in self.living_spaces]
        if person_id.isalpha():
            cprint("Wrong id please check")  
        else:
            person_id = int(person_id)                       
            if person_id in all_people_ids:
                person = self.get_person(person_id)
                if room_name in all_office_names:
                    allocated_office_names = [room for room in self.office_allocations.items()]
                    current_office = self.get_current_office(person_id)
                    available_offices = [room["name"] for room in self.offices if
                                 room["max_members"] > room["no_of_members"] \
                                 and room["name"].lower() != current_office["name"].lower()]

                    self.reallocate_room(person_id, room_name, current_office,\
                                        self.office_allocations, \
                                        allocated_office_names, \
                                        available_offices)
                elif room_name in all_living_space_names:
                    if person["role"] =="staff":
                        cprint("Staff does not get living space.", 'red')
                    else:
                        current_living_space = \
                        self.get_current_living_space(person_id)
                        allocated_living_space_names = []
                        for room in self.living_space_allocations:
                            allocated_living_space_names.append(room)
                        available_living_spaces = [room["name"] for room in\
                         self.living_spaces if
                                 room["max_members"] > room["no_of_members"] \
                                 and room["name"].lower() != \
                                 current_living_space["name"].lower()]
                        self.reallocate_room(person_id, room_name, \
                                             current_living_space,\
                                              self.living_space_allocations,\
                                               allocated_living_space_names, \
                                               available_living_spaces)
                else:
                    cprint("Room does not exist.", 'red')
            else:
                cprint("Person does not exist", 'red')



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
                    cprint(
                        "Please check the text file, some values are missing.")

    def print_allocations(self, *args):
        """Prints all allocated people and the rooms they have been allocated to.
            specifying file name saves allocations to the specified file."""
        args = list(args)
        if len(args) == 0:
            cprint("OFFICE ALLOCATIONS", 'blue')
            for room, people in self.office_allocations.items():
                cprint("{0}".format(room.upper()), 'yellow')
                for person in people:
                    cprint(
                        "{0}, {1}".format(person["person_id"], person["name"]),\
                         'yellow')
            # print living space and people in the living space
            cprint("LIVING SPACES", 'blue')
            for room, people in self.living_space_allocations.items():
                cprint("{0}".format(room.upper()), 'yellow')
                for person in people:
                    cprint(
                        "{0}, {1}".format(person["person_id"], person["name"]),\
                         'yellow')
        elif len(args) == 1:
            for arg in args:
                textfile = str(arg)+".txt"
                print(textfile)
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
                            "\t\t{0}, {1}\n" .format(person["person_id"], \
                            person["name"]))
                f.close()
                cprint("allocations saved into: {0}" .format(textfile), 'blue')
        else:
            cprint(
                "Please input corrent name of textfile eg: allocations", 'red')

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
            cprint("PEOPLE WITH NO OFFICES", 'blue')
            for room, people in self.office_allocations.items():
                for person in people:
                    allocated_people.append(person)
            for person in all_people:
                if person not in allocated_people:
                    cprint(
                        "{0}, {1}".format(person["person_id"], person["name"]),\
                         'yellow')
            # Fellows with no living space

            cprint("FELLOWS WITH NO LIVING SPACE:", 'blue')
            for room, people in self.living_space_allocations.items():
                for person in people:
                    allocated_fellows.append(person)
            for fellow in self.fellows:
                if fellow not in allocated_fellows:
                    cprint(
                        "{0}, {1}".format(fellow["person_id"], fellow["name"]),\
                         'yellow')

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
                            "\t{0}, {1}\n".format(person["person_id"], \
                            person["name"]))

                f.write("FELLOWS WITH NO LIVING SPACE:\n")
                for room, people in self.living_space_allocations.items():
                    for person in people:
                        allocated_fellows.append(person)
                for fellow in self.fellows:
                    if fellow not in allocated_fellows:
                        f.write(
                            "\t{0}, {1}\n".format(fellow["person_id"],\
                             fellow["name"]))
            cprint(
                "unallocated people saved to {0}" .format(text_file), 'blue')
        else:
            cprint("Please input valid text file: eg unallocated", 'red')

    def print_room(self, room_name):
        """Prints a room and the occupants of the room."""
        if isinstance(room_name, str):
            all_rooms = []
            allocated_office_names = [room for room in self.office_allocations]
            allocated_living_space_names = [
                room for room in self.living_space_allocations]
            for room in self.offices:
                all_rooms.append(room["name"])
            for room in self.living_spaces:
                all_rooms.append(room["name"])
            if room_name in all_rooms:
                if room_name in allocated_office_names:
                    cprint("{0}".format(room_name.upper()), 'yellow')
                    occupants = self.office_allocations.get(room_name)
                    for occupant in occupants:
                        cprint("person id   name", 'yellow')
                        cprint(
                            "{0}  {1}".format(occupant["person_id"], \
                            occupant["name"]))
                elif room_name in allocated_living_space_names:
                    cprint("{0}".format(room_name.upper()))
                    occupants = self.living_space_allocations.get(room_name)
                    for occupant in occupants:
                        cprint(
                            "{0} {1}".format(occupant["person_id"],\
                             occupant["name"]))
                else:
                    cprint("{0}".format(room_name), 'yellow')
                    cprint("Room is currently vacant.")
            else:
                return "Room does not exist."
        else:
            cprint("Please enter valid room name.")

    def save_state(self, *arg):
        pass


    def load_state(self, arg):
        pass

    def list_fellows(self):
        """Prints all fellows"""
        cprint("person id   fellow")
        for person in self.fellows:
            cprint(
                "{0} {1} ".format(person["person_id"], person["name"]), "yellow")

    def list_staff(self):
        """Prints all staff."""
        cprint("person id  staff")
        for person in self.staff:
            cprint(
                "{0} {1} ".format(person["person_id"], person["name"]), "yellow")

    def list_offices(self):
        """Prints all offices"""
        for office in self.offices:
            cprint("office name : {0} , no_of_members: {1}" .format(
                office["name"], office["no_of_members"]), 'yellow')

    def list_living_spaces(self):
        """Prints all living spaces."""
        for room in self.living_spaces:
            cprint("Room name: {0} , No_of_members: {1}" .format(
                room["name"], room["no_of_members"]), 'yellow')

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
        room = self.get_room(room_name)
        room_type = self.get_room(room_name)["room_type"]
        this_room = self.get_room(room_name)["data"]
        all_allocated_offices = [room for room in self.office_allocations]
        all_allocated_living_spaces = [
            room for room in self.living_space_allocations]
        if room:
            if room_type == "office":
                self.offices.remove(this_room)
                if room_name in all_allocated_offices:
                    del self.office_allocations[room_name]
                    cprint(
                        "Kindly reallocate people previously in office", 'red')
                else:
                    cprint("Office was vacant")
            else:
                self.living_spaces.remove(this_room)
                if room_name in all_allocated_living_spaces:
                    del self.living_space_allocations[room_name]
                    cprint(
                        "Kindly reallocate people previously in room", 'red')
                else:
                    cprint("Living Space was empty.", 'red')
        else:
            cprint("Room does not exist.", 'red')

    def save_state(self, args):
        """Saves the data generated by amity to an sqlite database. The database name is specified by the user. """
        dbfile = str(args)
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS person')
        c.execute('DROP TABLE IF EXISTS room')
        c.execute('DROP TABLE IF EXISTS allocation')
        c.execute(
            'CREATE TABLE IF NOT EXISTS person (person_id INTEGER PRIMARY KEY, name TEXT, role TEXT)WITHOUT ROWID')
        for fellow in self.fellows:
            this_person_id = fellow["person_id"]
            this_person_name = fellow["name"]
            this_person_role = "fellow"
            c.execute('INSERT OR IGNORE INTO person (person_id, name, role) VALUES(?, ?, ?)',
                      (this_person_id, this_person_name, this_person_role))
        for staff in self.staff:
            this_person_id = staff["person_id"]
            this_person_name = staff["name"]
            this_person_role = "staff"
            c.execute('INSERT OR IGNORE INTO person (person_id, name, role) VALUES(?, ?, ?)', (this_person_id, this_person_name, this_person_role)
                      )

        c.execute(
            'CREATE TABLE IF NOT EXISTS room (name TEXT , no_of_members INTEGER, room_type TEXT)')
        all_rooms = self.offices + self.living_spaces
        for room in all_rooms:
            roomtype = self.get_room(room["name"])["room_type"]
            this_room_name = room["name"]
            this_room_no_of_members = room["no_of_members"]
            if roomtype == "office":
                this_room_type = "office"
            else:
                this_room_type = "living_space"

            c.execute('INSERT INTO room (name, no_of_members, room_type) VALUES(?, ?, ?)', (this_room_name, this_room_no_of_members, this_room_type)
                      )

        c.execute(
            'CREATE TABLE IF NOT EXISTS allocation (room_name TEXT , person_id INTEGER)')
        for room, people in self.office_allocations.items():
            for person in people:
                this_room_name = room
                this_person_id = person["person_id"]
                c.execute('INSERT INTO allocation (room_name, person_id) VALUES(?, ?)', (this_room_name, this_person_id)
                          )
        for room, people in self.living_space_allocations.items():
            for person in people:
                this_room_name = room
                this_person_id = person["person_id"]
                c.execute('INSERT INTO allocation (room_name, person_id) VALUES(?, ?)', (this_room_name, this_person_id)
                          )

        conn.commit()
        conn.close()

    def load_state(self, args):
        """Loads data from the database file specified into the respective lists."""

        dbname = str(args)
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="fellow"'.format(
            tn="person", cn="role", col1="person_id", col2="name"))
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

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="staff"'.format(
            tn="person", cn="role", col1="person_id", col2="name"))
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

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="office"'.format(
            tn="room", cn="room_type", col1="name", col2="no_of_members"))
        offices = c.fetchall()
        for office in offices:
            office = list(office)
            office.append(6)
            keys = ["name", "no_of_members", "max_members"]
            officedict = {}
            for k, v in zip(keys, office):
                officedict[k] = v
            self.offices.append(officedict)

        c.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="living_space"'.format(
            tn="room", cn="room_type", col1="name", col2="no_of_members"))
        living_spaces = c.fetchall()
        for living_space in living_spaces:
            living_space = list(living_space)
            living_space.append(4)
            keys = ["name", "no_of_members", "max_members"]
            living_spacedict = {}
            for k, v in zip(keys, living_space):
                living_spacedict[k] = v
            self.living_spaces.append(living_spacedict)

        c.execute('SELECT {col1}, {col2} FROM {tn}'.format(
            tn="allocation", col1="room_name", col2="person_id"))
        all_allocations = c.fetchall()
        allocated_office_names = []
        allocated_living_space_names = []
        for allocation in all_allocations:
            allocation = list(allocation)
            room_name = allocation[0]
            person_id = allocation[1]
            room_type = self.get_room(room_name)["room_type"]
            person_data = self.get_person(int(person_id))["data"]
            if room_type == "office":
                if room_name not in allocated_office_names:
                    allocated_office_names.append("room_name")
                    self.office_allocations[room_name] = [person_data]
                    allocated_office_names.append(room_name)
                else:
                    self.office_allocations[room_name].append(person_data)

            else:
                if room_name not in allocated_living_space_names:
                    allocated_living_space_names.append("room_name")
                    self.living_space_allocations[room_name] = [person_data]
                    allocated_living_space_names.append(room_name)
                else:
                    self.living_space_allocations[
                        room_name].append(person_data)
        all_ids = []
        all_people = self.fellows+self.staff
        for person in all_people:
            all_ids.append(person["person_id"])

        self.people_counter = max(all_ids)
        cprint("Data reloaded to Amity", 'blue')

        conn.close()

