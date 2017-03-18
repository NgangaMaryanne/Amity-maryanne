#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    amity create_room (office | living_space ) <name>...
    amity add_person <firstname> <lastname> <role> [<wants_accomodation>]
    amity reallocate_room <person_id> <room_name>
    amity load_people <filename>
    amity print_allocations [-o <filename>]
    amity print_unallocated [-o <filename>]
    amity save_state [--db <dbname>]
    amity load_state <dbfile>
    amity print_room <room_name>
    amity list_fellows
    amity list_staff
    amity list_offices
    amity list_living_spaces
    amity delete_person <person_id>
    amity delete_room <room_name>
    amity (-i | --interactive)
    amity (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    -o FILE --output=FILE specify output file.
    --db=SQLITE_DATABASE  specify database name.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from amity import Amity
from termcolor import cprint
from pyfiglet import figlet_format


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):

    cprint("\n")
    cprint(figlet_format("AMITY".center(10), font="block"),
           "blue", attrs=["bold"])
    def introduction():
        cprint("\n")
        cprint("ROOM ALLOCATION COMMANDS:".center(30), 'yellow')
        cprint("\n")
        cprint(
            "1. create_room (office | living_space ) <name>...", 'yellow')
        cprint(
            "2. add_person <first_name> <last_name> (Fellow|Staff)"
            "[<wants_accomodation>]".center(40), 'yellow')
        cprint("3. reallocate_room <person_id> <room_name>".center(40), 'yellow')
        cprint("4. load_people <filename>", 'yellow')
        cprint("5. print_room <room_name>", 'yellow')
        cprint("6. list_fellows", 'yellow')
        cprint("7. list_staff", 'yellow')
        cprint("8. list_offices", 'yellow')
        cprint("9. list_living_spaces", 'yellow')
        cprint("9. delete_person <person_id>", 'yellow')
        cprint("9. delete_room <room_name>", 'yellow')

        cprint("\n")
        cprint("OTHER COMMANDS:".center(20), 'yellow')
        cprint("\n")
        cprint("1. help".center(10), 'yellow')
        cprint("2. quit".center(10), 'yellow')
        cprint("\n\n")

    intro = introduction()
    prompt = '(Amity-->) '
    file = None
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office | living_space ) <name>... """

        if arg['office']:
          self.amity.create_room("office", arg['<name>'])
        elif arg['living_space']:
          self.amity.create_room("living_space", arg['<name>'])
        else:
          print("please input valid room type")

    @docopt_cmd
    def do_add_person(self, arg):
      """Usage: add_person <firstname> <lastname> <role> [<wants_accomodation>]"""
      if arg['<wants_accomodation>']:
        self.amity.add_person(arg['<firstname>'], arg['<lastname>'], arg['<role>'], arg['<wants_accomodation>'])
      else:
        self.amity.add_person(arg['<firstname>'], arg['<lastname>'], arg['<role>'])

    @docopt_cmd
    def do_reallocate_room(self, arg):
      """Usage: reallocate_room <person_id> <room_name>"""
      self.amity.reallocate_room(arg['<person_id>'], arg['<room_name>'])

    @docopt_cmd
    def do_load_people(self,arg):
      """Usage: load_people <filename>"""
      self.amity.load_people(arg['<filename>'])

    @docopt_cmd
    def do_print_allocations(self, arg):
      """Usage: print_allocations [ -o <filename>]"""
      if arg['<filename>']:
        self.amity.print_allocations(arg['<filename>'])
      else:
        self.amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
      """Usage: print_unallocated [-o <filename>]"""
      if arg['<filename>']:
        self.amity.print_unallocated(arg['<filename>'])
      else:
        self.amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
      """Usage: print_room <room_name>"""
      self.amity.print_room(arg['<room_name>'])

    @docopt_cmd
    def do_save_state(self, arg):
      """Usage: save_state [--db <dbname>]"""
      if arg['<dbname>']:
        self.amity.save_state(arg['<dbname>'])
      else:
        self.amity.save_state("amitydb")
        cprint("Data automatically saved to amitydb")

    @docopt_cmd
    def do_load_state(self, arg):
      """Usage: load_state <dbfile>"""
      self.amity.load_state(arg['<dbfile>'])


    @docopt_cmd
    def do_list_fellows(self, arg):
      """Usage: list_fellows"""
      self.amity.list_fellows()

    @docopt_cmd
    def do_list_staff(self, arg):
      """Usage: list_staff"""
      self.amity.list_staff()

    @docopt_cmd
    def do_list_offices(self, arg):
      """Usage: list_offices"""
      self.amity.list_offices()

    @docopt_cmd
    def do_list_living_spaces(self, arg):
      """Usage: list_living_spaces"""
      self.amity.list_living_spaces()

    @docopt_cmd
    def do_delete_person(self, arg):
      """Usage: delete_person <person_id>"""
      self.amity.delete_person(arg['<person_id>'])

    @docopt_cmd
    def do_delete_room(self, arg):
      """Usage: delete_room <room_name>"""
      self.amity.delete_room(arg['<room_name>'])





    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(__doc__)
