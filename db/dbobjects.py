from dataclasses import dataclass
from datetime import date, datetime



@dataclass
class MainConfig():
    id          : int = None
    configran   : bool = None
    distro      : str = None
    startserver : bool = False
    stopserver  : bool = False
    version     : str = None
    releasetype : str = None
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
    id: int = None
    dateupdated:str = None
    runupdate: bool = True
    version: str = None
    releasetype: str = None

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
class ConfigObj():
    main_config: MainConfig = None
    self_update: SelfUpdate = None
    






