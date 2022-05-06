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
import time
from genericpath import exists
import requests
from functions import pythonversion, config, arguments, configsetup
from db.createdb import create_db
from selfupdate import SelfUpdate


# Sets the version # for the command line -v/--version response
VESRIONNUM = "4.0 Beta"

# Setting default init values
returncode = None # pylint: disable=C0103

# Checks for python version, exit if not greater than 3.6
pythonversion.python_version_check()

# Checks for command line arguments

args = arguments.read_args(VESRIONNUM)

# Creates the default config object
config = config.Config()

# Fixes pre version 4.0 config files
config.config_fix()

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# If the user hasn't used the -c/--config command line argument this will test to see if the DB exist.
# If it doesn't it will launch the config setup process
if args.config is False:

    if not exists('./db/embyupdate.db'):

        print()
        print("Database does NOT exist, creating database...")
        create_db()
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

configsetup.config_setup() # TODO remove me when done testing

try:

    configobj = config.read_config()

except Exception as e:
    print("EmbyUpdate: Couldn't read the Config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e) + " not found in config file!")
    print("There appears to be a config file error, re-runing config update to fix!")

try:
    # Now well try and update the app if the user chose that option
    if configobj.selfupdate.runupdate is True:
        #self_update = SelfUpdate(config)
        #config = self_update.self_update()
        print("self update disabled")

except Exception as e:
    print("EmbyUpdate: Couldn't read the Config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e) + " not found in config file!")
    print("There appears to be a config file error, re-runing config update to fix!")


# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
    """
    The timestamp function returns the current date and time.
    
    :returns: The current date and time.
    
    
    :return: The date and time of the current moment in this format: month/day/year
    :doc-author: Trelent
    """
    ts = time.strftime("%x %X", time.localtime())
    return "<" + ts + "> "

# The github API of releases for Emby Media Browser. This includes beta and production releases
URL = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(URL)
    updatejson = json.loads(response.text)
    # Here we search the github API response for the most recent version of beta or stable depending on what was chosen
    # above.
    for i, entry in enumerate(updatejson):
        if config.emby_release == 'Beta':

            if entry["prerelease"] is True:
                onlineversion = entry["tag_name"]
                break
        elif config.emby_release == 'Stable':

            if entry["prerelease"] is False:
                onlineversion = entry["tag_name"]
                break

        else:
            print("Couldn't determine release requested, value is " + config.emby_release)

except Exception as e:
    print(timestamp() + "EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
    print(timestamp() + "EmbyUpdate: Here's the error we got -- " + repr(e))
    print(config.emby_release)
    sys.exit()

##########################################################################################################
# This block is just setting up the variables for your selected distro. These can be updated as needed.  #
##########################################################################################################

# Debian/Ubuntu/Mint amd64 *************
if config.distro == "Debian X64":
    downloadurl = "https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-deb_" + onlineversion + "_amd64.deb"
    installfile = "dpkg -i -E emby-server-deb_" + onlineversion + "_amd64.deb"
    updatefile = "emby-server-deb_" + onlineversion + "_amd64.deb"
# ***************************************

# Debian/Ubuntu/Mint armhf *************
if config.distro == "Debian ARM":
    downloadurl = "https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-deb_" + onlineversion + "_armhf.deb"
    installfile = "dpkg -i emby-server-deb_" + onlineversion + "_armhf.deb"
    updatefile = "emby-server-deb_" + onlineversion + "_armhf.deb"
# ***************************************

# Arch Linux ***************************
if config.distro == "Arch":
    downloadurl = "notused"
    installfile = "pacman -S emby-server"
    updatefile = "notused"
# ***************************************

# CentOS X64 ***************************
# In Cent I think yum will handle the stop/start of the server, but change below if needed
if config.distro == "CentOS":
    downloadurl = "yum --y install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
    installfile = "notused"
    updatefile = "notused"
# ****************************************

# Fedora X64 ****************************
# Pretty sure dnf will stop/start the server, but change below if needed
if config.distro == "Fedora X64":
    downloadurl = "dnf -y install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
    installfile = "notused"
    updatefile = "notused"
# ***************************************

# Fedora Armv7hl ***********************
# Pretty sure dnf will stop/start the server, but change below if needed
if config.distro == "Fedora ARM":
    downloadurl = "dnf -y install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
    installfile = "notused"
    updatefile = "notused"
# ***************************************

# OpenSUSE X64 *************************
# Pretty sure zypper will stop/start the server, but change below as needed
if config.distro == "OpenSUSE X64":
    downloadurl = "zypper install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + \
                  "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
    installfile = "notused"
    updatefile = "notused"
# ***************************************

# OpenSUSE Armv7hl *********************
# Pretty sure zypper will stop/start the server, but change below as needed
if config.distro == "OpenSUSE ARM":
    downloadurl = "zypper install -y https://github.com/MediaBrowser/Emby.Releases/releases/download/" \
                  + onlineversion + "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
    installfile = "notused"
    updatefile = "notused"
# **************************************

###################################################################################################
# End distro setup block. End of user configurable sections. Don't change anything below this line. #
###################################################################################################

# Now were going to pull the installed version from the config file


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

    """ try:
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
        print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e)) """
