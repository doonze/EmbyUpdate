import subprocess
import time
import db.dbobjects as db

def update_emby(configobj: db.ConfigObj):
    
    try:
        distroconfig: db.DistroConfig = db.DistroConfig()
        distroconfig.pull_from_db(configobj.mainconfig.distro)
        # This will stop the server on a systemd distro if it's been set to true above
        if configobj.mainconfig.stopserver:
            print("Stopping Emby server.....")
            stopreturn = subprocess.call("systemctl stop emby-server", shell=True)
            time.sleep(3)
            if stopreturn > 0:
                print("Server Stop failed! Non-critical error! Investigate if needed.")

            print("Emby Server Stopped...")

        # Here we download the package to install if used
        if "notused" not in downloadurl:
            print("Starting Package download...")
            download = requests.get(downloadurl)
            with open(updatefile, 'wb') as file:
                file.write(download.content)
            print("Package downloaded!")

        # Next we install it if used
        if "notused" not in installfile:
            print("Installing/Updating Emby server....")
            installreturn = subprocess.call(installfile, shell=True)
            if installreturn > 0:
                print("Install/Update failed! Exiting!")
                sys.exit()
            print("Install/Update Finished!")

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        if "notused" not in updatefile:
            print("Removing install file...")
            subprocess.call("rm -f " + updatefile, shell=True)
            print("File removed!")

        # This will restart the server if using systemd if set to True above
        if configobj.mainconfig.stopserver:
            print("Restarting Emby server after update...")
            startreturn = subprocess.call("systemctl start emby-server", shell=True)
            if startreturn > 0:
                print("Server start failed. Non-critical to update but server may not be running. Investigate.")
            print("Server restarted!")

        # Lastly we write the newly installed version into the config file
        try:
            config.emby_version = onlinefileversion

            config.write_config()

            print(timestamp() + "EmbyUpdate: Updating to Emby version " + onlinefileversion +
                  " finished! Script exiting!")
            print('')
            print("*****************************************************************************")
            print("\n")

        except Exception as e:
            print(timestamp() + "EmbyUpdate: We had a problem writing to config after update!")
            print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
            sys.exit()

    except Exception as e:
        print(timestamp() + 'EmbyUpdate: Something failed in update. No update done, script exiting')
        print(timestamp() + "EmbyUpdate: Here's the error we got -- " + str(e))
