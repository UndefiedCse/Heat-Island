import shapely.geometry
from shapely.geometry import Polygon
import math
import folium


from heat_island.data_process import input_file_from_data_dir

def create_hexagon(longitude, latitude, radius_meters = 111111 * 0.001):
    """
    Creates a hexagon centered at a specified latitude and longitude.

    This function generates the vertices of a regular hexagon centered 
    at the given latitude and longitude. 
    The hexagon is approximated on the Earth's surface, considering the
    Earth as a sphere with a radius of 6,371,000 meters. The radius of 
    the hexagon is set as default to 0.001 degrees of latitude, 
    converted into meters. Each side of the hexagon is equal in length,
    and the vertices are calculated using the central angle for a 
    hexagon (60 degrees).

    Parameters:
    longitude (float): The longitude of the center of the hexagon.
    latitude (float): The latitude of the center of the hexagon.
    radius_meters (float): The desired radius of the hexagon, in meter.

    Returns:
    shapely.geometry.Polygon: A Polygon object representing the hexagon.
    Each vertex of the hexagon is a tuple containing the latitude and 
    longitude in decimal degrees.

    Note:
    - longitude should be entered before latitude.
    """

    # Earth's radius in meters
    earth_radius = 6371000

    # Convert radius from degrees in latitude to meters
    # 1 degree of latitude is approximately 111,111 meters
    # We use 0.001 degree of latitude as radius as default
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
    Converts a hexagon shape into GeoJSON format using Folium.

    This function takes a hexagon shape, typically created using a 
    geometry library like Shapely, and converts it into a GeoJSON 
    object using Folium. The GeoJSON object created includes type as
    'Feature', and the geometry is derived from the input hexagon shape. 

    Parameters:
    hexagon (shapely.geometry.Polygon): A Polygon object representing 
    the hexagon. The hexagon should be defined with its vertices as 
    latitude and longitude pairs.

    Returns:
    folium.features.GeoJson: A GeoJson object representing the hexagon.
    """

    return folium.GeoJson({
        "type": "Feature",
        "geometry": shapely.geometry.mapping(hexagon)
    })