import unittest
import os
import sys

"""
bash command to run test (once in respective directory):
python -m unittest discover  (runs all tests)
python -m unittest test_module_name  (runs just one module)
"""

current_dir = os.path.dirname(os.path.abspath(__name__))
src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
# Add the 'src' directory to the Python path
sys.path.append(src_dir)

from lib.app.app import MainUI

