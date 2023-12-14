"""
This module, dedicated to unit testing, ensures the reliability and
correctness of the functions defined in train.py,
which is part of the heat_island project.
The tests are designed to verify the functionality of various components
crucial to the training and handling of machine learning models,
specifically focusing on aspects like data cleaning, model saving, and
feature extraction.
"""

import unittest
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from heat_island import model

std = StandardScaler()
knn = KNeighborsRegressor()


class TestSaveModel(unittest.TestCase):
    """
    Concentrates on testing the save_model function.
    It includes tests for handling non-directory paths,
    non-model inputs, invalid scaler types
    """

    def test_nodir(self):
        """
        Test not a directory
        """
        path = 'Not a file'
        fname = 'tmp.bin'
        with self.assertRaises(ValueError):
            model.save_model(knn, std, path, fname)

    def test_notmodel(self):
        """
        Edge test for not a model input
        """
        with self.assertRaises(AttributeError):
            model.save_model('', std, '', 'temp.bin')

    def test_notstd(self):
        """
        Edge test for string input for scaler
        """
        with self.assertRaises(AttributeError):
            model.save_model(knn, '', '', 'tmp.bin')


FEATURES = ['Lat', 'Lon']
TARGET = 'Ave temp annual_F'
PATH_NORMAL = 'tests/data/normal.geojson'
PATH_SMALL = 'tests/data/small.geojson'
PATH_NAN = 'tests/data/nan.geojson'


class TestCleanData(unittest.TestCase):
    """
    Focuses on the clean_data function, ensuring proper handling of normal,
    small, and NaN-inclusive datasets.
    It validates the function's ability to process and
    clean geospatial data correctly.
    """

    def test_smoke_feature(self):
        """
        Simple test case checking row of features
        """
        data_feature, _ = model.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_feature), 10)

    def test_smoke_target(self):
        """
        Simple test case checking row of target
        """
        _, data_target = model.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_target), 10)

    def test_small(self):
        """
        Function should raise error when dataset is too small
        """
        with self.assertRaises(ValueError):
            model.clean_data(PATH_SMALL, FEATURES, TARGET)

    def test_nan(self):
        """
        Function should ignore data with NaN value
        """
        data_feature, _ = model.clean_data(PATH_NAN, FEATURES, TARGET)
        self.assertEqual(len(data_feature), 10)


class TestGetKeys(unittest.TestCase):
    """
    Verifies the get_keys function, ensuring it
    returns the correct list of feature keys used in the dataset.
    """

    def test_get_keys(self):
        """
        Test whether get_keys function
        returns the correct list of feature keys
        """
        expected_keys = ['centroid_stat_total_height_area',
                         'centroid_stat_avg_height_area',
                         'centroid_stat_mean', 'centroid_stat_std_dev',
                         'centroid_stat_min',
                         'centroid_stat_25%', 'centroid_stat_50%',
                         'centroid_stat_75%',
                         'centroid_stat_max', 'Lat', 'Lon']
        self.assertEqual(model.get_keys(), expected_keys)
