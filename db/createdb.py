"""
Creates DB tables and does initial data loads
"""

import sys
from contextlib import closing
from sqlite3 import Error
import db.dbobjects as db_obj
from db.db_functions import db_conn
from functions import exceptrace

DBVERSION = "1.0"


def create_distros():
    """
    The create_distros function creates a list of DistroConfig objects.
    """

    distro_list: db_obj.DistroConfig = []
    obj: db_obj.DistroConfig = None

    distro_list.append(db_obj.DistroConfig("Debian X64",
                                           "https://github.com/MediaBrowser/Emby.Releases/releases/"
                                           "download/{0}/{1}",
                                           "dpkg -i -E {0}",
                                           "emby-server-deb_{0}_amd64.deb"))

    distro_list.append(db_obj.DistroConfig("Debian ARM",
                                           "https://github.com/MediaBrowser/Emby.Releases/releases/"
                                           "download/{0}/{1}",
                                           "dpkg -i {0}",
                                           "emby-server-deb_{0}_armhf.deb"))

    distro_list.append(db_obj.DistroConfig("Arch",
                                           "notused",
                                           "pacman -S emby-server",
                                           "notused"))

    distro_list.append(db_obj.DistroConfig("CentOS",
                                           "yum --y install https://github.com/MediaBrowser/Emby.Releases/"
                                           "releases/download/{0}/emby-server-rpm_{0}_x86_64.rpm",
                                           "notused",
                                           "notused"))

    distro_list.append(db_obj.DistroConfig("Fedora X64",
                                           "dnf -y install https://github.com/MediaBrowser/Emby.Releases/"
                                           "releases/download/{0}/emby-server-rpm_{0}_x86_64.rpm",
                                           "notused",
                                           "notused"))

    distro_list.append(db_obj.DistroConfig("Fedora ARM",
                                           "dnf -y install https://github.com/MediaBrowser/Emby.Releases/"
                                           "releases/download/{0}/emby-server-rpm_{0}_armv7hl.rpm",
                                           "notused",
                                           "notused"))

    distro_list.append(db_obj.DistroConfig("OpenSUSE X64",
                                           "zypper install https://github.com/MediaBrowser/Emby.Releases/"
                                           "releases/download/{0}/emby-server-rpm_{0}_x86_64.rpm",
                                           "notused",
                                           "notused"))

    distro_list.append(db_obj.DistroConfig("OpenSUSE ARM",
                                           "zypper install -y https://github.com/MediaBrowser/Emby.Releases/"
                                           "releases/download/{0}/emby-server-rpm_{0}_armv7hl.rpm",
                                           "notused",
                                           "notused"))

    for obj in distro_list:
        obj.insert_to_db()


def populate_db(version_num):
    """
    The populate_db function is used to populate the database with some initial data.
    It is called when the server is started up and can be used to add default values for
    the main configuration options.  This function should only be called once at startup.
    However, it can be called manually to reset all setting to default.

    Args:

    Returns:
        Nothing
    """

    mainconfig = db_obj.MainConfig()
    mainconfig.insert_to_db()

    selfupdate = db_obj.SelfUpdate(version=version_num)
    selfupdate.insert_to_db()

    serverinfo = db_obj.ServerInfo()
    serverinfo.insert_to_db()


def create_db(version_num):
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
                cur.execute("DROP TABLE IF EXISTS Dbversion")
                cur.execute("DROP TABLE IF EXISTS Errors")
                cur.execute("DROP TABLE IF EXISTS ServerInfo")
                cur.execute("DROP TABLE IF EXISTS DistroConfig")

                main_config_sql = """
                CREATE TABLE "MainConfig" (
                "id"	        INTEGER NOT NULL UNIQUE,
                "configran"	    INTEGER NOT NULL,
                "distro"	    TEXT NOT NULL,
                "startserver"	INTEGER NOT NULL,
                "stopserver"	INTEGER NOT NULL,
                "version"	    TEXT NOT NULL,
                "releasetype"	TEXT NOT NULL,
                "dateupdated"	TEXT,
                "embygithubapi" TEXT NOT NULL,
                PRIMARY KEY("id")
                );
                """

                main_update_history_sql = """
                CREATE TABLE "MainUpdateHistory" (
                "id"	    INTEGER NOT NULL UNIQUE,
                "date"	    TEXT,
                "version"	TEXT,
                "success"	INTEGER NOT NULL,
                "errorid"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                self_update_sql = """
                CREATE TABLE "SelfUpdate" (
                "id"	        INTEGER NOT NULL UNIQUE,
                "dateupdated"	TEXT,
                "runupdate"	    INTEGER NOT NULL,
                "version"	    TEXT,
                "onlineversion"	TEXT,
                "releasetype"	TEXT NOT NULL,
                "selfgithubapi" TEXT NOT NULL,
                "downloadurl"   TEXT NOT NULL,
                "zipfile"       TEXT,
                PRIMARY KEY("id")
                );    
                """

                self_update_history_sql = """
                CREATE TABLE "SelfUpdateHistory" (
                "id"	    INTEGER NOT NULL UNIQUE,
                "date"	    TEXT,
                "version"	TEXT,
                "success"	INTEGER NOT NULL,
                "errorid"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                db_version_sql = """
                CREATE TABLE "DBversion" (
                "id"	        INTEGER NOT NULL UNIQUE,
                "version"	    TEXT NOT NULL UNIQUE,
                "dateupdated"	NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                "notes"    TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                errors_sql = """
                CREATE TABLE "Errors" (
                "id"	      INTEGER NOT NULL UNIQUE,
                "date"	      TEXT,
                "message"	  TEXT,
                "mainorself"  TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """

                server_info_sql = """
                CREATE TABLE "ServerInfo" (
                "id"	        INTEGER NOT NULL UNIQUE,
                "enablecheck"	INTEGER NOT NULL DEFAULT 1,
                "scheme"	    TEXT NOT NULL DEFAULT 'http://',
                "address"	    TEXT NOT NULL DEFAULT 'localhost',
                "port"	        TEXT NOT NULL DEFAULT 8096,
                "portused"	    INTEGER NOT NULL DEFAULT 1,
                "apipath"	    TEXT NOT NULL DEFAULT '/System/Info/Public',
                "fullurl"	    TEXT DEFAULT '',
                "version"	    TEXT DEFAULT '',
                PRIMARY KEY("id")
                );
                """

                distro_config_sql = """
                CREATE TABLE "DistroConfig" (
                "distro"	     TEXT NOT NULL UNIQUE,
                "downloadurl"	 TEXT NOT NULL,
                "installcommand" TEXT NOT NULL,
                "installfile"    TEXT NOT NULL,
                PRIMARY KEY("distro")
                );
                """

                cur.execute(main_config_sql)
                cur.execute(main_update_history_sql)
                cur.execute(self_update_sql)
                cur.execute(self_update_history_sql)
                cur.execute(db_version_sql)
                cur.execute(errors_sql)
                cur.execute(server_info_sql)
                cur.execute(distro_config_sql)

                populate_db(version_num)
                create_distros()
                db_obj.DBversion(version=DBVERSION,
                                 notes="Initial DB creation").insert_to_db()

    except Error:
        exceptrace.execpt_trace("***create_db: An error was encountered creating the DB",
                                sys.exc_info())
        print()
        print("We were not able to create the database, exiting...")
        sys.exit()
