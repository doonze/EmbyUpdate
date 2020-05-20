#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This program is used can called by the main program to update the app itself if needed
import sys
import os
import json
import requests
import os.path
import time
import pprint
import zipfile
import subprocess

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# Here we try python3 configparser import. If that fails it means user is running python2. So we import
# the python2 ConfigParser instead

try:
    import configparser
    config = configparser.ConfigParser()
    python = '3'
except ImportError:
    import ConfigParser
    config = ConfigParser.ConfigParser()
    python = '2'

installbeta = False

# Now we're going to open the config file reader
config.read('config.ini')
# We pull the config info based on if user is running python 2 or python 3
if python == '3':
    appversion = config['EmbyUpdate']['version']
elif python == '2':
    appversion = config.get('EmbyUpdate', 'version')

# We're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
	ts = time.strftime("%x %X", time.localtime())
	return ("<" + ts + "> ")

# The github API of releases for app. This includes beta and production releases
url = "https://api.github.com/repos/doonze/Embyupdate/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(url)
    updatejson = json.loads(response.text)
    # Here we search the github API response for the most recent version of beta or stable depending on what was chosen by the user
    for i, entry in enumerate(updatejson):
        if (installbeta == True):

            if entry["prerelease"] == True:
                onlineversion =  entry["tag_name"]
                versiontype = "Beta"
                break
        else:

            if entry["prerelease"] == False:
                onlineversion =  entry["tag_name"]
                versiontype = "Stable"
                break
except Exception as e:
    print(timestamp() + "EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
    print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
    print(e)
    sys.exit()

# Download URL for my github page (app home page) and we'll set the name of the current zip file
downloadurl = "wget -q --show-progress https://github.com/doonze/EmbyUpdate/archive/" + onlineversion + ".zip" 
zfile = onlineversion + ".zip"

# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

onlinefileversion = (onlineversion + "-" + versiontype)

if str(onlinefileversion) in str(appversion):
    # If the latest online verson matches the last installed version then we let you know and exit
    print(timestamp() + "EmbyUpdate: App is up to date!  Current and Online versions are at " + onlinefileversion + ". Nothing to see here... move along. Script exiting!")
    sys.exit()
else:
	# If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
    print('')
    print(timestamp() + "EmbyUpdate: Most recent app online version is " + onlinefileversion + " and current installed version is " + appversion + ". We're updating EmbyUpdate app.")
    print('')
    print("\n" + timestamp() + "EmbyUpdate: Starting self app update......")
    print('')

   	# Here we download the zip to install
    #subprocess.call(downloadurl,shell=True)

	# Next we unzip and install it to the directory where the app was ran from
    #with zipfile.ZipFile(zfile) as zip:
    #    for zip_info in zip.infolist():
    #        if zip_info.filename[-1] == '/':
    #            continue
    #        zip_info.filename = os.path.basename(zip_info.filename)
    #        zip.extract(zip_info, '')

	# And to keep things nice and clean, we remove the downloaded file once unzipped
    #subprocess.call("rm -f " + zfile,shell=True)

    # now we'll set the app as executable
    #st = os.stat("embyupdate.py")
    #os.chmod("embyupdate.py", st.st_mode | 0o111)

	# Lastly we write the newly installed version into the config file
    try:
        config['EmbyUpdate']['version'] = onlinefileversion
    except AttributeError:
        config.set('EmbyUpdate', 'version', onlinefileversion)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print('')
    print(timestamp() + "EmbyUpdate: Updating to EmbyUpdate app version " + onlinefileversion + " finished! Script exiting!")
    print('')
    print("*****************************************************************************")
    print("\n")
    subprocess.call('python3 embyupdate.py',shell=True)
    sys.exit()
