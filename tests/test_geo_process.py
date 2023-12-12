import unittest
import numpy as np
import shapely
import folium

#import sys, os
#sys.path.append(os.getcwd())
from heat_island import geo_process

class TestGeo(unittest.TestCase):
    """
    
    """

    def test_create_hexagon(self):
        latitude, longitude = 40.7128, -74.0060  # Example coordinates (New York City)
        radius_meters = 160  # 160 m radius

        # Create hexagon
        hexagon = geo_process.create_hexagon(latitude, longitude, radius_meters)

        # Check if the result is a Polygon
        self.assertIsInstance(hexagon, shapely.geometry.Polygon)

        # Check if the hexagon has 6 vertices
        self.assertEqual(len(hexagon.exterior.coords), 7)  # Includes closing vertex
        # The shapely.geometry.Polygon object includes the closing 
        # vertex in its exterior coordinates, which is why we expect 7 
        # vertices instead of 6.


    def test_hex_to_geojson(self):
        # Create a hexagon using shapely
        hexagon = shapely.geometry.Polygon([
            (0, 0),
            (1, 0),
            (1.5, 0.866),
            (1, 1.732),
            (0, 1.732),
            (-0.5, 0.866),
            (0, 0)
        ])

        # Convert to GeoJSON
        geojson_obj = geo_process.hex_to_geojson(hexagon)

        # Check if the result is an instance of folium.features.GeoJson
        self.assertIsInstance(geojson_obj, folium.features.GeoJson)

        # Check if the geometry in the GeoJSON is correct
        expected_geometry = shapely.geometry.mapping(hexagon)
        self.assertEqual(geojson_obj.data['geometry'], expected_geometry)

   
