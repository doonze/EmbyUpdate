#!/usr/bin/env python
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

import argparse
import json
import os.path
import subprocess
import sys
import time
import requests
from config import Config
from selfupdate import SelfUpdate

# Sets the version # for the command line -v/--version response
versionnum = "4.0 Beta"

# Setting default init values
returncode = 0

# Creates the default config object
config = Config()

# Fixes pre version 4.0 config files
config.config_fix()

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# This sets up the command line arguments
parser = argparse.ArgumentParser(description="An updater for Emby Media Player", prog='EmbyUpdate')
parser.add_argument('-c', '--config', action='store_true', help='Runs the config updater', required=False)
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + versionnum,
                    help='Displays version number')
args = parser.parse_args()

# If the user hasn't used the -c/--config command line argument this will test to see if the config file exist.
# If it doesn't it will launch the config setup process
if args.config is False:
    if not os.path.isfile("config.ini"):
        print("")
        print("Config file doesn't exist! Likely this is your first time running the script."
              " We will now run the config creater. If your sure config exist there may be permission issues.")
        print("")
        config.config_setup()

# Here we call configupdate to setup or update the config file if command line option -c was invoked
try:

    if args.config is True:
        print("")
        print("Config update started....")
        print("")
        returncode = config.config_setup()

        # Here we test to see if the called subprocess above got a return code. If the return code is 1 then
        # the entire process is exited and no updates will be installed. This is triggered by one of the two
        # cancel prompts in the configupdate.py script
        if returncode == 1:
            sys.exit()

except Exception as e:
    print("EmbyUpdate: Couldn't call the Config Updater.")
    print("EmbyUpdate: Here's the error we got -- " + str(e))

try:

    config.read_config()

except Exception as e:
    print("EmbyUpdate: Couldn't read the Config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e) + " not found in config file!")
    print("There appears to be a config file error, re-runing config update to fix!")

try:
    # Now well try and update the app if the user chose that option
    if config.self_update is True:
        self_update = SelfUpdate(config)
        config = self_update.self_update()

except Exception as e:
    print("EmbyUpdate: Couldn't read the Config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e) + " not found in config file!")
    print("There appears to be a config file error, re-runing config update to fix!")


# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
    ts = time.strftime("%x %X", time.localtime())
    return "<" + ts + "> "

# The github API of releases for Emby Media Browser. This includes beta and production releases
url = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(url)
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
