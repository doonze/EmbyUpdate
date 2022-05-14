"""
command line arguments
"""
import argparse
import sys
import db
from functions.colors import Terminalcolors as c
from functions.configsetup import config_setup


# This sets up the command line arguments
def read_args(version_num):
    """
    The read_args function is used to read in the arguments from the command line.
    It returns a list of arguments that can then be passed into other functions.

    Args:
        verNum: Hold the version number of the program

    Returns:
        A dictionary of the arguments passed to it
    """

    parser = argparse.ArgumentParser(
        description="An updater for Emby Media Player", prog='EmbyUpdate')
    parser.add_argument('-c', '--config', action='store_true',
                        help='Runs the config updater', required=False)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version_num,
                        help='Displays version number')
    parser.add_argument('--db_rebuild', action='store_true',
                        help='Rebuilds (Drops/Creates) the database. Resets to default. '
                        'All data will be lost.')
    parser.add_argument('-cd', '--config_display',
                        help='Displays config options. Default: All', nargs='?', const='all')
    args = parser.parse_args()

    # Here we call configupdate to setup or update the config file if command line option -c was invoked
    if args.config:
        print("")
        print("Config update started....")
        print("")
        config_setup()

    if args.db_rebuild:
        while True:
            print()
            response = input(f"Database rebuild was requested. "
                             f"{c.u_line}{c.bold}{c.fg.red}Are you sure?{c.end} "
                             f"All settings will be lost! [y/{c.fg.green}N{c.end}]: ")
            print()
            if response.casefold() == 'y':
                print("Database is being dropped and rebuilt...")
                print()
                db.createdb.create_db(version_num)
                print("Database has been rebuilt. Starting config...")
                print()
                config_setup()
                sys.exit()

            if response in ("n", "N", ""):
                print("Database rebuild has been canceled.")
                print()
                sys.exit()

            print(f"{response} was invalid input, please try again!")
