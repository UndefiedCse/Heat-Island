"""This file manages all unit test for getcoor module
"""
import unittest

from heat_island import getcoor


class TestGetcoor(unittest.TestCase):
    """This class manages unit test for getcoor.py
    under development it's here is to pass `workflow`
    """
    def test_noinputfile(self):
        """Quick Edge test
        """
        path = 'Not a file'
        with self.assertRaises(ValueError):
            getcoor.select_coordinate(path)
