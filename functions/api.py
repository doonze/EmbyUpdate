import requests
import json
from functions.urlbuilder import buildServerURL

def GetServerInfo():
    """
    The GetServerInfo function is used to get the server name and IP address from the user.
    It will then return a tuple containing these two pieces of information.
    
    :return: A string of the server name, ip address and port number
    :doc-author: Trelent
    """
    while True:
        r = input('Do you have a running instance of Emby on this server? Y/n: ')
        if r.casefold() == 'n':
            break



def GetRunningVersion() -> dict:
    """
    The GetRunningVersion function returns the version number of the latest build on the server.
    It is used to determine if a user's local copy of Emby is out-of-date.

    :return: The version of the running Emby server
    
    """

    while True:    
        try:           
            response = requests.get(buildServerURL())
            updatejson = json.loads(response.text)
            if "Version" in updatejson:
                return { 'version' : updatejson['Version'], 'url' : buildServerURL()}

        except:
            return { 'version' : None, 'url' : buildServerURL()}