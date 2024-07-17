#post_PIV_processing.py

"""This file contains the tools needed to deal with the PIV data after it has been created in PIVlab"""

#import neccesary packages and modules
import os
import numpy as np
from tqdm import tqdm
from file_managers import FileManagers
from PIV_processing_tools import PIVProcessingTools

#instantiate classes
fm = FileManagers()
ppt = PIVProcessingTools()

#load directory containing PIV files thid will also be where output files are stored. 
directory = fm.load_dn("Select a PIV directory")

##coordinate of the top right of your area of interest in real world coorinates (mm) 
#(this will be the coordinate of the top right corner of the top right pixel in the image used for PIV)
top_right_AOI = [0, 2000]

#create list of filenames within the directory for all .txt files.
text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

#load the metadata for the PIV (information about the pixel size, number of pixels and total dimensions of the input data) from the first file in the directory
metadata = ppt.load_metadata(directory + "/" + text_files[0])

#create empty 3d array for the u velocities and the velocities
u_array_3d = np.empty((metadata[3], metadata[2], 0))
v_array_3d = np.empty((metadata[3], metadata[2], 0))

for i, file in enumerate(tqdm(text_files, desc="Processing files")):

    filename = directory + "/" + text_files[i]

    #create 2d numpy arrays containing the u veocity and the v velocity data
    u_array_2d, v_array_2d = ppt.load_txt_to_numpy(filename, metadata[2], metadata[3])

    # First, expand the 2D array to have a new axis (axis=2)
    u_expanded_array = np.expand_dims(u_array_2d, axis=2)
    v_expanded_array = np.expand_dims(v_array_2d, axis=2)

    # Append the expanded array along the 3rd dimension of the 3D array
    u_array_3d = np.concatenate((u_array_3d, u_expanded_array), axis=2)
    v_array_3d = np.concatenate((v_array_3d, v_expanded_array), axis=2)


#now that we have u_array and v_array for each file, lets find the average across the 3rd dimension (across frames)
u_mean = np.nanmean(u_array_3d, axis=2)
v_mean = np.nanmean(v_array_3d, axis=2) * (-1) #multiply by -1 to get the axes going in the correct direction (positive y towards the top of the screen)

# Compute the net magnitude of the velocity
magnitude = np.sqrt(u_mean**2 + v_mean**2)

#create a 3d array with all of the outputs we are interested in: u_mean, v_mean, and magnitude
final_array_3d = np.stack((u_mean, v_mean, magnitude), axis=2)

#export the mean magnitude as a geotiff for viewing and future analysis
ppt.export_PIV_as_geotiff(magnitude, 32615, directory, top_right_AOI, metadata)

#export the mean u, mean v, and mean magnitude as a grid of points in a shapefile for viewing and future analysis
ppt.export_PIV_as_shp(final_array_3d, 32615, directory, top_right_AOI, metadata)
