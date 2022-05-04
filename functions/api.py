from turtle import update
import requests
import json
from functions.urlbuilder import buildServerURL


def GetRunningVersion() -> dict:
    """
    The GetRunningVersion function returns the version number of the latest build on the server.
    It is used to determine if a user's local copy of Emby is out-of-date.

    :return: The version of the running Emby server
    
    """

    while True:    
        try:
            URLinfoDict = buildServerURL()           
            response = requests.get(URLinfoDict['url'])
            updatejson = json.loads(response.text)
            if "Version" in updatejson:
                URLinfoDict['version'] = updatejson['Version']
                return URLinfoDict

        except:
            URLinfoDict['version'] = None
            return URLinfoDict