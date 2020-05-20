#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# EmbyUpdate Version 2.1 Beta
import sys
import os
import json
import requests
import os.path
import time
import argparse
import subprocess

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# Sets the version # for the conmand line -v/--version response
versionnum = "2.1 Beta"

# Just to make python happy
returncode = 0

# This sets up the command line arguments
parser = argparse.ArgumentParser(description="An updater for Emby Media Player",prog='EmbyUpdate')
parser.add_argument('-c','--config', action='store_true', help='Runs the config updater',required=False)
parser.add_argument('-v','--version', action='version', version='%(prog)s ' + versionnum,help='Displays version number')
args = parser.parse_args()

# If the user hasn't used the -c/--config command line argument this will test to see if the config file exist. If it doesn't
# it will prompt the user to run the config tool from the command line. This only needs done once.
if args.config == False:
	if not os.path.isfile("config.ini"):
		print("")
		print("Config file doesn't exist! Likely this is your first time running the script. You MUST run the script with option -c or --config to continue. This only has to be done once.")
		print("")
		sys.exit()

# Here we try python3 configparser import. If that fails it means user is running python2. So we import
# the python2 ConfigParser instead
try:
    import configparser
    config = configparser.ConfigParser()
    python = '3'
    if args.config == True:
        print("")
        print("Config update started....")
        print("")
        returncode = subprocess.call("python3 configupdate.py",shell=True)
        if returncode > 1:
            returncode = subprocess.call("python configupdate.py",shell=True)
except ImportError:
    import ConfigParser
    config = ConfigParser.ConfigParser()
    python = '2'
    if args.config == True:
        print("")
        print("Config update started....")
        print("")
        returncode = subprocess.call("python configupdate.py",shell=True)

# Here we test to see if the called subprocess above got a return code. If the return code is 1 then
# the entire process is exited and no updates will be installed. This is triggered by one of the two
# cancel prompts in the configupdate.py script
if returncode == 1:
    sys.exit()

# Now we're going to open the config file reader
config.read('config.ini')

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

# Here we pull the main config parms.
if python == '3':
	distro = config['DISTRO']['installdistro']
	installbeta = config['DISTRO']['releaseversion']
	serverstop = config['SERVER']['stopserver']
	serverstart = config['SERVER']['startserver']
	appupdate = config['EmbyUpdate']['autoupdate']
elif python == '2':
    distro = config.get('DISTRO', 'installdistro')
    installbeta = config.get('DISTRO', 'releaseversion')
    serverstop = config.get('SERVER', 'stopserver')
    serverstart = config.get('SERVER', 'startserver')
    appupdate = config.get('EmbyUpdate', 'autoupdate')

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
	ts = time.strftime("%x %X", time.localtime())
	return ("<" + ts + "> ")

# We'll try and update the app if the user chose that option
if appupdate == 'True':
    try:
        appupdatecode = subprocess.call("python3 selfupdate.py",shell=True)
        if returncode != 0:
            print('Python 3 was not found, falling back to python 2.')
            appupdatecode = subprocess.call("python selfupdate.py",shell=True)

    except:
        print("Couldn't launch Python for some reason to lanuch selfupdate!")
    print(appupdatecode)


# The github API of releases for Emby Media Browser. This includes beta and production releases
url = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(url)
    updatejson = json.loads(response.text)
    # Here we search the github API response for the most recent version of beta or stable depending on what was chosen 
    #above. 
    for i, entry in enumerate(updatejson):
        if installbeta == 'Beta':

            if entry["prerelease"] == True:
                onlineversion =  entry["tag_name"]
                versiontype = "Beta"
                break
        elif installbeta == 'Stable':

            if entry["prerelease"] == False:
                onlineversion =  entry["tag_name"]
                versiontype = "Stable"
                break

        else:
            print("Couldn't determine release requested, value is " + installbeta)

except Exception as e:
	print(timestamp() + "EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
	print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
	sys.exit()

##########################################################################################################
# This block is just setting up the variables for your selected distro. These can be updated as needed.  #
##########################################################################################################

# Debian/Ubuntu/Mint amd64 *************
if distro == "Debian X64":
	downloadurl = "wget -q --show-progress https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-deb_" + onlineversion + "_amd64.deb" 
	installfile = "dpkg -i -E emby-server-deb_" + onlineversion + "_amd64.deb"
	updatefile  = "emby-server-deb_" + onlineversion + "_amd64.deb"
#***************************************

# Debian/Ubuntu/Mint armhf *************
if distro == "Debian ARM":
	downloadurl = "wget -q --show-progress https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-deb_" + onlineversion + "_armhf.deb"
	installfile = "dpkg -i emby-server-deb_" + onlineversion + "_armhf.deb"
	updatefile  = "emby-server-deb_" + onlineversion + "_armhf.deb"
#***************************************

# Arch Linux ***************************
if distro == "Arch":
	downloadurl = "notused"
	installfile = "pacman -S emby-server"
	updatefile  = "notused"
#***************************************

# CentOS X64 ***************************
# In Cent I think yum will handle the stop/start of the server, but change below if needed
if distro == "CentOS":
	downloadurl = "yum install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
	installfile = "notused"
	updatefile  = "notused"
#****************************************

# Fedora X64 ****************************
# Pretty sure dnf will stop/start the server, but change below if needed
if distro == "Fedora X64":
	downloadurl = "dnf install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
	installfile = "notused"
	updatefile  = "notused"
#***************************************

# Fedora Armv7hl ***********************
# Pretty sure dnf will stop/start the server, but change delow if needed
if distro == "Fedora ARM":
	downloadurl = "dnf install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
	installfile = "notused"
	updatefile  = "notused"
#***************************************

# OpenSUSE X64 *************************
# Pretty sure zypper will stop/start the server, but change below as needed
if distro == "OpenSUSE X64":
	downloadurl = "zypper install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
	installfile = "notused"
	updatefile  = "notused"
#***************************************

# OpenSUSE Armv7hl *********************
# Pretty sure zypper will stop/start the server, but change below as needed
if distro == "OpenSUSE ARM":
	downloadurl = "zypper install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
	installfile = "notused"
	updatefile  = "notused"
#**************************************

###################################################################################################
# End distro setup block. End of user configable sections. Don't change anything below this line. #
###################################################################################################

# Now were going to pull the version from the config file
if python == '3':
	#This fires if user is running python3
	fileversion = config['SERVER']['embyversion']
elif python == '2':
	# This fires if user is running python2
	fileversion = config.get('SERVER', 'embyversion')

# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

onlinefileversion = (onlineversion + "-" + versiontype)

if str(onlinefileversion) in str(fileversion):
    # If the latest online verson matches the last installed version then we let you know and exit
    print(timestamp() + "EmbyUpdate: We're up to date!  Current and Online versions are at " + onlinefileversion + ". Nothing to see here... move along. Script exiting!")
    print('***')
else:
    # If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
    print(timestamp() + "EmbyUpdate: Most recent online version is " + onlinefileversion + " and current installed version is " + fileversion + ". We're updating Emby.")
    print("\n" + timestamp() + "EmbyUpdate: Starting update......")

    try:
        # This will stop the server on a systemd distro if it's been set to true above
        if serverstop is True:
            subprocess.call("systemctl stop emby-server",shell=True)
            for i in xrange(10,0,-1):
                sys.stdout.write(str(i)+' ')
                sys.stdout.flush()
                time.sleep(1)

        # Here we download the package to install if used
        #if "notused" not in downloadurl:
            #subprocess.call(downloadurl,shell=True)

        # Next we install it if used
        #if "notused" not in installfile:
            #os.system(installfile)
            #subprocess.call(installfile,shell=True)

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        #if "notused" not in updatefile:
            #subprocess.call("rm -f " + updatefile,shell=True)

        # This will restart the server if using systemd if set to True above
        if serverstart is True:
            subprocess.call("systemctl start emby-server",shell=True)

	    # Lastly we write the newly installed version into the config file
        try:
            config['SERVER']['embyversion'] = onlinefileversion
        except AttributeError:
            config.set('SERVER', 'embyversion', onlinefileversion)

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print(timestamp() + "EmbyUpdate: Updating to Emby version " + onlinefileversion + " finished! Script exiting!")
        print('')
        print("*****************************************************************************")
        print("\n")

    except Exception as e:
        print(timestamp() + 'EmbyUpdate: Something failed in update. No update done, script exiting')
        print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))

sys.exit()
