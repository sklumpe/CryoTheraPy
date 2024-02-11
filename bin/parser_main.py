import argparse
import sys
import os
from PyQt6.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__name__))
# change the path to be root
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

from src.gui.ctp import MainUI

def parse_arguments():
    parser = argparse.ArgumentParser(description="Main UI CTP.py")
    parser.add_argument("--skip_edit", "-s", required = False, action = "store_true", help = "Skip editing order of jobs")
    #parser.add_argument("--movie_path", "-m", required = False, help = "Path to movies")
    return parser.parse_args()

def main():
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()

    args = parse_arguments()

    if args.skip_edit:
        window.makeJobTabs()

    """
    if args.movie_path:
        window.line_path_movies.setText(args.movie_path)
        #MainUI.loadPathMovies(args.movie_path)
    """

    sys.exit(app.exec())

if __name__ == '__main__':
    main()