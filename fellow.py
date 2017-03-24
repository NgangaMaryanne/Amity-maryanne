from person import Person

class Fellow (Person):
    def __init__(self, person_id, name, role = "fellow"):
        super(Fellow, self).__init__(person_id, name, role)
        
    def __str__(self):
        pass