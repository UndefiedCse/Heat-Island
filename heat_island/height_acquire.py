"""
The 'height_acquire' module provides a comprehensive suite of functions for 
acquire and processing geographic data, specifically focusing on building 
heights, based on https://github.com/microsoft/GlobalMLBuildingFootprints. 
Key functionalities in the module include acquiring building heights within 
specific areas, calculating geometric centers of shapes, and performing 
weighted statistical analyses on geographical data. 



Key Functions:
- `height_acquire`: Acquires building height data from a specified hexagonal 
    area and returns a GeoDataFrame with these heights.
- `get_centroid`: Computes and adds the centroid of geometries in a GeoDataFrame.
- Statistical helper functions (`weighted_median`, `weighted_percentile`, `weighted_std`): 
    Provide statistical analysis tools for weighted data.
- `average_building_height_with_centroid`: Calculates various statistical 
    measures for building heights within a specified hexagon area.

Example Usage:
To use this module, first create a hexagonal area of interest using `create_hexagon` 
function from `heat_island.geo_process`, and then pass this hexagon to `height_acquire` 
to retrieve building heights within the area.

Author: @LilacHo
Date: 2023/12/13
"""


import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.geometry
import mercantile
from tqdm import tqdm
import os
import tempfile
import fiona

from heat_island.data_process import input_file_from_data_dir
from heat_island.geo_process import create_hexagon




def height_acquire(hexagon):
    """
    Acquires building height data from a specified hexagonal area.

    This function takes a hexagon polygon as input, checks its validity,
    and expands its bounds slightly. It then generates a set of quad 
    keys for tiles within these bounds at a specific zoom level. For 
    each quad key, the function queries a dataset, reads the correspond
    -ing GeoJSON data, and creates a GeoDataFrame that includes building
    heights. It finally concatenates all GeoDataFrames for each quad key
    into one combined GeoDataFrame, which it returns.

    Parameters:
        hexagon (shapely.geometry.polygon.Polygon): 
        A hexagon polygon representing the area of interest (AOI).

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the heights of 
        buildings within the specified hexagon area.

    Raises:
        ValueError: If the input is not a valid shapely polygon or if 
        there are issues with data retrieval based on quad keys.

    Example:
    >>> aoi_hexagon = create_hexagon(-122.34543, 47.65792)
    >>> buildings_heights_gdf = height_acquire(aoi_hexagon)

    Note:
    - This function is designed for use with hexagonal polygons specifically.
    - The hexagon should be a valid shapely polygon.
    """

    if type(hexagon) != shapely.geometry.polygon.Polygon:
        raise ValueError("polygon is invalid")

    # Get the bounds of the area of interest (AOI)
    minx, miny, maxx, maxy = hexagon.bounds
    # Slightly increase the area of interest to ensure coverage
    minx = minx - 0.001 # minimum longitude
    miny = miny - 0.001 # minimum latitude
    maxx = maxx + 0.001 # maximum longitude
    maxy = maxy + 0.001 # maximum latitude

    # Initialize an empty set to store quad keys
    quad_keys = set()
    # Generate quad keys for tiles within the bounds at zoom level 9
    for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
        quad_keys.add(int(mercantile.quadkey(tile)))
    # Convert the set of quad keys to a list
    quad_keys = list(quad_keys)
    print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")


    # Read the dataset links CSV file
    df = pd.read_csv(
        "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
    )

    # Create an empty GeoDataFrame
    combined_gdf = gpd.GeoDataFrame()
    # Debug print statement - can be removed in production
    # print(combined_gdf)

    # Iterate over each quad key
    for quad_key in tqdm(quad_keys):
        # Find rows in the dataset that match the current quad key
        rows = df[df["QuadKey"] == quad_key]

        # If exactly one row is found for the quad key
        if rows.shape[0] == 1:
            # Get the URL of the GeoJSON file
            url = rows.iloc[0]["Url"]
            # Read the GeoJSON file from the URL
            df2 = pd.read_json(url, lines=True)
            # Convert geometry data to Shapely shapes
            df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)

            # Create a GeoDataFrame from the data
            gdf = gpd.GeoDataFrame(df2, crs=4326)
            gdf['height'] = gdf['properties'].apply(lambda x: x.get('height'))
            gdf = gdf.drop(columns=['properties'])

            combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)
            # Debug print statement - can be removed in production
            # print(combined_gdf)

        # If multiple rows are found for a quad key, raise an error
        elif rows.shape[0] > 1:
            raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
        # If no rows are found for a quad key, raise an error
        else:
            raise ValueError(f"QuadKey not found in dataset: {quad_key}")
        
    return combined_gdf


def get_centroid(gdf):
    """
    Calculate and add the centroid of geometries in a GeoDataFrame.

    This function computes the centroid for each geometry in the 
    GeoDataFrame and adds these centroids as a new column to the 
    GeoDataFrame. The centroid of a shape is the geometric center of 
    all points in the shape.

    Parameters:
    gdf (GeoDataFrame): A GeoDataFrame containing geometries from which
    the centroids are to be calculated.

    Returns:
    GeoDataFrame: The original GeoDataFrame with an additional column 
    'centroid', containing the centroid of each geometry.
    """

    gdf['centroid'] = gdf.geometry.centroid
    # Debug print statement - can be removed in production
    # print(gdf)
    return gdf


def weighted_median(data, weights):
    """
    Calculate the weighted median of a dataset.

    This function computes the weighted median for a given set of data 
    points and their associated weights. It sorts the data and weights, 
    calculates the cumulative sum of the weights, and then finds the value 
    at which half of the total weight is accumulated. This value is the 
    weighted median.

    Parameters:
    data (array-like): An array, list, or similar structure containing 
    the data points. The data should be numeric.
    weights (array-like): An array, list, or similar structure containing 
    the weights corresponding to each data point. These should be non-negative 
    numbers and of the same length as the data array.

    Returns:
    float: The weighted median of the provided data points.

    Raises:
    ValueError: If `data` and `weights` have different lengths.
    ValueError: If any weight is negative.

    Example:
    >>> data = [1, 2, 3, 4, 5]
    >>> weights = [1, 2, 3, 4, 5]
    >>> weighted_median(data, weights)
    4.0

    Note:
    The weighted median is a measure of central tendency, similar to the 
    median, but each data point contributes to the final result according 
    to its associated weight. This is particularly useful in situations 
    where some data points are more significant than others.
    """
    if len(data) != len(weights):
        raise ValueError("Data and weights must have the same length.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative.")
    data_sorted, weights_sorted = zip(*sorted(zip(data, weights)))
    cum_weights = np.cumsum(weights_sorted)
    cutoff = weights.sum() / 2.0
    return np.interp(cutoff, cum_weights, data_sorted)


def weighted_percentile(data, weights, percentile):
    """
    Calculate the weighted percentile of a dataset.

    This function computes the weighted percentile for a given set of data 
    points, their associated weights, and the specified percentile. The data 
    and weights are sorted, and the cumulative weights are calculated. The 
    function then finds the data point at which the cumulative weight equals 
    the specified percentile of the total weight.

    Parameters:
    data (array-like): An array, list, or similar structure containing 
    the data points. The data should be numeric.
    weights (array-like): An array, list, or similar structure containing 
    the weights corresponding to each data point. These should be non-negative 
    numbers and of the same length as the data array.
    percentile (float): The desired percentile to calculate. This should be a 
    number between 0 and 100.

    Returns:
    float: The weighted percentile value of the provided data points.

    Raises:
    ValueError: If `data` and `weights` have different lengths.
    ValueError: If any weight is negative.
    ValueError: If `percentile` is not between 0 and 100.

    Example:
    >>> data = [1, 2, 3, 4, 5]
    >>> weights = [1, 2, 3, 4, 5]
    >>> weighted_percentile(data, weights, 50)
    4.0

    Note:
    The weighted percentile, like the weighted median, accounts for the 
    significance of each data point through its weight. This is useful in 
    datasets where certain observations are more important or frequent 
    than others. The percentile argument allows for flexibility in 
    determining the specific percentile value needed.
    """

    if len(data) != len(weights):
        raise ValueError("Data and weights must have the same length.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative.")
    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100.")
    data_sorted, weights_sorted = zip(*sorted(zip(data, weights)))
    cum_weights = np.cumsum(weights_sorted)
    cutoff = weights.sum() * percentile / 100.0
    return np.interp(cutoff, cum_weights, data_sorted)


def weighted_std(data, weights):
    """
    Calculate the weighted standard deviation of a dataset.

    This function computes the weighted standard deviation for a given set 
    of data points and their associated weights. The weighted standard 
    deviation is a measure of the spread of a set of numbers, where each 
    number's contribution to the spread is weighted. The function calculates 
    the weighted average (mean) of the data, computes the weighted variance 
    as the average of the squared deviations from the weighted mean, and 
    then returns the square root of the variance as the standard deviation.

    Parameters:
    data (array-like): An array, list, or similar structure containing 
    the data points. The data should be numeric.
    weights (array-like): An array, list, or similar structure containing 
    the weights corresponding to each data point. These should be non-negative 
    numbers and of the same length as the data array.

    Returns:
    float: The weighted standard deviation of the provided data points.

    Raises:
    ValueError: If `data` and `weights` have different lengths.
    ValueError: If any weight is negative.

    Example:
    >>> data = [1, 2, 3, 4, 5]
    >>> weights = [1, 2, 3, 4, 5]
    >>> weighted_std(data, weights)
    1.4142135623730951

    Note:
    The weighted standard deviation is useful in datasets where different 
    observations have varying levels of importance, represented by the 
    weights. This method differs from the traditional standard deviation 
    as it takes into account the weight of each data point, offering a 
    more nuanced view of data variability.
    """

    if len(data) != len(weights):
        raise ValueError("Data and weights must have the same length.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative.")
    average = np.average(data, weights=weights)
    variance = np.average((data - average)**2, weights=weights)
    return np.sqrt(variance)


def average_building_height_with_centroid(buildings, hexagon):
    """
    Calculate statistical measures of building heights within a hexagon 
    based on their centroids.

    This function selects buildings from a GeoDataFrame whose centroids 
    are within or intersect a specified hexagonal area. It computes various 
    statistical measures related to the building heights, such as total 
    height-area product, average height relative to the hexagon area, 
    weighted average height, and weighted statistical measures like 
    standard deviation and percentiles.

    Parameters:
    buildings (gpd.GeoDataFrame): A GeoDataFrame containing building data 
        with geometry and height information.
    hexagon (shapely.geometry.polygon.Polygon): A hexagon polygon 
        representing the area of interest.

    Returns:
    dict: A dictionary containing the following key-value pairs:
        - 'centroid_stat_total_height_area': Sum of the product of building 
            heights and their respective areas.
        - 'centroid_stat_avg_height_area': Average building height relative 
            to the hexagon area.
        - 'centroid_stat_mean': Weighted average of building heights.
        - 'centroid_stat_std_dev': Weighted standard deviation of building 
            heights.
        - 'centroid_stat_min': Minimum building height.
        - 'centroid_stat_25%': 25th percentile of building heights.
        - 'centroid_stat_50%': Median (50th percentile) of building heights.
        - 'centroid_stat_75%': 75th percentile of building heights.
        - 'centroid_stat_max': Maximum building height.

    Raises:
    ValueError: If the input is not a valid GeoDataFrame or hexagon polygon.

    Example:
    >>> hexagon = create_hexagon(-122.34543, 47.65792)
    >>> buildings_gdf = height_acquire(hexagon)
    >>> stats = average_building_height_with_centroid(buildings_gdf, hexagon)

    Note:
    - The function assumes that the 'buildings' GeoDataFrame contains a 'centroid' 
        column with centroid geometries of buildings.
    """

    # Select buildings whose centroid is within or intersects the hexagon
    buildings_within_hex = buildings[buildings['centroid'].within(hexagon)]
    # Debug print statement - can be removed in production
    # print(buildings_within_hex)

    # print(buildings_within_hex.columns)
    if buildings_within_hex.empty:
        # return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
        return {
            'centroid_stat_total_height_area': np.NaN,
            'centroid_stat_avg_height_area': np.NaN,
            'centroid_stat_mean': np.NaN,
            # 'centroid_stat_median': np.NaN,
            'centroid_stat_std_dev': np.NaN,
            'centroid_stat_min': np.NaN,
            'centroid_stat_25%': np.NaN,
            'centroid_stat_50%': np.NaN,
            'centroid_stat_75%': np.NaN,
            'centroid_stat_max': np.NaN
        }
    # Calculate the product of the area and height for each building
    buildings_within_hex['area_height'] = buildings_within_hex.area * buildings_within_hex['height']
    # Debug print statement - can be removed in productio
    # print(buildings_within_hex)


    # Method 1: related to hexagon area
    # Sum the products and divide by the area of the hexagon to get the average height
    total_height_area = buildings_within_hex['area_height'].sum()
    hexagon_area = hexagon.area
    # Debug print statement - can be removed in productio
    # print(hexagon_area)
    average_height_area = total_height_area / hexagon_area if hexagon_area != 0 else 0

    # Method 2: not related to hexagon area
    weighted_avg = np.average(buildings_within_hex['height'], weights=buildings_within_hex.area)

    # median = weighted_median(buildings_within_hex['height'], buildings_within_hex.area)
    percentile_0 = weighted_percentile(buildings_within_hex['height'], 
                                       buildings_within_hex.area, 0)
    percentile_25 = weighted_percentile(buildings_within_hex['height'], 
                                        buildings_within_hex.area, 25)
    percentile_50 = weighted_percentile(buildings_within_hex['height'], 
                                        buildings_within_hex.area, 50)
    percentile_75 = weighted_percentile(buildings_within_hex['height'], 
                                        buildings_within_hex.area, 75)
    percentile_100 = weighted_percentile(buildings_within_hex['height'], 
                                         buildings_within_hex.area, 100)
    std_dev = weighted_std(buildings_within_hex['height'], buildings_within_hex.area)

    return {
        'centroid_stat_total_height_area': total_height_area,
        'centroid_stat_avg_height_area': average_height_area,
        'centroid_stat_mean': weighted_avg,
        # 'centroid_stat_median': median,
        'centroid_stat_std_dev': std_dev,
        'centroid_stat_min': percentile_0,
        'centroid_stat_25%': percentile_25,
        'centroid_stat_50%': percentile_50,
        'centroid_stat_75%': percentile_75,
        'centroid_stat_max': percentile_100
    }




def seattle_height_acquire():
    """
    Acquires building height information for Seattle city limits and 
    stores it in a GeoJSON file.

    This function reads the Seattle city limits from a provided GeoJSON
    file and expands its area slightly to ensure complete coverage. It 
    then generates quad keys for tiles within this area at a specified 
    zoom level, using these keys to retrieve building footprint data 
    from an online dataset. The function filters and processes the data,
    extracting height information and storing it in a GeoJSON file for 
    further use.

    Steps:
    1. Read Seattle city limits from a GeoJSON file.
    2. Generate quad keys for tiles within the area bounds.
    3. Fetch building data for each quad key from an online dataset.
    4. Extract and process height information from the building data.
    5. Store the processed data in a GeoJSON file.

    Raises:
        ValueError: If multiple or no rows are found for a quad key in 
        the dataset.

    Output:
        A GeoJSON file containing polygons representing building 
        footprints with associated height data.
    """

    # # Example polygon
    # aoi_geom = {
    # "coordinates": [
    #     [
    #         [-122.34522236751503, 47.793350002297956],
    #         [-122.3452190137285, 47.79345987328376],
    #         [-122.34535989993172, 47.79346182082953],
    #         [-122.34536326515978, 47.793351950006006],
    #         [-122.34522236751503, 47.793350002297956],
    #     ]
    # ],
    # "type": "Polygon",
    # }

    # Read in the GeoJSON file for Seattle city limits
    seattle = gpd.read_file(input_file_from_data_dir("seattle-city-limits.geojson"))
    # Extract the first geometry object from the GeoDataFrame
    aoi_geom = seattle.geometry[0]
    # Change the type to shapely.geometry.polygon.Polygon
    aoi_shape = shapely.geometry.shape(aoi_geom)
    # Get the bounds of the area of interest (AOI)
    minx, miny, maxx, maxy = aoi_shape.bounds
    # For Seattle city limit:
    # minx = -122.40985799299995
    # miny = 47.64445376000003
    # maxx = -122.24563167199994
    # maxy = 47.73416571200005
    # Slightly increase the area of interest to ensure coverage
    minx = minx - 0.001 # minimum longitude
    miny = miny - 0.001 # minimum latitude
    maxx = maxx + 0.001 # maximum longitude
    maxy = maxy + 0.001 # maximum latitude

    # Define the output file name for the building footprints
    output_fn = os.path.join("data","seattle_building_footprints.geojson")


    # Initialize an empty set to store quad keys
    quad_keys = set()
    # Generate quad keys for tiles within the bounds at zoom level 9
    for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
        quad_keys.add(int(mercantile.quadkey(tile)))
    # Convert the set of quad keys to a list
    quad_keys = list(quad_keys)
    print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")


    # Read the dataset links CSV file
    df = pd.read_csv(
        "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
    )


    # Initialize index and a list to combine rows from different files
    idx = 0
    combined_rows = []

    # Create a temporary directory to store downloaded files
    with tempfile.TemporaryDirectory() as tmpdir:
        # List to store temporary file names
        tmp_fns = []
        # Iterate over each quad key
        for quad_key in tqdm(quad_keys):
            # Find rows in the dataset that match the current quad key
            rows = df[df["QuadKey"] == quad_key]
            # Debug print statement - can be removed in production
            # print(rows)

            # If exactly one row is found for the quad key
            if rows.shape[0] == 1:
                # Get the URL of the GeoJSON file
                url = rows.iloc[0]["Url"]
                # Read the GeoJSON file from the URL
                df2 = pd.read_json(url, lines=True)
                # Convert geometry data to Shapely shapes
                df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)
                # Debug print statement - can be removed in production
                # print(df2)

                # Create a GeoDataFrame from the data
                gdf = gpd.GeoDataFrame(df2, crs=4326)
                gdf['height'] = gdf['properties'].apply(lambda x: x.get('height'))
                gdf = gdf.drop(columns=['properties'])
                # Debug print statement - can be removed in production
                # print(gdf)

                # Define the file name for the temporary file
                fn = os.path.join(tmpdir, f"{quad_key}.geojson")
                tmp_fns.append(fn)

                # Write the GeoDataFrame to a GeoJSON file if it doesn't exist
                if not os.path.exists(fn):
                    gdf.to_file(fn, driver="GeoJSON")
            # If multiple rows are found for a quad key, raise an error
            elif rows.shape[0] > 1:
                raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
            # If no rows are found for a quad key, raise an error
            else:
                raise ValueError(f"QuadKey not found in dataset: {quad_key}")
            

        # Merge each temporary GeoJSON files into a single file
        for fn in tmp_fns:
            with fiona.open(fn, "r") as f:
                # Read each row in the file
                for row in tqdm(f):
                    row = dict(row)
                    shape = shapely.geometry.shape(row["geometry"])

                    # Check if the shape is within the area of interest
                    if aoi_shape.contains(shape):
                        properties = row["properties"]
                        # Remove the 'id' key if it exists
                        if "id" in row:
                            del row["id"]
                        
                        # Extract the height value from properties, assuming it's already a direct value and not a dict
                        height = properties.get('height')  # This assumes that 'height' is directly stored in properties

                        # Create a new properties dictionary with only 'id' and 'height'
                        new_properties = {"id": idx, "height": height}
                        idx += 1

                        # Update the row with the new properties
                        row["properties"] = new_properties

                        # Add the row to the combined rows list
                        combined_rows.append(row)


    # Define the schema for the output file
    schema = {
        "geometry": "Polygon",
        "properties": {
            "id": "int",
            "height": "float"
        }
    }

    # Write the combined rows to the output file with updated schema
    with fiona.open(output_fn, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema) as f:
        for row in combined_rows:
            # Make sure each row's attributes conform to the schema, including 'height'
            properties = row['properties']
            new_properties = {
                'id': properties['id'],
                # Get the 'height' value directly from the original properties dictionary
                'height': properties.get('height') 
            }

            # Check if 'height' value is missing）
            if new_properties['height'] is None or new_properties['height'] == -1:
                # Skip that polygon without height
                continue 

            # Construct a new row dictionary to match the schema
            new_row = {
                'type': 'Feature',
                'geometry': shapely.geometry.mapping(shapely.geometry.shape(row['geometry'])),
                'properties': new_properties
            }

            # Write the new rows to the output file
            f.write(new_row)
