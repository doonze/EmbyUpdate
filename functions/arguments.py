"""
command line arguments
"""
import argparse
import sys
import db
from db import createdb
from db import dbobjects as db
from db.editconfig import edit_config, edit_distroconfig
from functions.colors import Terminalcolors as c
from functions.configsetup import config_setup


# This sets up the command line arguments
def read_args(version):
    """
    The read_args function is used to read in the arguments from the command line.
    It returns a list of arguments that can then be passed into other functions.

    Args:
        version: Hold the version number of the program

    Returns:
        A dictionary of the arguments passed to it
    """

    parser = argparse.ArgumentParser(
        description="An updater for Emby Media Player",
        prog='EmbyUpdate')
    parser.add_argument('-c', '--config',
                        action='store_true',
                        help='Runs the config creator/updater',
                        required=False)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + version,
                        help='Displays version number')
    parser.add_argument('--db_rebuild',
                        action='store_true',
                        help=f'Rebuilds (Drops/Creates) the database. {c.fg.lt_red}Resets to '
                        f'default. All data will be lost.{c.end}')
    parser.add_argument('-cd',
                        dest='config_display',
                        choices=('mainconfig', 'selfupdate', 'serverinfo', 'distroconfig',
                                 'edit'),
                        help=f'''Config Display: Used to display config settings. Use with "edit"
                               to update configs. Can display or edit multiple configs at once. Examples: 
                               "{c.fg.cyan}-cd mainconfig serverinfo{c.end}" would display both configs. 
                               "{c.fg.cyan}-cd mainconfig serverinfo edit{c.end}" would allow you to edit both.
                               Allowable values are {c.fg.green}['mainconfig', 'selfupdate', 'serverinfo', 'distroconfig',
                                   'edit']{c.end}''',
                        type=str,
                        default=None,
                        nargs="+",
                        metavar="")
    parser.add_argument('-dl',
                        dest='logs_display',
                        choices=('emby', 'self', 'errors', 'runlog'),
                        help=f'''Logs Display: Used to display logs. Examples: 
                                   "{c.fg.cyan}-dl emby{c.end}" would display the Emby Server update logs. 
                                   "{c.fg.cyan}-dl emby self{c.end}" would display both the Emby logs and self logs.
                                   Allowable values are {c.fg.green}['emby', 'self', 'errors', 'runlog']{c.end}''',
                        type=str,
                        default=None,
                        nargs="+",
                        metavar="")
    args = parser.parse_args()

    # Here we call configupdate to set up or update the config file if command line
    # option -c was invoked
    if args.config:
        print("")
        print("Config update started....")
        print("")
        config_setup(version)

    # Here we rebuild the database
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
                createdb.create_db(version)
                print("Database has been rebuilt. Starting config...")
                print()
                config_setup()
                sys.exit()

            if response in ("n", "N", ""):
                print("Database rebuild has been canceled.")
                print()
                sys.exit()

            print(f"{response} was invalid input, please try again!")

    # Here we display the config settings
    display_config = args.config_display

    displayed = False

    if display_config is not None:
        if "mainconfig" in display_config:
            mainconfig = db.MainConfig()
            mainconfig.pull_from_db()
            key_map = mainconfig.print_me()
            if "edit" in display_config:
                edit_config(key_map, mainconfig)

            displayed = True

        if "selfupdate" in display_config:
            print()
            print(f"{c.fg.yellow}SelfUpdate:{c.end}")
            selfupdate = db.SelfUpdate()
            selfupdate.pull_from_db()
            key_map = selfupdate.print_me()
            if "edit" in display_config:
                edit_config(key_map, selfupdate)

            displayed = True

        if "serverinfo" in display_config:
            print()
            print(f"{c.fg.yellow}ServerInfo:{c.end}")
            serverinfo = db.ServerInfo()
            serverinfo.pull_from_db()
            key_map = serverinfo.print_me()
            if "edit" in display_config:
                edit_config(key_map, serverinfo)

            displayed = True

        if "distroconfig" in display_config:
            if "edit" in display_config:
                distroconfig = db.DistroConfig()
                distro_dict = distroconfig.print_me(edit=True)
                edit_distroconfig(distro_dict)
            else:    
                print()
                print(f"{c.fg.yellow}DistroConfig:{c.end}")
                distroconfig = db.DistroConfig()
                distro_dict = distroconfig.print_me()
            

            displayed = True

        if displayed:
            sys.exit()
