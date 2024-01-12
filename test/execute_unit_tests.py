import os
import sys

current_dir = os.path.dirname(os.path.abspath(__name__))
test_dir = os.path.abspath(os.path.join(current_dir, '../../../test'))
# Add the 'src' directory to the Python path
sys.path.append(test_dir)

from test_read_write import Test_Read_Write_Function_read_star
from test_read_write import Test_Read_Write_Function_write_star

#they are not showing an error (even when set wrong) when imported, only when executed in the other file directly
exe_test_read_star = Test_Read_Write_Function_read_star()
exe_test_read_star.test_read_star()

exe_test_write_star = Test_Read_Write_Function_write_star()
exe_test_write_star.test_write_star()