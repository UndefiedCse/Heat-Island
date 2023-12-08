import pandas as pd
import geopandas as gpd
import shapely.geometry
from shapely.geometry import Polygon
from geojson import Feature, Point, FeatureCollection
import json
import math
import numpy as np
import mercantile
from tqdm import tqdm
from folium import GeoJson
import os
import tempfile
import fiona
import folium

import sys
import requests
import rasterio
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
import rasterstats
import matplotlib
import matplotlib.pyplot as plt
from rasterio.features import geometry_mask

# get the path of current
sys.path.append(os.path.dirname(os.getcwd()))

from heat_island import data_process
from heat_island import geo_process

# set the dir and path of downloaded data
# or, after Lilac updating the import_file_from_data_dir.py,
# call import_file_from_data_dir function to create path for existing and output files
# existing
raw_building_path = data_process.input_file_from_data_dir('building')
raw_extent_path = data_process.input_file_from_data_dir('extent')
raw_weather_path = data_process.input_file_from_data_dir('weather')
raw_terrain_path = data_process.input_file_from_data_dir('terrain')
raw_boundary_path = data_process.input_file_from_data_dir('boundary')

# output
aggr_hex_path = data_process..model('hex')

'''read existing files'''
# building, extent, weather, boundary, terrain (set crs to 4326)
raw_building = gpd.read_file(raw_building_path)
raw_extent = gpd.read_file(raw_extent_path)
raw_weather = pd.read_csv(raw_weather_path)
raw_boundary = gpd.read_file(raw_boundary_path)

'''align crs for existing files'''


# align crs for all data(except weather which is still a dataframe), here we set all to 4326
# set_crs will set the terrain tif crs to target_crs
# target_crs sample: 'EPSG:4326'
def set_crs(input_file_path, output_file_path, target_crs):
    with rasterio.open(input_file_path) as src:
        # Define the new CRS
        dst_crs = target_crs

        # Calculate the transform and dimensions for the new CRS
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)

        # Create a metadata dictionary for the output file
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Open the output file
        with rasterio.open(output_file_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                # Reproject and write each band
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)


set_crs(raw_terrain_path, raw_terrain_path, 'EPSG:4326')
# terrain: from a tif file to a numpy.ndarray
with rasterio.open(raw_terrain_path) as src:
    raw_terrain = src.read()
print(src.meta)
print(type(raw_terrain))
print(raw_terrain.shape)

print(raw_building.crs)
print(raw_extent.crs)
print(raw_boundary.crs)

'''create hexagon for weather data which has lat and lon
user will have to specify radius
'''


# two function: create_hexagon, hex_to_geojson
# create_hexagon: function for creating hexagon
def create_hexagon(lat, lon, radius):
    # number of sides
    n_sides = 6
    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    # Earth's radius in meters
    earth_radius = 6371000

    # Calculate the radius of our hexagon in radians
    r_rad = radius / earth_radius

    # Calculate the vertices of the hexagon
    hexagon_vertices = []
    for i in range(n_sides):
        angle = math.pi / 3 * i
        x = lon_rad + r_rad * math.cos(angle)
        y = lat_rad + r_rad * math.sin(angle)
        # Convert the vertex back to degrees
        vertex = (math.degrees(x), math.degrees(y))
        hexagon_vertices.append(vertex)

    return Polygon(hexagon_vertices)


def hex_to_geojson(hexagon):
    return GeoJson({
        "type": "Feature",
        "geometry": shapely.geometry.mapping(hexagon)
    })


# call the create_hexagon for each row of raw_weather, the returned hexagon geometry stored in a new column
# slice desired columns to a new dataframe raw_hex
rex_radius = 160
raw_weather['hex'] = raw_weather.apply(lambda row: create_hexagon(row['Lat'], row['Lon'], rex_radius), axis=1)

raw_hex = raw_weather.copy()[['hex', 'Station ID', 'Lat', 'Lon', 'Elev (ft.)', 'Ave temp annual_F', 'Note']]
raw_hex.head()


# function: get_centroid
# get_centroid: take geometry of building footprint and compute the centroid coordinate
def get_centroid(df):
    df['centroid'] = df.geometry.centroid


# function: basic weighted statics calculation
def weighted_median(data, weights):
    data_sorted, weights_sorted = zip(*sorted(zip(data, weights)))
    cum_weights = np.cumsum(weights_sorted)
    cutoff = weights.sum() / 2.0
    return np.interp(cutoff, cum_weights, data_sorted)


def weighted_percentile(data, weights, percentile):
    data_sorted, weights_sorted = zip(*sorted(zip(data, weights)))
    cum_weights = np.cumsum(weights_sorted)
    cutoff = weights.sum() * percentile / 100.0
    return np.interp(cutoff, cum_weights, data_sorted)


def weighted_std(data, weights):
    average = np.average(data, weights=weights)
    variance = np.average((data - average) ** 2, weights=weights)
    return np.sqrt(variance)


# function: compute weighted statics of buildings whose centroid is within the hexagon
def average_building_height_with_centroid(buildings, hexagon):
    # Select buildings whose centroid is within or intersects the hexagon
    buildings_within_hex = buildings[buildings['centroid'].within(hexagon.hex)]
    # print(buildings_within_hex.columns)
    if buildings_within_hex.empty:
        # return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
        return {
            'centroid_stat_total_height_area': np.NaN,
            'centroid_stat_avg_height_area': np.NaN,
            'centroid_stat_mean': np.NaN,
            'centroid_stat_median': np.NaN,
            'centroid_stat_std_dev': np.NaN,
            'centroid_stat_min': np.NaN,
            'centroid_stat_25%': np.NaN,
            'centroid_stat_50%': np.NaN,
            'centroid_stat_75%': np.NaN,
            'centroid_stat_max': np.NaN
        }
    # Calculate the product of the area and height for each building
    buildings_within_hex['area_height'] = buildings_within_hex.area * buildings_within_hex['height']

    # Method 1: related to hexagon area
    # Sum the products and divide by the area of the hexagon to get the average height
    total_height_area = buildings_within_hex['area_height'].sum()
    hexagon_area = hexagon.hex.area
    print(hexagon_area)
    average_height_area = total_height_area / hexagon_area if hexagon_area != 0 else 0

    # Method 2: not related to hexagon area
    weighted_avg = np.average(buildings_within_hex['height'], weights=buildings_within_hex.area)

    median = weighted_median(buildings_within_hex['height'], buildings_within_hex.area)
    percentile_0 = weighted_percentile(buildings_within_hex['height'], buildings_within_hex.area, 0)
    percentile_25 = weighted_percentile(buildings_within_hex['height'], buildings_within_hex.area, 25)
    percentile_50 = weighted_percentile(buildings_within_hex['height'], buildings_within_hex.area, 50)
    percentile_75 = weighted_percentile(buildings_within_hex['height'], buildings_within_hex.area, 75)
    percentile_100 = weighted_percentile(buildings_within_hex['height'], buildings_within_hex.area, 100)
    std_dev = weighted_std(buildings_within_hex['height'], buildings_within_hex.area)

    return {
        'centroid_stat_total_height_area': total_height_area,
        'centroid_stat_avg_height_area': average_height_area,
        'centroid_stat_mean': weighted_avg,
        'centroid_stat_median': median,
        'centroid_stat_std_dev': std_dev,
        'centroid_stat_min': percentile_0,
        'centroid_stat_25%': percentile_25,
        'centroid_stat_50%': percentile_50,
        'centroid_stat_75%': percentile_75,
        'centroid_stat_max': percentile_100
    }


'''execute the weighted statics computation
user will specify what static neeeded
provided statics: ['total_height_area','avg_height_area','mean','median', 'std_dev', 'min', '25%','50%' ,'75%', 'max']
'''
raw_hex['centroid_stat_ALL'] = raw_hex.apply(lambda x: average_building_height_with_centroid(raw_building, x), axis=1)
for stat in ['total_height_area', 'avg_height_area', 'mean', 'median', 'std_dev', 'min', '25%', '50%', '75%', 'max']:
    # try:
    #     raw_hex = raw_hex.drop(['centroid_stat_' + stat],axis = 1)
    # except KeyError:
    #     pass
    raw_hex['centroid_stat_' + stat] = raw_hex['centroid_stat_ALL'].apply(lambda x: x['centroid_stat_' + stat])


# function: compute statics of terrain within the hexagon
def terrain_stats(terrain, hexagon):
    # Make sure 'terrain' is a Rasterio dataset and 'hexagon' is the geometry
    geom_mask = geometry_mask([hexagon], transform=terrain.transform, invert=True,
                              out_shape=(terrain.height, terrain.width))

    # Use the mask to select the terrain data
    selected_terrain = terrain.read(1)[geom_mask]

    # Calculate the statistics for the selected terrain data
    if selected_terrain.size > 0:
        mean = np.mean(selected_terrain)
        median = np.median(selected_terrain)
        std_dev = np.std(selected_terrain)
        min_val = np.min(selected_terrain)
        percentile_25 = np.percentile(selected_terrain, 25)
        percentile_50 = np.percentile(selected_terrain, 50)
        percentile_75 = np.percentile(selected_terrain, 75)
        max_val = np.max(selected_terrain)
    else:
        mean = median = std_dev = min_val = percentile_25 = percentile_50 = percentile_75 = max_val = np.nan

    return {
        'terrain_stat_mean': mean,
        'terrain_stat_median': median,
        'terrain_stat_std_dev': std_dev,
        'terrain_stat_min': min_val,
        'terrain_stat_25%': percentile_25,
        'terrain_stat_50%': percentile_50,
        'terrain_stat_75%': percentile_75,
        'terrain_stat_max': max_val
    }


'''execute the statics computation
user will specify what static needed
provided statics: ['mean', 'median', 'std_dev', 'min', '25%','50%', '75%', 'max']
'''
with rasterio.open(raw_terrain_path) as terrain_dataset:
    for stat in ['mean', 'median', 'std_dev', 'min', '25%', '50%', '75%', 'max']:
        raw_hex['terrain_stat_' + stat] = raw_hex.apply(
            lambda x: terrain_stats(terrain_dataset, x['hex'])[f'terrain_stat_{stat}'], axis=1)

# optional, convert the weather station elevation to meter
raw_hex['Elev (m.)'] = raw_hex['Elev (ft.)'].replace('-', np.nan).astype(float) * 0.3048

# optional, select columns user would like to keep

raw_hex = gpd.GeoDataFrame(raw_hex, geometry='hex')

raw_hex.to_file(aggr_hex_path, driver="GeoJSON")
