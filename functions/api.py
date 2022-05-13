"""
module for getting info from api's

Currently for the Emby server running on the system, the GitHub for this app, and the Emby
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

            serverinfo = db_obj.ServerInfo()
            serverinfo.pull_from_db()

            if serverinfo.portused:
                serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}:{serverinfo.port}'\
                    f'{serverinfo.apipath}'
            else:
                serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}{serverinfo.apipath}'

            response = requests.get(serverinfo.fullurl)
            updatejson = json.loads(response.text)
            if "Version" in updatejson:
                serverinfo.version = updatejson['Version']
                return serverinfo

        except requests.exceptions.RequestException:
            serverinfo.version = "None"
            return serverinfo


def get_self_online_version() -> db_obj.SelfUpdate:
    """
    The get_self_version function is used to get the most recent version of this script from GitHub.
    It is called by the selfupdate function and returns a SelfUpdate object with two attributes:
    selfgithubapi, which is the API link for all releases on GitHub, and version, which is 
    the most recent release tag name.

    Args:
        None

    Returns:
        The version of the current script from github
    """

    try:

        selfupdate: db_obj.SelfUpdate = db_obj.SelfUpdate()
        selfupdate.pull_from_db()

        response = requests.get(selfupdate.selfgithubapi)
        updatejson = json.loads(response.text)

        # Here we search the github API response for the most recent version of beta or stable
        # depending on what was chosen by the user
        for entry in updatejson:
            
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
        exceptrace.execpt_trace("*** Selfupdate: Could get git version from GitHub. "
                                "We will not be able update this script for now!", sys.exc_info())
        selfupdate.onlineversion = None
        return selfupdate


def get_main_online_version(configobj: db_obj.ConfigObj) -> db_obj.ConfigObj:
    """
    We first check the running server version and record that. We then pull the latest online version
    from github to know if we need to update. 

    Args:
        configobj:db_obj.ConfigObj: Pass the configobj object

    Returns:
        The online version of the script
    """

    # Now we're just going to see what the latest version is! If we get any funky response we'll exit
    # the script.
    try:
        configobj.serverinfo = get_running_version()
        if configobj.serverinfo.enablecheck:
            if configobj.serverinfo.version == "None":
                print()
                print("Running Emby server check is enabled, however, I was not able to "
                      "reach the server. Have you changed the port or address of your "
                      "Emby server? Is it down? If you feel this is incorrect rerun config "
                      "setup and update the server info. I'm going to make assumptions based "
                      "on the last good update I was able to run (I track such things). But if "
                      "you used a method other than myself to update (or this is a first run), "
                      "we may waste some resources updateing to a version you already have. "
                      "Won't hurt nothin'.")
                print()

        response = requests.get(configobj.mainconfig.embygithubapi)
        updatejson = json.loads(response.text)
        # Here we search the github API response for the most recent version of beta or stable
        # depending on what was chosen above.
        for entry in updatejson:

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
