#transfer_gopro_files.py

"""This script is used to transfer an entire directory with all subdirectories in tact"""

#import neccesary packages and modules
from file_managers import FileManagers

#instantiate file managers
fm = FileManagers()

#select directory to transfer
source = fm.load_dn("select directory to transfer")

#select destination directory
destination = fm.load_dn("select destination directory")

#now transfer!
fm.transfer_directory(source, destination)
