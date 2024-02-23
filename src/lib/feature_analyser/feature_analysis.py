# automatically exclude tilts based on parameters determined in motioncorr and ctffind (before ML)

import os
import sys
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
# change the path to be until src
root_dir = os.path.abspath(os.path.join(current_dir, '../../../'))
sys.path.append(root_dir)

from src.read_write.read_write import read_star

class Main:
    def __init__(self, in_mics, out_dir, y1, y2, y3, y4, y5, y6, y7, y8, y9):
        self.mics = in_mics
        self.out_dir = out_dir
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4
        self.y5 = y5
        self.y6 = y6
        self.y7 = y7
        self.y8 = y8
        self.y9 = y9
        self.make_plots()

    def make_plots(self):
        self.nr_of_plots = []
        if self.y1:
            self.nr_of_plots.append(self.y1)

        if self.y2:
            self.nr_of_plots.append(self.y2)

        if self.y3:
            self.nr_of_plots.append(self.y3)

        if self.y4:
            self.nr_of_plots.append(self.y4)
        
        if self.y5:
            self.nr_of_plots.append(self.y5)

        if self.y6:
            self.nr_of_plots.append(self.y6)

        if self.y7:
            self.nr_of_plots.append(self.y7)

        if self.y8:
            self.nr_of_plots.append(self.y8)
        
        if self.y9:
            self.nr_of_plots.append(self.y9)
            
        self.abs_path_to_ctf_star = os.path.join(os.getcwd(), self.mics)
        self.tilt_series_ctf_star_df = read_star(self.abs_path_to_ctf_star)
        
        self.logfile = FPDF()

        for graph in self.nr_of_plots:
            fig, ax = plt.subplots()
            line = ax.plot([], [])
            ax.set_title(f"Average {graph} across Tilts")
            ax.set_xlabel("Tilt-Angle")
            ax.set_ylabel(f"{graph}")
            
            
            #self.values_all_tilts = pd.DataFrame() 
            self.i = 0
            # loop through all titl series and add their values for the respective parameter to the plot
            for tilt_series in self.tilt_series_ctf_star_df["rlnTomoTiltSeriesStarFile"]:
                
                self.tilt_star = read_star(tilt_series)
                # remove neg tilt axis (only have positive angle, otherwise -60 will be the first, not 0)
                #self.tilt_star["rlnTomoNominalStageTiltAngle"] = self.tilt_star["rlnTomoNominalStageTiltAngle"].abs() + 10 # lamella was milled at -10° --> +10 is 0° on the sample (see in mdoc)
                self.tilts_in_tilt_order = self.tilt_star.sort_values("rlnTomoNominalStageTiltAngle")

                #print(self.tilts_in_tilt_order)

                self.tilt_axis = self.tilts_in_tilt_order["rlnTomoNominalStageTiltAngle"]

                # set up df in the first iteration
                if self.i == 0:
                    self.values_all_tilts = pd.DataFrame()
                    self.values_all_tilts.index = self.tilt_axis
                    self.i += 1 

                # define axis for plot
                # Get Position_XX.star as name of the col
                self.name = tilt_series.split("/")[-1]

                # Set the index of the series to the same as the index of the df (= the tilt angle)
                self.col_of_param = self.tilts_in_tilt_order[graph]
                self.col_of_param.index = self.tilt_axis
                self.values_all_tilts[self.name] = self.col_of_param

            #self.median = self.values_all_tilts.median(axis=1)
            self.mean = self.values_all_tilts.mean(axis=1)
            self.std = self.values_all_tilts.std(axis=1)
            ax.plot(self.mean.index, self.mean, label = graph, color="salmon")
            # Add a band representing the standard deviation aroung the line
            ax.fill_between(self.mean.index, (self.mean + self.std), (self.mean - self.std), alpha=0.3, label = "Standard Deviation", color="royalblue")
            # Error bars instead of a continuous band:
            #ax.errorbar(self.mean.index, self.mean, yerr=self.std, fmt="o", label = "Standard Deviation")
            
            # Get std deviation
            self.std = self.values_all_tilts.std(axis=1)

            ax.legend()
            fig.savefig(f"{self.out_dir}/{graph}.png", dpi = 300)
            plt.close(fig)
            self.logfile.add_page()
            self.logfile.image(f"{self.out_dir}/{graph}.png", w = 200, h = 150)
        
        self.logfile.output(f"{self.out_dir}/logfile.pdf", "F")


if __name__ == "__main__":
    print(sys.argv)
    
    # Define option names
    option_names = {
        "--in_mics": "in_mics",
        "--o": "out_dir",
        "--y1": "y1",
        "--y2": "y2",
        "--y3": "y3",
        "--y4": "y4",
        "--y5": "y5",
        "--y6": "y6",
        "--y7": "y7",
        "--y8": "y8",
        "--y9": "y9",
        "--j": "nr_threads"
    }

    # Initialize variables with None to handle optional parameters

    y1 = None
    y2 = None
    y3 = None
    y4 = None
    y5 = None
    y6 = None
    y7 = None
    y8 = None
    y9 = None
    
    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in option_names:
            # Get the variable name associated with the option
            var_name = option_names[sys.argv[i]]
            # Assign the value after the option to the corresponding variable
            globals()[var_name] = sys.argv[i + 1]
            if y1 == "all":
                y1 = "rlnAccumMotionTotal"
                y2 = "rlnAccumMotionEarly"
                y3 = "rlnAccumMotionLate"
                y4 = "rlnDefocusU"
                y5 = "rlnDefocusV"
                y6 = "rlnDefocusAngle"
                y7 = "rlnCtfFigureOfMerit"
                y8 = "rlnCtfMaxResolution"
                i += 16
            else:
                i += 2
        else:
            print("Invalid option:", sys.argv[i])
            sys.exit(1)

    # Check if all required arguments are provided
    if None in [in_mics, out_dir]:
        print("Usage: {} --in_mics <input_tilt_file> --o <output_directory> [--j <nr_threads>]".format(sys.argv[0]))
        sys.exit(1)

    main_instance = Main(in_mics, out_dir, y1, y2, y3, y4, y5, y6, y7, y8, y9)

