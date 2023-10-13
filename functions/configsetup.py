"""
Config setup module

"""
import sys
from os.path import exists
from sqlite3 import Error
from db import createdb, dbobjects
from functions import api, exceptrace, colors

c = colors.Terminalcolors()


def config_setup(version):
    """
    The config_setup function will gather user input and write it to the database.
    This function will also be used to read from the database when needed.

    Args:
        version: Current version of EmbyUpdate

    """
    # We'll check if the DB exist or not
    if not exists('./db/embyupdate.db'):
        print()
        print(f"Database does {c.fg.red}NOT{c.end} exist, creating database...")
        createdb.create_db(version)
        print()
    # Now we'll start gathering user input

    # First to check if Emby is running, so we can get the version
    serverinfo: dbobjects.ServerInfo = api.get_running_version()

    # If the option to check server is True, and the sever is not reachable, we'll run the server
    # setup
    if serverinfo.enablecheck:
        if serverinfo.version == "None":
            print()
            print("I didn't find a running Emby instance on this server.")
            print(f"I tried the address {c.fg.cyan}{serverinfo.fullurl}{c.end}")
            print("If this is correct, make sure the server is running. If you")
            print("haven't installed Emby yet, select [1] to skip this for now")
            print("at the prompt below. Emby will install after config setup.")
            print()
            print("* This is not required, however the script will try to update   *")
            print("* Emby to the latest version as we cannot contact the server   *")
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

                response = input(
                    "Make your choice by number, or use 4 or C to cancel update [?]: ")
                print()

                if str(response) == "1":
                    print("Skipping server check and continuing config setup...")
                    print()
                    break

                if str(response) == "2":
                    serverinfo.enablecheck = False
                    serverinfo.update_db()
                    print()
                    print("Server check has been permanently disabled.")
                    print()
                    break

                if str(response) == "3":
                    while True:
                        while loop:
                            print(f"{c.fg.green}*** Just hitting enter will retain current "
                                  f"values. ***{c.end}")
                            print()
                            response = input("Do you use a port to access your server? "
                                             f"Current value is ({c.fg.cyan}{serverinfo.portused}"
                                             f"{c.end}) [y/n]: ")
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
                            response = input("Do you use SSL/TLS to access your server? "
                                             f"[{c.fg.green}Example: HTTPS://{c.end}] Current value is "
                                             f"({c.fg.cyan}{serverinfo.scheme}{c.end}) [y/n]: ")

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
                                            print(
                                                "That was an invalid selection, try again.")
                                            print()

                                        break

                                    print()
                                    print(
                                        "Invalid response. Enter (y)es or (n)o.")

                                else:
                                    print()
                                    print(f"I was able to connect. Server Name: {c.fg.lt_cyan}"
                                          f"{serverrecheck.servername}{c.end} "
                                          f"Version: {c.fg.lt_cyan}{serverrecheck.version}{c.end}")
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

                loop = False  # Fires if 1 or 2 was selected, breaking out of the loop
    else:
        print()
        print("Server check disabled, skipping...")
        print()

    configobj: dbobjects.ConfigObj = dbobjects.ConfigObj().get_config()
    distros = dbobjects.DistroConfig().pull_distros()
    distro_dict = {}
    for i, row in enumerate(distros, start=1):
        distro_dict[str(i)] = row['distro']
        print(f"[{c.fg.pink}{str(i)}{c.end}] {c.fg.lt_blue}{row['distro']}{c.end}")
    print(f"[{c.fg.pink}C{c.end}] {c.bold}{c.fg.lt_blue}Cancel config update{c.end}")
    # Next user will choose their distro
    print(f"{c.bold}{c.fg.lt_green}")
    print("*** Just pressing enter will keep current option ***")
    print(c.end)

    while True:
        distro_choice = input(f"Choose your distro by number or C to cancel update. "
                              f"Current distro is ({c.fg.lt_cyan}{configobj.mainconfig.distro}"
                              f"{c.end}): [?] ")

        if str(distro_choice) in distro_dict.keys():  # pylint: disable=consider-iterating-dictionary
            configobj.mainconfig.distro = distro_dict[distro_choice]
            break

        if str(distro_choice) == "":
            break

        if str(distro_choice.casefold()) == "c":
            print("")
            print("Exiting config update and installer....")
            print("")
            sys.exit()

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose a number "
              f"or C to cancel. Please Try again.")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}Distro: {configobj.mainconfig.distro} chosen{c.end}")
    print("")

    # Now user chooses beta or Stable releases

    while True:
        choose_beta = input("Do you want to install the beta version of Emby Server? "
                            f"Current release setting is ({c.fg.lt_cyan}"
                            f"{configobj.mainconfig.releasetype}{c.end}): [y/n] ")
        if choose_beta.casefold() == "y":
            configobj.mainconfig.releasetype = "Beta"
            break

        if choose_beta in ("n", "N"):
            configobj.mainconfig.releasetype = "Stable"
            break

        if choose_beta == "":
            break

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose y or n")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}{configobj.mainconfig.releasetype} version of Emby has been "
          f"chosen for install{c.end}")
    print("")

    # User chooses if they wish to stop the server before installing updates. Not normally needed.

    while True:
        emby_stop = input(f"Do we need to manually STOP the Emby server to install? "
                          f"{c.fg.orange}*RARELY NEEDED*{c.end} Current setting is "
                          f"({c.fg.lt_cyan}{configobj.mainconfig.stopserver}{c.end}): [y/N] ")

        if emby_stop.casefold() == "y":
            configobj.mainconfig.stopserver = True
            break

        if emby_stop in ("n", "N"):
            configobj.mainconfig.stopserver = False
            break

        if emby_stop == "":
            break

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose y or n")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}Stopping the server is set to: {c.bold}"
          f"{configobj.mainconfig.stopserver}{c.end}")
    print("")

    # User chooses if they wish to start the server again after updates. Not normally needed.
    while True:
        emby_start = input(f"Do we need to manually START the Emby server to install? "
                           f"{c.fg.orange}*RARELY NEEDED*{c.end} Current setting is "
                           f"({c.fg.lt_cyan}{configobj.mainconfig.stopserver}{c.end}): [y/N] ")
        if emby_start.casefold() == "y":
            configobj.mainconfig.startserver = True
            break

        if emby_start in ("n", "N"):
            configobj.mainconfig.startserver = False
            break

        if emby_start == "":
            break

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose y or n")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}Starting the server is set to: {c.bold}"
          f"{configobj.mainconfig.stopserver}{c.end}")
    print("")

    # User chooses if they wish to autoupdate the Update app (this program)
    while True:
        script_update = input("Keep EmbyUpdate (this script) up to date with latest version? "
                              f"Current setting is ({c.fg.lt_cyan}"
                              f"{configobj.selfupdate.runupdate}{c.end}): [Y/n] ")

        if script_update in ("y", "Y"):
            configobj.selfupdate.runupdate = True
            break

        if script_update.casefold() == "n":
            configobj.selfupdate.runupdate = False
            break

        if script_update == "":
            break

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose y or n")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}Updating of this script has been set to: "
          f"{c.bold}{configobj.selfupdate.runupdate}{c.end}")
    print("")

    # User chooses if they want to update to beta or stable for the script
    while True:

        script_beta_choice = input("Install EmbyUpdate Beta versions (this script)? "
                                   f"Current release setting is {c.fg.lt_cyan}"
                                   f"{configobj.selfupdate.releasetype}{c.end}: [y/N] ")

        if script_beta_choice.casefold() == "y":
            configobj.selfupdate.releasetype = "Beta"
            break

        if script_beta_choice in ("n", "N"):
            configobj.selfupdate.releasetype = "Stable"
            break

        if script_beta_choice == "":
            break

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end} Please choose (y)es or (n)o")
        print("")

    print("")
    print(f"{c.fg.lt_cyan}Release version of this the updater set to: "
          f"{c.bold}{configobj.selfupdate.releasetype}{c.end}")
    print("")

    print("Choices to write to config file...")
    print(
        f"Linux distro version to update: {c.fg.lt_cyan}{configobj.mainconfig.distro}{c.end}")
    print(f"The chosen Emby Server release version is: "
          f"{c.fg.lt_cyan}{configobj.mainconfig.releasetype}{c.end}")
    print(f"Server set to be manually stopped: "
          f"{c.fg.lt_cyan}{configobj.mainconfig.stopserver}{c.end}")
    print(f"Server set to be manually started: "
          f"{c.fg.lt_cyan}{configobj.mainconfig.startserver}{c.end}")
    print(f"EmbyUpdate app set to autoupdate: "
          f"{c.fg.lt_cyan}{configobj.selfupdate.runupdate}{c.end}")
    print(f"EmbyUpdate app set to update to release: "
          f"{c.fg.lt_cyan}{configobj.selfupdate.releasetype}{c.end}")
    print("")

    while True:
        confirm = input(f"Please review above choices and type {c.fg.green}CONFIRM{c.end} "
                        f"to continue or c to cancel the application! "
                        f"[{c.fg.green}CONFIRM{c.end}/c] ")
        if confirm.casefold() == "c":
            print("")
            print("Exiting config update and installer. No changes were made and nothing "
                  "will be installed!")
            print("")
            sys.exit()
        elif confirm == "CONFIRM":
            # Now we write the config to the database
            try:
                configobj.mainconfig.configran = True
                configobj.mainconfig.update_db()
                configobj.selfupdate.update_db()
                serverinfo.update_db()
                print("")
                print("Config written to database!")
                print("")
                break
            except Error:
                exceptrace.execpt_trace("*** EmbyUpdate: Couldn't update the database. ***",
                                        sys.exc_info())
                print()
                print("EmbyUpdate: Cannot continue, exiting.")
                sys.exit()

        print("")
        print(f"{c.bold}{c.fg.red}Invalid Choice!{c.end}. Please type CONFIRM to continue "
              f"or (c)ancel!!")
        print("")
