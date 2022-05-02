import requests
import json
from functions.urlbuilder import buildServerURL

def GetServerInfo():
    while True:
        r = input('Do you have a running instance of Emby on this server? Y/n: ')
        if r.casefold() == 'n':
            break



def GetRunningVersion():

    while True:    
        try:           
            response = requests.get(buildServerURL())
            updatejson = json.loads(response.text)
            if "Version" in updatejson:
                return updatejson['Version']

        except:
            print("Server not running, or not found.")
            GetServerInfo()
            break