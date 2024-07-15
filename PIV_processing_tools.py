#PIV_processing_tools.py

"""houses all of the important tools needed to post process piv data"""

#import packages and modules
import pandas as pd
import numpy as np

class PIVProcessingTools():
    """Class containing PIV processing tools"""

    def __init__(self):
        print("initialized")

    def load_metadata(self, filename):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename, skiprows=2)

        #instantiate counter variables
        x_num = None
        rows_before_change = 0
        previous_value = df.iloc[0, 0]

        #cound number of rows before change in x value
        for index, row in df.iterrows():
            current_value = row[df.columns[0]]
            
            # Check if the value in the target column has changed
            if current_value != previous_value:
                break
            
            rows_before_change += 1
            previous_value = current_value

        #initialze counter variables
        y_num = None
        previous_value = None
        change_count = 0

        #count number of changes in x value
        for index, row in df.iterrows():
            current_value = row[df.columns[0]]
            
            # Check if the value in the target column has changed
            if current_value != previous_value:
                change_count += 1
            
            previous_value = current_value

        #HERE ARE THE VARIABLES
        x_origin = df.iloc[0, 0]
        y_origin = df.iloc[0, 1]

        x_num = rows_before_change
        y_num = change_count

        x_size = df.iloc[x_num, 0] - df.iloc[0, 0]
        y_size = df.iloc[1, 1] - df.iloc[0, 1]

        print("X origin: ", x_origin)
        print("Y origin: ", y_origin)
        print("x_num: ", x_num)
        print("y_num: ", y_num)
        print("x_size: ", x_size)
        print("y_size: ", y_size)

        metadata = [x_origin, y_origin, x_num, y_num, x_size, y_size]

        return metadata
    
    def load_txt_to_numpy(self, filename, x_num, y_num):

        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename, skiprows=2)

        #Extract values from the 3rd column (Column3)
        u_values = df.iloc[:, 2].values
        v_values = df.iloc[:, 3].values

        # Reshape the values into a 2D NumPy array
        u_array_2d = u_values.reshape(y_num, x_num)
        u_array_2d = np.transpose(u_array_2d)
        v_array_2d = v_values.reshape(y_num, x_num)
        v_array_2d = np.transpose(v_array_2d)

        return u_array_2d, v_array_2d