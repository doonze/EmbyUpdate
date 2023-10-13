#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
"""
EmbyUpdate: The main file and only executable script of the EmbyUpdate package


###############################################################################################
# This script can be used to keep Emby servers for linux automatically up to date.            #
# It is set up for the X64 and ARM versions of Debian,Ubuntu,Mint,CentOS,Fedora,Arch and      #
# OpenSUSE. Most of these packages will stop/start the server as needed in the internal       #
# install logic of the distro's installer. But if your distro uses systemd then this script   #
# has logic that can stop and start the server if needed. If you don't have systemd then      #
# if you want the server stopped and started by the script you'll need to modify the          #
# commands as needed.                                                                         #
# Must use python 3.6 +. 3.7 + recommended as dataclasses are used.                           #
###############################################################################################
"""

__version__ = "v4.1"
__author__ = "Justin Hopper"
__email__ = "doonze@gmail.com"
__maintainer__ = "Justin Hopper"
__copyright__ = "Copyright 2023, EmbyUpdate"
__license__ = "GNU3"
__status__ = "Beta"
__credits__ = [""]

# ------------------------------------------------------------------------------------------

import os.path
import sys
import directoryfix
from genericpath import exists
try:
    from functions import (pythonversion, config, arguments, configsetup, selfupdate,
                           api, updatecheck, install, colors)
    from db import createdb, dbobjects

except Exception:
    os.chdir(sys.path[0])
    if os.path.exists("configupdate.py"):
        directoryfix.fix_directory()
        os.execv(sys.argv[0], sys.argv)


def main():
    """
    The main function is the entry point for the program. It is called when embyupdate starts up
    and checks to see if there are any updates available. If there are, it will download them
    and install them.
    """

    # pylint: disable=C0103
    c = colors.Terminalcolors()
    # Sets the version # for the command line -v/--version response
    version = f"{__version__} - {__status__}"

    # Checks for command line arguments
    arguments.read_args(version)

    # Checks for python version, exit if not greater than 3.6
    pythonversion.python_version_check()

    # Fixes pre version 4.0 config files if they exist (upgrade to new DB config system)
    config.Config().config_fix(version)

    # First we're going to force the working path to be where the script lives
    os.chdir(sys.path[0])

    # This will test to see if the DB exist. If it doesn't it will create it and
    # launch the config setup process

    if not exists('./db/embyupdate.db'):
        print()
        print(f"Database does {c.fg.red}NOT{c.end} exist, creating database...")
        createdb.create_db(version)
        print()
        print("Starting config setup...")
        configsetup.config_setup(version)

    # else:
    #    print(f"Database exists! {c.fg.green}CHECK PASSED{c.end}!")

    # We'll get the config from the DB
    config_obj: dbobjects.ConfigObj = dbobjects.ConfigObj().get_config()
    if not config_obj.mainconfig.configran:
        configsetup.config_setup(version)
    config_obj.selfupdate.version = version

    # Now well try and update this app if the user chose that option
    if config_obj.selfupdate.runupdate is True:
        selfupdate.self_update(config_obj)

    config_obj = api.get_main_online_version(config_obj)

    # Ok, we've got all the info we need. Now we'll test if we even need to update or not

    update_needed = updatecheck.check_for_update(config_obj)  # pylint: disable=E1111

    if update_needed:
        install.update_emby(config_obj)


if __name__ == "__main__":
    main()
