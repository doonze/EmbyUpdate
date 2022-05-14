#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
"""
EmbyUpdate: The main file and only executable script of the EmbyUpdate package


###############################################################################################
# This script can be used to to keep Emby servers for linux automatically up to date.         #
# It is setup for the X64 and ARM versions of Debian,Ubuntu,Mint,CentOS,Fedora,Arch and       #
# OpenSUSE. Most of these packages will stop/start the server as needed in the internal       #
# install logic of the distro's installer. But if your distro uses systemd then this script   #
# has logic that can stop and start the server if needed. If you don't have systemd then      #
# if you want the server stopped and started by the script you'll need to modify the          #
# commands as needed.                                                                         #
# Must use python 3.6 +. 3.7 + recommended as dataclasses are used.                           #
###############################################################################################
"""

__version__ = "v4.0"
__author__ = "Justin Hopper"
__email__ = "doonze@gmail.com"
__maintainer__ = "Justin Hopper"
__copyright__ = "Copyright 2022, EmbyUpdate"
__license__ = "GNU3"
__status__ = "Beta"
__credits__ = [""]

# ------------------------------------------------------------------------------------------

import os.path
import sys
from genericpath import exists
from functions import (pythonversion, config, arguments, configsetup, selfupdate,
                       api, updatecheck, install, colors)
from db import createdb, dbobjects

c = colors.Terminalcolors()

def main():
    """
    The main function is the entry point for the program. It is called when embyupdate starts up 
    and checks to see if there are any updates available. If there are, it will download them
    and install them.
    """
    
    # pylint: disable=C0103

    # Sets the version # for the command line -v/--version response
    VERSIONNUM = f"{__version__} - {__status__}"

    # Checks for python version, exit if not greater than 3.6
    pythonversion.python_version_check()

    # Creates the default config object
    configfix = config.Config()

    # Fixes pre version 4.0 config files
    configfix.config_fix(VERSIONNUM)

    # First we're going to force the working path to be where the script lives
    os.chdir(sys.path[0])

    # This will test to see if the DB exist. If it doesn't it will create it and 
    # launch the config setup process

    if not exists('./db/embyupdate.db'):

        print()
        print(f"Database does {c.fg.red}NOT{c.end} exist, creating database...")
        createdb.create_db(VERSIONNUM)
        print()
        print("Starting config setup...")
        configsetup.config_setup()
        
    else:
        print(f"Database exists! {c.fg.green}CHECK PASSED{c.end}!")
        
    # Checks for command line arguments
    arguments.read_args(VERSIONNUM)
        
    # We'll get the config from the DB
    configobj: dbobjects.ConfigObj = dbobjects.ConfigObj().get_config()
    configobj.selfupdate.version = VERSIONNUM

    # Now well try and update the app if the user chose that option
    if configobj.selfupdate.runupdate is True:
        selfupdate.self_update(configobj)

    configobj = api.get_main_online_version(configobj)


    # Ok, we've got all the info we need. Now we'll test if we even need to update or not

    update_needed = updatecheck.check_for_update(configobj)  # pylint: disable=E1111

    if update_needed:
        install.update_emby(configobj)
        
if __name__ == "__main__":
    main()
