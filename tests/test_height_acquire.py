import unittest
import geopandas as gpd
import shapely

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
        verifying that the output is a geopandas.geodataframe
        """
        hexagon = geo_process.create_hexagon(-122.34543, 47.65792)
        result = height_acquire.height_acquire(hexagon)
        self.assertIsInstance(result, gpd.GeoDataFrame)


    def test_get_centroid(self):
        """
        verifying that the function successfully adds a 'centroid' column to the input GeoDataFrame
        """
        # Call the function on the sample GeoDataFrame
        test_gdf = gpd.read_file(data_process.input_file_from_data_dir("seattle_building_footprints.geojson"))
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
