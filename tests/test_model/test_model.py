""" This file manages all unit tests for train.py
"""

import unittest
import os
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from heat_island.model import train

std = StandardScaler()
knn = KNeighborsRegressor()


def make_dummyjson(path: str, condition: list = None):
    """Create dummy geojson file called `tmp.geojson` at selected directory

    Args:
        dir (str, optional): directory for dummy file. Defaults to ''.
        condition (list, optional): condition currently have
                                    'small' for small dataset
                                    'NaN' for 1 null row. Defaults to [].

    Raises:
        ValueError: If there is existing file so function does not overwrite.

    Returns:
        str: path to dummy file
        list: list of keys to features
        str: key for target or y
    """
    if os.path.isfile(path):
        raise ValueError("Can't create dummy file")
    if condition is None:
        condition = []
    with open(path, 'w', encoding='utf-8') as dmm:
        dmm.write('{"features":[')
        dmm.write('{"properties":{"Lat": 47.613, "Lon": -122.342,')
        dmm.write('"T": 50.107}},')
        dmm.write('{"properties":{"Lat": 47.620, "Lon": -122.356,')
        dmm.write('"T": 53.560}},')
        if 'NaN' in condition:
            dmm.write('{"properties":{"Lat": 47.622, "Lon": -122.318,')
            dmm.write('"T": null}},')
            dmm.write('{"properties":{"Lat": null, "Lon": -122.318,')
            dmm.write('"T": 50.107}},')
            dmm.write('{"properties":{"Lat": 47.622, "Lon": null,')
            dmm.write('"T": 50.107}},')
        else:
            dmm.write('{"properties":{"Lat": 47.622, "Lon": -122.312,')
            dmm.write('"T": 50.107}},')
        if 'small' not in condition:
            dmm.write('{"properties":{"Lat": 47.621, "Lon": -122.327,')
            dmm.write('"T": 50.107}},')
            dmm.write('{"properties":{"Lat": 47.602, "Lon": -122.312,')
            dmm.write('"T": 53.064}},')
        dmm.write('{"properties":{"Lat": 47.620, "Lon": -122.309,')
        dmm.write('"T":51.564}}]}')
    return path


FEATURES = ['Lat', 'Lon']
TARGET = 'T'
PATH_NORMAL = make_dummyjson('normal.geojson')
PATH_SMALL = make_dummyjson('small.geojson', ['small'])
PATH_NAN = make_dummyjson('nan.geojson', ['NaN'])
PATH_SMALLNAN = make_dummyjson('small_nan.geojson', ['small', 'NaN'])


class TestSaveModel(unittest.TestCase):
    """This class manages unit test for save model function
    """

    def test_nodir(self):
        """Test not a directory
        """
        path = 'Not a file'
        fname = 'tmp.bin'
        with self.assertRaises(ValueError):
            train.save_model(knn, std, path, fname)

    def test_notmodel(self):
        """Edge test for not a model input
        """
        with self.assertRaises(AttributeError):
            train.save_model('', std, '', 'temp.bin')

    def test_notstd(self):
        """Edge test for string input for scaler
        """
        with self.assertRaises(AttributeError):
            train.save_model(knn, '', '', 'tmp.bin')


# Work in progress
class TestCleanData(unittest.TestCase):
    """This class manages unit test for clean data function
    """

    def test_smoke_feature(self):
        """Simple test case checking row of features
        """
        data_feature, _ = train.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_feature), 6)

    def test_smoke_target(self):
        """Simple test case checking row of target
        """
        _, data_target = train.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_target), 6)

    def test_small(self):
        """Function should raise error when dataset is too small
        """
        with self.assertRaises(ValueError):
            train.clean_data(PATH_SMALL, FEATURES, TARGET)

    def test_nan(self):
        """Function should ignore data with NaN value
        """
        tmp_feature, _ = train.clean_data(PATH_NAN, FEATURES, TARGET)
        self.assertEqual(len(tmp_feature), 5)


os.remove(PATH_NORMAL)
os.remove(PATH_NAN)
os.remove(PATH_SMALL)
os.remove(PATH_SMALLNAN)
