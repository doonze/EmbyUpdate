import db.dbobjects as db
from functions import timestamp


def check_for_update(configobj: db.ConfigObj) -> bool:
    """
    The check_for_update function checks the current version of Emby against the latest online
    version.  If there is a new version available, it will return True and print out what the
    current installed and online versions are.  If there is no update available, it will return
    False and print out what the current installed and online versions are.



    Args:
        configobj:db.ConfigObj: Pass the configobj to the function

    Returns:
        True if the online version is newer than the installed

    """

    if configobj.serverinfo.version is None:
        current_version = configobj.mainconfig.version
    else:
        current_version = configobj.serverinfo.version

    if str(configobj.onlineversion) == str(current_version):
        # If the latest online version matches the last installed version then we let you
        # know and exit
        print(f"{timestamp.time_stamp()} EmbyUpdate: We're up to date!  Current and Online "
              f" versions are at {current_version} - {configobj.mainconfig.releasetype}"
              ". Exiting.")
        print('***')
        return False

    # If the online version DOESN'T match the last installed version we let you know what
    # the versions are and start updating
    print(f"{timestamp.time_stamp()} EmbyUpdate: Most recent online version is "
          f"{configobj.onlineversion} - {configobj.mainconfig.releasetype} and current installed "
          f"version is {current_version} - {configobj.mainconfig.releasetype}. "
          "We're updating Emby.")
    print()
    print(f"{timestamp.time_stamp()} EmbyUpdate: Starting update......")
    return True