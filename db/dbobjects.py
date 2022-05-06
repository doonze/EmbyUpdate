"""
dbobjects
"""
from dataclasses import dataclass
from datetime import date
from pprint import pp
import db.db_functions as db


@dataclass
class MainConfig:
    """
    Class for interfacing with the MainConfig table

    Attributes: 
    id          : int = 1
    configran   : bool = False
    distro      : str = None
    startserver : bool = False
    stopserver  : bool = False
    version     : str = 'First Run'
    releasetype : str = 'Stable'
    dateupdated : str = None
    """
    id          : int = 1
    configran   : bool = False
    distro      : str = None
    startserver : bool = False
    stopserver  : bool = False
    version     : str = 'First Run'
    releasetype : str = 'Stable'
    dateupdated : str = None

    def write_to_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'mainconfig', 'id', 1)

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(),'mainconfig', 'id', 1, self)

    def print_me(self):
        """
        Prints opject to ouput
        """    
        pp(self, depth=1, indent=4)

@dataclass
class MainUpdateHistory():
    id: int
    date: date
    version: str
    success: bool
    errorid: int

@dataclass
class SelfUpdate():
    id: int = 1
    dateupdated:str = None
    runupdate: bool = True
    version: str = "First Run"
    releasetype: str = "Stable"
    
    def write_to_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'selfupdate', 'id', 1)

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(),'selfupdate', 'id', 1, self)

    def print_me(self):
        """
        Prints opject to ouput
        """
        print(self, depth=1, indent=4)

@dataclass
class SelfUpdateHistory():
    id: int
    date: date
    version: str
    success: bool
    errorid: int

@dataclass
class DbUpdateHistory():
    version: str
    date: date
    notes: str

@dataclass
class DBversion():
    version: str
    dateupdated: date

@dataclass
class Errors():
    id: int
    date: date
    message: str
    mainorself: str

@dataclass
class ServerInfo:
    id: int = 1
    enablecheck: bool = True
    scheme: str = 'https://'
    address: str = 'localhost'
    port: str = '8096'
    portused: bool = True
    apipath: str = '/System/Info/Public'
    fullurl: str = None
    version: str = None

    def write_to_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'serverinfo', 'id', 1)

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(),'serverinfo', 'id', 1, self)

    def print_me(self):
        """
        Prints opject to ouput
        """
        print(self)
        