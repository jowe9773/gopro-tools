#post_PIV_processing.py

"""This file contains the tools needed to deal with the PIV data after it has been created in PIVlab"""

#import neccesary packages and modules
import os
import numpy as np
from file_managers import FileManagers
from PIV_processing_tools import PIVProcessingTools

#instantiate classes
fm = FileManagers()
ppt = PIVProcessingTools()

#load directory containing PIV files
directory = fm.load_dn("Select a PIV directory")

text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
print(text_files)

metadata = ppt.load_metadata(directory + "/" + text_files[0])

x_border_offset = metadata[0] - (metadata[4]/2)
y_border_offset = metadata[1] - (metadata[5]/2)

#geotransorm parameters
geotransform = [
    0 + (x_border_offset*1000),                  # top left x
    metadata[4]*1000,        # w-e pixel resolution
    0.0,                # rotation, 0 if image is "north up"
    2000 - (y_border_offset*1000),               # top left y
    0.0,                # rotation, 0 if image is "north up"
    -metadata[5]*1000        # n-s pixel resolution (negative value for north-up images)
]

#create empty 3d array for the u velocities and the velocities
u_array_3d = np.empty((metadata[2], metadata[3], 0))
v_array_3d = np.empty((metadata[2], metadata[3], 0))

for i in range(len(text_files)):

    filename = directory + "/" + text_files[i]

    u_array_2d, v_array_2d = ppt.load_txt_to_numpy(filename, metadata[2], metadata[3])


    # First, expand the 2D array to have a new axis (axis=2)
    u_expanded_array = np.expand_dims(u_array_2d, axis=2)
    v_expanded_array = np.expand_dims(v_array_2d, axis=2)

    # Append the expanded array along the 3rd dimension of the 3D array
    u_array_3d = np.concatenate((u_array_3d, u_expanded_array), axis=2)
    v_array_3d = np.concatenate((v_array_3d, v_expanded_array), axis=2)

#now that we have u_array and v_array for each file, lets find the average across the 3rd dimension (across frames)
u_mean = np.nanmean(u_array_3d, axis=2)
v_mean = np.nanmean(v_array_3d, axis=2) * (-1) #to get the axes going in the correct direction (positive y towards the top of the screen)

# Compute the magnitude of the velocity
magnitude = np.sqrt(u_mean**2 + v_mean**2)

#create a 3d array with all of the outputs we are interested in: u_mean, v_mean, and magnitude
final_array_3d = np.stack((u_mean, v_mean, magnitude), axis=2)

ppt.export_PIV_as_geotiff(magnitude, 32615, directory, geotransform)

ppt.export_PIV_as_shp(final_array_3d, metadata, 32615, directory)