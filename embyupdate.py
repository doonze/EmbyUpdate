#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import sys
import os
import json
import requests
import os.path
import time

###############################################################################################
# This script can be used to to keep Emby servers for linux automatically up to date.         #
# It is setup for the X64 and ARM versions of Debian,Ubuntu,Mint,CentOS,Fedora,Arch and       #
# OpenSUSE. Most of these packages will stop/start the server as needed in the internal       #
# install logic of the distro's installer. But if your distro uses systemd then this script   #
# has logic that can stop and start the server if needed. If you don't have systemd then      #
# if you want the server stopped and started by the script you'll need to modify the          #
# commands as needed. Just make sure if not running Debian/Ubuntu/Mint X64 to comment out     #
# that block of code and uncomment the correct block for your Distro/Architecture.            #
# Should work with both python 2.7 and all flavors of 3.                                      #
###############################################################################################

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
	ts = time.strftime("%x %X", time.localtime())
	return ("<" + ts + "> ")

# This URL is for production release only
url = "https://api.github.com/repos/mediabrowser/Emby.releases/releases/latest"

# At this time I can't find the API path for beta, I'll add if I ever figure it out

# Next we want to see if we have created a version.txt file yet, we'll create one
# if we haven't. Any error we let you know about.
try:
	if not os.path.isfile("version.txt"):
		print(timestamp() + "EmbyUpdate: version.txt doesn't exist, we'll create it.")
		firstrun = open("version.txt", "a").close()
except Exception as e:
	print(timestamp() + "EmbyUpdate: Couldn't create the version.txt file. Permission issues? We can't continue")
	print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
	sys.exit()

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
	response = requests.get(url)
	updatejson = json.loads(response.text)
	onlineversion = updatejson["name"]
except Exception as e:
	print(timestamp() + "EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
	print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
	print(e)
	sys.exit()

##################################################################################
# Uncomment the correct download link, intsall, and updatefile for your distro!!!#
# Defaults to Debian/Ubuntu/Mint X64. Comment those out to use a differnt one!!!!#
##################################################################################

# Debian/Ubuntu/Mint amd64 *************
serverstop  = False
serverstart = False
downloadurl = "wget -q --show-progress https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-deb_" + onlineversion + "_amd64.deb" 
installfile = "dpkg -i -E emby-server-deb_" + onlineversion + "_amd64.deb"
updatefile  = "emby-server-deb_" + onlineversion + "_amd64.deb"
#***************************************

# Debian/Ubuntu/Mint armhf *************
#serverstop  = False
#serverstart = False
#downloadurl = "wget -q --show-progress https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-deb_" + onlineversion + "_armhf.deb"
#installfile = "dpkg -i emby-server-deb_" + onlineversion + "_armhf.deb"
#updatefile  = "emby-server-deb_" + onlineversion + "_armhf.deb"
#***************************************

# Arch Linux ***************************
#serverstop  = True
#serverstart = True
#downloadurl = "notused"
#installfile = "pacman -S emby-server"
#updatefile  = "notused"
#***************************************

# CentOS X64 ***************************
# In Cent I think yum will handle the stop/start of the server, but change below if needed
#serverstop  = False
#serverstart = False
#downloadurl = "yum install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
#installfile = "notused"
#updatefile  = "notused"
#****************************************

# Fedora X64 ****************************
# Pretty sure dnf will stop/start the server, but change below if needed
#serverstop  = False
#serverstart = False
#downloadurl = "dnf install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
#installfile = "notused"
#updatefile  = "notused"
#***************************************

# Fedora Armv7hl ***********************
# Pretty sure dnf will stop/start the server, but change delow if needed
#serverstop  = False
#serverstart = False
#downloadurl = "dnf install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
#installfile = "notused"
#updatefile  = "notused"
#***************************************

# OpenSUSE X64 *************************
# Pretty sure zypper will stop/start the server, but change below as needed
#serverstop  = False
#serverstart = False
#downloadurl = "zypper install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_x86_64.rpm"
#installfile = "notused"
#updatefile  = "notused"
#***************************************

# OpenSUSE Armv7hl *********************
# Pretty sure zypper will stop/start the server, but change below as needed
#serverstop  = False
#serverstart = False
#downloadurl = "zypper install https://github.com/MediaBrowser/Emby.Releases/releases/download/" + onlineversion + "/emby-server-rpm_" + onlineversion + "_armv7hl.rpm"
#installfile = "notused"
#updatefile  = "notused"
#**************************************

# Now that we know the latest version we're going to see if we need to update.
# What we do is compaire the latest version to the last updated version recored in
# version.txt
fileread = open("version.txt", "r")
fileversion = fileread.read()
fileread.close

# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

if str(onlineversion) in str(fileversion):
	# If the latest online verson matches the last installed version then we let you know and exit
	print(timestamp() + "EmbyUpdate: We're up to date! Nothing to see here... move along. Script exiting!")
	sys.exit()
else:
	# If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
	print(timestamp() + "EmbyUpdate: Most recent online version is " + onlineversion + " and current installed version is " + fileversion + ". We're updating Emby.")

	# This will stop the server on a systemd distro if it's been set to true above
	if serverstop is True:
		os.system("systemctl stop emby-server")
		for i in xrange(10,0,-1):
			sys.stdout.write(str(i)+' ')
			sys.stdout.flush()
			time.sleep(1)


	print("\n" + timestamp() + "EmbyUpdate: Starting update......")

	# Here we download the package to install if used
	if "notused" not in downloadurl:
		os.system(downloadurl)

	# Next we install it if used
	if "notused" not in installfile:
		os.system(installfile)

	# And to keep things nice and clean, we remove the downloaded file once installed if needed
	if "notused" not in updatefile:
		os.system("rm -f " + updatefile)

	# This will restart the server if using systemd if set to True above.
	if serverstart is True:
		os.system("systemctl start emby-server")

	# Lastly we write the newly installed version into the versions.txt file
	f = open("version.txt", "w")
	f.write(str(onlineversion))
	f.close
	print(timestamp() + "EmbyUpdate: Updating to Emby version " + onlineversion + " finished! Script exiting!")
	print("*****************************************************************************")
	print("\n")
	sys.exit()
