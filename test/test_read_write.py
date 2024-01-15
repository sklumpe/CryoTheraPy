import unittest
import os
import sys
import tempfile

current_dir = os.path.dirname(os.path.abspath(__name__))
src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
# Add the 'src' directory to the Python path
sys.path.append(src_dir)

from lib.read_write import read_star, write_star


class Test_Read_Write_Function_read_star(unittest.TestCase):
    def test_read_star(self):
        """
        testing whether the function creates a dict from the star file.
        """
        result = type(read_star("/fs/pool/pool-plitzko3/Michael/01-Data/relion/pipeline_test/schemes/Schemes/master_scheme/scheme.star")) == dict
        # Use assert methods to check if the result matches the expected value
        self.assertTrue(result, True)

class Test_Read_Write_Function_write_star(unittest.TestCase):
    def test_write_star(self):
        """
        testing whether the function creates a .star file from dataframe.
        """
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "test.star")
            test_data = read_star(star_path)
            # Run the function to create the file
            write_star(test_data, temp_file)

            # Check if the file exists and has the correct extension
            self.assertTrue(os.path.exists(temp_file))
            self.assertTrue(temp_file.endswith(".star"))
