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

import json
import os.path
import sys
from genericpath import exists
import requests
from functions import pythonversion, config, arguments, configsetup, selfupdate, timestamp, api
from db import createdb, dbobjects

# pylint: disable=C0103

# Sets the version # for the command line -v/--version response
VERSIONNUM = "4.0 Beta"

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
    createdb.create_db()
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

# Now well try and update the app if the user chose that option
if configobj.selfupdate.runupdate is True:
    selfupdate.self_update()
        
configobj = api.get_main_online_version(configobj)


# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

onlinefileversion = (onlineversion + "-" + config.emby_release)

if str(onlinefileversion) in str(config.emby_version):
    # If the latest online version matches the last installed version then we let you know and exit
    print(timestamp() + "EmbyUpdate: We're up to date!  Current and Online versions are at " + onlinefileversion +
          ". Exiting.")
    print('***')
else:
    # If the online version DOESN'T match the last installed version we let you know what the versions are and start
    # updating
    print(timestamp() + "EmbyUpdate: Most recent online version is "
          + onlinefileversion + " and current installed version is " + config.emby_version + ". We're updating Emby.")
    print("\n" + timestamp() + "EmbyUpdate: Starting update......")

    try:
        # This will stop the server on a systemd distro if it's been set to true above
        if config.stop_server is True:
            print("Stopping Emby server.....")
            stopreturn = subprocess.call("systemctl stop emby-server", shell=True)
            time.sleep(3)
            if stopreturn > 0:
                print("Server Stop failed! Non-critical error! Investigate if needed.")

            print("Emby Server Stopped...")

        # Here we download the package to install if used
        if "notused" not in downloadurl:
            print("Starting Package download...")
            download = requests.get(downloadurl)
            with open(updatefile, 'wb') as file:
                file.write(download.content)
            print("Package downloaded!")

        # Next we install it if used
        if "notused" not in installfile:
            print("Installing/Updating Emby server....")
            installreturn = subprocess.call(installfile, shell=True)
            if installreturn > 0:
                print("Install/Update failed! Exiting!")
                sys.exit()
            print("Install/Update Finished!")

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        if "notused" not in updatefile:
            print("Removing install file...")
            subprocess.call("rm -f " + updatefile, shell=True)
            print("File removed!")

        # This will restart the server if using systemd if set to True above
        if config.start_server is True:
            print("Restarting Emby server after update...")
            startreturn = subprocess.call("systemctl start emby-server", shell=True)
            if startreturn > 0:
                print("Server start failed. Non-critical to update but server may not be running. Investigate.")
            print("Server restarted!")

        # Lastly we write the newly installed version into the config file
        try:
            config.emby_version = onlinefileversion

            config.write_config()

            print(timestamp() + "EmbyUpdate: Updating to Emby version " + onlinefileversion +
                  " finished! Script exiting!")
            print('')
            print("*****************************************************************************")
            print("\n")

        except Exception as e:
            print(timestamp() + "EmbyUpdate: We had a problem writing to config after update!")
            print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
            sys.exit()

    except Exception as e:
        print(timestamp() + 'EmbyUpdate: Something failed in update. No update done, script exiting')
        print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
