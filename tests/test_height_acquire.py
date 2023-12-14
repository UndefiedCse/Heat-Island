import unittest
import geopandas as gpd
import shapely
import numpy as np

from heat_island import height_acquire
from heat_island import geo_process
from heat_island import data_process

class TestHeight(unittest.TestCase):
    """
    
    """

    def test_invalid_polygon_input(self):
        """
        Test with invalid polygon and ensure raise a ValueError
        """
        with self.assertRaises(ValueError):
            height_acquire.height_acquire("invalid_polygon")


    def test_valid_polygon_output_type(self):
        """
        Verifying that the output is a geopandas.geodataframe
        """
        hexagon = geo_process.create_hexagon(-122.34543, 47.65792)
        result = height_acquire.height_acquire(hexagon)
        self.assertIsInstance(result, gpd.GeoDataFrame)


    def test_get_centroid(self):
        """
        Verifying that the function successfully adds a 'centroid' column to the input GeoDataFrame
        """
        # Call the function on the sample GeoDataFrame
        test_gdf = gpd.read_file(data_process.input_file_from_data_dir("seattle_building_footprints.geojson"))
        # Implement the target function
        height_acquire.get_centroid(test_gdf)
        # Check if 'centroid' column exists in the returned GeoDataFrame
        self.assertIn('centroid', test_gdf.columns)

        # Furthermore, check the type of the centroid column entries
        self.assertTrue(all(isinstance(geom, shapely.geometry.Point) for geom in test_gdf['centroid']))


    def test_with_invalid_geometry(self):
        """
        Test with Invalid Geometry: 
        Test the function's behavior when provided with invalid geometry data.
        """
        invalid_geometry = [None, "not_a_geometry"]
        gdf = gpd.GeoDataFrame({'geometry': invalid_geometry})
        with self.assertRaises(TypeError):  # or another appropriate exception
            height_acquire.get_centroid(gdf)

    
    def test_with_multiple_geometries(self):
        """
        Test with Multiple Geometries: 
        Ensure the function works correctly with a GeoDataFrame containing multiple geometries.
        """
        geometries = [shapely.geometry.Point(1, 1), shapely.geometry.Point(2, 2)]
        gdf = gpd.GeoDataFrame({'geometry': geometries})
        result_gdf = height_acquire.get_centroid(gdf)
        self.assertEqual(len(result_gdf), len(geometries))
        self.assertIn('centroid', result_gdf.columns)
        for centroid, geometry in zip(result_gdf['centroid'], geometries):
            self.assertEqual(centroid, geometry)

    
    def setUp_average_building_height_with_centroid(self):
        # Create a sample hexagon and buildings for testing
        self.hexagon = shapely.geometry.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        self.buildings = gpd.GeoDataFrame({
            'geometry': [shapely.geometry.Point(0.5, 0.5), shapely.geometry.Point(1.5, 1.5)],
            'height': [10, 20],
            'centroid': [shapely.geometry.Point(0.5, 0.5), shapely.geometry.Point(1.5, 1.5)]
        })

    def test_with_invalid_inputs(self):
        with self.assertRaises(ValueError):
            height_acquire.average_building_height_with_centroid("not_a_geodataframe", self.hexagon)
        with self.assertRaises(ValueError):
            height_acquire.average_building_height_with_centroid(self.buildings, "not_a_polygon")

    def test_with_valid_inputs(self):
        result = height_acquire.average_building_height_with_centroid(self.buildings, self.hexagon)
        self.assertIsInstance(result, dict)
        self.assertIn('centroid_stat_mean', result)

    def test_with_empty_geodataframe(self):
        empty_gdf = gpd.GeoDataFrame(columns=['geometry', 'height', 'centroid'])
        result = height_acquire.average_building_height_with_centroid(empty_gdf, self.hexagon)
        for key, value in result.items():
            self.assertTrue(np.isnan(value))
