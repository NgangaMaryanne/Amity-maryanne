from person import Person

class Fellow (Person):
    def __init__(self, person_id, name):
        super().__init__(person_id, name)
        