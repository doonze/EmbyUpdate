from .db_functions import db_create_connection
from contextlib import closing

""" 
DB                          Tables
------------------------------------------------------------------------------------------------------------
MainConfig              |  id, configran, distro, startserver, stopserver, version, releasetype, dateupdated
MainUpdateHistory       |  id, date, version , success, errorid
SelfUpdate              |  id, dateupdate, runupdate, version, releasetype
SelfUpdateHistory       |  id, date, version, success, errorid
DbUpdateHistory         |  version, date, notes
Dbversion               |  version, dateupdated
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
            PRIMARY KEY("id" AUTOINCREMENT)
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
            "runupdate"	INTEGER NOT NULL DEFAULT 0,
            "version"	TEXT NOT NULL DEFAULT 'First Run',
            "releasetype"	TEXT NOT NULL DEFAULT 'Stable',
            PRIMARY KEY("id" AUTOINCREMENT)
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

            Dbversion = """
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

            cur.execute(MainConfig)
            cur.execute(MainUpdateHistory)
            cur.execute(SelfUpdate)
            cur.execute(SelfUpdateHistory)
            cur.execute(DbUpdateHistory)
            cur.execute(Dbversion)
            cur.execute(Errors)

            values = (0, 'None', 0, 0, 'First Run', 'Stable')
            sql = """ INSERT INTO MainConfig(configran, distro, startserver, stopserver, version, 
            releasetype) VALUES (?,?,?,?,?,?) """
            cur.execute(sql, values)
            conn.commit()

            values = ('None', 0, 'First Run', 'Stable')
            sql = """ INSERT INTO SelfUpdate(dateupdated, runupdate, version, releasetype)
            VALUES (?,?,?,?) """
            cur.execute(sql, values)
            conn.commit()



