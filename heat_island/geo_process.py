"""
This module converts a central coordinate into hexagons for use in ML and also to
display them as GeoJson for use in Folium.

Functions:
    create_hexagon(latitude, longitude): Creates a hexagon Polygon surrounding given
        latitude and longitude.
    hex_to_geojson(hexagon): Converts a hexagon polygon into GeoJson format for Folium.
"""
import math
import shapely.geometry
from shapely.geometry import Polygon
import folium

def create_hexagon(latitude, longitude):
    """
    Creates hexagon shaped Polygon centered around latitude and longitude.

    Args:
        latitude (float): The latitude of the user-selected point
        longitude (float): The longitude of the user-selected point

    Returns:
        shapely.geometry.Polygon: Hexagon centered around the input args
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
    """
    Converts hexagon Polygon into GeoJson for Folium

    Args:
        hexagon (shapely.geometry.Polygon): The hexagon polygon

    Returns:
        folium.GeoJson: Hexagon shape in GeoJson for use in Folium
    """  
    return folium.GeoJson({
        "type": "Feature",
        "geometry": shapely.geometry.mapping(hexagon)
    })
