# library for the functions required for the basic functions of the application
import sys
import os
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem, QTabWidget

current_dir = os.path.dirname(os.path.abspath(__name__))
# change the path to be until src
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

#from lib.functions import get_value_from_tab
from src.read_write.read_write import get_alias, get_alias_reverse, job_star_dict

def change_bckgrnd(table_widget, row_index, col_index, colour = (QColor(200, 200, 200))):
    """
    change the background colour of the respective field in the table to signal that this field was filled automatically.

    Args:
        row_index (int): row of the field for which the colour should be changed.
        col_index (int): column of the field for which the colour should be changed.
        colour (str): 3 values determining the colour the field is set to (default = darker grey).

    Example:
        auto_change_value changes a value of a field when a certain microscopy set-up is selected, this function
        will then turn the background dark grey, signalling that this is already the correct value.
    """
    table_widget.item(row_index, col_index).setBackground(colour)


def change_values(table_widget, param_val_dict, job_names):
    """
    goes to the tab defined and changes the respective parameter to the new value.

    Args:
        table_widget (PyQt6 tabWidge): the widget in which the values should be changed.
        param_val_dict (dict): dictionary containing the parameter as key and the new value as value.
        job_names (pd.Series): series of job names to check for aliases.

    Example:
        table_widget = table
        param_val_dict = {"Path to movies": "../../movies/*.eer"}
        job_names = jobs_in_scheme
        First, the aliases yaml is searched for an alias for "Path to movies". Then, it iterates 
        over the rows in col 0 of the table looking for "Path to movies" (or the respective alias).
        If the parameter is found, "../../movies/*.eer" is set in col 1 of the table at the respective 
        position and the background colour of that field is changed.
    """
    nRows = table_widget.rowCount()
    for param, value in param_val_dict.items():
        # look for an alias for the param and if one is present, set the param to this alias
        original_param_name = None
        for job in job_names:
            original_param_name = get_alias(job, param)
            if original_param_name:
                break

        # if an alias was found, use it as the param name. If not, use param of the param_val_dict
        param_to_set = original_param_name if original_param_name else param
        
        # find the row corresponding to the param in the table
        for row in range(nRows):
            current_param = table_widget.item(row, 0).text()
            if current_param == param_to_set:
                # set the value and change background color
                table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
                change_bckgrnd(table_widget, row, 1)
                break


def update_df(job_star_dict, table_widget, table_nRows, table_nCols, current_job_tab, path_to_alias_yaml_for_unitTest = "../src/read_write/config_aliases.yaml"):
    """
    update the df that is turned into a job.star file afterwards.

    Args:
        job_star_dict (dict): a dict containing a dict for each job, each containing a df with the respective
        parameters as value to the key "joboptions_values"
        table_widget (PyQt6 tabWidge): the widget containing the updated values.
        table_nRows (int): number or rows in table of current tab.
        table_nCols (int): number or columns in table of current tab.
        current_job_tab (str): name of the current job (for aliases).

    Returns:
        updated job_star_dict.

    Example:
        job_star_dict = job_star_dict
        table_widget = table
        table_nRows = 30
        table_nCols = 2
        current_job_tab = "importmovies"
        It will go through the table row by row, extracting the input into each field. For inputs in the first
        columns, it will look for aliases in the yaml file, so all params have the name that Relion expects.
        Once the correct param name is determined, it writes the respective input into the respective position
        in the "joboptions_values" df of the "importmovies" dict inside the job_star_dict dict.
    """
    for row in range(table_nRows):
        for col in range(table_nCols):
            # set the value to the text in the respective field (determined by row and col index)
            value = table_widget.item(row, col).text()
            # check whether there is an alias for a parameter name and if yes, change back to original name 
            if col == 0:
                original_param_name = get_alias_reverse(current_job_tab, value, path_to_alias_yaml_for_unitTest)
                if original_param_name != None:
                    # param_name = original_param_name
                    value = original_param_name     
            # insert value at the position defined by the index of the table
            job_star_dict[current_job_tab]["joboptions_values"].iloc[row, col] = value
    return(job_star_dict)
