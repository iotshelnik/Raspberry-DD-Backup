# Raspberry-DD-Backup #
Create a backup using the DD command. Scripts to make life easier.

___
# How to: #
## Server side ##
_The original "pishrink.sh" script is at [github](https://github.com/Drewsif/PiShrink) page._

### Installation ###

```bash
wget https://raw.githubusercontent.com/iotshelnik/Raspberry-DD-Backup/main/pishrink.sh
chmod +x pishrink.sh
sudo mv pishrink.sh /usr/local/bin
```

### Usage ###

You may read about usage at original "pishrink.sh" script page:
[ Drewsif / PiShrink ](https://github.com/Drewsif/PiShrink#pishrink).

Note: Script is modified to delete some additional directories and to compress image after shrinking with gzip (it is `-p` and `-z` keys) as the default option. Even if you are not using these keys in command.

## Raspberry Pi side:
___
_Check that Python3 version is 3.6 ot highter._

_Check that NFS server IP is accessible._
___
### Usage ###

```bash
wget https://raw.githubusercontent.com/iotshelnik/Raspberry-DD-Backup/main/RPi-Backup.py
sudo python3 RPi-Backup.py --nfs '172.28.10.100:/share-dir'
```
Follow on-screen instructions.

After Image is created unmount NFS share:
```bash
sudo umount /Backups
```

___

## Example for RPi-Backup.py script ##
```
pi@raspberry:~ $ sudo python3 RPi-Backup_v0.1.py --nfs '172.28.10.100:/share-dir'
The NFS share to mount is: 172.28.10.100:/share-dir 
The hostname is: raspberry
Check|Create the directory for backup: 
 /Backups/raspberry/
The date is: 05032022-11-39
The '/boot' directory is stored at: /dev/mmcblk0p1 subdrive.


The block devices presented in this system are:

NAME      FSTYPE  SIZE TYPE MOUNTPOINT
mmcblk0            29G disk 
mmcblk0p1 vfat    256M part /boot
mmcblk0p2 ext4   28.8G part /

Select with device is boot drive with OS?
[ 1 - /dev/mmcblk0 | 2 - /dev/sda ] : 1
The "/dev/mmcblk0" will be as a source to copy from!

Sectors count: 60868608
Physical block size: 512
Run the command below to create the backup image from SD card with OS to the NFS storage:

sudo dd if=/dev/mmcblk0 of=/Backups/raspberry/raspberry_05032022-11-39.img bs=4096 count=7608576 status=progress conv=fsync
Or use command below, but ansure that the "pv" is installed !
sudo dd if=/dev/mmcblk0 bs=4096 count=7608576 | pv | sudo dd of=/Backups/raspberry/raspberry_05032022-11-39.img

To run in backgroud use next command:
sudo dd if=/dev/mmcblk0 of=/Backups/raspberry/raspberry_05032022-11-39.img bs=4096 count=7608576 &
```