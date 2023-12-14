"""
test_geo_process.py: Tests for geo_process.py

Tests included in this module:
- test_invalid_polygon_input(): Test the response to invalid polygon inputs.
- test_valid_polygon_output_type(): Verify the output type from the height acquisition process.
- test_get_centroid(): Check the addition of 'centroid' column in GeoDataFrame.
- test_with_multiple_geometries(): Validate the functioning with multiple geometries in a GeoDataFrame.

Set up: 
python -m unittest discover
"""

import unittest
import shapely
import folium

from heat_island import geo_process


class TestGeo(unittest.TestCase):
    """
    This class contains test cases designed to verify the correctness of 
    functions in geo_process.py.
    """


    def test_create_hexagon(self):
        """
        This test verifies that the `create_hexagon` function in the 
        `geo_process` module correctly creates a hexagon shape. The 
        function is expected to produce a valid `shapely.geometry.Polygon` 
        object representing a hexagon centered at the given latitude and 
        longitude, with each side having the specified radius.

        The test uses example coordinates (New York City) and a predefined
        radius to create the hexagon. It then checks two aspects:
        1. Whether the resulting object is indeed a Polygon.
        2. Whether the hexagon has the correct number of vertices 
            (6 vertices plus the closing vertex, totaling 7).
        """

        latitude, longitude = 40.7128, -74.0060  # Example coordinates (New York City)
        radius_meters = 160  # 160 m radius

        # Create hexagon
        hexagon = geo_process.create_hexagon(longitude, latitude, radius_meters)

        # Check if the result is a Polygon
        self.assertIsInstance(hexagon, shapely.geometry.Polygon)

        # Check if the hexagon has 6 vertices
        self.assertEqual(len(hexagon.exterior.coords), 7)  # Includes closing vertex
        # The shapely.geometry.Polygon object includes the closing
        # vertex in its exterior coordinates, which is why we expect 7
        # vertices instead of 6.


    def test_hex_to_geojson(self):
        """
        This test verifies the functionality of the `hex_to_geojson` 
        function in the `geo_process` module. The function is expected 
        to take a hexagonal `shapely.geometry.Polygon` object and 
        convert it into a GeoJSON object, suitable for use with mapping 
        libraries like Folium.

        The test involves two primary checks:
        1. Whether the resulting object is an instance of `folium.features.GeoJson`.
        2. Whether the geometry of the converted GeoJSON object matches 
            the original hexagon's geometry.
        """

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
