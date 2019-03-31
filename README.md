# EmbyUpdate
A python script for automatically updating Emby Server to the latest version on Linux distros.

This script has been tested with python 2.7 and 3+. I suggest using python 3, it always tries python 3 commands first. If those fail it falls back to python 2 commands. In the end it doesn't matter, it runs the same on both. However if you run it with 3 there won't be behind the scenes exceptions happening. If you don't have 3, or have mapped 3 to python instead of python3 you may get some chatter from the app. It was tested and developed on Debian 9. I haven't tested it on any other distro but it should work fine on Ubuntu and Mint for sure, or any other Debian based distro. It has also been coded (but not tested) to work with several other distor's listed below.

* Backup your server before doing anything!! Install the Emby backup/restore plugin and get a good backup!
* It's possiable to loose your settings if you are switching from a repo version to the standalone version this script installs. So make sure you have that backup!
* If switching from repo version make sure you uninstall the repo version first (apt remove emby-server or your disto's process) or your next distro repo upgrade could switch you back to repo version. MAKE SURE YOU HAVE A BACKUP!!

### Prerequisites 

For Debian and it's derivatives all you need is:
```
wget
```
and one of these:
```
python
python3 (optional but highly suggested)
```

### Getting Started

You will need to have root/sudo/admin access to your server to use this script. It won't have access to update your server otherwise. But you have to have those access rights to install Emby anyway, so moot point.

Download the release .zip of your choice. Unzip the files into a directory you have full access to. I suggest a directory in your home directory called embyupdate. The very first time you run the script it will tell you that you have to run the config first. You'll have to run the following command and answer a few questions. Hitting enter on all but the first question will setup the defaults.

```
sudo python embyupdate.py --config
```
Here's the config options questions, all are required:

First you choose your distro from the list, or choose c to cancel and not create/update the config file nor install/update Emby.

```
[1] Debian X64
[2] Debian ARM
[3] Arch
[4] CentOS
[5] Fedora X64
[6] Fedora ARM
[7] OpenSUSE X64
[8] OpenSUSE ARM
[C] Cancel config update
Choose your distro by number or C to cancel update [?]:
```

Next question default is no. You can just hit enter if you don't want to install beta versions. Enter y if you DO want to install beta versions.

```
Do you want to install the beta version? [y/N]
```

Just hit enter unless you need to have the server stopped before installing. I don't think any distro needs this, but it's there if needed or you have issues. Default is no.

```
Do we need to manually stop the server to install? (Likely only needed for Arch.) [y/N]
```

Just hit enter here unless you need to have the server started manually after install. Once again I don't think this is needed, but it's there if so, and if you have any issues. Default is no.

```
Do we need to manually start the server after install? (Likely only needed for Arch.) [y/N]
```

Defalut is yes. Unless you have a reason you don't want to keep the script updated, just hit enter. This will only update to Stable releases, beta releases will be ignored. I have no desire to change this behavior as I don't plan on keeping an up to date beta version. Only time I'll release beta's is if I'm doing major changes that need testing.

## It takes two runs for script updates to take effect. It does update the script (this program) during the first run, but as the script is already running during the update the changes are not implimented. The next time the script is called it will be running on the updated code. I have an idea on how to correct this behavior, but the need hasn't justified the complete code overhaul yet.

```
Keep EmbyUpdate (this script) up to date with latest version? [Y/n]
```

The last question will show you all the config options you have selected, and will ask you to type CONFIRM (all caps, just like that) or c to cancel the config creation/update. Typing CONFIRM will move on to installing/updating Emby, cancel will discard all changes and stop the install.

```
Choices to write to config file...
Linux distro version to update: Debian X64
The chosen version for install is: Stable
Server will NOT be manually stopped on install.
Server will NOT be manually started after install.
Script (EmbyUpdate) will be automatically updated!

Please review above choices and type CONFIRM to continue or c to cancel update and install! [CONFIRM/c]
```

You can invoke the config interface at any time with -c or --config, any changes you choose will be updated and the installer ran. After inital creation you'll only have need to rerun it if you want to change something. Otherwise normal usage is listed below.

Usage is: 
```
sudo python embyupdate.py 
```
or
```
sudo python3 embyupdate.py (suggested)
```
or if you have made it executable (see Deployment below)
```
sudo ./embyupdate.py
```

Also, there are a few command line arguments you can use:

```
-c/--config = config creator/updator
-v/--version = display current version
-h/--help = displays help
```

Script sudo/root to be able to install packages and Stop/Start the server if needed. You can of course leave off the sudo if your already root.

### **I however suggest running it as a cron job as root.** 

See deployment section for cron example

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
(Or anything based on them. If you want to modify the code it should work on any distro)

### Script Logic Flow

1. Script will test to see if config file exist. If it doesn't it will notify user they must run the config creator and exit. Once the config has been setup the script will move on to installing the latest Emby version. 

2. Script will pull the latest beta or stable version from Emby's github page depending on which you selected. Once it finds the most recent desired version it will stop searching the API and move on with that version. If it encouters any errors pulling from the page it will exit the script letting you know it failed and will try to tell you why.

3. Once it has pulled the latest version number it will test to see if that is the more recent version installed. 
  
 * The script keeps track of versions after the first install. However it will always try and update the server to the latest version the first time the script is run. This if for both Emby AND the App itself. On Debian derived distro's it will download the latest deb, but if the latest version is already the current version it won't do anything and will exit. It will however update the config file with the most recent version. It will also overwrite the EmbyUpdate app itself with the latest version if updating it was selected in options. Every other future run should be normal.
    
4. The script will start the upgrade now, first checking to see if your settings ask it to stop the server. As written this will only work on systemd systems, but the commands can be changed in the code as needed. This is not required in most cases as the install packages normally stops/starts the server when it's being updated anyway. But it's in the script if needed.

4. For Debian based distros the script will download the newest deb file from Emby github. It will then run dpkg on the downloaded file    installing it as long as the version it's trying to install isn't also the current version. Dpkg stops and starts the server for you.    It will then delete the deb file to keep things nice and clean.
   
   The app itself also checks for a more recent version. If it finds one it downloads the .zip file from my github releases, unzips it      in the current working directory, and then deletes the .zip to keep things nice and tidy. It will also mark the embyupdate.py file as    executable. Not needed, but I can so I did.
    
   All other distros I believe do the three above steps from one command (yum, zypper, pacman, dnf) I have taken that into account in
   the script and as long as you've correctly selected the distro you should be fine. (untested)
   
5. Lastly, if everything has gone ok with no errors, the script will write the newly installed version numbers into the config file.


## Deployment

Download, copy, git, svn, or use any other way you know to get the script on your box. An easy way is to download the source .zip in releases and unzip in in the desired directory (suggested way). I created a directory just for this script. It will download the deb's and create the version.txt file and log into whatever directory you have it in.

ALL FILE MUST REMAIN IN THE SAME DIRECTORY! Everything it does happens in the directory embyupdate.py lives in. If you move anything, delete anything, or rename anything your going to have issues. The script knows what directory it's in and behaves accordingly. You can move it anywhere, but you must move ALL FILES.

Make the job executable by running this command on the script (optional)
```
sudo chmod u+x embyupdate.py 
```
Then you can run the script with a simple (optional)
```
sudo ./embyupdate.py
```
Or if you placed it in your $PATH (really optional! And untested)
```
sudo embyupdate.py
```

As stated above you must either be root or use sudo because the script calls privileged Linux commands. I also highly suggest running the script through cron as root.

Example CRONTAB entry:
```
35 12   * * *    root  /usr/bin/python3 /path/to/embyupdate/embyupdate.py >> /path/to/embyupdate/embyupdate.log 2>&1
```
That runs the script every day at 12:35 and creates a log file in the location of my choice. I use my script location.

However, if your user has sudo access without a password, you could update the commands in the script by apending
```
sudo
```
in front of them. (I mean the systemd commands and the package install command). Then you could run the script as normal from your user.
```
./embyupdate.py
```

## Authors

* Justin Hopper - **Creator**
