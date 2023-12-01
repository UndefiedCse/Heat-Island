import unittest

from heat_island.getcoor import getcoor


class TestGetcoor(unittest.TestCase):
    """This class manages unit test for getcoor.py
    under development it's here is to pass `workflow`
    """
    def test_noinputfile(self):
        path = 'Not a file'
        with self.assertRaises(ValueError):
            getcoor.select_coordinate(path)
