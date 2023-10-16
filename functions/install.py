"""
The main module to update and install Emby
"""

import os
from sqlite3 import Error
import subprocess
import sys
import time
import requests
from genericpath import exists
import db.dbobjects as db
from functions import exceptrace, timestamp


# pylint: disable=broad-except
# pylint: disable=line-too-long
# pylint: disable=too-many-statements


def update_emby(configobj: db.ConfigObj):
    """
    The update_emby function is the main function of this script. Its purpose is to update Emby Media Server
    to a newer version if available. The function will check for an updated package and install it if needed, 
    and then restart the server after updating if needed.

    Args:
        configobj:db.ConfigObj: Pull the config from the database and update it

    Returns:
        Nothing
    """

    try:
        distro_config: db.DistroConfig = db.DistroConfig()
        distro_config.pull_from_db(configobj.mainconfig.distro)
        install_file = distro_config.installfile.format(online_version=configobj.onlineversion)
        download_url = distro_config.downloadurl.format(online_version=configobj.onlineversion,
                                                        install_file=install_file)
        install_command = distro_config.installcommand.format(install_file=distro_config.installfile.
                                                              format(online_version=configobj.onlineversion))

        # This will stop the server if it's been set to true
        if configobj.mainconfig.stopserver:

            print()
            print(f"{timestamp.time_stamp()} Stopping Emby server.....")

            stop_return = subprocess.call("sudo service emby-server stop", shell=True)

            time.sleep(3)

            if stop_return > 0:
                print()
                print(f"{timestamp.time_stamp()} Server Stop failed! Non-critical error! Investigate if needed.")
            else:
                print()
                print(f"{timestamp.time_stamp()} Emby Server Stopped...")

        # Here we download the package to install if used
        if "notused" not in distro_config.downloadurl:
            print(f"{timestamp.time_stamp()} Starting Package download... Please wait, this can take several minutes.")

            download = requests.get(download_url)

            with open(install_file, 'wb') as file:
                file.write(download.content)

            print(f" {timestamp.time_stamp()} Package downloaded!")

        # Next we install it if used
        if "notused" not in distro_config.installfile:

            print(f"{timestamp.time_stamp()} Installing/Updating Emby server....")

            install_return = subprocess.call(install_command, shell=True)

            if install_return > 0:
                print(f"{timestamp.time_stamp()} Install/Update failed! Exiting!")
                sys.exit()
            else:
                print(f"{timestamp.time_stamp()} Install/Update Finished!")

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        if "notused" not in distro_config.installfile:

            if exists(install_file):
                print(f"{timestamp.time_stamp()}Removing install file...")

                os.remove(install_file)

                print(f"{timestamp.time_stamp()}File removed!")

        # This will restart the server if set to True
        if configobj.mainconfig.stopserver:
            print(f"{timestamp.time_stamp()} Restarting Emby server after update...")
            start_return = subprocess.call("sudo service emby-server start", shell=True)
            if start_return > 0:
                print(f"{timestamp.time_stamp()} Server start failed. Non-critical to update but server may not be "
                      f"running. Investigate.")
            else:
                print(f"{timestamp.time_stamp()} Server restarted!")

        # Lastly we write the newly installed version into the config file
        try:
            configobj.mainconfig.version = configobj.onlineversion
            configobj.mainconfig.dateupdated = timestamp.time_stamp(False)
            db.MainUpdateHistory(date=timestamp.time_stamp(False), version=configobj.onlineversion,
                                 success=True, errorid=0).insert_to_db()
            configobj.mainconfig.update_db()

            print(f"{timestamp.time_stamp()} EmbyUpdate: Updated to Emby version {configobj.mainconfig.version}."
                  " We're done! Script exiting!")
            print('')
            print(
                "*****************************************************************************")
            print("\n")

        except Error:
            print()
            exceptrace.execpt_trace("Emby Server Update: Couldn't write config to database after "
                                    "update finished. ", sys.exc_info(), "Emby")
            db.MainUpdateHistory(date=timestamp.time_stamp(False), version=configobj.onlineversion,
                                 success=False, errorid=2).insert_to_db()

    except Exception:
        exceptrace.execpt_trace("Emby Server Update: Something went wrong on the update/install.", sys.exc_info(),
                                "Emby")
        db.MainUpdateHistory(date=timestamp.time_stamp(False), version=configobj.onlineversion,
                             success=False, errorid=1).insert_to_db()