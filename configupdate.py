#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This file is used to configure and create the config file. It's called from the main app
# EmbyUpdate configupdate file

from builtins import input  # For python 2 compatability and use of input
import sys
import os
from configparser import ConfigParser
import configparser


# Now we'll start gathering user input
# First user will choose their distro

print("[1] Debian X64")
print("[2] Debian ARM")
print("[3] Arch")
print("[4] CentOS")
print("[5] Fedora X64")
print("[6] Fedora ARM")
print("[7] OpenSUSE X64")
print("[8] OpenSUSE ARM")
print("[C] Cancel config update")

while True:
    distrochoice = input("Choose your distro by number or C to cancel update [?]: ")
    if str(distrochoice) == "1":
        chosendistro = "Debian X64"
        break
    elif str(distrochoice) == "2":
        chosendistro = "Debian ARM"
        break
    elif str(distrochoice) == "3":
        chosendistro = "Arch"
        break
    elif str(distrochoice) == "4":
        chosendistro = "CentOS"
        break
    elif str(distrochoice) == "5":
        chosendistro = "Fedora X64"
        break
    elif str(distrochoice) == "6":
        chosendistro = "Fedora ARM"
        break
    elif str(distrochoice) == "7":
        chosendistro = "OpenSUSE X64"
        break
    elif str(distrochoice) == "8":
        chosendistro = "OpenSUSE ARM"
        break
    elif str(distrochoice) == "c" or str(distrochoice) == "C":
        print("")
        print("Exiting config update and installer....")
        print("")
        sys.exit(1)
    else:
        print("")
        print("Invalid Choice! Valid choices are 1-8 or C to cancel. Please Try again.")
        print("")

print("")
print(chosendistro + " Chosen")
print("")

# Now user chooses beta or Stable releases

while True:
    choosebeta = input("Do you want to install the beta version of Emby Server? [y/N] ")
    if choosebeta == "y" or choosebeta == "Y":
        emby_beta_choice = "Beta"
        break
    elif choosebeta == "n" or choosebeta == "N" or choosebeta == "":
        emby_beta_choice = "Stable"
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(emby_beta_choice + " version of Emby has been chosen for install.")
print("")

# User chooses if they wish to stop the server before installing updates. Not normally needed.

while True:
    servstop = input("Do we need to manually stop the server to install? (Likely only needed for Arch.) [y/N] ")
    if servstop == "y" or servstop == "Y":
        servstopchoice = "Server will be manually stopped on install."
        stopserver = True
        break
    elif servstop == "n" or servstop == "N" or servstop == "":
        servstopchoice = "Server will NOT be manually stopped on install."
        stopserver = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(servstopchoice)
print("")

# User chooses if they wish to start the server again after updates. Not normally needed.
while True:
    servstart = input("Do we need to manually start the server after install? (Likely only needed for Arch.) [y/N] ")
    if servstart == "y" or servstart == "Y":
        servstartchoice = "Server will be manually started after install."
        startserver = True
        break
    elif servstart == "n" or servstart == "N" or servstart == "":
        servstartchoice = "Server will NOT be manually started after install."
        startserver = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(servstartchoice)
print("")

# User chooses if they wish to autoupdate the Update app (this program)
while True:
    scriptupdate = input("Keep EmbyUpdate (this script) up to date with latest version? [Y/n] ")
    if scriptupdate == "y" or scriptupdate == "Y" or scriptupdate == "":
        scriptupdatechoice = "Script (EmbyUpdate) will be automatically updated!"
        autoupdate = True
        break
    elif scriptupdate == "n" or scriptupdate == "N":
        scriptupdatechoice = "Script (EmbyUpdate) will NOT be automatically updated!"
        autoupdate = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(scriptupdatechoice)
print("")

# User chooses if they want to update to beta or stable for the script
while True:
    script_beta_choice = input("Install EmbyUpdate Beta versions (this script)? [y/N] ")
    if script_beta_choice.casefold() == "y":
        self_beta_choice = "Script (EmbyUpdate) will be automatically updated!"
        self_beta_update = True
        break
    elif script_beta_choice.casefold() == "n" or script_beta_choice == "":
        self_beta_choice = "Script (EmbyUpdate) will NOT be automatically updated!"
        self_beta_update = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(self_beta_choice)
print("")

print("Choices to write to config file...")
print("Linux distro version to update: " + chosendistro)
print("The chosen Emby Server install version. is: " + emby_beta_choice)
print(servstopchoice)
print(servstartchoice)
print(scriptupdatechoice)
print(self_beta_choice)
print("")

while True:
    confirm = input("Please review above choices and type CONFIRM to continue or c to cancel update "
                    "and install! [CONFIRM/c] ")
    if confirm == "c" or confirm == "C":
        print("")
        print("Exiting config update and installer. No changes were made and nothing will be installed!")
        print("")
        sys.exit(1)
    elif confirm == "CONFIRM":
        break
    else:
        print("")
        print("Invalid choice. Please type CONFIRM to continue or c to cancel!!")
        print("")


# Setup the config interface
config = configparser.ConfigParser()

# Test if the config file exist
try:
    if not os.path.isfile("config.ini"):
        cfgexist = False
    else:
        cfgexist = True
except Exception as e:
    print("EmbyUpdate: Couldn't access the config.ini file. Permission issues? We can't continue")
    print("EmbyUpdate: Here's the error we got -- " + str(e))
    sys.exit(1)

# If config doesn't exist (cfgexist False) it will create it with the correct values filled in and
# if it does exist (cfgexist True) it will simply update the existing config
try:
    if cfgexist is False:
        config['DISTRO'] = {'installdistro': chosendistro, 'releaseversion': emby_beta_choice}
        config['SERVER'] = {'stopserver': stopserver, 'startserver': startserver, 'embyversion': "First Run"}
        config['EmbyUpdate'] = {'autoupdate': autoupdate, 'version': "First Run", 'releaseversion': script_beta_choice}
    elif cfgexist is True:
        config.read('config.ini')
        config['DISTRO']['installdistro'] = chosendistro
        config['DISTRO']['releaseversion'] = emby_beta_choice
        config['SERVER']['stopserver'] = str(stopserver)
        config['SERVER']['startserver'] = str(startserver)
        config['EmbyUpdate']['autoupdate'] = str(autoupdate)
        config['EmbyUpdate']['releaseversion'] = str(script_beta_choice)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
except Exception as e:
    print("EmbyUpdate: Couldn't write to the config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e))
    sys.exit(1)

print("")
print("Config written to file, install continuing!")
print("")
