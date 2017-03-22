import sqlite3


class AmityDatabase(object):
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
    def cur(self):
        """Creates instance of database connection cursor method"""
        return self.conn.cursor()

    def commit(self):
        """Commit changes to database."""
        return self.conn.commit()

    def close(self):
        """Close database connection."""
        return self.conn.close()

    def create_tables (self):
        """Creates tables in specified database file."""
        cursor = self.cur()
        cursor.execute('DROP TABLE IF EXISTS person')
        cursor.execute('DROP TABLE IF EXISTS room')
        cursor.execute('DROP TABLE IF EXISTS allocation')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS person (person_id INTEGER PRIMARY KEY, name TEXT, role TEXT)WITHOUT ROWID')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS room (name TEXT , no_of_members INTEGER, room_type TEXT)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS allocation (room_name TEXT , person_id INTEGER)')

    def save_person(self, person_id, person_name, person_role):
        """Inserts person data into person table"""
        cursor = self.cur()
        cursor.execute('INSERT OR IGNORE INTO person (person_id, name, role) VALUES(?, ?, ?)',
                      (person_id, person_name, person_role)
                      )
    def save_room(self, room_name, room_no_of_members, this_room_type):
        """Inserts data into the room table."""
        cursor = self.cur()
        cursor.execute('INSERT INTO room (name, no_of_members, room_type) VALUES(?, ?, ?)', (room_name, room_no_of_members, this_room_type)
                      )
    def save_allocations(self, this_room_name, this_person_id):
        """Inserts data into the allocations table."""
        cursor = self.cur()
        cursor.execute('INSERT INTO allocation (room_name, person_id) VALUES(?, ?)', (this_room_name, this_person_id)
                          )
    def get_people(self):
        """Retrieves people records from the person table."""
        cursor = self.cur()
        cursor.execute('SELECT * FROM {tn} '.format(tn="person"))
        all_people = cursor.fetchall()
        return all_people

    def get_offices(self):
        """Retrieves offices from the room table."""
        cursor = self.cur()
        cursor.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="office"'.format(
            tn="room", cn="room_type", col1="name", col2="no_of_members"))
        offices = cursor.fetchall()
        return offices

    def get_living_spaces(self):
        """Retrieves living spaces from the room table."""
        cursor = self.cur()
        cursor.execute('SELECT {col1}, {col2} FROM {tn} WHERE {cn}="living_space"'.format(
            tn="room", cn="room_type", col1="name", col2="no_of_members"))
        living_spaces = cursor.fetchall()
        return living_spaces

    def get_allocations(self):
        """Retrieves allocations from the allocations table."""
        cursor = self.cur()
        cursor.execute('SELECT {col1}, {col2} FROM {tn}'.format(
            tn="allocation", col1="room_name", col2="person_id"))
        allocations = cursor.fetchall()
        return allocations
