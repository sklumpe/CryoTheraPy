# automatically exclude tilts based on parameters determined in motioncorr and ctffind (before ML)
import os
import sys
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
# change the path to be until src
root_dir = os.path.abspath(os.path.join(current_dir, '../../../'))
sys.path.append(root_dir)

from src.read_write.read_write import read_star, write_star
from src.lib.exclude_tilts.exclude_tilts_rules_lib import col_of_df_to_series, series_higher_lower, combine_vectors, remove_tilts


class Main:
    def __init__(self, in_mics, out_dir, shift_min, shift_max, defocus_min, defocus_max, resolution_min, resolution_max, nr_threads):
        self.mics = in_mics
        self.out_dir = out_dir
        self.shift = (int(shift_min), int(shift_max))
        self.defocus = (int(defocus_min), int(defocus_max))
        self.res = (int(resolution_min), int(resolution_max))
        self.nr_threads = nr_threads
        self.loop_series_in_star()

    def loop_series_in_star(self):
        """
        loop through the tilt series found in the .star file and perform the respective functions on them
        to exclude tilts that are not within the set range of the respective parameter. 


        Example:
            path_tilt_series_ctf_star = /fs/pool/pool-plitzko3/Michael/01-Data/relion/pipeline_test/schemes/CtfFind/job122/tilt_series_ctf.star
            param_range_dict = {"rlnCtfMaxResolution": (8, 9)}
        """
        self.param_range_dict = ({})
        self.param_range_dict["rlnAccumMotionTotal"] = self.shift
        self.param_range_dict["rlnDefocusU"] = self.defocus
        self.param_range_dict["rlnCtfMaxResolution"] = self.res


        # Make dir for individual tilt series' .star files
        self.tilt_series_dir = os.path.join(self.out_dir, "tilt_series")
        os.makedirs(self.tilt_series_dir, exist_ok=True)

        # Get working dir and input directory to construct the absolute path to the .star file
        self.abs_path_to_ctf_star = os.path.join(os.getcwd(), self.mics)
        self.tilt_series_ctf_star_df = read_star(self.abs_path_to_ctf_star)

        for index, current_tilt in self.tilt_series_ctf_star_df.iterrows():
            self.indiv_tilt_star_path = current_tilt["rlnTomoTiltSeriesStarFile"]
            self.tilt_star_dict = read_star(self.indiv_tilt_star_path, do_dict = True)
            self.tilt_star_dict_name_of_df = current_tilt["rlnTomoName"]
            self.tilt_star_df = self.tilt_star_dict[self.tilt_star_dict_name_of_df]

            self.all_0_1_across_params = pd.DataFrame(index = range(len(self.tilt_star_df)), columns = (self.param_range_dict.keys()))

            for param, thresholds in self.param_range_dict.items():
                current_param = col_of_df_to_series(self.tilt_star_df, param)
                param_runaways = series_higher_lower(current_param, thresholds)
                self.all_0_1_across_params[param] = param_runaways
            
            self.tilts_to_keep = combine_vectors(self.all_0_1_across_params)
            self.updated_df = remove_tilts(self.tilt_star_df, self.tilts_to_keep)
            self.updated_star_as_dict = {self.tilt_star_dict_name_of_df: self.updated_df}
            # Individual tilts are called CtfFind/jobXXX/tilt_series/Position_YY.star --> only want last part as file name
            self.file_name = self.indiv_tilt_star_path.split("/")[-1]
            self.new_path = os.path.join(self.tilt_series_dir, self.file_name)
            write_star(self.updated_star_as_dict, self.new_path)

        # Write a star file pointing to the updated tilt_series/Position_YY.star files as input for next job
        # Get the current job number
        self.tilt_series_star_list = col_of_df_to_series(self.tilt_series_ctf_star_df, "rlnTomoTiltSeriesStarFile")
        self.tilt_series_ctf_star_dict = read_star(self.abs_path_to_ctf_star, do_dict = True)
        
        self.name_jobXXX = self.out_dir.split("/")[1]
        self.name_job_number = self.name_jobXXX.split("job")[1]
        # Change the name of the files being pointed to (CtfFind/jobXXX/tilt_series/Position_10.star to External/jobYYY/tilt_series/Position_10.star)
        self.part_to_replace = self.tilt_series_star_list[0].split("/tilt_series")[0]
        self.updated_tilt_series_star_col = self.tilt_series_star_list.str.replace(self.part_to_replace, f"External/job{self.name_job_number}")
        # Replace the column pointing to the old .star files with the new series
        self.tilt_series_ctf_star_dict["global"]["rlnTomoTiltSeriesStarFile"] = self.updated_tilt_series_star_col
        # Write the star file
        self.updated_tilt_series_star_path = os.path.join(os.getcwd(), self.out_dir, "excluded_tilts_rule.star")
        write_star(self.tilt_series_ctf_star_dict, self.updated_tilt_series_star_path)
        

if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) != 19:
        print("Usage: {} --i <input_tilt_file> --o <output_directory> --r_min <min_resolution> --r_max <max_resolution>".format(sys.argv[0]))
        sys.exit(1)

    in_mics = sys.argv[2]
    out_dir = sys.argv[4]
    shift_min = sys.argv[6]
    shift_max = sys.argv[8]
    defocus_min = sys.argv[10]
    defocus_max = sys.argv[12]
    resolution_min = sys.argv[14]
    resolution_max = sys.argv[16]
    nr_threads = sys.argv[18]

    main_instance = Main(in_mics, out_dir, shift_min, shift_max, defocus_min, defocus_max, resolution_min, resolution_max, nr_threads)
