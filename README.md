# EmbyUpdate
A python script for automatically updating Emby Server to the latest version on Linux distros.

# Version 4.1+ is a whole new animal. 
* Requires Python 3.6+ (must install dataclasses to use on 3.6 however)
* Converted from a config.ini file to SQLite DB as a config manager
* I've Tested the updates from the old system installs, to the new, 9 ways from Sunday. If I break your install, sorry. Best to just install 4.11+ manually and set it all up again if you're broken after the update. I really tried to test everything the best I could
* Now talks to the server if it's running to get what version it's on
* Will update and rerun itself to run with new changes instantly
* Lot's more... oh so much more. Too much to list.

# How to install

1. Backup your server before doing anything!! Install the Emby backup/restore plugin and get a good backup!
2. It's possible to loose your settings if you are switching from a repo version to the standalone version this script installs. So make sure you have that backup!
3. If switching from repo version make sure you uninstall the repo version first (apt remove emby-server or your disto's process) or your next distro repo upgrade could switch you back to repo version. MAKE SURE YOU HAVE A BACKUP!!
4. Must use sudo to run the script as it calls system commands to install Emby Server. You can't manually install Emby without root privlages, and my app can't either
5. Best install path: Go to releases and find the most recent Stable version (will be the top one that says Stable). Download the desired archive file under sources. Unzip somewhere handy.
      - Alt install path: Clone or download the master branch. I don't suggest this as I sometimes am working on things in master and can't promise 100% stablility. I'll try my best tho.
7. Once installed run the embyupdate.py file ```sudo ./embyupdate.py``` or ```sudo python3 embyupdate.py``` or the like. However you have your system setup.
8. The app guides you throught the rest, step by step.

More info on installing in the wiki here: [Install Instructions](https://github.com/doonze/EmbyUpdate/wiki/Initial-install-and-setup)
  
# Prerequisites 

For Debian and it's derivatives all you need is:
```
python3
```

for Python you'll need to get:

```
requests
```
(install through pip or apt. Google is your best friend if you need to know specifics for your system)

### Getting Started

The configuration wizard is pretty self-explanatory. But if you want a more indepth guide you can see it here: [Configuration Manager](https://github.com/doonze/EmbyUpdate/wiki/Configuration-Manager)

### Update automation

You can run the script at any time manually to update Emby Server. What you didn't come here to manually have to update like you do now. You want an automated solution! See [Deployment](#deployment) below for more info on that.

### Supported Linux Distros
```
Debian
Ubuntu
Mint
CentOS
Fedora
Arch Linux
OpenSuse
```
(Or anything based on them. If you want to modify the code it should work on any distro). If you are running a distro you don't see here, let me know. Raise an issue. I'll get it added if you'll help me to test it.

### Script Logic Flow

First run:
1. Script will test to see if the database exist. If it doesn't it will create it, check to see it it can talk to a running server to pull the current version number, and then launch the configuration wizard. 
2. After the wizard is finished, it goes into it's normal update mode. It will try to pull the current version from Emby server itself. If you don't have a server installed yet, if the server is down, or you've changed the ports, it will simply install the latest version. If you already have Emby installed, on all tested distro's it will simply get a message "Emby is already on that version" and do nothing. On future runs it now knows what version is installed (cause it tried to install it), so it won't do that again. 

Normal runs:
1. App checks for any updates to itself (if that option was selected). If it finds an update it will download it, install it, and restart the app with the new code.
2. It will then try to reach the server to get it's version number. If it cannot reach the server, it will fall back on its install history to guess what version you're on. It will assume the last version it installed.
3. It will then poll the Emby GitHub page and find the most recent release. If that release doesn't match the installed version. It will download the new version.
4. The script will start the upgrade now, first checking to see if your settings ask it to stop the server. As written this will only work on systemd systems, but the commands can be changed in the code as needed. This is not required in most cases as the install package normally stops/starts the server when it's being updated anyway. But it's in the script if needed. It still there for fringe cases.
5. It will then install the latest version.
6. Lastly, if everything has gone ok with no errors, it updates the database with what it did, and what versions it installed.


## Deployment

See [Deployment](https://github.com/doonze/EmbyUpdate/wiki/Deployment)

## Authors

* Justin Hopper - **Creator**
