"""This module is used to convert geographic data in .tif format to dataframe
User can choose whether to save converted data to .csv format. **Warning: file size can be large**
"""
import os
import rasterio
from rasterio.warp import calculate_default_transform,reproject,Resampling
import numpy as np
import pandas as pd

def tif2df(input_path:str,output_path:str=''
            ,overwrite:bool=False):
    """Function used to convert .tif file to dataframe with option to save as .csv

    Args:
        input_path (str): relative path for input file
        output_path (str, optional): relative path for output file. Defaults to ''.
        overwrite (bool, optional): Whether do you want to overwrite file. Defaults to False.

    Raises:
        ValueError: If input file does not exist
        ValueError: If output file exist and does not allow to overwrite
        ValueError: If request for save file but directory does not exist

    Returns:
        dataframe: dataframe of .tif file (lat,long,band_1,band_2,...)
    """
    # Check whether input file exist
    if not os.path.isfile(input_path):
        raise ValueError("Selected file does not exist")
    # Check for output file so it don't overwrite exist file
    if os.path.isfile(output_path) and overwrite is False:
        raise ValueError("Output file exist! rename outputfile or set overwrite to True")
    if output_path != '' and not os.path.isdir(output_path[:output_path.rfind('/')+1]):
        raise ValueError("Output directory does not exist")
    sampling = Resampling.cubic
    with rasterio.open(input_path) as src:
        # Read metadata
        transform = src.transform
        # Calculate the transformation to 'epsg:4326'
        dst_transform, width, height = calculate_default_transform(
            src.crs, 'epsg:4326', src.width, src.height, left=src.bounds[0]
            ,bottom=src.bounds[1],right=src.bounds[2],top=src.bounds[3]
        )

        # Copy metadata and update
        dst_meta = src.meta.copy()
        dst_meta.update({
            'crs':'epsg:4326',
            'transform': dst_transform,
            'width':width,
            'height':height
        })

        # Generate latitude and longitude grids
        lon,lat = np.meshgrid(
            np.arange(width)*dst_transform[0]+dst_transform[2],
            np.arange(height)*dst_transform[4]+dst_transform[5]
        )
        lat = lat.flatten()
        lon = lon.flatten()

        df = pd.DataFrame({
            'lat': lat,
            'lon': lon
        })
        # loop through all band (mostly 1)
        for band_id in range(1,src.count +1):
        # Create empty array to store transformed data
            dst_array = np.empty((height,width), dtype=src.meta['dtype'])

            # Reproject data to new coordinate system
            reproject(
                rasterio.band(src,band_id),
                dst_array,
                transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs='epsg:4326',
                resampling=sampling
            )

            df[f'band_{band_id}'] = dst_array.flatten()
        if output_path != "":
            if os.path.isfile(output_path):
                os.remove(output_path)
            df.to_csv(output_path,index=False)
        return df
