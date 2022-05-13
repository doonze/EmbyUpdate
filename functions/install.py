"""
The main module to update and install Emby
"""

from sqlite3 import Error
import subprocess
import sys
import time
import requests
import db.dbobjects as db
from functions import exceptrace, timestamp

# pylint: disable=broad-except
# pylint: disable=line-too-long


def update_emby(configobj: db.ConfigObj):
    """
    The update_emby function is the main function of this script. It's purpose is to update Emby Media Server
    to a newer version if available. The function will check for an updated package and install it if needed, 
    and then restart the server after updating if needed.

    Args:
        configobj:db.ConfigObj: Pull the config from the database and update it

    Returns:
        Nothing
    """

    try:
        distroconfig: db.DistroConfig = db.DistroConfig()
        distroconfig.pull_from_db(configobj.mainconfig.distro)
        # This will stop the server on a systemd distro if it's been set to true above
        if configobj.mainconfig.stopserver:
            print("Stopping Emby server.....")
            stopreturn = subprocess.call(
                "systemctl stop emby-server", shell=True)
            time.sleep(3)
            if stopreturn > 0:
                print("Server Stop failed! Non-critical error! Investigate if needed.")

            print("Emby Server Stopped...")

        # Here we download the package to install if used
        if "notused" not in distroconfig.downloadurl:
            print("Starting Package download...")
            download = requests.get(distroconfig.downloadurl)
            with open(distroconfig.installfile, 'wb') as file:
                file.write(download.content)
            print("Package downloaded!")

        # Next we install it if used
        if "notused" not in distroconfig.installfile:
            print("Installing/Updating Emby server....")
            installreturn = subprocess.call(
                distroconfig.installfile, shell=True)
            if installreturn > 0:
                print("Install/Update failed! Exiting!")
                sys.exit()
            print("Install/Update Finished!")

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        if "notused" not in distroconfig.installfile:
            print("Removing install file...")
            subprocess.call("rm -f " + distroconfig.installfile, shell=True)
            print("File removed!")

        # This will restart the server if using systemd if set to True above
        if configobj.mainconfig.stopserver:
            print("Restarting Emby server after update...")
            startreturn = subprocess.call(
                "systemctl start emby-server", shell=True)
            if startreturn > 0:
                print(
                    "Server start failed. Non-critical to update but server may not be running. Investigate.")
            print("Server restarted!")

        # Lastly we write the newly installed version into the config file
        try:
            configobj.mainconfig.update_db()

            print(f"{timestamp.time_stamp()} EmbyUpdate: Updated to Emby version {configobj.mainconfig.version}."
                  " We're done! Script exiting!")
            print('')
            print(
                "*****************************************************************************")
            print("\n")

        except Error:
            print()
            exceptrace.execpt_trace("*** EmbyUpdate: Couldn't write config to database after "
                                    "update finished. ", sys.exc_info())
            sys.exit()

    except Exception:
        exceptrace.execpt_trace(
            "*** EmbyUpdate: Something went wrong on the update/install.", sys.exc_info())
