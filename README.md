# EmbyUpdate
A python script for automatically updating Emby to the latest version on Linux distros.


This script has been tested on python 2.7 and 3+. It was tested and developed on Debian 9. I haven't tested it on any other distro but it should work fine on Ubuntu and Mint for sure, or any other Debian based distro. It has also been coded to working with several other distor's listed below.

Usage is: sudo python embyupdate.py (needs sudo to be able to install packages and Stop/Start the server if needed)

I however suggest running it as a cron job as root

The purpose of this script is to add automatic updating of the Emby server to linux boxes. 

List of distros directly supported, if available both the X64 and ARM versions are present.
Debian
Ubuntu
Mint
CentOS
Fedora
Arch Linux
OpenSuse
(Or anything based on them. If you want to modify the code it should work on any distro)

** For any Distro but Debian/Ubuntu/Mint you have to comment out the default code block, find your distro code block, and uncomment it's settings. **

Here's the scripts logic flow:

1. Script will pull the latest production version from Emby's github page. If it encouters any errors pulling from the page it will exit      the script letting you know it failed and will try to tell you why.

2. Once it has pulled the latest version number it will test to see if the version.txt file exist already. 
  
  a. If it doesn't exist it will create a blank version.txt file. Script will notify you and exit if it can't create the file or              encounters any other errors. Due to the file being blank, it will always try and update the server to the latest version the first      time the script is run. On Debian derived distro's it will download the latest deb, but if the latest version is already the            current version it won't do anything and will exit. It will however update the version.txt file with the version it just installed.      Every other future run should be normal.
  
  b. If version.txt exist, it will compare the version download from github with the most recent installed version in version.txt. If        they match the script will let you know and exit. If they don't match the script will move on to installing the latest version.
  
3. The script will start the upgrade now, first checking to see if your Distro settings (or manual settings) ask it to stop the server.    As written this will only work on systemd systems, but the commands can be changed as needed. This is not required in most cases as      the install packages normally stops/starts the server when it's being updated anyway. But it's in the script if needed.

4. For Debian based distros the script will download the newest deb file from Emby github. It will then run dpkg on the downloaded file    installing it as long as the version it's trying to install isn't also the current version. Dpkg stops and starts the server for you.    It will then delete the deb file to keep things nice and clean.
    
   All other distros I believe do the three above steps from one command (yum, zypper, pacman, dnf) I have taken that into account in
   the script and as long as you've uncomments out the correct commands for your distro you should be fine. (untested)
   
5. Lastly, if everything has gone ok with no errors, the script will write the newly installed version number into version.txt


