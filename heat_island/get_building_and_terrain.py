"""
this module acquire terrain data based on study boundary (geojson),
and get trimmed tif file from USGS 3D Elevation Program (3DEP), with the resolution of 1/3 Arc Second
for the Seattle, the link is https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/historical/n48w123/USGS_13_n48w123_20230608.tif
"""
import os
import tempfile

import fiona
import geopandas as gpd
import mercantile
import pandas as pd
import rasterio
import requests
import shapely
import shapely.geometry
from shapely.geometry import Polygon

from heat_island import data_process
from tqdm import tqdm


def get_buffered_bounding_box_of_boundary(input_boundary_name):
    """

    Args:
        input_boundary_name: file name of study area boundary (i.e., 'seattle-city-limits.geojson')

    Returns:
        a rectangle geometry of buffered bounding box of input boundary, with buffer of 0.008 degree
    """
    input_boundary_path = data_process.input_file_from_data_dir(input_boundary_name)
    input_boundary = gpd.read_file(input_boundary_path)
    output_aoi_path = data_process.input_file_from_data_dir("aoi.geojson")

    buffered_boundary = input_boundary["geometry"].buffer(0.008)
    bound_box = buffered_boundary.total_bounds

    coordinates_bound_box = [
        (bound_box[0], bound_box[3]),
        (bound_box[0], bound_box[1]),
        (bound_box[2], bound_box[1]),
        (bound_box[2], bound_box[3]),
    ]
    aoi_geom = {
        "coordinates": [coordinates_bound_box],
        "type": "Polygon",
    }
    aoi_shape = shapely.geometry.shape(aoi_geom)
    aoi_polygon = Polygon(coordinates_bound_box)
    aoi_gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[aoi_polygon])

    # Save the GeoDataFrame as a GeoJSON file
    aoi_gdf.to_file(output_aoi_path, driver="GeoJSON")
    return aoi_shape


def get_building_tile_id(aoi_shape):
    """

    Args:
        aoi_shape: geometry getting from get_buffered_bounding_box_of_boundary

    Returns:
        quad_keys: building tile id(s)
    """
    minx, miny, maxx, maxy = aoi_shape.bounds
    quad_keys = set()
    for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
        quad_keys.add(int(mercantile.quadkey(tile)))
    quad_keys = list(quad_keys)
    print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")
    return quad_keys


def download_building_geometry(quad_keys, aoi_shape, output_building_name):
    """
    Args:
        quad_keys: building tile id get from get_building_tile_id
        aoi_shape: geometry getting from get_buffered_bounding_box_of_boundary
        output_building_name: name of output file (i.e., 'building')
    Returns:
    """
    output_building_path = data_process.input_file_from_data_dir(output_building_name)
    db = pd.read_csv(
        "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
    )
    idx = 0
    combined_rows = []
    # new a temporary dir tmpdir
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download the GeoJSON files for each tile that intersects the input geometry
        tmp_fns = []
        for quad_key in tqdm(quad_keys):
            # find the row with matching quad_key
            rows = db[db["QuadKey"] == quad_key]
            # if do find a row, get the url, read as josn, comvert to geodataframe
            if rows.shape[0] == 1:
                url = rows.iloc[0]["Url"]

                df2 = pd.read_json(url, lines=True)
                df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)

                gdf = gpd.GeoDataFrame(df2, crs=4326)
                gdf["height"] = gdf["properties"].apply(lambda x: x.get("height"))
                gdf = gdf.drop(columns=["properties"])
                # create a file path for new new gdf with quad_key as filename, append to file list tmp_fns
                fn = os.path.join(tmpdir, f"{quad_key}.geojson")
                tmp_fns.append(fn)
                if not os.path.exists(fn):
                    gdf.to_file(fn, driver="GeoJSON")
            elif rows.shape[0] > 1:
                raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
            else:
                raise ValueError(f"QuadKey not found in dataset: {quad_key}")

        # Merge the GeoJSON files into a single file
        for fn in tmp_fns:
            with fiona.open(fn, "r") as f:
                # read every row in a GeoJSON file
                for row in tqdm(f):
                    row = dict(row)
                    shape = shapely.geometry.shape(row["geometry"])
                    # select shape that is contained in area of interest
                    if aoi_shape.contains(shape):
                        properties = row["properties"]
                        # Remove the original 'id' if present
                        if "id" in properties:
                            del properties["id"]

                        # Extract the height value from properties, assuming it's already a direct value and not a dict
                        height = properties.get(
                            "height"
                        )  # This assumes that 'height' is directly stored in properties

                        # Create a new properties dictionary with only 'id' and 'height'
                        new_properties = {"id": idx, "height": height}

                        idx += 1

                        # Update the row with the new properties
                        row["properties"] = new_properties

                        # Append the updated row to the combined_rows list
                        combined_rows.append(row)

    # update schema to include 'height'
    schema = {"geometry": "Polygon", "properties": {"id": "int", "height": "float"}}

    # write the updated schema to file
    with fiona.open(
            output_building_path, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema
    ) as f:
        for row in combined_rows:
            properties = row["properties"]
            new_properties = {
                "id": properties["id"],
                "height": properties.get("height"),
            }

            # check if 'height' is None
            if new_properties["height"] is None:
                continue

            # new a dict for row with updated schema
            new_row = {
                "type": "Feature",
                "geometry": shapely.geometry.mapping(
                    shapely.geometry.shape(row["geometry"])
                ),
                "properties": new_properties,
            }

            # write to new row
            f.write(new_row)

    print("You have just successfully downloaded building geometry with height!")
    return output_building_name


def get_building_statics(output_building_name):
    output_building_path = data_process.input_file_from_data_dir(output_building_name)
    building = gpd.read_file(output_building_path)
    print("building dataset has shape:" + str(building.shape))
    print("building dataset's columns:" + str(building.columns))
    print(building.describe())


def get_terrain(
        output_complete_terrain_name,
        output_trimmed_terrain_name,
        url="https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/historical/n48w123/USGS_13_n48w123_20230608.tif",
):
    """
    Args:
        output_complete_terrain_name (i.e., 'complete_terrain.tif')
        output_trimmed_terrain_name (i.e., 'trimmed_terrain.tif')
        url: default is set to Seattle area
    Returns:
    """

    # saved path
    complete_geotiff_path = data_process.input_file_from_data_dir(
        output_complete_terrain_name
    )
    trimmed_geotiff_path = data_process.input_file_from_data_dir(
        output_trimmed_terrain_name
    )
    output_aoi_path = data_process.input_file_from_data_dir("aoi.geojson")
    aoi_gdf = gpd.read_file(output_aoi_path)

    # Download the GeoTIFF file
    response = requests.get(url)

    # Save the downloaded file to a local path
    with open(complete_geotiff_path, "wb") as f:
        f.write(response.content)

    from rasterio.mask import mask

    # Ensure the GeoDataFrame is in the same CRS as the GeoTIFF
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

    # Save the cropped image
    with rasterio.open(trimmed_geotiff_path, "w", **out_meta) as dest:
        dest.write(out_image)

    return output_trimmed_terrain_name
