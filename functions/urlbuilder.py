import sys
from xmlrpc.client import Server
from db.db_functions import db_return_class_object, db_conn
from db.dbobjects import ServerInfo, UrlObj
from functions.exceptrace import execptTrace

def buildServerURL() -> ServerInfo:
    """
    The buildServerURL function is used to build the URL for the server.
    It takes no arguments and returns a string containing the full URL of 
    the server.
    
    Args:
        None
    
    Returns:
        A dictionary that has the  api url that is used to connect to the server and the 
        ServerInfo dataclass object   
    """       

    try:
        serverinfo = ServerInfo()
        serverinfo = db_return_class_object(db_conn(), 'ServerInfo', 'id', 1, ServerInfo)

        if serverinfo.portused:
            serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}:{serverinfo.port}{serverinfo.apipath}'
            return serverinfo
        else:
            serverinfo.fullurl = f'{serverinfo.scheme}{serverinfo.address}{serverinfo.apipath}'
            return serverinfo

    except Exception as e:
        execptTrace("******urlbuilder: There was an error building the Server URL******", sys.exc_info())
