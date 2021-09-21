#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This program is used can called by the main program to update the app itself if needed
import sys
import json
import requests
import os.path
import time
import zipfile
import subprocess
from config import Config


# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp():
    ts = time.strftime("%x %X", time.localtime())
    return "<" + ts + "> "


class SelfUpdate:

    def __init__(self, config):
        self.config: Config = config
        self.url: str = "https://api.github.com/repos/doonze/Embyupdate/releases"
        self.online_version: str = ""

    # We're going to force the working path to be where the script lives

    def self_update(self):

        # Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
        try:
            os.chdir(sys.path[0])
            response = requests.get(self.url)
            updatejson = json.loads(response.text)
            # Here we search the github API response for the most recent version of beta or stable depending on what was
            # chosen by the user
            for i, entry in enumerate(updatejson):
                if self.config.self_release == "Beta":

                    if entry["prerelease"] is True:
                        self.online_version = entry["tag_name"]
                        break
                else:

                    if entry["prerelease"] is False:
                        self.online_version = entry["tag_name"]
                        break

        except Exception as e:
            print(
                timestamp() + "EmbyUpdate(self): We didn't get an expected response from the github api, "
                              "script is exiting!")
            print(timestamp() + "EmbyUpdate(self): Here's the error we got -- " + str(e))
            print(e)
            sys.exit()

        try:
            # Download URL for my github page (app home page) and we'll set some needed variables
            downloadurl = "https://github.com/doonze/EmbyUpdate/archive/" + self.online_version + ".zip"
            zfile = self.online_version + ".zip"
            online_file_version = (self.online_version + "-" + self.config.self_release)
            zip_base_path = ("EmbyUpdate-" + self.online_version[1:] + "/")
            # Ok, we've got all the info we need. Now we'll test if we even need to update or not.

            if str(online_file_version) in str(self.config.self_version):

                # If the latest online version matches the last installed version then we let you know and exit
                print(timestamp() + "EmbyUpdate(self): App is up to date!  Current and Online versions are at "
                      + online_file_version + ". Exiting!")

            else:

                # If the online version DOESN'T match the last installed version we let you know what the versions are
                # and start updating
                print('')
                print(timestamp() + "EmbyUpdate(self): Most recent app online version is "
                      + online_file_version + " and current installed version is "
                      + self.config.self_version + ". We're updating EmbyUpdate app.")
                print('')
                print("\n" + timestamp() + "EmbyUpdate(self): Starting self app update......")
                print('')

                # Here we download the zip to install
                print("Starting Package download...")
                download = requests.get(downloadurl)
                with open(zfile, 'wb') as file:
                    file.write(download.content)
                print("Package downloaded!")

                # Next we unzip and install it to the directory where the app was ran from
                with zipfile.ZipFile(zfile) as unzip:
                    for zip_info in unzip.infolist():
                        if zip_info.filename[-1] == '/':
                            continue
                        zip_info.filename = zip_info.filename.replace(zip_base_path, "")
                        unzip.extract(zip_info, '')

                # And to keep things nice and clean, we remove the downloaded file once unzipped
                os.remove(zfile)

                # now we'll set the app as executable
                st = os.stat("embyupdate.py")
                os.chmod("embyupdate.py", st.st_mode | 0o111)

        except Exception as e:
            print(timestamp() + "EmbyUpdate(self): We had a problem installing new version of updater!")
            print(timestamp() + "EmbyUpdate(self): Here's the error we got -- " + str(e))
            sys.exit()

        # Lastly we write the newly installed version into the config file
        try:
            self.config.self_version = online_file_version
            self.config.write_config()
            print('')
            print(timestamp() + "EmbyUpdate(self): Updating to EmbyUpdate app version "
                  + online_file_version + " finished! Script exiting!")
            print('')
            print("*****************************************************************************")
            print("\n")
            return self.config

        except Exception as e:
            print(timestamp() + "EmbyUpdate(self): We had a problem writing to config after update!")
            print(timestamp() + "EmbyUpdate(self): Here's the error we got -- " + str(e))
            sys.exit()
