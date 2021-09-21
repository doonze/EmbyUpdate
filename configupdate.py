#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This file is used to configure and create the config file. It's called from the main app
# EmbyUpdate configupdate file

from builtins import input  # For python 2 compatibility and use of input
import sys
import os
import configparser

configuration = {
    "distro": "None",
    "stopserver": False,
    "startserver": False,
    "embyversion": "First Run",
    "embyrelease": "Stable",
    "selfupdate": True,
    "selfversion": "First Run",
    "selfrelease": "Stable",
    "3.7configfixed": False
}

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
    distro_choice = input("Choose your distro by number or C to cancel update [?]: ")
    if str(distro_choice) == "1":
        configuration["distro"] = "Debian X64"
        break
    elif str(distro_choice) == "2":
        configuration["distro"] = "Debian ARM"
        break
    elif str(distro_choice) == "3":
        configuration["distro"] = "Arch"
        break
    elif str(distro_choice) == "4":
        configuration["distro"] = "CentOS"
        break
    elif str(distro_choice) == "5":
        configuration["distro"] = "Fedora X64"
        break
    elif str(distro_choice) == "6":
        configuration["distro"] = "Fedora ARM"
        break
    elif str(distro_choice) == "7":
        configuration["distro"] = "OpenSUSE X64"
        break
    elif str(distro_choice) == "8":
        configuration["distro"] = "OpenSUSE ARM"
        break
    elif str(distro_choice.casefold()) == "c":
        print("")
        print("Exiting config update and installer....")
        print("")
        sys.exit(1)
    else:
        print("")
        print("Invalid Choice! Valid choices are 1-8 or C to cancel. Please Try again.")
        print("")

print("")
print(configuration["distro"] + " Chosen")
print("")

# Now user chooses beta or Stable releases

while True:
    choose_beta = input("Do you want to install the beta version of Emby Server? [y/N] ")
    if choose_beta.casefold() == "y":
        configuration["embyrelease"] = "Beta"
        break
    elif choose_beta == "n" or choose_beta == "N" or choose_beta == "":
        configuration["embyrelease"] = "Stable"
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(configuration["embyrelease"] + " version of Emby has been chosen for install.")
print("")

# User chooses if they wish to stop the server before installing updates. Not normally needed.

while True:
    servstop = input("Do we need to manually stop the server to install? (Likely only needed for Arch.) [y/N] ")
    if servstop.casefold() == "y":
        servstopchoice = "Server will be manually stopped on install."
        configuration["stopserver"] = True
        break
    elif servstop == "n" or servstop == "N" or servstop == "":
        servstopchoice = "Server will NOT be manually stopped on install."
        configuration["stopserver"]  = False
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
    if servstart.casefold() == "y":
        server_start_choice = "Server will be manually started after install."
        configuration["startserver"] = True
        break
    elif servstart == "n" or servstart == "N" or servstart == "":
        server_start_choice = "Server will NOT be manually started after install."
        configuration["startserver"] = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(server_start_choice)
print("")

# User chooses if they wish to autoupdate the Update app (this program)
while True:
    script_update = input("Keep EmbyUpdate (this script) up to date with latest version? [Y/n] ")
    if script_update.casefold() == "y" or script_update == "":
        script_update_choice = "Script (EmbyUpdate) will be automatically updated!"
        configuration["selfupdate"] = True
        break
    elif script_update.casefold() == "n":
        script_update_choice = "Script (EmbyUpdate) will NOT be automatically updated!"
        configuration["selfupdate"] = False
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(script_update_choice)
print("")

# User chooses if they want to update to beta or stable for the script
while True:
    script_beta_choice = input("Install EmbyUpdate Beta versions (this script)? [y/N] ")
    if script_beta_choice.casefold() == "y":
        self_beta_choice = "Script (EmbyUpdate) will be automatically updated to Beta!"
        configuration["selfrelease"] = "Beta"
        break
    elif script_beta_choice.casefold() == "n" or script_beta_choice == "":
        self_beta_choice = "Script (EmbyUpdate) will NOT be automatically updated to Stable!"
        configuration["selfrelease"] = "Stable"
        break
    else:
        print("")
        print("Invalid choice. Please choose y or n")
        print("")

print("")
print(self_beta_choice)
print("")

print("Choices to write to config file...")
print("Linux distro version to update: " + configuration["distro"])
print("The chosen Emby Server install version. is: " + configuration["embyrelease"])
print(servstopchoice)
print(server_start_choice)
print(script_update_choice)
print(self_beta_choice)
print("")

while True:
    confirm = input("Please review above choices and type CONFIRM to continue or c to cancel update "
                    "and install! [CONFIRM/c] ")
    if confirm.casefold() == "c":
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

# If config doesn't exist it will create it with the correct values filled in and
# if it does exist it will simply update the existing config
try:
    if cfgexist is False:
        config['DISTRO'] = {'installdistro': configuration["distro"]}
        config['SERVER'] = {'stopserver': configuration["stopserver"],
                            'startserver': configuration["startserver"],
                            'embyversion': configuration["embyversion"],
                            'embyrelease': configuration["embyrelease"]}
        config['EMBYUPDATE'] = {'selfupdate': configuration["selfupdate"],
                                'selfversion': configuration["selfversion"],
                                'selfrelease': configuration["selfrelease"]}
    elif cfgexist is True:
        config.read('config.ini')
        config['DISTRO']['installdistro'] = configuration["distro"]
        config['SERVER']['stopserver'] = configuration["stopserver"]
        config['SERVER']['startserver'] = configuration["startserver"]
        config['SERVER']['embyrelease'] = configuration["embyrelease"]
        config['EMBYUPDATE']['selfupdate'] = configuration["selfupdate"]
        config['EMBYUPDATE']['selfrelease'] = configuration["selfrelease"]
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
except Exception as e:
    print("EmbyUpdate: Couldn't write to the config file.")
    print("EmbyUpdate: Here's the error we got -- " + str(e))
    sys.exit(1)

print("")
print("Config written to file, install continuing!")
print("")
