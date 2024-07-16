#PIV_processing_tools.py

"""houses all of the important tools needed to post process piv data"""

#import packages and modules
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from osgeo import gdal,osr

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

        x_dim = x_size * x_num
        y_dim = y_size * y_num

        print("X origin: ", x_origin)
        print("Y origin: ", y_origin)
        print("x_num: ", x_num)
        print("y_num: ", y_num)
        print("x_size: ", x_size)
        print("y_size: ", y_size)
        print("x_dim: ", x_dim)
        print("y_dim: ", y_dim)

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
    
    def export_PIV_as_geotiff(self, out_array, projection_num, directory, geotransform):
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(projection_num)

        datout = np.squeeze(out_array)

        datout[np.isnan(datout)] = -9999
        driver = gdal.GetDriverByName('GTiff')
        cols,rows = np.shape(datout)

        output_filename = directory + "/out_array.tif"

        ds = driver.Create(output_filename, rows, cols, 1, gdal.GDT_Float32, [ 'COMPRESS=LZW' ] )
        if proj is not None:
            ds.SetProjection(proj.ExportToWkt())

        ds.SetGeoTransform(geotransform)
        ss_band = ds.GetRasterBand(1)
        ss_band.WriteArray(datout)
        ss_band.SetNoDataValue(-9999)
        ss_band.FlushCache()
        ss_band.ComputeStatistics(False)
        ss_band.SetUnitType('m')

    def export_PIV_as_shp(self, out_array, metadata, projection_num, directory):

        # Unpack the start coordinates
        x_start = metadata[0] * 1000
        y_start = 2000 - metadata[1] * 1000
        
        # Get the dimensions of the array
        rows, cols, num_attributes = out_array.shape
        
        # Create a list to store the point geometries and their attributes
        points = []

        # Iterate over the array to create points and attributes
        for i in range(rows):
            
            for j in range(cols):
                # Calculate the coordinates of the current point
                x = x_start + j * metadata[4] * 1000
                y = y_start - i * metadata[5] * 1000

                # Create a Point object
                point = Point(x, y)

                # Extract the attributes for the current point
                attributes = out_array[i, j, :]

                # Append the point and attributes to the list
                points.append((point, *attributes))

        # Create a GeoDataFrame from the list of points and attributes
        attribute_names = ["u_mean", "v_mean", "magnitude_mean"]
        columns = ['geometry'] + attribute_names

        gdf = gpd.GeoDataFrame(points, columns=columns)

        # Set the CRS
        gdf.set_crs(epsg=projection_num, inplace=True)

        # Save the GeoDataFrame to a shapefile
        gdf.to_file(directory + "/out_array.shp")
