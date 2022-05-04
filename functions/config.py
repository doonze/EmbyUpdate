import sys
import configparser
from os import remove, path
from genericpath import exists
from turtle import update
from cupshelpers import missingPackagesAndExecutables
from db.createdb import CreateDB
from db.dbobjects import MainConfig, SelfUpdate, ConfigObj, ServerInfo
from db.db_functions import *
from functions.api import GetRunningVersion


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

            result_main = db_update_class_in_table(db_create_connection, mainconfig, 'MainConfig', 'id', 1)
            result_self = db_update_class_in_table(db_create_connection, selfupdate, 'SelfUpdate', 'id', 1)            

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
            configobj.main_config = db_return_class_object(db_create_connection(), 'MainConfig', 'id', '1', MainConfig)
            configobj.self_update = db_return_class_object(db_create_connection(), 'SelfUpdate', 'id', '1', SelfUpdate)

            # Here we pull the main config params.
            

            return configobj

        except Exception as e:
            print("EmbyUpdate: Couldn't write to the config file.")
            print("EmbyUpdate: Here's the error we got -- " + str(e))

    def config_setup(self):
        """
        The config_setup function will gather user input and write it to the database.
        This function will also be used to read from the database when needed.
        
        
        Args:
            self: Access variables that belongs to the class
     
        """
        
        # Now we'll start gathering user input

        # First to check if Emby is running so we can get the version #
        runningVersion = GetRunningVersion()

        if runningVersion['version'] == None:
            print()
            print("I didn't find a running Emby instance on this server.")
            print(f"I tried the default address {runningVersion['url']}")
            print("If this is correct, make sure the sever is running.")
            print()
            print("[1] You can skip this check for now")
            print("[2] Permanently disable this check")
            print("[3] Update the server address")
            print("[4] Cancel this run (maybe to start the server?)")
            print()

            loop = True
            while loop:

                r = input("Make your choice by number, use 4 or C to cancel update [?]: ")

                if str(r) == "1":
                    break

                elif str(r) == "2":
                    db_update_value(db_create_connection, 'ServerInfo', 'enablecheck', False, 'id', 1)
                    print("Server check has been permanently disabled.")
                    break

                elif str(r) == "3":                   
                    while True:
                        serverinfo = ServerInfo()
                        scheme: str = "http://"
                        
                        ssl : bool = False
                        portNum : str = ""

                        while True:
                            r = input("Do you use a port to access your server? [Y/n]: ")

                            if r.casefold() == "y" or r == "":
                                serverinfo.portused = True
                                break
                            elif r.casefold() == "n":
                                serverinfo.portused = False
                                break
                            else:
                                print("Invalid response. Enter (y)es or (n)o.")
                                print()
                        
                        while True:
                            r = input("Do you use ssl to access your server (HTTPS://)? [Y/n]: ")

                            if r.casefold() == "y" or r == "":
                                serverinfo.scheme = "https://"
                                break
                            elif r.casefold() == "n":
                                serverinfo.scheme = "http://"
                                break
                            else:
                                print("Invalid response. Enter (y)es or (n)o.")
                            
                        if serverinfo.portused: 
                            serverinfo.port = input("Please enter port number: ")
                        
                        serverinfo.address = input("Please enter address: ")
                        
                        while True:
                            if serverinfo.portused:
                                print()
                                print(f"Here's what I have: {serverinfo.scheme}{serverinfo.address}:{serverinfo.port}")
                                print()
                            else:
                                print()
                                print(f"Here's what I have: {serverinfo.scheme}{serverinfo.address}")
                                print()

                            r = input("Is this correct? [Y/n]: ")
                            if r.casefold() == "y" or r == "":
                                db_insert_class_in_table(db_create_connection, serverinfo, 'ServerInfo')

                                # TODO: Needs to pull the existing serverinfo data first before all this
                                # in case this is a config update and not a new install. Also need to display the 
                                # current values and ask if the need changed first
                                # TODO: At this point It's writing the changes to the DB, but we need to check FIRST
                                # that the settings work before writing the info
                                # TODO: Add a cancel if the new setting don't work, and another chance to disable
                                # the server check
                                # 
                                

                        

                        









        # Next user will choose their distro

        print("[1] Debian X64")
        print("[2] Debian ARM")
        print("[3] Arch")
        print("[4] CentOS")
        print("[5] Fedora X64")
        print("[6] Fedora ARM")
        print("[7] OpenSUSE X64")
        print("[8] OpenSUSE ARM")
        print("[C] Cancel config update")

        while True:
            distro_choice = input("Choose your distro by number or C to cancel update [?]: ")
            if str(distro_choice) == "1":
                self.distro = "Debian X64"
                break
            elif str(distro_choice) == "2":
                self.distro = "Debian ARM"
                break
            elif str(distro_choice) == "3":
                self.distro = "Arch"
                break
            elif str(distro_choice) == "4":
                self.distro = "CentOS"
                break
            elif str(distro_choice) == "5":
                self.distro = "Fedora X64"
                break
            elif str(distro_choice) == "6":
                self.distro = "Fedora ARM"
                break
            elif str(distro_choice) == "7":
                self.distro = "OpenSUSE X64"
                break
            elif str(distro_choice) == "8":
                self.distro = "OpenSUSE ARM"
                break
            elif str(distro_choice.casefold()) == "c":
                print("")
                print("Exiting config update and installer....")
                print("")
                sys.exit(1)
            else:
                print("")
                print("Invalid Choice! Valid choices are 1-8 or C to cancel. Please Try again.")
                print("")

        print("")
        print(self.distro + " Chosen")
        print("")

        # Now user chooses beta or Stable releases

        while True:
            choose_beta = input("Do you want to install the beta version of Emby Server? [y/N] ")
            if choose_beta.casefold() == "y":
                self.emby_release = "Beta"
                break
            elif choose_beta == "n" or choose_beta == "N" or choose_beta == "":
                self.emby_release = "Stable"
                break
            else:
                print("")
                print("Invalid choice. Please choose y or n")
                print("")

        print("")
        print(self.emby_release + " version of Emby has been chosen for install.")
        print("")

        # User chooses if they wish to stop the server before installing updates. Not normally needed.

        while True:
            servstop = input("Do we need to manually stop the server to install? (Likely only needed for Arch.) [y/N] ")
            if servstop.casefold() == "y":
                servstopchoice = "Server will be manually stopped on install."
                self.stop_server = True
                break
            elif servstop == "n" or servstop == "N" or servstop == "":
                servstopchoice = "Server will NOT be manually stopped on install."
                self.stop_server = False
                break
            else:
                print("")
                print("Invalid choice. Please choose y or n")
                print("")

        print("")
        print(servstopchoice)
        print("")

        # User chooses if they wish to start the server again after updates. Not normally needed.
        while True:
            servstart = input(
                "Do we need to manually start the server after install? (Likely only needed for Arch.) [y/N] ")
            if servstart.casefold() == "y":
                server_start_choice = "Server will be manually started after install."
                self.start_server = True
                break
            elif servstart == "n" or servstart == "N" or servstart == "":
                server_start_choice = "Server will NOT be manually started after install."
                self.start_server = False
                break
            else:
                print("")
                print("Invalid choice. Please choose y or n")
                print("")

        print("")
        print(server_start_choice)
        print("")

        # User chooses if they wish to autoupdate the Update app (this program)
        while True:
            script_update = input("Keep EmbyUpdate (this script) up to date with latest version? [Y/n] ")
            if script_update.casefold() == "y" or script_update == "":
                script_update_choice = "Script (EmbyUpdate) will be automatically updated!"
                self.self_update = True
                break
            elif script_update.casefold() == "n":
                script_update_choice = "Script (EmbyUpdate) will NOT be automatically updated!"
                self.self_update = False
                break
            else:
                print("")
                print("Invalid choice. Please choose y or n")
                print("")

        print("")
        print(script_update_choice)
        print("")

        # User chooses if they want to update to beta or stable for the script
        while True:
            script_beta_choice = input("Install EmbyUpdate Beta versions (this script)? [y/N] ")
            if script_beta_choice.casefold() == "y":
                self_beta_choice = "Script (EmbyUpdate) will be automatically updated to Beta!"
                self.self_release = "Beta"
                break
            elif script_beta_choice.casefold() == "n" or script_beta_choice == "":
                self_beta_choice = "Script (EmbyUpdate) will NOT be automatically updated to Stable!"
                self.self_release = "Stable"
                break
            else:
                print("")
                print("Invalid choice. Please choose y or n")
                print("")

        print("")
        print(self_beta_choice)
        print("")

        print("Choices to write to config file...")
        print("Linux distro version to update: " + self.distro)
        print("The chosen Emby Server install version. is: " + self.emby_release)
        print(servstopchoice)
        print(server_start_choice)
        print(script_update_choice)
        print(self_beta_choice)
        print("")

        while True:
            confirm = input("Please review above choices and type CONFIRM to continue or c to cancel update "
                            "and install! [CONFIRM/c] ")
            if confirm.casefold() == "c":
                print("")
                print("Exiting config update and installer. No changes were made and nothing will be installed!")
                print("")
                sys.exit(1)
            elif confirm == "CONFIRM":
                break
            else:
                print("")
                print("Invalid choice. Please type CONFIRM to continue or c to cancel!!")
                print("")

        # Setup the config interface

        # Test if the DB exist and creates it if it doesn't
        if not exists('./db/embyupdate.db'):
            try: 
                print()
                print("DB does NOT exist, creating DB...")
                CreateDB()
                print("DB has been created.")
                print()
            except Exception as e:
                print("EmbyUpdate: Couldn't create the DataBase.")
                print("EmbyUpdate: Here's the error we got -- " + str(e))

        # Now we write the config to the database
        try:
            self.write_config()
        except Exception as e:
            print("EmbyUpdate: Couldn't update the database.")
            print("EmbyUpdate: Here's the error we got -- " + str(e))
            print("EmbyUpdate: Cannot continue, exiting.")
            sys.exit(1)

        print("")
        print("Config written to database, install continuing!")
        print("")
