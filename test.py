import unittest
import sqlite3
import os
import tempfile
from unittest import mock 

from amity import Amity
from fellow import Fellow
from living_space import LivingSpace
from office import Office
from staff import Staff


class AmityTest(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.fellows = [{"person_id":1, "name":"Maryanne Waceke"}, {"person_id":2, "name":"Cynthia Wangui"}]
        self.amity.offices = [{"name": "camelot", "no_of_members": 1, "max_members": 6}, {
            "name": "hogwarts", "no_of_members": 0, "max_members": 6}, {"name":"narnia", "no_of_members":6,"max_members":6}]
        self.amity.living_spaces = [
            {"name": "emerald", "no_of_members": 4, "max_members": 4}]
        self.amity.staff = [{"person_id":2, "name": "Mwaura Kariuki"}]
        self.amity.office_allocations = {"camelot":[{"person_id":1, "name":"Maryanne Waceke"}]}

       
        

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
        self.assertEqual(self.amity.add_person("harry", "kimani", "2"), "Please specify whether person is fellow or staff.")

    def test_add_person_does_not_allocate_staff_accomodation(self):
        original_length = len(self.amity.staff)
        self.assertEqual(self.amity.add_person("Stella", "Murimi", "staff", "yes"), "Staff does not get living space. staff created with no living space.")

    def test_create_room_one_room(self):
        original_length = len(self.amity.offices)
        self.amity.create_room("office", "narnia")
        self.assertTrue(len(self.amity.offices) > original_length)

    def test_create_room_more_rooms(self):
        original_length = len(self.amity.living_spaces)
        self.amity.create_room("living_space", ["quartz", "topaz", "emerald"])
        self.assertEqual(len(self.amity.living_spaces), original_length+2)


    def test_create_room_does_not_create_duplicate_rooms(self):
        #refer to self.amity.offices camelot exists
        original_length = len(self.amity.offices)
        self.amity.create_room("office",["camelot"])
        self.assertEqual(len(self.amity.offices), original_length)


    def test_create_room_takes_either_living_space_or_office_for_type(self):
        self.assertEqual(self.amity.create_room("sitting_room", "narnia"),"Please input a room type of either office or living space.")

    def test_create_room_only_takes_strings_as_room_names(self):
        self.assertEqual(self.amity.create_room("office", ["1"]), "Office name is not a valid office name.", 'red')

    def test_reallocate_room_works(self):
        original_camelot_occupants = self.amity.offices[0]["no_of_members"]
        original_hogwarts_occupants = self.amity.offices[1]["no_of_members"]
        self.amity.reallocate_room(1, "hogwarts")
        camelot = [room for room in self.amity.offices if room["name"] is "camelot"][0]
        self.assertTrue(camelot["no_of_members"]>0)

    def test_reallocate_room_does_not_reallocate_inexistent_rooms(self):
        self.assertTrue(self.amity.reallocate_room(1, "platform"), "Please try again.")

    def test_reallocate_room_does_not_Reallocate_inexistent_people(self):
        self.assertTrue(self.amity.reallocate_room(3, "hogwarts"), "Person does not exist.")

    def test_print_room_does_not_print_inexistent_rooms(self):
        self.assertEqual(self.amity.print_room("shell"), "Room does not exist.")

    def test_delete_room_works(self):
        original_length_of_offices = len(self.amity.offices)
        self.amity.delete_room("narnia")
        self.assertTrue(original_length_of_offices > len(self.amity.offices))

    def test_delete_person_works(self):
         original_no_of_fellows = len(self.amity.fellows)
         self.amity.delete_person(2)
         self.assertTrue(len(self.amity.fellows)<original_no_of_fellows)

    # def test_print_allocations_works(self):
    #     my_function = mock.Mock()
    #     self.amity.print_allocations(my_function)
    #     my_function.self.amity.print_allocations.assert_called_with()

    # def test_print_unallocated_works(self):
    #     temporary_unallocated = os.path.join(tempfile.gettempdir(), "tempunallocated")

    # def test_save_state_works(self):
    #     self.amity.save_state = MagicMock
    #     self.amity.save_state.assert_called_with("amitydb")
        
    # def test_load_state_works(self):
    #     pass
   

    def tearDown(self):
        self.amity





if __name__ == '__main__':
    unittest.main()
