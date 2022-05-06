import json
import requests
from db.dbobjects import ServerInfo



def get_running_version():
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
                serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}:{serverinfo.port}{serverinfo.apipath}'
            else:
                serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}{serverinfo.apipath}'
                                  
            response = requests.get(serverinfo.fullurl)
            updatejson = json.loads(response.text)
            if "Version" in updatejson:
                serverinfo.version = updatejson['Version']
                return serverinfo

        except:
            serverinfo.version = None
            return serverinfo