import unittest

from amity import Amity
from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff

class AmityTest(unittest.TestCase):
    def setUp(self):
        self.amity=Amity()
        self.fellow = Fellow()
        self.Staff = Staff()
        self.office = Office()
        self.livingspace= LivingSpace()
    def test_add_person_fellow(self):
        self.amity.fellows = []
        original_length = len(self.amity.fellows)
        self.amity.add_person("Jake", "Mwai", "fellow", "yes")
        self.assertTrue(len(self.amity.fellows)>original_length)


    def test_add_person_staff(self):
        self.amity.staff = []
        original_length = len(self.amity.staff)
        self.amity.add_person("Sally", "Irungu", "staff")
        self.assertTrue(len(self.amity.staff)>original_length)

    def test_add_person_takes_either_role_of_staff_or_fellow(self):
        self.amity.staff = []
        original_length = len(self.amity.staff)
        with self.assertRaises(ValueError):
            self.amity.add_person("harry", "kimani", [])



    def test_add_person_takes_either_yes_or_no_for_wants_accomodaton(self):
        self.amity.fellows = []
        original_length = len(self.amity.fellows)
        with self.assertRaises(ValueError):
            self.amity.add_person("harry", "kimani", "fellow", 3)


    def test_add_person_does_not_allocate_staff_accomodation(self):
        self.amity.staff = []
        original_length = len(self.amity.staff)
        self.amity.add_person("Stella", "Murimi", "staff", "yes")
        self.assertTrue(len(self.amity.staff)==original_length)

    def test_create_room_one_room(self):
        self.amity.offices=[]
        original_length=len(self.amity.offices)
        self.amity.create_room("living_space", "narnia")
        self.assertTrue(len(self.amity.offices)>original_length)

    def test_create_room_more_rooms(self):
        self.amity.offices= []
        original_length = len(self.amity.offices)
        self.amity.create_room("living_space", "narnia","topaz","emerald")
        self.assertTrue(len(self.amity.offices)>original_length)












if __name__=='__main__':
    unittest.main()




