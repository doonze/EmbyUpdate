"""
Config setup module

"""
import sys
from sqlite3 import Error
import db.dbobjects as db_obj
from functions import api, exceptrace

def config_setup():
    """
    The config_setup function will gather user input and write it to the database.
    This function will also be used to read from the database when needed.

    Args:
        self: Access variables that belongs to the class

    """

    # Now we'll start gathering user input

    # First to check if Emby is running so we can get the version 
    serverinfo: db_obj.ServerInfo = api.get_running_version()

    # If the option to check server is True, and the sever is not reachable, we'll run the server
    # setup
    if serverinfo.enablecheck:
        if serverinfo.version == "None":
            print()
            print("I didn't find a running Emby instance on this server.")
            print(f"I tried the address {serverinfo.fullurl}")
            print("If this is correct, make sure the server is running.")
            print()
            print("* This is not required, however the script will try to update   *")
            print("* Emby to the lastest version as we cannot contact the server   *")
            print("* to find what version it's currently running. It doesn't hurt  *")
            print("* anything to do so. But saves some time on slow connections if *")
            print("* your already running the latest version. After the first      *")
            print("* update we'll keep track of the version installed anyway.      *")
            print()
            print("[1] You can skip this check for now")
            print("[2] Permanently disable this check")
            print("[3] Update the server address")
            print("[4] Cancel this run (maybe to start the server?)")
            print()
            
            loop = True
            while loop:

                response = input("Make your choice by number, or use 4 or C to cancel update [?]: ")
                print()

                if str(response) == "1":
                    print("Skipping server check and continuing config setup...")
                    print()
                    loop = False
                    break

                if str(response) == "2":
                    serverinfo.enablecheck = False
                    serverinfo.update_db()
                    print()
                    print("Server check has been permanently disabled.")
                    print()
                    loop = False
                    break

                if str(response) == "3":
                    while True:
                        while loop:
                            print("*** Just hitting enter will retain current values. ***")
                            print()
                            response = input("Do you use a port to access your server? "
                                f"Current value is ({serverinfo.portused}) [y/n]: ")
                            if response.casefold() == "y":
                                serverinfo.portused = True
                                break

                            if response.casefold() == "n":
                                serverinfo.portused = False
                                break

                            if response == "":
                                break

                            print("Invalid response. Enter (y)es or (n)o.")
                            print()

                        while True:
                            response = input("Do you use ssl to access your server? "
                                f"[Example: HTTPS://] Current value is ({serverinfo.scheme}) "
                                "[y/n]: ")

                            if response.casefold() == "y":
                                serverinfo.scheme = "https://"
                                break

                            if response.casefold() == "n":
                                serverinfo.scheme = "http://"
                                break

                            if response == "":
                                break

                            print("Invalid response. Enter (y)es or (n)o.")

                        if serverinfo.portused:
                            response = input("Please enter port number. "
                                f"Current value is ({serverinfo.port}): ")
                            if response != "":
                                serverinfo.port = response

                        response = input(f"Please enter address. Current value is "
                            f"({serverinfo.address}): ")
                        if response != "":
                            serverinfo.address = response

                        while True:
                            if serverinfo.portused:
                                print()
                                print("Here's what I have: "
                                    f"{serverinfo.scheme}{serverinfo.address}:{serverinfo.port}")
                                print()
                            else:
                                print()
                                print(f"Here's what I have: "
                                    f"{serverinfo.scheme}{serverinfo.address}")
                                print()

                            response = input("Is this correct? [Y/n]: ")
                            if response.casefold() == "y" or response == "":
                                serverinfo.update_db()
                                serverrecheck = api.get_running_version()
                                if serverrecheck.version is None:
                                    print()
                                    response = input("I'm still not able to connect. "
                                        "Try with different settings? [Y/n]: ")
                                    print()

                                    if response.casefold() == 'y' or response == "":
                                        break

                                    if response.casefold() == 'n':
                                        while True:
                                            print()
                                            response = input("Would you like to disable this "
                                                "check? [Y/n]: ")
                                            if response.casefold() == 'y' or response == "":
                                                serverinfo.enablecheck = False
                                                serverinfo.update_db()
                                                break

                                            if response.casefold() == 'n':
                                                break


                                            print()
                                            print("That was an invalid selection, try again.")
                                            print()

                                        break

                                    print()
                                    print("Invalid response. Enter (y)es or (n)o.")

                                else:
                                    print()
                                    print("I was able to connect. Current version is "
                                        f"{serverrecheck.version}")
                                    serverrecheck.update_db()
                                    print()
                                    loop = False
                                    break
                            elif response.casefold() == "n":
                                print()
                                break
                        if loop:
                            continue
                        break
                elif str(response) == '4' or str(response.casefold()) == 'c':
                    sys.exit()
                else:
                    print()
                    print("Input invalid. Please enter 1-4 or (c)ancel.")
                    print()
                    continue
    else:
        print()
        print("Server check disabled, skipping...")
        print()

    configobj: db_obj.ConfigObj = db_obj.ConfigObj()
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
        distro_choice = input(f"Choose your distro by number or C to cancel update. "
                              f"Current distro is ({configobj.mainconfig.distro}): [?] ")
        if str(distro_choice) == "1":
            configobj.mainconfig.distro = "Debian X64"
            break
        elif str(distro_choice) == "2":
            configobj.mainconfig.distro = "Debian ARM"
            break
        elif str(distro_choice) == "3":
            configobj.mainconfig.distro = "Arch"
            break
        elif str(distro_choice) == "4":
            configobj.mainconfig.distro = "CentOS"
            break
        elif str(distro_choice) == "5":
            configobj.mainconfig.distro = "Fedora X64"
            break
        elif str(distro_choice) == "6":
            configobj.mainconfig.distro = "Fedora ARM"
            break
        elif str(distro_choice) == "7":
            configobj.mainconfig.distro = "OpenSUSE X64"
            break
        elif str(distro_choice) == "8":
            configobj.mainconfig.distro = "OpenSUSE ARM"
            break
        elif str(distro_choice.casefold()) == "c":
            print("")
            print("Exiting config update and installer....")
            print("")
            sys.exit()
        else:
            print("")
            print("Invalid Choice! Valid choices are 1-8 or C to cancel. Please Try again.")
            print("")

    print("")
    print(configobj.mainconfig.distro + " Chosen")
    print("")

    # Now user chooses beta or Stable releases

    while True:
        choose_beta = input("Do you want to install the beta version of Emby Server? "
                            f"Current release setting is ({configobj.mainconfig.releasetype}): "
                            "[y/N] ")
        if choose_beta.casefold() == "y":
            configobj.mainconfig.releasetype = "Beta"
            break

        if choose_beta in ("n", "N", ""):
            configobj.mainconfig.releasetype = "Stable"
            break

        print("")
        print("Invalid choice. Please choose y or n")
        print("")

    print("")
    print(configobj.mainconfig.releasetype + " version of Emby has been chosen for install.")
    print("")

    # User chooses if they wish to stop the server before installing updates. Not normally needed.

    while True:
        servstop = input("Do we need to manually stop the server to install? *RARELY NEEDED* "
                         f"Current setting is ({configobj.mainconfig.stopserver}): [y/N] ")
        if servstop.casefold() == "y":
            servstopchoice = "Server will be manually stopped on install."
            configobj.mainconfig.stopserver = True
            break

        if servstop in ("n", "N", ""):
            servstopchoice = "Server will NOT be manually stopped on install."
            configobj.mainconfig.stopserver = False
            break

        print("")
        print("Invalid choice. Please choose y or n")
        print("")

    print("")
    print(servstopchoice)
    print("")

    # User chooses if they wish to start the server again after updates. Not normally needed.
    while True:
        servstart = input("Do we need to manually start the server after install? *RARELY NEEDED* "
                f"Current setting is ({configobj.mainconfig.startserver}): [y/N] ")
        if servstart.casefold() == "y":
            server_start_choice = "Server will be manually started after install."
            configobj.mainconfig.startserver = True
            break

        if servstart in ("n", "N", ""):
            server_start_choice = "Server will NOT be manually started after install."
            configobj.mainconfig.startserver = False
            break

        print("")
        print("Invalid choice. Please choose y or n")
        print("")

    print("")
    print(server_start_choice)
    print("")

    # User chooses if they wish to autoupdate the Update app (this program)
    while True:
        script_update = input("Keep EmbyUpdate (this script) up to date with latest version? "
            f"Current setting is ({configobj.selfupdate.runupdate}): [Y/n] ")

        if script_update in ("y", "Y", ""):
            script_update_choice = "Script (EmbyUpdate) will be automatically updated!"
            configobj.selfupdate.runupdate = True
            break

        if script_update.casefold() == "n":
            script_update_choice = "Script (EmbyUpdate) will NOT be automatically updated!"
            configobj.selfupdate.runupdate = False
            break

        print("")
        print("Invalid choice. Please choose y or n")
        print("")

    print("")
    print(script_update_choice)
    print("")

    # User chooses if they want to update to beta or stable for the script
    while True:

        script_beta_choice = input("Install EmbyUpdate Beta versions (this script)? "
            f"Current release setting is {configobj.selfupdate.releasetype}: [y/N] ")

        if script_beta_choice.casefold() == "y":
            self_beta_choice = "Script (EmbyUpdate) will be automatically updated to Beta!"
            configobj.selfupdate.releasetype = "Beta"
            break

        if script_beta_choice in ("n", "N", ""):
            self_beta_choice = "Script (EmbyUpdate) will NOT be automatically updated to Stable!"
            configobj.selfupdate.releasetype = "Stable"
            break

        print("")
        print("Invalid choice. Please choose (y)es or (n)o")
        print("")

    print("")
    print(self_beta_choice)
    print("")

    print("Choices to write to config file...")
    print(f"Linux distro version to update: {configobj.mainconfig.distro}")
    print(f"The chosen Emby Server release version is: {configobj.mainconfig.releasetype}")
    print(f"Server set to be manually stopped: {configobj.mainconfig.stopserver}")
    print(f"Server set to be manually started: {configobj.mainconfig.startserver}")
    print(f"EmbyUpdate app set to autoupdate: {configobj.selfupdate.runupdate}")
    print(f"EmbyUpdate app set to update to release: {configobj.selfupdate.releasetype}")
    print("")

    while True:
        confirm = input("Please review above choices and type CONFIRM to continue or c to "
            "cancel the application! [CONFIRM/c] ")
        if confirm.casefold() == "c":
            print("")
            print("Exiting config update and installer. No changes were made and nothing "
                "will be installed!")
            print("")
            sys.exit()
        elif confirm == "CONFIRM":
            # Now we write the config to the database
            try:
                configobj.mainconfig.update_db()
                configobj.selfupdate.update_db()
                serverinfo.update_db()
                print("")
                print("Config written to database, install continuing!")
                print("")
                break
            except Error:
                exceptrace.execpt_trace("*** EmbyUpdate: Couldn't update the database. ***",
                    sys.exc_info())
                print()
                print("EmbyUpdate: Cannot continue, exiting.")
                sys.exit()

        print("")
        print("Invalid choice. Please type CONFIRM to continue or (c)ancel!!")
        print("")
           