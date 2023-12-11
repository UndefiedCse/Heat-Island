""" This file manages all unit tests for train.py
"""

import unittest
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from heat_island import model

std = StandardScaler()
knn = KNeighborsRegressor()


class TestSaveModel(unittest.TestCase):
    """This class manages unit test for save model function
    """

    def test_nodir(self):
        """Test not a directory
        """
        path = 'Not a file'
        fname = 'tmp.bin'
        with self.assertRaises(ValueError):
            model.save_model(knn, std, path, fname)

    def test_notmodel(self):
        """Edge test for not a model input
        """
        with self.assertRaises(AttributeError):
            model.save_model('', std, '', 'temp.bin')

    def test_notstd(self):
        """Edge test for string input for scaler
        """
        with self.assertRaises(AttributeError):
            model.save_model(knn, '', '', 'tmp.bin')


FEATURES = ['Lat', 'Lon']
TARGET = 'Ave temp annual_F'
PATH_NORMAL = 'tests/data/normal.geojson'
PATH_SMALL = 'tests/data/small.geojson'
PATH_NAN = 'tests/data/nan.geojson'


class TestCleanData(unittest.TestCase):
    """This class manages unit test for clean data function
    """

    def test_smoke_feature(self):
        """Simple test case checking row of features
        """
        data_feature, _ = model.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_feature), 10)

    def test_smoke_target(self):
        """Simple test case checking row of target
        """
        _, data_target = model.clean_data(PATH_NORMAL, FEATURES, TARGET)
        self.assertEqual(len(data_target), 10)

    def test_small(self):
        """Function should raise error when dataset is too small
        """
        with self.assertRaises(ValueError):
            model.clean_data(PATH_SMALL, FEATURES, TARGET)

    def test_nan(self):
        """Function should ignore data with NaN value
        """
        data_feature, _ = model.clean_data(PATH_NAN, FEATURES, TARGET)
        self.assertEqual(len(data_feature), 10)


if __name__ == '__main__':
    print('checking')
    print('complete')
