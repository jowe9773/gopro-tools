#post_PIV_processing.py

"""This file contains the tools needed to deal with the PIV data after it has been created in PIVlab"""

#import neccesary packages and modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from file_managers import FileManagers
from PIV_processing_tools import PIVProcessingTools

#instantiate classes
fm = FileManagers()
ppt = PIVProcessingTools()


# Replace 'filename.txt' with your file's name
filename = fm.load_fn("Select a PIV file")


metadata = ppt.load_metadata(filename)

u_array_2d, v_array_2d = ppt.load_txt_to_numpy(filename, metadata[2], metadata[3])


"""#save u veloxity to a 2D numpy array
array_3d = np.empty((y_num, x_num, 0))

# First, expand the 2D array to have a new axis (axis=2)
expanded_array = np.expand_dims(array_2d, axis=2)

# Append the expanded array along the 3rd dimension of the 3D array
array_3d = np.concatenate((array_3d, expanded_array), axis=2)"""