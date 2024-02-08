import yaml
import os
import starfile
import subprocess
import glob

#from lib.functions import calculate_dose_rate_per_pixel, extract_eer_from_header

def read_config(filename):
  """
  reads a configuration file in yaml format.
  
  Args:
    filename (str): name of the .yaml file.
  
  Returns: 
    dict: dictioanry with paramName and data.
  """
  with open(filename) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    
  return data    


def read_star(scheme_name):
  """
  reads a .star file and turns it into a pd df.

  Args:
    scheme_name (str): path to a star file.

  Returns:
    df: dataframe containing the information of the star file at the defined location.

  """
  data_as_df = starfile.read(scheme_name)
  return data_as_df


path_to_scheme = "/fs/gpfs41/lv01/fileset02/pool/pool-plitzko3/Michael/00-Other/CryoTheraPy/data/master_scheme_bck"
scheme_star_dict = read_star(path_to_scheme + "/scheme.star")


# create a pd.series from the edges in the scheme.star (= the order of jobs that are executed), removing the
# first and the last as they are usually EXIT_maxtime and WAIT, i.e. not jobs
jobs_in_scheme = scheme_star_dict["scheme_edges"].rlnSchemeEdgeOutputNodeName.iloc[1:-1]


job_star_dict = {
  f"{job}": read_star(os.path.join(path_to_scheme, f"{job}/job.star"))
  for job in jobs_in_scheme
}
#job_star_dict["scheme_star"] = scheme_star_dict


def get_alias(job, parameter):
  """
  some inputs used by Relion are not self-explanatory (eg. qsub_extra2) so a yaml list was created to change the 
  respective name that is displayed while still keeping the original name for writing the data.

  Args:
    job (str): job name the parameter is used for.
    parameter (str): parameter name.

  Returns:
    alias (str): alias displayed instead of the parameter name.

  Example:
    job
  """
  # path works for any module in the lib/app/ directory
  # "r" means that the file should be opened with reading permissions
  with open("../src/read_write/config_aliases.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)

   # go through entries in the aliases dict
  for entry in yaml_data["aliases"]:
    # if the entry Job of one of the lists equals the given job or all and the entry Parameter contains the given 
    # parameter name, return the entry Alias
    if (entry["Job"] == job or entry["Job"] == "all") and entry["Parameter"] == parameter:
      return entry["Alias"]
  return None


# do the same the other way around to get the parameter name from the alias again
def get_alias_reverse(job, alias):
  """
  reverse of the get alias function, i.e. returns the parameter name as used in the .star file when entering the 
  alias. Kept seperate to keep reading and writing clearly separated to avoid errors. 

  Args:
    job (str): job name the parameter is used for.
    alias (str): alias displayed instead of the parameter name.

  Returns:
    parameter (str): parameter name as displayed in the job.star file.

  Example:
    job
  """
  # path works for any module in the lib/app/ directory
  with open("../src/read_write/config_aliases.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)

  # go through entries in the aliases dict
  for entry in yaml_data["aliases"]:
    # if the entry Job of one of the lists equals the given job or all and the entry Alias contains the given 
    # parameter name, return the entry Parameter
    if (entry["Job"] == job or entry["Job"] == "all") and entry["Alias"] == alias:
      return entry["Parameter"]
  return None


 # so it only fetches the first instance of *.eer, not all of them
def read_header(path_to_frames):
  """
  reads header of a file to fetch the nr of eer's to calculate the optimal split using the calculate_dose_rate_per_pixel function.

  Args:
    path_to_frames (str): path to the respective frames.

  Returns:
    eer_split (dict): best possible eer split per frame as value so it can be added to the dict when transferring
                      information from the file path to the input data.
  Example:

  """
  #with open(path_to_frames, "rb") as frame:
  eer_file = glob.glob(f"{path_to_frames}/*.eer")[0]
  command = f"header {eer_file}"
  result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
  header = str(result)
  eers = extract_eer_from_header(header)
  print(eers)
  #eer_split = calculate_dose_rate_per_pixel(eers)
  #header = frame.read()
  #print(result.stdout)
  


def read_mdoc(path_to_mdoc_dir):
  """
  reads mdoc file and fetches the relevant parameters to automatically set the respective values.

  Args:
    path_to_mdoc (str): path to the directory containing the mdoc files.
  
  Returns:
    return_mdoc_data (dict): values set in the config_reading_meta.yaml file for the respective meta-data type.

  Example:
    input = path to mdoc file
    output = returns a dict with the respective "x/z dimension", "Pixel size in A", and "Voltage of Microscope"
            (names must be set in the config_reading_meta.yaml file and be the same as in the 
            config_aliases.yaml file). This can subsequently be used to update the respective fields in the table.  
  """
  return_mdoc_data = {}
  # using the dir, access the first mdoc file in the folder
  path_to_mdoc = glob.glob(f"{path_to_mdoc_dir}")[0]
  # get respective mdoc file
  with open(path_to_mdoc, "r") as mdoc_file:
    # store the lines in that mdoc file in a list to iterate over
    mdoc_list = [line.strip() for line in mdoc_file if line.strip()]
    # get entries to look for in the mdoc file (based on the config_reading_meta.yaml file)
    # when only accessing the config_reading_meta.yaml file here, it's only accessed once a valid file-path is 
    # entered, not everytime there is a change to the QLine field
    with open("../src/read_write/config_reading_meta.yaml", "r") as yaml_file:
      yaml_data = yaml.safe_load(yaml_file)
      print("mdoc file found")
      # access the respective list in the config_reading_meta.yaml file (parameter to look for in mdoc and respective alias)
      yaml_mdoc = yaml_data["meta_data"].get("mdoc", [])
      # access the list of dicts
      for yaml_entry in yaml_mdoc:
        # iterate through the meta data yaml to get the parameters which should be found (and the associated alias as key)
        for yaml_param_name, yaml_alias in yaml_entry.items():
          # iterate through the lines in the mdoc file until the respective entry is found
          for mdoc_current_line in mdoc_list:
            # remove spaces ect that might be in front/after the parameter name
            mdoc_current_line = mdoc_current_line.strip()
            # Skip empty lines
            if not mdoc_current_line:
              continue
            else:
              # data in the mdoc file is in this format: "PixelSpacing = 2.93" --> separate into key and value
              mdoc_key_value = mdoc_current_line.split("=")
              mdoc_current_line_key = mdoc_key_value[0].strip()
              mdoc_current_line_value = mdoc_key_value[1].strip()
              # if the current line holds the information we want as specified in the yaml), add it to the data dict
              # (keys = alias; value = value in meta data)
              if yaml_param_name == mdoc_current_line_key:
                # ImageSize contains both xdim and ydim in the mdoc file, have to split it up
                if mdoc_current_line_key == "ImageSize" and len(mdoc_current_line_value.split()) == 2:
                  xdim, ydim = mdoc_current_line_value.split()
                  # Add entries for both x and y dimensions
                  yaml_alias = "x dimensions"
                  return_mdoc_data[yaml_alias] = xdim
                  yaml_alias = "y dimensions"
                  return_mdoc_data[yaml_alias] = ydim
                else:      
                  return_mdoc_data[yaml_alias] = mdoc_current_line_value
  return(return_mdoc_data) 


def load_config(microscope):
  """
  reads the config_microscopes.yaml file, looks for the chosen microscope setup, and returns a list of dicts
  containing the parameters that are solely based on the setup.

  Args:
    microscope (str): the name of the microscope setup.

  Returns:
    entry["Parameters"] (list): a list of dicts, with each dict containing one parameter name and the associated value.

  Example:
    when the input is "Titan Krios 4", as it is when choosing this setup in the ui, the config_microscopes.yaml
    file will be opened and the list "microscopes" will be searched for a dict where the entry "Microscope" is 
    "Titan Krios 4". If this is found, the list saved under the key "Parameters" of the same dict, containing a 
    dict for every parameter solely determined by the setup (key = parameter, value = associated value), will be returned.
  """
  with open("../config/config_microscopes.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)
  # go through entries in the microscopes dict
  for entry in yaml_data["microscopes"]:
    # look for an entry that equals the selected microscope
    if entry["Microscope"] == microscope:
      # return the list (containing a dict for each parameter) at the entry Parameters
      return entry["Parameters"]


def locate_val(job_name:str, var:str, job_dict = "joboptions_values", column_variable = "rlnJobOptionVariable", column_value = "rlnJobOptionValue"):
  """
  locates the value defined of the dict defined in the job_star_dict dictionary so it can be displayed and edited.

  Args:
    job_name (str): job name as str as it's stated in the job_star_dict ("importmovies", "motioncorr", "ctffind", "aligntilts", "reconstruction").
    var (str): name of variable/parameter that should be changed (parameters as defined in the job.star files).
    job_dict (str): dataframe that should be accessed inside the job defined in job_name (standard input is the df containing the parameters).
    column_variable (str): column in the dataframe containing the parameters (standard input is the correct name).
    column_value (str): column in the dataframe containing the values assigned to each parameter (standard input is the correct name).

  Returns:
    str: value that is currently assigned to the defined parameter of the defined job.
  """
  val = job_star_dict[job_name][job_dict].loc[job_star_dict[job_name][job_dict][column_variable] == var, column_value].values[0]
  return val


def update_job_star_dict(job_name, param, value):
  """
  updates the job_star_dict dictionary (containing all .star files of the repective jobs) with the values provided.

  Args:
    job_name (str): job name as str as it's stated in the job_star_dict ("importmovies", "motioncorr", "ctffind", "aligntilts", "reconstruction").
    param (str): parameter that should be updated as str as it's called in the respective job.star file.
    value (str): new value that should be placed in the job.star file for the set parameter.

  Returns:
    job_star_dict with updated value for respective parameter.
  """
  index = job_star_dict[job_name]["joboptions_values"].index[job_star_dict[job_name]["joboptions_values"]["rlnJobOptionVariable"] == param]
  job_star_dict[job_name]["joboptions_values"].iloc[index, 1] = value
  return job_star_dict

def write_star(scheme_name, path_and_name):
  """
  reads a pd df and turns it into a .star file.

  Args:
    scheme_name (df): dataframe with the information of the star file.
    path_and_name (str): path (including file name) to where the new file should be saved.

  Returns:
    .star file: star file at the given path.

  """
  df_as_star = starfile.write(scheme_name, path_and_name)
  return df_as_star

# create a dict with the parameter names as keys and the names that should appear in the UI as values to 
# provide further explanation (e.g. qsub_extra2 doesn't tell the user what to give as input).
param_names = {
  "importmovies":{
    # all the parameters for importmovies
    "Cs": "Spherical aberration",
    "Q0": "Amplitude contrast",
    "angpix": "Pixel size in \u212B",
    #do_coords
    #do_coords_flipZ
    #do_flipYZ
    #do_flipZ
    #do_other
    "do_queue": "Add to external queue",
    #do_tiltseries
    #do_tomo
    #dose_is_per_movie_frame
    #dose_rate
    #flip_tiltseries_hand
    #fn_in_other
    #hand
    #images_are_motion_corrected
    #io_tomos
    "kV": "kV of Microscope",
    "mdoc_files": "Path to mdoc files",
    #min_dedicated
    "movie_files": "Path to images",
    #mtf_file
    #node_type
    #optics_group_particles
    #order_list
    #other_args
    #part_star
    #part_tomos
    #prefix
    "qsub": "q-submission script",
    #qsub_extra1
    #qsub_extra2
    #qsub_extra3
    #qsub_extra4
    #qsubscript
    #queuename
    #tilt_axis_angle
    #tomo_star
},
  "motioncorr":{
    # all parameters for motioncorr
    "bfactor": "B factor",
    "bin_factor": "Binning factor",
    "do_even_odd_split": "Split data for denoising",
    #do_float16
    #do_own_motioncor
    #do_queue
    #do_save_ps
    #eer_grouping
    #fn_defect
    #fn_gain_ref
    #fn_motioncor2_exe
    #gain_flip
    #gain_rot
    #gpu_ids
    #group_for_ps
    #group_frames
    #input_star_mics
    #min_dedicated
    #nr_mpi
    #nr_threads
    #other_args
    #other_motioncor2_args
    #patch_x
    #patch_y
    #qsub
    #qsub_extra1
    #qsub_extra2
    #qsub_extra3
    #qsub_extra4
    #qsubscript
    #queuename
},
  "ctffind":{
    # all parameters for ctffind
    "box": "Box size",
    #ctf_win
    #dast
    #dfmax
    #dfmin
    #dfstep
    #do_EPA
    #do_ignore_ctffind_params
    #do_phaseshift
    #do_queue
    #fn_ctffind_exe
    #fn_gctf_exe
    #gpu_ids
    #input_star_mics
    #min_dedicated
    #nr_mpi
    #other_args
    #other_gctf_args
    #phase_max
    #phase_min
    #phase_step
    #qsub
    #qsub_extra1
    #qsub_extra2
    #qsub_extra3
    #qsub_extra4
    #qsubscript
    #queuename
    #resmax
    #resmin
    #slow_search
    #use_ctffind4
    #use_gctf
    #use_given_ps
},
  "aligntilts":{

},
  "reconstruction":{

}
}

# create Sphinx documentation: sphinx-build -M html docs/ docs/
# remove everything in the _build: make clean
# update Sphinx documentation: make html