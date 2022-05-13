#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
# EmbyUpdate

###############################################################################################
# This script can be used to to keep Emby servers for linux automatically up to date.         #
# It is setup for the X64 and ARM versions of Debian,Ubuntu,Mint,CentOS,Fedora,Arch and       #
# OpenSUSE. Most of these packages will stop/start the server as needed in the internal       #
# install logic of the distro's installer. But if your distro uses systemd then this script   #
# has logic that can stop and start the server if needed. If you don't have systemd then      #
# if you want the server stopped and started by the script you'll need to modify the          #
# commands as needed.                                                                         #
# Should work with both python 2.7 and all flavors of 3.                                      #
###############################################################################################

import os.path
import sys
from genericpath import exists
from functions import (pythonversion, config, arguments, configsetup, selfupdate,
                       api, updatecheck, install)
from db import createdb, dbobjects

# pylint: disable=C0103

# Sets the version # for the command line -v/--version response
VERSIONNUM = "v4.0 - Beta"

# Setting default init values
returncode = None

# Checks for python version, exit if not greater than 3.6
pythonversion.python_version_check()

# Checks for command line arguments

args = arguments.read_args(VERSIONNUM)

# Creates the default config object
configfix = config.Config()

# Fixes pre version 4.0 config files
configfix.config_fix()

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# This will test to see if the DB exist.If it doesn't it will launch the config setup process

if not exists('./db/embyupdate.db'):

    print()
    print("Database does NOT exist, creating database...")
    createdb.create_db(VERSIONNUM)
    print("Database has been created.")
    print()
    print("Starting config setup...")
    print()
    configsetup.config_setup()

# Here we call configupdate to setup or update the config file if command line option -c was invoked
if args.config is True:
    print("")
    print("Config update started....")
    print("")
    configsetup.config_setup()

# We'll get the config from the DB
configobj: dbobjects.ConfigObj = dbobjects.ConfigObj().get_config()
configobj.selfupdate.version = VERSIONNUM

# Now well try and update the app if the user chose that option
if configobj.selfupdate.runupdate is True:
    selfupdate.self_update(configobj)
        
configobj = api.get_main_online_version(configobj)


# Ok, we've got all the info we need. Now we'll test if we even need to update or not

update_needed = updatecheck.check_for_update(configobj) # pylint: disable=E1111

if update_needed:
    install.update_emby(configobj)
    