"""
this module acquire terrain data based on study boundary (geojson),
and get trimmed tif file from USGS 3D Elevation Program (3DEP), with the resolution of 1/3 Arc Second
for Seattle, the link is https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/historical/n48w123/USGS_13_n48w123_20230608.tif
"""

import geopandas as gpd
import rasterio
import requests
from rasterio.mask import mask
from shapely.geometry import Polygon

from heat_island import data_process


def terrain_acquire(input_boundary_name, output_complete_terrain_name,
                    output_trimmed_terrain_name,
                    url="https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/historical/n48w123/USGS_13_n48w123_20230608.tif"):
    """
    Args:
        input_boundary_name: file name of study area boundary (i.e., 'seattle-city-limits.geojson')
        output_complete_terrain_name (i.e., 'complete_terrain.tif')
        output_trimmed_terrain_name (i.e., 'trimmed_terrain.tif')
        url: default is set to Seattle area

    Output:
        a complete terrain from the url provided, as tif file
        and a trimmed terrain with the extended bounding box, as tif file
    """
    # set input boundary path, read file
    input_boundary_path = data_process.input_file_from_data_dir(input_boundary_name)
    input_boundary = gpd.read_file(input_boundary_path)

    # set output saved path
    complete_geotiff_path = data_process.input_file_from_data_dir(output_complete_terrain_name)
    trimmed_geotiff_path = data_process.input_file_from_data_dir(output_trimmed_terrain_name)

    # create extended bounding box of input boundary, as area of interest
    buffered_boundary = input_boundary["geometry"].buffer(0.008)
    bound_box = buffered_boundary.total_bounds
    coordinates_bound_box = [
        (bound_box[0], bound_box[3]),
        (bound_box[0], bound_box[1]),
        (bound_box[2], bound_box[1]),
        (bound_box[2], bound_box[3]),
    ]
    aoi_polygon = Polygon(coordinates_bound_box)
    aoi_gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[aoi_polygon])

    # Download the GeoTIFF file from the url to a local path
    response = requests.get(url)
    with open(complete_geotiff_path, "wb") as f:
        f.write(response.content)

    # trim the original terrain with the area of interest
    with rasterio.open(complete_geotiff_path) as src:
        gdf = aoi_gdf.to_crs(src.crs.data)

        # Perform the crop
        out_image, out_transform = mask(dataset=src, shapes=gdf.geometry, crop=True)
        out_meta = src.meta.copy()
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[3],
                "transform": out_transform,
            }
        )

    # Save the cropped terrain
    with rasterio.open(trimmed_geotiff_path, "w", **out_meta) as o:
        o.write(out_image)

    print("Your terrain is now trimmed and saved as your appointed name")
