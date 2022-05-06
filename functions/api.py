from http import server
from turtle import update
import requests
import json
from db.db_functions import db_conn, db_return_class_object
from db.dbobjects import ServerInfo
from functions.urlbuilder import buildServerURL


def GetRunningVersion():
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