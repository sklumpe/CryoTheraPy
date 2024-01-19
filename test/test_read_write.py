import unittest
import os
import sys
import tempfile
import pandas as pd

"""
bash command to run test (once in respective directory):
python -m unittest discover  (runs all tests)
python -m unittest test_module_name  (runs just one module)
"""

current_dir = os.path.dirname(os.path.abspath(__name__))
src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
# Add the 'src' directory to the Python path
sys.path.append(src_dir)

from lib.read_write import read_config, read_star, write_star, job_star_dict, locate_val

# don't have the yaml file yet so changed it to create a temporary file for the test of the function
class test_read_write_function_read_config(unittest.TestCase):
    def test_read_config(self):
        """
        testing whether the function returns a dict.
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".yaml") as temp_file:
            temp_file.write("key1: value1\nkey2: value2\n")
        # Get the temporary file path
        temp_file_path = temp_file.name

        try:
            # Call the read_config function to get the result
            config_file = read_config(temp_file_path)
            self.assertIsInstance(config_file, dict, "read_config does not accurately create a dictionary from the YAML file")
       
        finally:
            # delete the temporary file again
            os.remove(temp_file_path)
        """
        config_file = read_config()
        self.assertIsInstance(config_file, dict, "read_config does not accurately create a dict from the yaml file")
        """

class test_read_write_function_read_star(unittest.TestCase):
    def test_read_star(self):
        """
        testing whether the function creates a dict from the star file.
        """
        starfile = read_star("/fs/gpfs41/lv01/fileset02/pool/pool-plitzko3/Michael/00-Other/CryoTheraPy/src/lib/app/master_scheme_bck/scheme.star")
        result = type(starfile) == dict
        # Use assert methods to check if the result matches the expected value
        #if result["scheme_jobs"].empty or result["scheme_edges"].empty == True:
        self.assertFalse(starfile["scheme_jobs"].empty or starfile["scheme_edges"].empty, "scheme.star file doesn't have all required entries")
        self.assertTrue(result, "read_star function does not accurately return a dict containing the data from the .star file as df")

class test_read_write_variable_job_star_dict(unittest.TestCase):
    def test_job_star_dict(self):
        """
        testing whether the job_star_dict variable has the correct format, as much is based on this.
        """
        for key in job_star_dict.keys():
            dataframe = any(isinstance(job_star_dict[key][sub_key], pd.DataFrame) for sub_key in job_star_dict[key].keys())
            self.assertTrue(dataframe, "job_star_dict is not correctly formatted")
        self.assertIn("scheme_star", job_star_dict, "scheme.star file is not properly included")

# not ideal yet bc the paths are hard-coded (and the same way as in the function) but wasn't sure how to set up a proper test here since the values are changing and the function just locates them.
class test_read_write_function_locate_val(unittest.TestCase):
    def test_locate_val(self):
        """
        testing whether the locate_val function correctly locates the respective value.
        """
        val_located = locate_val("importmovies", "Cs")
        val_actual_df = read_star("/fs/gpfs41/lv01/fileset02/pool/pool-plitzko3/Michael/00-Other/CryoTheraPy/src/lib/app/master_scheme_bck/importmovies/job.star")["joboptions_values"]
        val_actual = val_actual_df.loc[val_actual_df["rlnJobOptionVariable"] == "Cs", "rlnJobOptionValue"].values[0]
        self.assertEqual(val_located, val_actual, "the located value is not the same as the value in the backup file")


class test_read_write_update_job_star_dict(unittest.TestCase):
    def test_update_job_star_dict(self):
        """
        
        """
        pass

class test_read_write_function_write_star(unittest.TestCase):
    def test_write_star(self):
        """
        testing whether the function creates a .star file from dataframe.
        """
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "test.star")
            test_data = job_star_dict["importmovies"]
            # Run the function to create the file
            write_star(test_data, temp_file)

            # Check if the file exists and has the correct extension
            self.assertTrue(os.path.exists(temp_file))
            self.assertTrue(temp_file.endswith(".star"), "no .star file is created at the target location")

class test_read_write_variable_job_names(unittest.TestCase):
    def test_param_names(self):
        """
        testing whether the keys in param_names have corresponding parameter names in the respective job.star
        """
        pass