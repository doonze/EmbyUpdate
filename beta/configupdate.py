#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This file is used to configure and create the config file. It's called from the main app

import sys
import os

# First we'll try python 3 configparser import. If that fails we'll try python 2. This will 
# determine which were using. 
try:
    import configparser
    python = '3'
except ImportError:
    import ConfigParser
    python = '2'

# This function is for compatability between python 3 and python 2
input_func = None
try:
    input_func = raw_input
except NameError:
    input_func = input

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
	distrochoice = input_func("Choose your distro by number or C to cancel update [?]: ")
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
	choosebeta = input_func("Do you want to install the beta version? [y/N] ")
	if choosebeta == "y" or choosebeta == "Y":
		betachoice = "Beta"
		break
	elif choosebeta == "n" or choosebeta == "N" or choosebeta == "":
		betachoice = "Stable"
		break
	else:
		print("")
		print("Invalid choice. Please choose y or n")
		print("")

print("")
print(betachoice + " version of Emby has been choosen for install.")
print("")

# User chooses if they wish to stop the server before installing updates. Not normally needed.

while True:
	servstop = input_func("Do we need to manually stop the server to install? (Likely only needed for Arch.) [y/N] ")
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
	servstart = input_func("Do we need to manually start the server after install? (Likely only needed for Arch.) [y/N] ")
	if servstart == "y" or servstart == "Y":
		servstartchoice = "Server will be manually started after install."
		startserver = True
		break
	elif servstop == "n" or servstart == "N" or servstart == "":
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
	scriptupdate = input_func("Keep EmbyUpdate (this script) up to date with latest version? [Y/n] ")
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

print("Choices to write to config file...")
print("Linux distro version to update: " + chosendistro)
print("The chosen version for install is: " + betachoice)
print(servstopchoice)
print(servstartchoice)
print(scriptupdatechoice)
print("")

while True:
	confirm = input_func("Please review above choices and type CONFIRM to continue or c to cancel update and install! [CONFIRM/c] ")
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


try:
	config = configparser.ConfigParser()
except:
	config = ConfigParser.ConfigParser()

try:
	if not os.path.isfile("config.ini"):
		cfgexist = False
	else:
		cfgexist = True
except Exception as e:
	print("EmbyUpdate: Couldn't access the config.ini file. Permission issues? We can't continue")
	print("EmbyUpdate: Here's the error we got -- " + str(e))
	sys.exit(1)

try:
	if cfgexist == False:
		config['DISTRO'] = {'installdistro' : chosendistro, 'releaseversion' : betachoice}
		config['SERVER'] = {'stopserver' : stopserver, 'startserver' : startserver, 'embyversion' : "First Run"}
		config['EmbyUpdate'] = {'autoupdate' : autoupdate, 'version' : "First Run"}
	elif cfgexist == True:
		config.read('config.ini')
		config['DISTRO']['installdistro'] = chosendistro
		config['DISTRO']['releaseversion'] = betachoice
		config['SERVER']['stopserver'] = str(stopserver)
		config['SERVER']['startserver'] = str(startserver)
		config['EmbyUpdate']['autoupdate'] = str(autoupdate)
	with open('config.ini', 'w') as configfile:
		config.write(configfile)
except:
	if cfgexist == False:
		config.add_section('DISTRO')
		config.set('DISTRO', 'installdistro', chosendistro)
		config.set('DISTRO', 'releaseversion', betachoice)
		config.add_section('SERVER')
		config.set('SERVER', 'stopserver', stopserver)
		config.set('SERVER', 'startserver', startserver)
		config.set('SERVER', 'embyversion', "First Run")
		config.add_section('EmbyUpdate')
		config.set('EmbyUpdate', 'autoupdate', autoupdate)
		config.set('EmbyUpdate', 'version' , "First Run")
	elif cfgexist == True:
		config.read('config.ini')
		config.set('DISTRO', 'installdistro', chosendistro)
		config.set('DISTRO', 'releaseversion', betachoice)
		config.set('SERVER', 'stopserver', str(stopserver))
		config.set('SERVER', 'startserver', str(startserver))
		config.set('EmbyUpdate', 'autoupdate', str(autoupdate))
	with open('config.ini', 'w') as configfile:
		config.write(configfile)

print("")
print("Config written to file, install continuing!")
print("")


