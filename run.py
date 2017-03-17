#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    amity create_room (office | living_space ) <name>...
    add_person <firstname> <lastname> <role> [<wants_accomodation>]
    reallocate_room <person_id> <room_name>
    load_people <filename>
    print_allocations [-o <filename>]
    print_unallocated [-o <filename>]
    save_state [--db <dbname>]
    load_state <dbfile>
    print_room <room_name>
    print_fellows
    print_staff
    print_offices
    print_living_spaces
    delete_person <person_id>
    delete_room <room_name>
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
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
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

    @docopt_cmd
    def do_load_state(self, arg):
      """Usage: load_state <dbfile>"""
      self.amity.load_state(arg['<dbfile>'])


    @docopt_cmd
    def do_print_fellows(self, arg):
      """Usage: print_fellows"""
      self.amity.print_fellows()

    @docopt_cmd
    def do_print_staff(self, arg):
      """Usage: print_staff"""
      self.amity.print_staff()

    @docopt_cmd
    def do_print_offices(self, arg):
      """Usage: print_offices"""
      self.amity.print_offices()

    @docopt_cmd
    def do_print_living_spaces(self, arg):
      """Usage: print_living_spaces"""
      self.amity.print_living_spaces()

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
