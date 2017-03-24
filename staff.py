from person import Person

class Staff(Person):
    def __init__(self, person_id, name, role = "staff"):
        super(Staff, self).__init__(person_id, name, role)

    def __str__(self):
        pass
