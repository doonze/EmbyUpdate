"""
This module is used when a self-update of the script is needed
"""

from sqlite3 import Error
import sys
import os.path
import zipfile
from genericpath import exists
import requests
from functions import api, timestamp
import db.dbobjects as db


def self_update(configobj: db.ConfigObj):
    """
    The self_update function is used to update the EmbyUpdate app. It does this by checking
    the latest version of the app online and comparing it to what is currently installed on
    your machine. It will then download the latest version if needed. Once downloaded, it
    will delete any previous versions of embyupdate from your machine (including older
    versions of this script). Lastly, it sets itself as executable, so you can run the script
    directly from terminal.

    Args:

    Returns:
        The updated version of the embyupdate app
    """

    # Now we're just going to see what the latest version is! If we get any funky response we'll
    # exit the script.

    try:
        # Download the latest version for the requested release
        selfupdate = api.get_self_online_version()
        selfupdate.version = configobj.selfupdate.version

        # Build the zip file name
        selfupdate.zipfile = f"{selfupdate.onlineversion}.zip"

        # Build path for unzipping
        zip_base_path = ("EmbyUpdate-" + selfupdate.onlineversion[1:] + "/")

        # Ok, we've got all the info we need. Now we'll test if we even need to update or not.

        if f"{selfupdate.onlineversion} - {selfupdate.releasetype}" == str(selfupdate.version):

            # If the latest online version matches the last installed version then we let you know
            # and exit
            print(f"{timestamp.time_stamp()} EmbyUpdate(self): App is up to date!  Current and "
                  f"Online versions are at {selfupdate.onlineversion} - {selfupdate.releasetype}. "
                  "Continuing...")
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
        print(f"{timestamp.time_stamp()} Starting Package download...")
        download = requests.get(f"{selfupdate.downloadurl}{selfupdate.zipfile}")
        with open(selfupdate.zipfile, 'wb') as file:
            file.write(download.content)
        print(f"{timestamp.time_stamp()} Package downloaded!")

        # Next we unzip and install it to the directory where the app was run from
        with zipfile.ZipFile(selfupdate.zipfile) as unzip:
            for zip_info in unzip.infolist():
                if zip_info.filename[-1] == '/':
                    continue
                zip_info.filename = zip_info.filename.replace(
                   zip_base_path, "")
                unzip.extract(zip_info, '')

        # And to keep things nice and clean, we remove the downloaded file once unzipped
        # then do some cleanup if updating from an older pre 4.0 version
        if exists(selfupdate.zipfile):
            os.remove(selfupdate.zipfile)

        if exists('configupdate.py'):
            os.remove('configupdate.py')

        if exists('selfupdate.py'):
            os.remove('selfupdate.py')

        # now we'll set the app as executable
        state = os.stat("embyupdate.py")
        os.chmod("embyupdate.py", state.st_mode | 0o111)

    except Exception as exception:
        print(timestamp.time_stamp() + "EmbyUpdate(self): We had a problem installing new version of updater!")
        print(timestamp.time_stamp() + "EmbyUpdate(self): Here's the error we got -- " + str(exception))
        db.SelfUpdateHistory(date=timestamp.time_stamp(False),
                             version=selfupdate.onlineversion,
                             success=False,
                             errorid=1).insert_to_db()

    # We write the newly installed version into the config file and restart the
    # program
    try:
        selfupdate.version = selfupdate.onlineversion
        selfupdate.dateupdated = timestamp.time_stamp(False)
        selfupdate.onlineversion = None
        selfupdate.zipfile = None
        selfupdate.update_db()
        print('')
        print(timestamp.time_stamp() + "EmbyUpdate(self): Updating to EmbyUpdate app version "
              + selfupdate.version + " finished! Script restarting to run with new update!")
        print('')
        print(
            "*****************************************************************************")
        print("\n")

        # Now we'll update the UpdateHistoryTable
        db.SelfUpdateHistory(date=timestamp.time_stamp(False),
                             version=selfupdate.version,
                             success=True,
                             errorid=0).insert_to_db()

        # Here we restart the program
        os.execv(sys.argv[0], sys.argv)

    except Error as exception:
        print(timestamp.time_stamp() +
              "EmbyUpdate(self): We had a problem writing to config after update!")
        print(timestamp.time_stamp() +
              "EmbyUpdate(self): Here's the error we got -- " + str(exception))
        db.SelfUpdateHistory(date=timestamp.time_stamp(False),
                             version=selfupdate.onlineversion,
                             success=True,
                             errorid=2).insert_to_db()
        sys.exit()
