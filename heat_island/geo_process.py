# import pandas as pd
# import geopandas as gpd
import shapely.geometry
from shapely.geometry import Polygon
# from geojson import Feature, Point, FeatureCollection
# import json
import math
# import mercantile
# from tqdm import tqdm
# from folium import GeoJson
# import os
# import tempfile
# import fiona
import folium
# import os
# import requests
# import rasterio
# import rasterstats
# import matplotlib
# import matplotlib.pyplot as plt

def create_hexagon(latitude, longitude):
    """
    
    """

    # Earth's radius in meters
    earth_radius = 6371000

    # Convert radius from degrees in latitude to meters
    # 1 degree of latitude is approximately 111,111 meters
    # We use 0.001 degree of latitude as radius
    radius_meters = 111111 * 0.001
    # Calculate the radius of our hexagon in radians
    r_rad = radius_meters / earth_radius

    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # number of sides
    n_sides = 6

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
    return folium.GeoJson({
        "type": "Feature",
        "geometry": shapely.geometry.mapping(hexagon)
    })