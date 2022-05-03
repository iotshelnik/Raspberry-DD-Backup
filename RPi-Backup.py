# This requires Python's modules
import os
import socket
import time
import subprocess
import argparse
from subprocess import PIPE
from subprocess import check_call
from subprocess import check_output

# The print(f'') forman needs the python3.6 minimum version !!!
# So I used print(''.format()) 

# Get incommand argument
parser = argparse.ArgumentParser(description='Script to mount the NFS share and to prepare the command for create backup of the SD card to it.')
parser.add_argument("-nfs","--nfs", help="Prints the export path to NFS share. Like: aa.bb.cc.dd:/share-dir ",required=True, type=str)
args = parser.parse_args()
print(f"The NFS share to mount is: {args.nfs} ")

# Get hostname.
RPiHostname = socket.gethostname()
print ("The hostname is: {}".format(RPiHostname))

# Base path where NFSv4 is mounted
NFSv4Path = "/Backups"
# Check and create if needed the directory with hostname
os.makedirs(NFSv4Path, exist_ok=True)
# Join path test (with "/" at the and!)

# How to mount a network directory using python
check_call( 'mount -t nfs ' + args.nfs + ' ' + NFSv4Path, shell=True )

# Set variable for backup path
BackupPath = os.path.join(NFSv4Path, socket.gethostname(), "")
# Check and create if needed the directory with hostname
print("Check|Create the directory for backup: \n {}".format(BackupPath) )
os.makedirs(BackupPath, exist_ok=True)

# Get current time and date to use in filename
timestr = time.strftime("%m%d%Y-%H-%M")
# Test variable with time and date
print ('The date is: {}'.format(timestr))
# Set Filename variable
BackupFileName = RPiHostname + '_' + timestr + '.img'

# variable for cmd
CMDOutFile = 'of=' + BackupPath + BackupFileName

# Next is need for "dd" command
# determine the boot drive in linux using drive path
df = check_output(['df']).decode()
dflines = df.split('\n')
for line in dflines:
        if '/boot' in line:
                print("The '/boot' directory is stored at: {} subdrive.".format(line.split(' ')[0]))

print('\n')
print('The block devices presented in this system are:\n')
LSBLK = subprocess.run(['lsblk', '-o', 'NAME,FSTYPE,SIZE,TYPE,MOUNTPOINT', '-l'], stdout=subprocess.PIPE, encoding='utf-8').stdout
print(LSBLK)
# create question to select variable entry
question = int( input("Select with device is boot drive with OS?\n[ 1 - /dev/mmcblk0 | 2 - /dev/sda ] : ") )
if question == 1:
    print ('The "/dev/mmcblk0" will be as a source to copy from!\n')
    SourceDevice = 'if=/dev/mmcblk0'
    # Sectors count
    print ( 'Sectors count: ' + str(open('/sys/block/mmcblk0/size','r').read()).strip() )
    SectorsCount = int(open('/sys/block/mmcblk0/size','r').read())
    # Physical block size
    print ( 'Physical block size: ' + str(open('/sys/block/mmcblk0/queue/physical_block_size','r').read()).strip() )
    PhysicalBlockSize = int(open('/sys/block/mmcblk0/queue/physical_block_size','r').read())
elif question == 2:
    print ('The "/dev/sda" will be as a source to copy from!\n')
    SourceDevice = 'if=/dev/sda'
    # Sectors count
    print ( 'Sectors count: ' + str(open('/sys/block/sda/size','r').read()).strip() )
    SectorsCount = int(open('/sys/block/sda/size','r').read())
    # Physical block size
    print ( 'Physical block size: ' + str(open('/sys/block/sda/queue/physical_block_size','r').read()).strip() )
    PhysicalBlockSize = int(open('/sys/block/sda/queue/physical_block_size','r').read())

# To speedup command execution we change the counter and the block size accordingly
SectorsCount = int( SectorsCount / 8 )
PhysicalBlockSize = int( PhysicalBlockSize * 8 )
# Convert to string and concatenate
SectorsCount = ('count=' + str(SectorsCount)).strip()
PhysicalBlockSize = ('bs=' + str(PhysicalBlockSize)).strip()
# Print results
print ('Run the command below to create the backup image from SD card with OS to the NFS storage:\n')
print ("sudo dd {} {} {} {} status=progress conv=fsync".format(SourceDevice,CMDOutFile,PhysicalBlockSize,SectorsCount))
print ('Or use command below, but ansure that the "pv" is installed !')
print ('sudo dd {} {} {} | pv | sudo dd {}'.format(SourceDevice,PhysicalBlockSize,SectorsCount,CMDOutFile))
print ()
print ('To run in backgroud use next command:')
print ("sudo dd {} {} {} {} &".format(SourceDevice,CMDOutFile,PhysicalBlockSize,SectorsCount))

## To clear console
#clear = lambda: os.system('clear')
## Shell cmd for 'dd'
#cmd = ["dd", SourceDevice, CMDOutFile, "bs=512", "status=progress", "conv=fsync"]
#
#process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
#
#line = ''
#while True:
#    out = process.stderr.read(1)
#    if out == '' and process.poll() != None:
#        break
#    if out != '':
#        s = out.decode("utf-8")
#        if s == '\r':
#            clear()
#            print(line)
#            line = ''
#        else:
#            clear()
#            line = line + s
#
## Print
#print ("Jobe is done!")