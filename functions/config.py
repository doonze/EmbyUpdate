import sys
import configparser
from os import remove, path
from genericpath import exists
from db.createdb import create_db
from db.dbobjects import MainConfig, SelfUpdate, ConfigObj
from db.db_functions import *
from functions.api import get_running_version


class Config:

    def __init__(self):
        self.config_file = configparser.ConfigParser()
        self.distro = "None"
        self.stop_server = False
        self.start_server = False
        self.emby_version = "First Run"
        self.emby_release = "Stable"
        self.self_update = True
        self.self_version = "First Run"
        self.self_release = "Beta"

    def config_fix(self):
        """ Convert to new DB config if needed (for versions before 4.0)."""
        try:
            # We'll read the config file to find if it's a version that needs fixing, if so we'll copy the current
            # settings into our configuration dictionary
            self.config_file.read("config.ini")
            if self.config_file.has_option('DISTRO', 'releaseversion'):
                self.distro = self.config_file['DISTRO']['installdistro']
                self.emby_release = self.config_file['DISTRO']['releaseversion']
                self.stop_server = self.config_file['SERVER']['stopserver']
                self.start_server = self.config_file['SERVER']['startserver']
                self.emby_version = self.config_file['SERVER']['embyversion']
                self.self_update = self.config_file['EmbyUpdate']['autoupdate']
                self.self_version = self.config_file['EmbyUpdate']['version']

                # Now that we have all the settings, we'll remove the config file
                if path.isfile("config.ini"):
                    remove("config.ini")

                # We'll also clean up the old configupdate.py file that's no longer used
                if path.isfile("configupdate.py"):
                    remove("configupdate.py")

                # And now we'll recreate the new file
                Config.create_config(self)
                print("")
                print("It was found you had a pre-version 4.0 config file, it's been deleted and recreated to "
                      "conform to post 4.0 config file styles.")
                print("")

        except Exception as ex:
            print("EmbyUpdate: Couldn't read the Config file.")
            print("EmbyUpdate: Here's the error we got -- " + str(ex) + " not found in config file!")
            print("There appears to be a config file error, re-runing config update to fix!")

    def write_config(self):
        """
        This function will write (update) the current Config class object to the database

        """
        try:

            mainconfig = MainConfig()
            selfupdate = SelfUpdate()

            # Main config 
            mainconfig.distro = self.distro
            mainconfig.stopserver = self.stop_server
            mainconfig.startserver = self.start_server
            mainconfig.version = self.emby_version
            mainconfig.releasetype = self.emby_release

            # Self update config            
            selfupdate.runupdate = self.self_update
            selfupdate.releasetype = self.self_release
            selfupdate.version = self.self_version

            result_main = db_update_class_in_table(db_conn, mainconfig, 'MainConfig', 'id', 1)
            result_self = db_update_class_in_table(db_conn, selfupdate, 'SelfUpdate', 'id', 1)            

        except Exception as e:
            print("EmbyUpdate: Couldn't write to the config file.")
            print("EmbyUpdate: Here's the error we got -- " + str(e))
            sys.exit(1)

    def create_config(self):
        """
         This function will create the config.ini file


        """
        print("create config, remove me")
        try:

            self.config_file['DISTRO'] = {'installdistro': self.distro}
            self.config_file['SERVER'] = {'stopserver': self.stop_server,
                                          'startserver': self.start_server,
                                          'embyversion': self.emby_version,
                                          'embyrelease': self.emby_release}
            self.config_file['EMBYUPDATE'] = {'selfupdate': self.self_update,
                                              'selfversion': self.self_version,
                                              'selfrelease': self.self_release}

            with open('config.ini', 'w') as configfile:
                self.config_file.write(configfile)

        except Exception as e:
            print("EmbyUpdate: Couldn't create the config file!")
            print("EmbyUpdate: Here's the error we got -- " + str(e))

    def read_config(self):
        """
        Used to read the entire config file into the Config class object

        """
        try:

            configobj = ConfigObj()
            

            # Now we're going to read the config from the database
            configobj.mainconfig.pull_from_db()
            configobj.selfupdate.pull_from_db()

            # Here we pull the main config params.
            

            return configobj

        except Exception as e:
            print("EmbyUpdate: Couldn't write to the config file.")
            print("EmbyUpdate: Here's the error we got -- " + str(e))

    
