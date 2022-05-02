from dataclasses import dataclass
from datetime import date, datetime



@dataclass
class MainConfig():
    id          : int = 1
    configran   : bool = False
    distro      : str = None
    startserver : bool = False
    stopserver  : bool = False
    version     : str = 'First Run'
    releasetype : str = 'Stable'
    dateupdated : str = None

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
class ServerInfo():
    id: int = 1
    enablecheck: bool = True
    scheme: str = 'https://'
    address: str = 'localhost'
    port: str = '8096'
    portused: bool = True
    apipath: str = '/System/Info/Public'

@dataclass
class ConfigObj():
    main_config: MainConfig = None
    self_update: SelfUpdate = None
    






