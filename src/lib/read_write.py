
import yaml
import os
import starfile

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

path_to_scheme = "/fs/gpfs41/lv01/fileset02/pool/pool-plitzko3/Michael/00-Other/CryoTheraPy/src/lib/app/master_scheme_bck"
scheme_star_dict = read_star(path_to_scheme + "/scheme.star")
# create a pd.series from the edges in the scheme.star (= the order of jobs that are executed), removing the
# first and the last as they are usually EXIT_maxtime and WAIT, i.e. not jobs
jobs_in_scheme = scheme_star_dict["scheme_edges"].rlnSchemeEdgeOutputNodeName.iloc[1:-1]

job_star_dict = {
  f"{job}": read_star(os.path.join(path_to_scheme, f"{job}/job.star"))
  for job in jobs_in_scheme
}
job_star_dict["scheme_star"] = scheme_star_dict

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

param_names = {
  "importmovies":{
    # all the parameters for importmovies
    "Q0": "Amplitude contrast",
    "angpix": "Pixel size in \u212B",
    #do_coords
    #do_coords_flipZ
    #do_flipYZ
    #do_flipZ
    #do_other
    #do_queue
    #do_tiltseries
    #do_tomo
    #dose_is_per_movie_frame
    #dose_rate
    #flip_tiltseries_hand
    #fn_in_other
    #hand
    #images_are_motion_corrected
    #io_tomos
    #kV
    #mdoc_files
    #min_dedicated
    #movie_files
    #mtf_file
    #node_type
    #optics_group_particles
    #order_list
    #other_args
    #part_star
    #part_tomos
    #prefix
    #qsub
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
    #bin_factor
    #do_even_odd_split
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