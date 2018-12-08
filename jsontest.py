#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import sys
import os
import json
import requests
import os.path
import time
import pprint

installbeta = False

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
	ts = time.strftime("%x %X", time.localtime())
	return ("<" + ts + "> ")

# URL to try and prase
url = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
	response = requests.get(url)
	updatejson = json.loads(response.text)
	for i, entry in enumerate(updatejson):
		if (installbeta == True):

			if entry["prerelease"] == True:
				version =  entry["tag_name"]
				break
		else:

			if entry["prerelease"] == False:
				version =  entry["tag_name"]
				break

	print(version)

	# jsonresponse = updatejson["tag_name"]
	# print(jsonresponse)
	# pprint.pprint(updatejson)
except Exception as e:
	print(timestamp() + "EmbyUpdate: We didn't get an expected response from the github api, script is exiting!")
	print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
	print(e)
	sys.exit()

sys.exit()
