from dataclasses import dataclass
from datetime import date, datetime



@dataclass
class MainConfig():
    id          : int
    configran   : bool
    distro      : str
    startserver : bool
    stopserver  : bool
    version     : str
    releasetype : str
    dateupdated : date

@dataclass
class MainUpdateHistory():
    id: int
    date: date
    version: str
    success: bool
    errorid: int

@dataclass
class SelfUpdate():
    id: int
    dateupdated: date
    runupdate: bool
    version: str
    releasetype: str

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
class errors():
    id: int
    date: date
    message: str
    mainorself: str






