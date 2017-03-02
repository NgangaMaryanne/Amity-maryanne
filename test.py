import unittest

from amity import Amity
from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff


class AmityTest(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.fellow = Fellow()
        self.Staff = Staff()
        self.office = Office()
        self.livingspace = LivingSpace()

    def test_add_person_fellow(self):
        self.amity.fellows = [{"id":"F16", "name":"Maryanne Waceke","role":"fellow" ,"office":"camelot"}]
        original_length = len(self.amity.fellows)
        self.amity.add_person("Jake", "Mwai", "fellow", "yes")
        self.assertTrue(len(self.amity.fellows) > original_length)

    def test_add_person_staff(self):
        self.amity.staff = []
        original_length = len(self.amity.staff)
        self.amity.add_person("Sally", "Irungu", "staff")
        self.assertTrue(len(self.amity.staff) > original_length)

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
        self.assertEqual(self.amity.staff[0]["living_space"], None)

    def test_create_room_one_room(self):
        self.amity.offices = []
        original_length = len(self.amity.offices)
        self.amity.create_room("living_space", "narnia")
        self.assertTrue(len(self.amity.offices) > original_length)

    def test_create_room_more_rooms(self):
        self.amity.offices = []
        original_length = len(self.amity.offices)
        self.amity.create_room("living_space", "narnia", "topaz", "emerald")
        self.assertEqual(len(self.amity.offices), original_length+3)

    def test_create_room_takes_either_living_space_or_office_for_type(self):
        # self.amity.offices = [{"name": "camelot", "no_of_members": 1, "max_members": 6}]
        # self.amity.living_spaces = [{"name": "emerald", "no_of_members": 1, "max_members": 4}]
        # offices_original_length = len(self.amity.offices)
        # living_spaces_original_length = len(self.amity.living_spaces)
        # self.amity.create_room("sitting_room", "topaz")
        # self.assertEqual(len(self.amity.offices), offices_original_length)
        self.assertEqual(self.amity.create_room("sitting_room", "narnia"),"Please input valid room type")

    def test_create_room_only_takes_strings_as_room_names(self):
        self.assertEqual(self.amity.create_room("office", 1, 2), "Please enter valid room names.")

    def test_allocate_office(self):
        pass
    def test_allocate_living_space_works(self):
        self.amity.living_spaces = [
            {"name": "emerald", "no_of_members": 1, "max_members": 4}]
        original_occupants = self.amity.living_spaces[0]["no_of_members"]
        self.amity.allocate_living_space("F120", "emerald")
        self.assertTrue(
            self.amity.living_spaces[0]["no_of_members"] > original_occupants)

    def test_allocate_living_space_doesnt_allocate_staff(self):
        # self.amity.living_spaces = [
        #     {"name": "emerald", "no_of_members": 1, "max_members": 4}]
        # original_occupants = self.amity.living_spaces[0]["no_of_members"]
        # self.amity.allocate_living_space("S12", "emerald")
        # self.assertEqual(
        #     self.amity.living_spaces[0]["no_of_members"], original_occupants)
        self.assertEqual(self.amity.allocate_living_space("S12", "emerald"), "Staff cannot be allocated living space.")


    def test_allocate_living_space_doesnt_allocate_beyond_maximum(self):
        self.amity.living_spaces = [
            {"name": "emerald", "no_of_members": 4, "max_members": 4}]
        # original_occupants = self.amity.living_spaces[0]["no_of_members"]
        # self.amity.allocate_living_space("F120", "emerald")
        # self.assertEqual(
        #     self.amity.living_spaces[0]["no_of_members"], original_occupants)
        self.assertEqual(self.amity.allocate_living_space("F120", "emerald"), "Room full.")

    def test_reallocate_office_works(self):
        self.amity.offices = [{"name": "camelot", "no_of_members": 1, "max_members": 6}, {
            "name": "hogwarts", "no_of_members": 0, "max_members": 6}]
        self.amity.fellows = [{"id":"F16", "name":"Maryanne Waceke","role":"fellow" ,"office":"camelot"}]
        original_camelot_occupants = self.amity.offices[0]["no_of_members"]
        original_hogwarts_occupants = self.amity.offices[1]["no_of_members"]
        self.amity.reallocate_office("F16", "hogwarts")
        self.assertTrue(self.amity.offices[0]["no_of_members"]<original_camelot_occupants)
        self.assertTrue(self.amity.offices[1]["no_of_members"]>original_hogwarts_occupants)




if __name__ == '__main__':
    unittest.main()
