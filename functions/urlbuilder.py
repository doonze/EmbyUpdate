import sys
from db.db_functions import db_return_class_object, db_create_connection
from db.dbobjects import ServerInfo
from functions.exceptrace import execptTrace

def buildServerURL() -> str:
    """
    The buildServerURL function is used to build the URL for the server.
    It takes no arguments and returns a string containing the full URL of 
    the server.
    
    Args:
    
    Returns:
        The api url that is used to connect to the server
   
    """
       

    try:
        serverinfo = db_return_class_object(db_create_connection(), 'ServerInfo', 'id', 1, ServerInfo)

        if serverinfo.portused:
            return f'{serverinfo.scheme}{serverinfo.address}:{serverinfo.port}{serverinfo.apipath}'
        else:
            return f'{serverinfo.scheme}{serverinfo.address}{serverinfo.apipath}'

    except Exception as e:
        execptTrace("******urlbuilder: There was an error building the Server URL******", sys.exc_info())
