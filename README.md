# Raspberry-DD-Backup
Create a backup using the DD command. Scripts to make life easier.

# CMU side:
___
_Check that Python3 version is 3.6 ot highter._

_Check that NFS server IP is accessible._
___
1. Run script "RPi-Backup.py" on the CMU
2. Run one of the command displayed on the screen as the result of the script
3. Wait till command is done
4. Unmount NFS share (or it will be unmounted on next boot)

# Server side:
_Check the script "pishrink.sh" (modified one, **NOT** original from github) is placed at "/usr/local/bin"!_

`chmod +x pishrink.sh`

`sudo mv pishrink.sh /usr/local/bin`
___

1. Run script "pishrink.sh" 

`sudo pishrink.sh /path/to/cmu_image.img`

2. Move shrinked file to directory that configured at your WEB server to give access to download files from.

___
In our case the NFS share is stored on the DELL UNITY Storage. So the "Server" means the some server where you configuren the WEB to download stored backup from mounted NFS share.

___
_Original script "pishrink.sh" is taken at [Drewsif](https://github.com/Drewsif)_