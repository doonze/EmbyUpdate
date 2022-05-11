# This Python file uses the following encoding: utf-8
# This program is used can called by the main program to update the app itself if needed
from sqlite3 import Error
import sys
import os.path
import zipfile
import requests
from functions import api, timestamp


def self_update():
    """
    The self_update function is used to update the EmbyUpdate app. It does this by checking
    the latest version of the app online and comparing it to what is currently installed on
    your machine. It will then download the latest version if needed. Once downloaded, it
    will delete any previous versions of embyupdate from your machine (including older
    versions of this script). Lastly, it sets itself as executable so you can run the script
    directly from terminal.

    Args:

    Returns:
        The updated version of the embyupdate app

    Doc Author:
        Trelent
    """

    # Now we're just going to see what the latest version is! If we get any funky response we'll
    # exit the script.

    try:
        # Download the latest version for the requested release
        selfupdate = api.get_self_version()

        # Build the zip file name
        selfupdate.zipzile = f"{selfupdate.onlineversion}.zip"

        # Build path for unziping
        zip_base_path = ("EmbyUpdate-" + selfupdate.onlineversion[1:] + "/")

        # Ok, we've got all the info we need. Now we'll test if we even need to update or not.

        if str(selfupdate.onlineversion) in str(selfupdate.version):

            # If the latest online version matches the last installed version then we let you know
            # and exit
            print(f"{timestamp.time_stamp()} EmbyUpdate(self): App is up to date!  Current and "
                  f"Online versions are at {selfupdate.onlineversion} - {selfupdate.releasetype}. "
                  "Exiting!")
            return selfupdate

        # If the online version DOESN'T match the last installed version we let you know what the
        # versions are and start updating
        print('')
        print(f"{timestamp.time_stamp()} EmbyUpdate(self update): Most recent app online version is"
              f" {selfupdate.onlineversion} and current installed version is "
              f"{selfupdate.version}. We're updating EmbyUpdate app.")
        print('')
        print(
            f"{timestamp.time_stamp()} EmbyUpdate(self): Starting self app update......")
        print('')

        # Here we download the zip to install
        print("Starting Package download...")
        download = requests.get(
            f"{selfupdate.downloadurl}{selfupdate.zipzile}")
        with open(selfupdate.zipzile, 'wb') as file:
            file.write(download.content)
        print("Package downloaded!")

        # Next we unzip and install it to the directory where the app was ran from
        with zipfile.ZipFile(selfupdate.zipfile) as unzip:
            for zip_info in unzip.infolist():
                if zip_info.filename[-1] == '/':
                    continue
                zip_info.filename = zip_info.filename.replace(
                    zip_base_path, "")
                unzip.extract(zip_info, '')

        # And to keep things nice and clean, we remove the downloaded file once unzipped
        os.remove(selfupdate.zipfile)

        # now we'll set the app as executable
        state = os.stat("embyupdate.py")
        os.chmod("embyupdate.py", state.st_mode | 0o111)

    except zipfile.error as exception:
        print(timestamp.time_stamp(
        ) + "EmbyUpdate(self): We had a problem installing new version of updater!")
        print(timestamp.time_stamp() +
              "EmbyUpdate(self): Here's the error we got -- " + str(exception))
        sys.exit()

    # Lastly we write the newly installed version into the config file
    try:
        selfupdate.version = selfupdate.onlineversion
        selfupdate.onlineversion = None
        selfupdate.zipfile = None
        selfupdate.update_db()
        print('')
        print(timestamp.time_stamp() + "EmbyUpdate(self): Updating to EmbyUpdate app version "
              + selfupdate.version + " finished! Script exiting!")
        print('')
        print(
            "*****************************************************************************")
        print("\n")
        return selfupdate

    except Error as exception:
        print(timestamp.time_stamp() +
              "EmbyUpdate(self): We had a problem writing to config after update!")
        print(timestamp.time_stamp() +
              "EmbyUpdate(self): Here's the error we got -- " + str(exception))
        sys.exit()
