"""
This module is dedicated to performing comprehensive unit tests
on the getcoor module of the heat_island project.
It aims to verify the functionality and
error handling of functions responsible for managing geographic coordinates,
including creating geometry collections from GeoJSON features and
facilitating user interaction for coordinate selection
through a browser interface.
The tests are crucial to ensuring the module's reliability and
robustness in processing geographic data.
"""

import unittest
from unittest.mock import patch, mock_open
from heat_island.getcoor import make_collection, open_browser
from heat_island.getcoor import select_coordinate


class TestMakeCollection(unittest.TestCase):
    """
    testing the make_collection function,
    ensuring it correctly handles various scenarios
    related to input data format and structure.
    """

    def test_empty_feature_list(self):
        """
        Test if an empty list raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection([])

    def test_invalid_feature_format(self):
        """
        Test if a non-list type raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection("not a list")

    def test_invalid_feature_structure(self):
        """
        Test if a list with non-dictionary elements
        raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection(["not", "a", "dict"])

    def test_missing_geometry_key(self):
        """
        Test if a list of dictionaries
        without 'geometry' key raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection([{"no_geometry": None}])

    def test_invalid_geometry_type(self):
        """
        Test if 'geometry' not being a dictionary
        raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection([{"geometry": "not a dict"}])

    def test_missing_coordinates_key(self):
        """
        Test if 'geometry' dictionary without 'coordinates' key
        raises ValueError
        """
        with self.assertRaises(ValueError):
            make_collection([{"geometry": {}}])


class TestOpenBrowser(unittest.TestCase):
    """
    Tests the open_browser function,
    which involves file and directory validations and
    handling GeoJSON data for map rendering.
    """

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_invalid_output_directory(self, mock_isfile, mock_isdir):
        """
        Test if a non-existent directory raises ValueError
        """
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        with self.assertRaises(ValueError):
            open_browser('valid/path.json', 'invalid/dir')

    @patch('os.path.isfile')
    def test_invalid_json_path_type(self, mock_isfile):
        """
        Test if a non-string json_path raises ValueError
        """
        mock_isfile.return_value = True
        with self.assertRaises(ValueError):
            open_browser(123, '')

    @patch('os.path.isfile')
    def test_non_existent_json_file(self, mock_isfile):
        """
        Test if a non-existent .json file raises ValueError
        """
        mock_isfile.return_value = False
        with self.assertRaises(ValueError):
            open_browser('nonexistent/path.json', '')

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"features": []}')
    @patch('os.path.isfile')
    def test_invalid_json_file_type(self, mock_isfile, mock_file):
        """
        Test if an invalid file type raises ValueError
        """
        mock_isfile.return_value = True
        with self.assertRaises(ValueError):
            open_browser('invalid/path.txt', '')


class TestSelectCoordinate(unittest.TestCase):
    """
    Examines the select_coordinate function,
    particularly focusing on file validation and error handling.
    """

    @patch('os.path.isfile')
    def test_non_existent_boundary_file(self, mock_isfile):
        """
        Test if a non-existent boundary file raises ValueError
        """
        mock_isfile.return_value = False
        with self.assertRaises(ValueError):
            select_coordinate('nonexistent/path.json')
