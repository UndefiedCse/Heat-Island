import rasterio
from rasterio.warp import calculate_default_transform,reproject,Resampling
import numpy as np
import pandas as pd

# Path to .tif files
input_path = 'demo/data/dsm/NT27SW_50CM_DSM_PHASE5.tif'

# Output to the same folder with same name but different format
output_path = input_path[:-3]+'csv'

# Choose resampling type 
# ['Nearest-neighbor':nearest, 'Bilinear':bilinear, 'Cubic':cubic]
sampling = Resampling.cubic

with rasterio.open(input_path) as src:
    # Read metadata
    transform = src.transform
    crs = src.crs
    left,bot,right,top = src.bounds
    # Calculate the transformation to 'epsg:4326'
    dst_transform, width, height = calculate_default_transform(
        crs, 'epsg:4326', src.width, src.height, left=left,bottom=bot,right=right,top=top
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
    lat_flat = lat.flatten()
    lon_flat = lon.flatten()

    df = pd.DataFrame({
        'lat': lat_flat,
        'lon': lon_flat
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
            src_crs=crs,
            dst_transform=dst_transform,
            dst_crs='epsg:4326',
            resampling=sampling
        )

        df[f'band_{band_id}'] = dst_array.flatten()
    
    df.to_csv(output_path,index=False)