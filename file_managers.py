#file_managers.py

"""module containing methods for managing files"""

#import necessary packages and modules
import shutil
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import csv
import skvideo.io


class FileManagers:
    """Class contains methods for managing files"""

    def __init__(self):
        print("Initialized File Managers")

    def load_dn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        directory and returns the full path to the directory 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what directory to select"""

        root = tk.Tk()
        root.withdraw()
        directory_name = filedialog.askdirectory(title = purpose)

        return directory_name

    def load_fn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        file and returns the full path to the file 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what file to select"""

        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title = purpose)

        return filename

    def import_gcps(self):
        """module for importing ground control points as lists"""

        gcps_fn = self.load_fn("GCPs file") #load filename/path of the GCPs

        gcps_rw_list = [] #make list for real world coordinates of GCPs
        gcps_image_list = [] #make list for image coordinates of GCPs

        #Read csv file into a list of real world and a list of image gcp coordinates
        with open(gcps_fn, 'r', newline='') as csvfile:
            # Create a CSV reader object
            csv_reader = csv.reader(csvfile)

            # Skip the header row
            next(csv_reader)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Each row is a list where each element represents a column value
                gcps_image_list.append(row[1:3])
                gcps_rw_list.append(row[3:5])

                gcps = [gcps_rw_list, gcps_image_list]

        return gcps

    def load_video_metadata(self, vid_file):
        """This method is to load video metadata"""

        metadata = skvideo.io.ffprobe(vid_file)

        return metadata

    def transfer_directory(self, src, dst):
        """This method is to transfer an entire directory from one location to another while preserving all subfolders"""
        def get_all_files_and_dirs(src):
            all_files_dirs = []
            for root, dirs, files in os.walk(src):
                for file in files:
                    all_files_dirs.append(os.path.join(root, file))
                for directory in dirs:
                    all_files_dirs.append(os.path.join(root, directory))
            return all_files_dirs

        def copy_file(src, dst):
            if os.path.isdir(src):
                os.makedirs(dst, exist_ok=True)
            else:
                shutil.copy2(src, dst)

        try:
            # Get all files and directories in the source directory
            items = get_all_files_and_dirs(src)

            # Create the destination directory if it doesn't exist
            os.makedirs(dst, exist_ok=True)

            # Initialize the progress bar
            with tqdm(total=len(items), unit='item') as pbar:
                for item in items:
                    relative_path = os.path.relpath(item, src)
                    dst_path = os.path.join(dst, relative_path)
                    copy_file(item, dst_path)
                    pbar.update(1)
            
            print(f"Directory '{src}' has been transferred to '{dst}' successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
