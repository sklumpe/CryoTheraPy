from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

from lib.read_write import jobs_in_scheme
from lib.app.ctp import MainUI

def get_value_from_tab(tab, parameter_alias):
    """
    go to the specified tab and get the value of a specified parameter.

    Args:
        tab (str): name of the tab (based on the name of the job).
        parameter_alias (str): name of the parameter (check for aliases in the yaml file).

    Returns:
        value (str): value corresponding to the parameter and the job specified.

    Example:
        input = "importmovies", "Pixel in A"
        output = 2.93 
    """
    # have to remove this part and set this kind of function in the class --> have table widget as input

    
    nRows = table_widget.rowCount()
    for row in range(nRows):
        current_param = table_widget.item(row, 0).text()
        # if the param we are looking for is equal to the param in the row in the table, change the
        # value in that table to the value to the value of the dict (path or header information).
        # Additionally, change the colour of the field to clarify that this has been automatically set.
        if current_param == parameter_alias:
            current_value = table_widget.item(row, 1).text()
            return current_value

def calculate_dose_rate_per_pixel(pixel_size_a, exposure_times, dose_per_angstrom, eer_sections, dose_per_frame = 0.3):
  """
  copied that one from Joe's Tomoman script
  """
  pixel_area = pixel_size_a**2
  dose_rate_per_pixel = dose_per_angstrom * pixel_area * exposure_times

  # Optimize EER grouping
  best_modulo = 9999 # dose rate (per ang better) also input !
  dose_per_frame = dose_rate_per_pixel / dose_per_frame #= input field 0.3 base
  group = round(702 / dose_per_frame)
  eer_groups = 10

  for i in range(-3, 4):
      test_group = group + i

      if test_group < 3:
          continue

      remainder = eer_sections % test_group

      if remainder <= best_modulo and remainder <= 10:
          best_modulo = remainder
          eer_groups = test_group

  return dose_rate_per_pixel, eer_groups



import re

def extract_eer_from_header(header):
    """
    extracts the number of eer sections from the provided text.
    Args:
        header (str): string of the header

    Returns:
        eers (int) or None: the number of sections if found, None otherwise.

    Example:
        input = Size=     159038 K\n\n                    This is a TIFF file.\n\n Number of columns, rows, sections .....   16384   16384     396\n Map mode ..............................    0   (byte)                     \n Start cols, rows, sects, grid x,y,z ...    0     0     0   16384  16384    396\n Pixel spacing (Angstroms ...
        output: 396
    """
    # hard coded it bc I couldn't get it to work 
    # Define the regular expression pattern to match the number of sections
    pattern = r"Number of columns, rows, sections \.{5,}\s*\d+\s*\d+\s*(\d+)"
    # Search for the pattern in the text
    eers = re.search(pattern, header)
    # If match is found, extract and return the number of sections
    if eers:
        return int(eers.group(1))
    else:
        return None



