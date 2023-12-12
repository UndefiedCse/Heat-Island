import unittest
import geopandas as gpd

from heat_island import height_acquire
from heat_island import geo_process

class TestHeight(unittest.TestCase):
    """
    
    """

    def test_invalid_polygon_input(self):
        with self.assertRaises(ValueError):
            height_acquire.height_acquire("invalid_polygon")

    def test_valid_polygon_output_type(self):
        hexagon = geo_process.create_hexagon(-122.34543, 47.65792)
        result = height_acquire.height_acquire(hexagon)
        self.assertIsInstance(result, gpd.GeoDataFrame)