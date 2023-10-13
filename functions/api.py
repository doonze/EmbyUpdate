"""
module for getting info from APIs

Currently, for the Emby server running on the system, the GitHub for this app, and the Emby
GitHub.
"""

import sys
import json
import requests
import db.dbobjects as db_obj
from functions import exceptrace


def get_running_version() -> db_obj.ServerInfo:
    """
    The GetRunningVersion function returns the version number of the latest build on the server.
    It is used to determine if a user's local copy of Emby is out-of-date.

    :return: The server info of the running Emby server
    """

    while True:
        try:

            server_info = db_obj.ServerInfo().pull_from_db()

            if server_info.portused:
                server_info.fullurl = f'{server_info.scheme}{server_info.address}:{server_info.port}'\
                    f'{server_info.apipath}'
            else:
                server_info.fullurl = f'{server_info.scheme}{server_info.address}{server_info.apipath}'

            response = requests.get(server_info.fullurl)
            update_json = json.loads(response.text)
            if "Version" in update_json:
                server_info.version = update_json['Version']
                server_info.servername = update_json['ServerName']
                return server_info

        except requests.exceptions.RequestException:
            server_info.version = "None"
            return server_info


def get_self_online_version() -> db_obj.SelfUpdate:
    """
    The get_self_version function is used to get the most recent version of this script from GitHub.
    It is called by the selfupdate function and returns a SelfUpdate object with two attributes:
    selfgithubapi, which is the API link for all releases on GitHub, and version, which is
    the most recent release tag name.

    Returns:
        The version of the current script from GitHub
    """

    try:

        selfupdate: db_obj.SelfUpdate = db_obj.SelfUpdate()
        selfupdate.pull_from_db()

        response = requests.get(selfupdate.selfgithubapi)
        update_json = json.loads(response.text)

        # Here we search the GitHub API response for the most recent version of beta or stable
        # depending on what was chosen by the user
        for entry in update_json:

            if selfupdate.releasetype == "Beta":

                if entry["prerelease"] is True:
                    selfupdate.onlineversion = entry["tag_name"]
                    break
            else:

                if entry["prerelease"] is False:
                    selfupdate.onlineversion = entry["tag_name"]
                    break

        return selfupdate

    except requests.exceptions.RequestException:
        exceptrace.execpt_trace("*** Selfupdate: Couldn't get git version from GitHub. "
                                "We will not be able update this script for now!", sys.exc_info())
        selfupdate.onlineversion = None
        return selfupdate


def get_main_online_version(configobj: db_obj.ConfigObj) -> db_obj.ConfigObj:
    """
    We first check the running server version and record that. We then pull the latest online
    version from GitHub to know if we need to update.

    Args:
        configobj:db_obj.ConfigObj: Pass the configobj object

    Returns:
        The online version of the script
    """

    # Now we're just going to see what the latest version is! If we get any funky response we'll
    # exit the script.
    try:
        configobj.serverinfo = get_running_version()
        if configobj.serverinfo.enablecheck:
            if configobj.serverinfo.version == "None":
                print()
                print("If this is a run to install emby for the first time, ignore this message.\n"
                      "Running Emby server check is enabled, however, I was not able to \n"
                      "reach the server. Have you changed the port or address of your \n"
                      "Emby server? Is it down? If you feel this is incorrect rerun config \n"
                      "setup and update the server info. I'm going to make assumptions based \n"
                      "on the last good update I was able to run (I track such things). But if \n"
                      "you used a method other than myself to update (or this is a first run), \n"
                      "we may waste some resources updating to a version you already have. \n"
                      "Won't hurt nothin'. Just waste both our times. ;)")
                print()

        response = requests.get(configobj.mainconfig.embygithubapi)
        update_json = json.loads(response.text)
        # Here we search the GitHub API response for the most recent version of beta or stable
        # depending on what was chosen above.
        for entry in update_json:

            if configobj.mainconfig.releasetype == 'Beta':

                if entry["prerelease"] is True:
                    configobj.onlineversion = entry["tag_name"]
                    break

            elif configobj.mainconfig.releasetype == 'Stable':

                if entry["prerelease"] is False:
                    configobj.onlineversion = entry["tag_name"]
                    break

            else:
                print("Couldn't find release type requested in GigHub API result, value is "
                      f"{configobj.mainconfig.releasetype}")
                configobj.onlineversion = None

        return configobj

    except requests.exceptions.RequestException:
        exceptrace.execpt_trace("*** EmbyUpdate: Couldn't get git version from GitHub. "
                                "We will not be able update this script for now!", sys.exc_info())
        configobj.onlineversion = None
        return configobj
