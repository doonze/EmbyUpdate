"""
dbobjects
"""
from dataclasses import dataclass
from datetime import date
from pprint import pp
import db.db_functions as db
# import embyupdate


@dataclass
class MainConfig:
    """
    Class for interfacing with the mainconfig table

    Attributes:
    id          : int = 1
    configran   : bool = False
    distro      : str = None
    startserver : bool = False
    stopserver  : bool = False
    version     : str = 'First Run'
    releasetype : str = 'Stable'
    dateupdated : str = None
    embygithubapi: str
    downloadurl: str
    """
    id: int = 1
    configran: bool = False
    distro: str = "None Chosen"
    startserver: bool = False
    stopserver: bool = False
    version: str = 'First Run'
    releasetype: str = 'Stable'
    dateupdated: str = None
    embygithubapi: str = "https://api.github.com/repos/mediabrowser/Emby.releases/releases"

    def update_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'MainConfig', 'id', 1)

    def insert_to_db(self):
        """
        The insert_to_db function inserts the data into a database.
        It takes in the self object and uses it to insert data into a database.
        """

        db.db_insert_class_in_table(db.db_conn(), self, 'MainConfig')

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(), 'MainConfig', 'id', 1, self)

    def print_me(self):
        """
        Prints object to output
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
    dateupdated: str = None
    runupdate: bool = True
    version: str = "test"
    onlineversion: str = None
    releasetype: str = 'Stable'
    selfgithubapi: str = 'https://api.github.com/repos/doonze/Embyupdate/releases'
    downloadurl: str = 'https://github.com/doonze/EmbyUpdate/archive/'
    zipfile: str = None

    def update_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'SelfUpdate', 'id', 1)

    def insert_to_db(self):
        db.db_insert_class_in_table(db.db_conn(), self, 'SelfUpdate')

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(), 'SelfUpdate', 'id', 1, self)

    def print_me(self):
        """
        Prints object to output
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

    def update_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(db.db_conn(), self, 'ServerInfo', 'id', 1)

    def insert_to_db(self):
        db.db_insert_class_in_table(db.db_conn(), self, 'ServerInfo')

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(), 'ServerInfo', 'id', 1, self)

    def print_me(self):
        """
        Prints object to output
        """
        print(self)


@dataclass
class ConfigObj:
    mainconfig: MainConfig = MainConfig()
    selfupdate: SelfUpdate = SelfUpdate()
    serverinfo: ServerInfo = ServerInfo()
    onlineversion: str = None
    
    def get_config(self):
        """
        The get_config function pulls the configuration from the database and returns it as a dataclass object.
        
        
        Args:
            self: Reference the class object itself
        
        Returns:
            The config dataclass object
        """
        
        self.mainconfig.pull_from_db()
        self.selfupdate.pull_from_db()
        self.serverinfo.pull_from_db()
        
        return self


@dataclass
class DistroConfig:
    distro: str
    downloadurl: str
    installcommand: str
    installfile: str

    def update_db(self):
        """
        Writes object to DB
        """
        db.db_update_class_in_table(
            db.db_conn(), self, 'DistroConfig', 'distro', self.distro)

    def insert_to_db(self):
        """
        The insert_to_db function inserts the data into a database.
        It takes in the self object and uses it to insert data into a database.
        """
        db.db_insert_class_in_table(db.db_conn(), self, 'DistroConfig')

    def pull_from_db(self, what):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(
            db.db_conn(), 'DistroConfig', 'distro', what, self)

    def print_me(self):
        """
        Prints object to output
        """
        pp(self, depth=1, indent=4)
