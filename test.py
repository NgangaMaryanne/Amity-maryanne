import unittest
import sqlite3
import os

from amity import Amity
from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff


class AmityTest(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.fellows = [{"name":"Maryanne Waceke","role":"fellow" ,"office":"camelot"}]
        self.amity.offices = [{"name": "camelot", "no_of_members": 1, "max_members": 6}, {
            "name": "hogwarts", "no_of_members": 0, "max_members": 6}]
        self.amity.living_spaces = [
            {"name": "emerald", "no_of_members": 4, "max_members": 4}]
        self.amity.staff = []

    def test_add_person_fellow(self):
        original_length = len(self.amity.fellows)
        self.amity.add_person("Jake", "Mwai", "fellow", "yes")
        self.assertTrue(len(self.amity.fellows) > original_length)

    def test_add_person_staff(self):
        original_length = len(self.amity.staff)
        self.amity.add_person("Sally", "Irungu", "staff")
        self.assertTrue(len(self.amity.staff) > original_length)

    def test_add_person_takes_either_role_of_staff_or_fellow(self):
        original_length = len(self.amity.staff)
        self.assertEqual(self.amity.add_person("harry", "kimani", 2), "Please enter valid role.")

    def test_add_person_takes_either_yes_or_no_for_wants_accomodaton(self):
        original_length = len(self.amity.fellows)
        self.assertEqual(self.amity.add_person("harry", "kimani", "fellow", 3),"invalid accomodation option, fellow created but not assigned living space.")

    def test_add_person_does_not_allocate_staff_accomodation(self):
        original_length = len(self.amity.staff)
        self.assertEqual(self.amity.add_person("Stella", "Murimi", "staff", "yes"), "Staff does not get living space. staff created with no living space.")

    def test_create_room_one_room(self):
        original_length = len(self.amity.offices)
        self.amity.create_room("office", "narnia")
        self.assertTrue(len(self.amity.offices) > original_length)

    def test_create_room_more_rooms(self):
        original_length = len(self.amity.living_spaces)
        self.amity.create_room("living_space", "narnia", "topaz", "emerald")
        self.assertEqual(len(self.amity.living_spaces), original_length+2)


    def test_create_room_does_not_create_duplicate_rooms(self):
        #refer to self.amity.offices camelot exists
        original_length = len(self.amity.offices)
        self.amity.create_room("office","camelot","valhalla")
        self.assertEqual(len(self.amity.offices), original_length+1)


    def test_create_room_takes_either_living_space_or_office_for_type(self):
        self.assertEqual(self.amity.create_room("sitting_room", "narnia"),"Please input a room type of either office or living space.")

    def test_create_room_only_takes_strings_as_room_names(self):
        self.assertEqual(self.amity.create_room("office", 1, 2), "room name should be a string.")

    # def test_allocate_office(self):
    #     pass
    def test_allocate_living_space_works(self):
        original_occupants = self.amity.living_spaces[0]["no_of_members"]
        self.amity.allocate_living_space("F120", "emerald")
        self.assertTrue(
            self.amity.living_spaces[0]["no_of_members"] > original_occupants)

    def test_allocate_living_space_doesnt_allocate_staff(self):
        self.assertEqual(self.amity.allocate_living_space("S12", "emerald"), "Staff cannot be allocated living space.")

    @unittest.skip("dictionary error")
    def test_allocate_living_space_doesnt_allocate_beyond_maximum(self):
        self.amity.allocate_living_space("F120", "emerald")
        import pdb; pdb.set_trace()
        self.assertNotEqual(self.amity.fellows[0]["living_space"], "emerald")

    def test_reallocate_office_works(self):
        original_camelot_occupants = self.amity.offices[0]["no_of_members"]
        original_hogwarts_occupants = self.amity.offices[1]["no_of_members"]
        self.amity.reallocate_office("F16", "hogwarts")
        self.assertTrue(self.amity.offices[0]["no_of_members"]<original_camelot_occupants)
        self.assertTrue(self.amity.offices[1]["no_of_members"]>original_hogwarts_occupants)

    def tearDown(self):
        self.amity





if __name__ == '__main__':
    unittest.main()
