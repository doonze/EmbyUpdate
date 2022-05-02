from site import execsitecustomize
from .db_functions import db_create_connection
from contextlib import closing
from db.db_functions import db_insert_class_in_table
import db.dbobjects

""" 
DB                          Tables
------------------------------------------------------------------------------------------------------------
MainConfig              |  id, configran, distro, startserver, stopserver, version, releasetype, dateupdated
MainUpdateHistory       |  id, date, version, success, errorid
SelfUpdate              |  id, dateupdated, runupdate, version, releasetype
SelfUpdateHistory       |  id, date, version, success, errorid
DbUpdateHistory         |  version, date, notes
DBversion               |  version, dateupdated
Errors                  |  id, date, message, mainorself
------------------------------------------------------------------------------------------------------------
"""



def CreateDB():
    conn = db_create_connection()    
    with conn:
        with closing(conn.cursor()) as cur:

            cur.execute("DROP TABLE IF EXISTS MainConfig")
            cur.execute("DROP TABLE IF EXISTS MainUpdateHistory")
            cur.execute("DROP TABLE IF EXISTS SelfUpdate")
            cur.execute("DROP TABLE IF EXISTS SelfUpdateHistory")
            cur.execute("DROP TABLE IF EXISTS DbUpdateHistory")
            cur.execute("DROP TABLE IF EXISTS Dbversion")
            cur.execute("DROP TABLE IF EXISTS Errors")
            cur.execute("DROP TABLE IF EXISTS ServerInfo")

            MainConfig = """
            CREATE TABLE "MainConfig" (
            "id"	INTEGER NOT NULL UNIQUE,
            "configran"	INTEGER NOT NULL DEFAULT 0,
            "distro"	TEXT NOT NULL DEFAULT 'None',
            "startserver"	INTEGER NOT NULL DEFAULT 0,
            "stopserver"	INTEGER NOT NULL DEFAULT 0,
            "version"	TEXT NOT NULL DEFAULT 'First Run',
            "releasetype"	TEXT NOT NULL DEFAULT 'Stable',
            "dateupdated"	TEXT,
            PRIMARY KEY("id")
            );
            """

            MainUpdateHistory = """
            CREATE TABLE "MainUpdateHistory" (
            "id"	INTEGER NOT NULL UNIQUE,
            "date"	TEXT,
            "version"	TEXT,
            "success"	INTEGER NOT NULL DEFAULT 0,
            "errorid"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """

            SelfUpdate = """
            CREATE TABLE "SelfUpdate" (
            "id"	INTEGER NOT NULL UNIQUE,
            "dateupdated"	TEXT NOT NULL DEFAULT 'None',
            "runupdate"	INTEGER NOT NULL DEFAULT 1,
            "version"	TEXT NOT NULL DEFAULT 'First Run',
            "releasetype"	TEXT NOT NULL DEFAULT 'Stable',
            PRIMARY KEY("id")
            );    
            """    

            SelfUpdateHistory = """
            CREATE TABLE "SelfUpdateHistory" (
            "id"	INTEGER NOT NULL UNIQUE,
            "date"	TEXT,
            "version"	TEXT,
            "success"	INTEGER NOT NULL DEFAULT 0,
            "errorid"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """

            DbUpdateHistory = """
            CREATE TABLE "DBUpdateHistory" (
            "version"	INTEGER NOT NULL UNIQUE,
            "date"	TEXT,
            "notes"	TEXT,
            PRIMARY KEY("version")
            );
            """

            DBversion = """
            CREATE TABLE "DBversion" (
            "version"	INTEGER NOT NULL DEFAULT 1 UNIQUE,
            "dateupdated"	TEXT,
            PRIMARY KEY("version")
            );
            """

            Errors = """
            CREATE TABLE "Errors" (
            "id"	INTEGER NOT NULL UNIQUE,
            "date"	TEXT,
            "message"	TEXT,
            "mainorself"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """

            ServerInfo = """
            CREATE TABLE "ServerInfo" (
            "id"	INTEGER NOT NULL UNIQUE,
            "enablecheck"	INTEGER NOT NULL DEFAULT 1,
            "scheme"	TEXT NOT NULL DEFAULT 'http://',
            "address"	TEXT NOT NULL DEFAULT 'localhost',
            "port"	TEXT NOT NULL DEFAULT 8096,
            "portused"	INTEGER NOT NULL DEFAULT 1,
            "apipath"	TEXT NOT NULL DEFAULT '/System/Info/Public',
            PRIMARY KEY("id")
            );
            """ 

            cur.execute(MainConfig)
            cur.execute(MainUpdateHistory)
            cur.execute(SelfUpdate)
            cur.execute(SelfUpdateHistory)
            cur.execute(DbUpdateHistory)
            cur.execute(DBversion)
            cur.execute(Errors)
            cur.execute(ServerInfo)

            mainconfig = db.dbobjects.MainConfig(1, 0, 'None', 0, 0, 'First Run', 'Stable')
            db_insert_class_in_table(conn, mainconfig, 'MainConfig')

            selfupdate = db.dbobjects.SelfUpdate(1, 'None', 1, 'First Run', 'Stable')
            db_insert_class_in_table(conn, selfupdate, 'SelfUpdate')

            serverinfo = db.dbobjects.ServerInfo(1, 1, 'http://', 'localhost', '8096', 1, '/System/Info/Public')
            db_insert_class_in_table(conn, serverinfo, 'ServerInfo')



