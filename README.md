# EmbyUpdate
A python script for automatically updating Emby Server to the latest version on Linux distros.

This script has been tested on python 2.7 and 3+. It was tested and developed on Debian 9. I haven't tested it on any other distro but it should work fine on Ubuntu and Mint for sure, or any other Debian based distro. It has also been coded to working with several other distor's listed below.

### Prerequisites 

For Debian and it's derivatives all you need is:
```
wget
```

### Getting Started

Usage is: 
```
sudo python embyupdate.py 
```
or
```
sudo python3 embyupdate.py
```
or if you have made it executable (see Deployment below)
```
sudo ./embyupdate.py
```
Needs sudo to be able to install packages and Stop/Start the server if needed

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

** For any Distro but Debian/Ubuntu/Mint you have to chage the distro varable as it set to Debian flavors by default **

### Script Logic Flow

1. Script will pull the latest production version from Emby's github page. If it encouters any errors pulling from the page it will exit      the script letting you know it failed and will try to tell you why.

2. Once it has pulled the latest version number it will test to see if the version.txt file exist already. 
  
 * If it doesn't exist it will create a blank version.txt file. Script will notify you and exit if it can't create the file or              encounters any other errors. Due to the file being blank, it will always try and update the server to the latest version the first      time the script is run. On Debian derived distro's it will download the latest deb, but if the latest version is already the            current version it won't do anything and will exit. It will however update the version.txt file with the version it just installed.      Every other future run should be normal.
  
 * If version.txt exist, it will compare the version download from github with the most recent installed version in version.txt. If        they match the script will let you know and exit. If they don't match the script will move on to installing the latest version.
  
3. The script will start the upgrade now, first checking to see if your Distro settings (or manual settings) ask it to stop the server.    As written this will only work on systemd systems, but the commands can be changed as needed. This is not required in most cases as      the install packages normally stops/starts the server when it's being updated anyway. But it's in the script if needed.

4. For Debian based distros the script will download the newest deb file from Emby github. It will then run dpkg on the downloaded file    installing it as long as the version it's trying to install isn't also the current version. Dpkg stops and starts the server for you.    It will then delete the deb file to keep things nice and clean.
    
   All other distros I believe do the three above steps from one command (yum, zypper, pacman, dnf) I have taken that into account in
   the script and as long as you've uncomments out the correct commands for your distro you should be fine. (untested)
   
5. Lastly, if everything has gone ok with no errors, the script will write the newly installed version number into version.txt


## Deployment

Download, copy, git, svn, or use any other way you know to get the script on your box. I created a directory just for this script. It will download the deb's and create the version.txt file into whatever directory you have it in.

Make the job executable by running this command on the script
```
sudo chmod u+x embyupdate.py
```
Then you can run the script with a simple
```
sudo ./embyupdate.py
```
Or if you placed it in your $PATH
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
