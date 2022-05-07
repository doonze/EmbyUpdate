"""
module for getting info from api's

Returns:
    object: config object updated from api
"""
import sys
import json
import requests
from db.dbobjects import ServerInfo, SelfUpdate
from functions import exceptrace



def get_running_version() -> ServerInfo:
    """
    The GetRunningVersion function returns the version number of the latest build on the server.
    It is used to determine if a user's local copy of Emby is out-of-date.

    :return: The server info of the running Emby server
    """

    while True:
        try:

            serverinfo = ServerInfo()
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
            serverinfo.version = None
            return serverinfo


def get_self_version() -> SelfUpdate:
    """
    The get_self_version function is used to get the most recent version of this script from GitHub.
    It is called by the selfupdate function and returns a SelfUpdate object with two attributes:
    selfgithubapi, which is the API link for all releases on GitHub, and version, which is 
    the most recent release tag name.

    Args:
        None

    Returns:
        The version of the current script from github

    Doc Author:
        Trelent
    """

    try:
        
        selfupdate: SelfUpdate = SelfUpdate()
        selfupdate.pull_from_db()
        
        response = requests.get(selfupdate.selfgithubapi)
        updatejson = json.loads(response.text)
        # Here we search the github API response for the most recent version of beta or stable
        # depending on what was chosen by the user
        for i, entry in enumerate(updatejson):
            if selfupdate.releasetype == "Beta":

                if entry["prerelease"] is True:
                    selfupdate.version = entry["tag_name"]
            else:
                if entry["prerelease"] is False:
                    selfupdate.version = entry["tag_name"]
        
        return selfupdate

    except requests.exceptions.RequestException:
        exceptrace.execpt_trace("*** Selfupdate: Could get git version from GitHub. "
                               "We will not be able update this script for now!", sys.exc_info())
        selfupdate.version = None
        return selfupdate