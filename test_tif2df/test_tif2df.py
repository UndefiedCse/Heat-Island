"""This is module for testing tif2df function.
Run this file from home directory to avoid error.
"""
import unittest
import os
from tif2df.tif2df import tif2df

def compare_file(fn1,fn2):
    """Simple function for file comparison
    ref:https://stackoverflow.com/questions/54838554/how-do-i-compare-the-content-of-files-in-python

    Args:
        fn1 (str): file name 1
        fn2 (str): file name 2

    Returns:
        bool: Whether both file are identical or either file does not exist
    """
    if not os.path.isfile(fn1) or not os.path.isfile(fn2):
        raise ValueError("Some files does not exist")
    with open(fn1, 'r') as file1, open(fn2, 'r') as file2:
        return file1.read() == file2.read()

def remove_file(fn):
    """Simple function to remove file if exist

    Args:
        fn (str): file path
    """
    if os.path.isfile(fn):
        os.remove(fn)

class Test_tif2df(unittest.TestCase):
    """This class manages unit test for tif2df function
    """
    finput_path = 'test_tif2df/float.tif'
    foutput_path = 'test_tif2df/float.csv'
    f_sol = 'test_tif2df/float_sol.csv'
    shinput_path = 'test_tif2df/shade.tif'
    shoutput_path = 'test_tif2df/shade.csv'
    sh_sol = 'test_tif2df/shade_sol.csv'
    def test_smoke(self):
        remove_file(self.foutput_path)
        overwrite = False
        tif2df(self.finput_path,self.foutput_path,overwrite)
        remove_file(self.foutput_path)

    def test_notstr(self):
        """Function should return TypeError when input path is not string
        """
        input_path = []
        with self.assertRaises(TypeError):
            tif2df(input_path)
    
    def test_input_nofile(self):
        """Function should return ValueError when input file does not exist
        """
        input_path = 'test.tif'
        with self.assertRaises(ValueError):
            tif2df(input_path)

    def test_output_nodir(self):
        """Function should return ValueError when there is no directory for output
        """
        output = 'unknown/test.csv'
        with self.assertRaises(ValueError):
            tif2df(self.finput_path,output)

    def test_oneshot(self):
        """Comparing output file function with shade_sol.csv
        """
        remove_file(self.shoutput_path)
        tif2df(self.shinput_path,self.shoutput_path)
        self.assertTrue(compare_file(self.shoutput_path,self.sh_sol))
        remove_file(self.shoutput_path)