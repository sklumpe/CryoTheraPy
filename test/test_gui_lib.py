import unittest
from unittest.mock import patch
import tempfile
import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QLineEdit, QTableWidget, QApplication, QTableWidgetItem
from PyQt6.QtGui import QColor

current_dir = os.path.dirname(os.path.abspath(__name__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from src.gui.gui_lib import browse_dirs, change_bckgrnd, change_values, update_df, abs_to_loc_path
from src.read_write.read_write import job_star_dict


class set_up(unittest.TestCase):
    @classmethod
    def setUpClass(appl):
        # Create a QApplication instance
        appl.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(appl):
        # Clean up the QApplication instance
        appl.app.quit()


class test_gui_lib_function_browse_dirs(set_up):
    """
    Test whether the browse_dirs function accurately sets the QLineEdit.Text() to the path of the 
    selected directory.
    """
    def setUp(self):
        # Create a QLineEdit field
        self.line_edit = QLineEdit()

        # create a temporary directory
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory and its contents after the test is completed
        os.rmdir(self.temp_dir)

    def test_browse_dirs(self):
        with patch("src.gui.gui_lib.QFileDialog.getExistingDirectory", return_value=self.temp_dir):
            # Call the browse_dirs function
            browse_dirs(self.line_edit)

            # Get the text in the QLineEdit
            path = self.line_edit.text()
            # Add the / to the path (as is done in the browse_dirs function)
            path_dir = os.path.abspath(self.temp_dir) + "/"
            # Assert that the path is equal to the path of the temporary directory
            self.assertEqual(path, path_dir, "The path to the directory is not copied correctly")
            

class test_gui_lib_function_change_bckgrnd(set_up):
    def test_change_bckgrnd(self):
        """
        test whether the change_bckgrnd function changes the background of a selected field in a
        table.
        """
        # create a dummy QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(2)
        self.table_widget.setColumnCount(2)
        # set a QTableWidgetItem in the table widget
        self.table_widget.setItem(0, 0, QTableWidgetItem("UnitTest"))

        # call the function
        change_bckgrnd(self.table_widget, 0, 0)

        # Check if the background color has changed to the default color (darker grey)
        expected_color = QColor(200, 200, 200)
        actual_color = self.table_widget.item(0, 0).background().color()
        self.assertEqual(actual_color, expected_color, "The background colour was not set to QColor(200, 200, 200)")


class test_gui_lib_function_change_values(set_up):
    def test_change_values(self):
        """
        test whether the change_values function accurately searches a table for a key of a dict
        and changes the respective entry of the next col to the value of the dict.
        """
        # create a table widget with 4 rows and 2 columns
        table_widget = QTableWidget()
        table_widget.setColumnCount(2)
        table_widget.setRowCount(4)

        # populate the table with sample data
        test_data = [("this", "1"), ("is", "2"), ("a", "3"), ("unit", "4"), ("test", "5")]
        for row, (col0, col1) in enumerate(test_data):
            table_widget.setItem(row, 0, QTableWidgetItem(col0))
            table_widget.setItem(row, 1, QTableWidgetItem(col1))

        # create the dictionary with the to-be-set values
        test_param_val_dict = {"is": "5"}

        # create a series for the function but don't include any aliases
        job_names = pd.Series()

        change_values(table_widget, test_param_val_dict, job_names)

        # check if the value was updated correctly
        expected_value = "5"
        for row in range(table_widget.rowCount()):
            if table_widget.item(row, 0).text() == "is":
                actual_value = table_widget.item(row, 1).text()
                self.assertEqual(actual_value, expected_value, "The values were not changed correctly")
                break


class test_gui_lib_function_update_df(set_up):
    """
    test whether the update_df function accurately updates a df bsed on the values of a table. For this,
    a table is created first and populated. Then, these inputs are used to update the job_star_dict using
    the update_df, as well as to create a new df. Lastly, the 2 df's are compared.
    """
    def setUp(self):
        self.current_job_tab = "importmovies"
        self.start_dict = job_star_dict
        # create a table widget with 2 columns and 10 rows
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(10)
        self.table_widget.setColumnCount(2)

        # fill the table with inputs
        for row in range(10):
            for col in range(2):
                self.table_widget.setItem(row, col, QTableWidgetItem(f"Value_{row}_{col}"))

    def test_update_df(self):
        # put any job as test

        updated_dict = update_df(self.start_dict, self.table_widget, 10, 2, self.current_job_tab, "src/read_write/config_aliases.yaml")
        updated_dict_first10 = updated_dict[self.current_job_tab]["joboptions_values"].iloc[:10, :2]
        # create a df to check that the function updated the DataFrame correctly
        columns = ["rlnJobOptionVariable", "rlnJobOptionValue"]
        expected_df_state = pd.DataFrame(columns = columns)
        for row in range(10):
            for col, col_name in enumerate(columns):
                value = self.table_widget.item(row, col).text()
                expected_df_state.at[row, col_name] = value

        self.assertTrue(expected_df_state.equals(updated_dict_first10), "The df is not properly updated")


class test_gui_lib_function_abs_to_loc_path(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_in_dir = os.path.join(os.getcwd(), "test_in_directory")
        self.test_out_dir = os.path.join(os.getcwd(), "test_out_directory")
        self.frames_dir = os.path.join(self.test_in_dir, "frames")
        self.mdocs_dir = os.path.join(self.test_in_dir, "mdocs")
        os.makedirs(self.test_in_dir)
        os.makedirs(self.test_out_dir)
        os.makedirs(self.frames_dir)
        os.makedirs(self.mdocs_dir)

    def tearDown(self):
        # Remove symbolic links and temporary directories after testing
        os.remove(os.path.join(self.test_out_dir, "frames"))
        os.remove(os.path.join(self.test_out_dir, "mdocs"))
        os.rmdir(self.frames_dir)
        os.rmdir(self.mdocs_dir)
        os.rmdir(self.test_in_dir)
        os.rmdir(self.test_out_dir)


    def test_abs_to_loc_path_symlinks_created(self):
        """
        test whether the the cwd is properly reset afterwards and symlinks are created properly.
        """
        self.original_directory = os.getcwd()

        path_frames = self.frames_dir
        path_mdocs = self.mdocs_dir
        path_out_dir = self.test_out_dir

        abs_to_loc_path(path_frames, path_mdocs, path_out_dir)

        self.after_directory = os.getcwd()

        # Check if symbolic links are created
        self.assertEqual(self.original_directory, self.after_directory, "cwd is not properly reset at the end")
        self.assertTrue(os.path.islink(os.path.join(path_out_dir, "frames")), "frames link is not properly created")
        self.assertTrue(os.path.islink(os.path.join(path_out_dir, "mdocs")), "mdoc link is not properly created")