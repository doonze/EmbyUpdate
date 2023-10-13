"""
legacy config reader, only used to convert to new database format
"""
import sys
import configparser
from os import remove
from genericpath import exists
from db.createdb import create_db
from db.dbobjects import ConfigObj
from functions import exceptrace


# pylint: disable=broad-except

class Config:
    """
    This class is now only used to convert from older versions of the config process to the new
    database version
    """

    def __init__(self):
        self.config_file = configparser.ConfigParser()
        self.distro = "None"
        self.stop_server = False
        self.start_server = False
        self.emby_version = "First Run"
        self.emby_release = "Stable"
        self.self_update = True
        self.self_version = "First Run"
        self.self_release = "Stable"

    def config_fix(self, version):
        """ Convert to new DB config if needed (for versions before 4.0)."""
        try:

            if exists("config.ini"):
                print()
                print("I've detected an old style config file. I will now try to fix it if")
                print("it's pre version 3.5, and then recreate your settings in the new")
                print("database config.")
            else:
                return None

            # We'll read the config file to find if it's a version that needs fixing, if so we'll
            # copy the current settings into our configuration dictionary
            self.config_file.read("config.ini")
            if self.config_file.has_option('DISTRO', 'releaseversion'):
                print()
                print("Old style config found, trying to fix it")
                self.distro = self.config_file['DISTRO']['installdistro']
                self.emby_release = self.config_file['DISTRO']['releaseversion']
                self.stop_server = self.config_file['SERVER']['stopserver']
                self.start_server = self.config_file['SERVER']['startserver']
                self.emby_version = self.config_file['SERVER']['embyversion']
                self.self_update = self.config_file['EmbyUpdate']['autoupdate']
                self.self_version = self.config_file['EmbyUpdate']['version']

            else:
                print()
                print("Reading old style config so we can write it to the database.")
                self.distro = self.config_file['DISTRO']['installdistro']
                self.stop_server = self.config_file['SERVER'].getboolean('stopserver')
                self.start_server = self.config_file['SERVER'].getboolean('startserver')
                self.emby_version = self.config_file['SERVER']['embyversion']
                self.emby_release = self.config_file['SERVER']['embyrelease']
                self.self_update = self.config_file['EMBYUPDATE'].getboolean('selfupdate')
                self.self_version = self.config_file['EMBYUPDATE']['selfversion']
                self.self_release = self.config_file['EMBYUPDATE']['selfrelease']

            # Now we'll create the DB
            if not exists('./db/embyupdate.db'):
                print()
                print("Trying to create Database...")
                create_db(version)

            # Next we'll put the old config data in our new dataclass style config
            # and write the old config to the new database
            print()
            print("Converting settings...")
            configobj = ConfigObj().get_config()
            configobj.mainconfig.distro = self.distro
            configobj.mainconfig.stopserver = self.stop_server
            configobj.mainconfig.startserver = self.start_server
            configobj.mainconfig.version = self.emby_version
            configobj.mainconfig.releasetype = self.emby_release
            configobj.selfupdate.runupdate = self.self_update
            configobj.selfupdate.version = self.self_version
            configobj.selfupdate.releasetype = self.self_release
            print()
            print("Settings converted from old config file... Writing to database.")
            configobj.mainconfig.update_db()
            configobj.selfupdate.update_db()
            print()
            print("Imported settings written to database")

            # Now that we have all the settings converted, we'll remove the config file
            if exists("config.ini"):
                print()
                print("Trying to remove config file...")
                remove("config.ini")
                print("config.ini removed. (no longer needed)")

            # We'll also clean up the old configupdate.py file that's no longer used
            if exists("configupdate.py"):
                print("configupdate.py removed (no longer needed).")
                remove("configupdate.py")

        except (OSError, SystemError):
            exceptrace.execpt_trace("***config_fix: An error was encountered..",
                                    sys.exc_info())
            print()
            print("We were not able to finish the conversion to the new config system.")
            print("Unfortunately, I cannot tell if you want Emby Stable or Beta, and it")
            print("won't tell me what release type it is if I ask it. I don't want to")
            print("overwrite your current server with the wrong version. This will break")
            print("you if you run this script unattended automatically (cron or systemd) ")
            print("and I'm sorry about that.")
            print()
            print("If you're seeing this, the best bet is to delete config.ini yourself")
            print("and then run 'embyupdate.py -c' to force a new run of the config process")
            print("and just start fresh. Again sorry, if you raise an issue and give me the")
            print("details on my github page, I'll fix it. But that doesn't help you now.")
            print()
            print("I'm exiting.... and very upset about it.")
            sys.exit()
