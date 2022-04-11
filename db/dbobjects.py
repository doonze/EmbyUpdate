from dataclasses import dataclass
from datetime import date, datetime
from dbconnector import DBConn
import db_functions

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
class SelfUpdate():
    id: int




""" t = MainConfig(1, False, "Test", False, False, "1.1", "Stable", "None")
r = db_functions.db_update_class_in_table(db_functions.db_create_connection(), t, "MainConfig", "id", "1")
print(r) """





