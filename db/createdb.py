"""
Creates DB tables and does initial data loads
"""

import sys
from contextlib import closing
from sqlite3 import Error

import db.dbobjects as db_obj
from db.db_functions import db_conn
from db.dbobjects import DistroConfig
from functions import exceptrace

DB_VERSION = "1.0"


# pylint: disable=line-too-long

def create_distros():
    """
    The create_distros function creates a list of DistroConfig objects.
    """
    dist_entry = db_obj.DistroConfig
    distro_list: list[DistroConfig] = \
        [dist_entry("Debian X64",
                    "https://github.com/MediaBrowser/Emby.Releases/releases/"
                    "download/{online_version}/{install_file}",
                    "sudo dpkg -i -E {install_file}",
                    "emby-server-deb_{online_version}_amd64.deb"),
         dist_entry("Debian ARM",
                    "https://github.com/MediaBrowser/Emby.Releases/releases/"
                    "download/{online_version}/{install_file}",
                    "dpkg -i {install_file}",
                    "emby-server-deb_{online_version}_armhf.deb"),
         dist_entry("Arch",
                    "notused",
                    "sudo pacman -S emby-server",
                    "notused"),
         dist_entry("CentOS",
                    "sudo yum --y install https://github.com/MediaBrowser/Emby.Releases/"
                    "releases/download/{online_version}/emby-server-rpm_{online_version}_x86_64.rpm",
                    "notused",
                    "notused"),
         dist_entry("Fedora X64",
                    "sudo dnf -y install https://github.com/MediaBrowser/Emby.Releases/"
                    "releases/download/{online_version}/emby-server-rpm_{online_version}_x86_64.rpm",
                    "notused",
                    "notused"),
         dist_entry("Fedora ARM",
                    "sudo dnf -y install https://github.com/MediaBrowser/Emby.Releases/"
                    "releases/download/{online_version}/emby-server-rpm_{online_version}_aarch64.rpm",
                    "notused",
                    "notused"),
         dist_entry("OpenSUSE X64",
                    "sudo zypper install https://github.com/MediaBrowser/Emby.Releases/"
                    "releases/download/{online_version}/emby-server-rpm_{online_version}_x86_64.rpm",
                    "notused",
                    "notused"),
         dist_entry("OpenSUSE ARM",
                    "sudo zypper install -y https://github.com/MediaBrowser/Emby.Releases/"
                    "releases/download/{online_version}/emby-server-rpm_{online_version}_aarch64.rpm",
                    "notused",
                    "notused")]

    for obj in distro_list:
        obj.insert_to_db()


def populate_db(version_num):
    """
    The populate_db function is used to populate the database with some initial data.
    It is called when the program is first ran and can be used to add default values for
    the main configuration options.  This function should only be called once for a new installation.
    However, it can be called manually to reset all setting to default.

    Args:

    Returns:
        Nothing
    """

    main_config = db_obj.MainConfig()
    main_config.insert_to_db()

    self_update = db_obj.SelfUpdate(version=version_num)
    self_update.insert_to_db()

    server_info = db_obj.ServerInfo()
    server_info.insert_to_db()


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
                cur.execute("DROP TABLE IF EXISTS DBversion")
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
                "errorid"	TEXT,
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
                "servername"	TEXT DEFAULT '',
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
                db_obj.DBversion(version=DB_VERSION,
                                 notes="Initial DB creation").insert_to_db()

                print()
                print(f"Database version {DB_VERSION} has been created!")

    except Error:
        exceptrace.execpt_trace("***create_db: An error was encountered creating the DB",
                                sys.exc_info())
        print()
        print("We were not able to create the database, exiting...")
        sys.exit()
