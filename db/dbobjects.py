"""
This module is a collection of dataclasses that reflect the tables in the database.
All database functions happen within these classes.
"""

from contextlib import closing
from dataclasses import dataclass
from datetime import date
from pprint import pp
import db.db_functions as db


@dataclass
class MainConfig:
    """
    Class for interfacing with the MainConfig table
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
    """
    Class for interfacing with the MainUpdateHistory table
    """
    id: int = None
    date: date = None
    version: str = None
    success: bool = None
    errorid: int = None
    
    def insert_to_db(self):
        """
        The insert_to_db function inserts a new row into the DBVersion table with the version number.
        
        
        Args:
            self: Access the variables in the class
        """
        
        sql = f"""INSERT into MainUpdateHistory (date, version, success, errorid)
                  VALUES({self.date, self.version, self.success, self.errorid})"""
        
        conn = db.db_conn()
        with conn:
            with closing(conn.cursor()) as cur:
                cur = conn.cursor()
                cur.execute(sql)
        

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(), 'MainUpdateHistory', 'id', '(SELECT MAX(ID)  FROM TABLE)', self)

    def print_me(self):
        """
        Prints object to output
        """
        print(self)


@dataclass
class SelfUpdate():
    """
    Class for interfacing with the SelfUpdate table
    """
    id: int = 1
    dateupdated: str = None
    runupdate: bool = True
    version: str = None
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
    """
    Class for interfacing with the SelfUpdateHistory table
    """
    id: int
    date: date
    version: str
    success: bool
    errorid: int


@dataclass
class DBversion():
    """
    Class for interfacing with the DBversion table
    """
    id: str = None
    version: str = None
    dateupdated: date = None
    notes: str = None

    def insert_to_db(self):
        """
        The insert_to_db function inserts a new row into the DBVersion table with the version number.
        
        
        Args:
            self: Access the variables in the class
        """
        
        sql = f"INSERT into DBversion (version) VALUES({self.version})"
        
        conn = db.db_conn()
        with conn:
            with closing(conn.cursor()) as cur:
                cur = conn.cursor()
                cur.execute(sql)
        

    def pull_from_db(self):
        """
        Pulls object table from DB
        """
        db.db_return_class_object(db.db_conn(), 'DBversion', 'id', '(SELECT MAX(ID)  FROM TABLE)', self)

    def print_me(self):
        """
        Prints object to output
        """
        print(self)


@dataclass
class Errors():
    """
    Class for interfacing with the Errors table
    """
    id: int
    date: date
    message: str
    mainorself: str


@dataclass
class ServerInfo:
    """
    Class for interfacing with the SErverInfo table
    """
    id: int = 1
    enablecheck: bool = True
    scheme: str = 'http://'
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
    """
    Class for interfacing with the ConfigObj object. This holds the Mainconfig,
    SelfUpdate, and ServerInfo tables. As well as the temp field onlineversion.
    """
    mainconfig: MainConfig = MainConfig()
    selfupdate: SelfUpdate = SelfUpdate()
    serverinfo: ServerInfo = ServerInfo()
    onlineversion: str = None
    
    def get_config(self):
        """
        The get_config function pulls the configuration from the database tables MainConfig,
        SelfUpdate, and ServerInfo then returns it as a dataclass object.
        
        
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
    """
    Class for interfacing with the DistroConfig table
    """
    distro: str = None
    downloadurl: str = None
    installcommand: str = None
    installfile: str = None

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
        db.db_return_class_object(db.db_conn(), 'DistroConfig', 'distro', what, self)
        
    def pull_distros(self):
        """
        pulls all distros from table and returns them
        """
        return db.db_select_values(db.db_conn(),'DistroConfig','distro')

    def print_me(self):
        """
        Prints object to output
        """
        pp(self, depth=1, indent=4)
