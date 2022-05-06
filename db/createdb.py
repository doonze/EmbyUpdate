"""
Creates DB tables
"""
import sys
from contextlib import closing
from sqlite3 import Error
import db.dbobjects
from db.db_functions import db_conn
from functions import exceptrace



# Tables                     Columns
# -------------------------------------------------------------------------------------------------
# MainConfig              |  id, configran, distro, startserver, stopserver, version, releasetype,
#                         |  dateupdated, embygithubapi
# MainUpdateHistory       |  id, date, version, success, errorid
# SelfUpdate              |  id, dateupdated, runupdate, version, releasetype
# SelfUpdateHistory       |  id, date, version, success, errorid
# DbUpdateHistory         |  version, date, notes
# DBversion               |  version, dateupdated
# Errors                  |  id, date, message, mainorself
# ServerInfo              |  id, enablecheck, scheme, addresss, port, portused, apipath, fullurl,
#                         |  version
# -------------------------------------------------------------------------------------------------




def create_db():
    """
    The CreateDB function creates the database tables for the program.
    """
    try:
        conn = db_conn()
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

                main_config_sql = """
                CREATE TABLE "MainConfig" (
                "id"	INTEGER NOT NULL UNIQUE,
                "configran"	INTEGER NOT NULL DEFAULT 0,
                "distro"	TEXT NOT NULL DEFAULT 'None',
                "startserver"	INTEGER NOT NULL DEFAULT 0,
                "stopserver"	INTEGER NOT NULL DEFAULT 0,
                "version"	TEXT NOT NULL DEFAULT 'First Run',
                "releasetype"	TEXT NOT NULL DEFAULT 'Stable',
                "dateupdated"	TEXT,
                "embygithubapi" TEXT NOT NULL DEFAULT 'https://api.github.com/repos/mediabrowser/Emby.releases/releases',
                PRIMARY KEY("id")
                );
                """

                main_update_history_sql = """
                CREATE TABLE "MainUpdateHistory" (
                "id"	INTEGER NOT NULL UNIQUE,
                "date"	TEXT,
                "version"	TEXT,
                "success"	INTEGER NOT NULL DEFAULT 0,
                "errorid"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                self_update_sql = """
                CREATE TABLE "SelfUpdate" (
                "id"	INTEGER NOT NULL UNIQUE,
                "dateupdated"	TEXT DEFAULT 'None',
                "runupdate"	INTEGER NOT NULL DEFAULT 1,
                "version"	TEXT NOT NULL DEFAULT 'First Run',
                "releasetype"	TEXT NOT NULL DEFAULT 'Stable',
                PRIMARY KEY("id")
                );    
                """

                self_update_history_sql = """
                CREATE TABLE "SelfUpdateHistory" (
                "id"	INTEGER NOT NULL UNIQUE,
                "date"	TEXT,
                "version"	TEXT,
                "success"	INTEGER NOT NULL DEFAULT 0,
                "errorid"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                db_update_history_sql = """
                CREATE TABLE "DBUpdateHistory" (
                "version"	INTEGER NOT NULL UNIQUE,
                "date"	TEXT,
                "notes"	TEXT,
                PRIMARY KEY("version")
                );
                """

                db_version_sql = """
                CREATE TABLE "DBversion" (
                "version"	INTEGER NOT NULL DEFAULT 1 UNIQUE,
                "dateupdated"	TEXT,
                PRIMARY KEY("version")
                );
                """

                errors_sql = """
                CREATE TABLE "Errors" (
                "id"	INTEGER NOT NULL UNIQUE,
                "date"	TEXT,
                "message"	TEXT,
                "mainorself"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                server_info_sql = """
                CREATE TABLE "ServerInfo" (
                "id"	INTEGER NOT NULL UNIQUE,
                "enablecheck"	INTEGER NOT NULL DEFAULT 1,
                "scheme"	TEXT NOT NULL DEFAULT 'http://',
                "address"	TEXT NOT NULL DEFAULT 'localhost',
                "port"	TEXT NOT NULL DEFAULT 8096,
                "portused"	INTEGER NOT NULL DEFAULT 1,
                "apipath"	TEXT NOT NULL DEFAULT '/System/Info/Public',
                "fullurl"	TEXT DEFAULT '',
                "version"	TEXT DEFAULT '',
                PRIMARY KEY("id")
                );
                """

                cur.execute(main_config_sql)
                cur.execute(main_update_history_sql)
                cur.execute(self_update_sql)
                cur.execute(self_update_history_sql)
                cur.execute(db_update_history_sql)
                cur.execute(db_version_sql)
                cur.execute(errors_sql)
                cur.execute(server_info_sql)

                mainconfig = db.dbobjects.MainConfig(1, 0, 'None', 0, 0, 'First Run', 'Stable')
                mainconfig.write_to_db()

                selfupdate = db.dbobjects.SelfUpdate(1, 'None', 1, 'First Run', 'Stable')
                selfupdate.write_to_db()

                serverinfo = db.dbobjects.ServerInfo(1, 1, 'http://', 'localhost', '8096', 1, \
                    '/System/Info/Public')
                serverinfo.write_to_db()

    except Error:
        exceptrace.execpt_trace("***create_db: An error was enountered creating the DB", \
            sys.exc_info())
        