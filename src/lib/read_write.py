
import yaml
import starfile
import os

def readConfig(filename):
  """
  read a configuration file in yaml format

  :arguments: filename 
  :returns: dictioanry with paramName and data
  """
  with open(filename) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    
  return data    


def read_star(scheme_name):
  """
  reads a .star file and turns it into a pd df.

  Input:
  scheme_name = (path to) a star file.

  Output:
  data_as_df = dataframe with the information of the star file.

  """
  data_as_df = starfile.read(scheme_name)
  return data_as_df

path_to_scheme = "./master_scheme"

job_star_dict = {
    "importmovies": read_star(os.path.join(path_to_scheme, "importmovies/job.star")),
    "motioncorr": read_star(os.path.join(path_to_scheme, "motioncorr/job.star")),
    "ctffind": read_star(os.path.join(path_to_scheme, "ctffind/job.star")),
    "scheme_star": read_star(os.path.join(path_to_scheme, "scheme.star"))
}

def locate_val(job_name:str, var:str, job_dict = "joboptions_values", column_variable = "rlnJobOptionVariable", column_value = "rlnJobOptionValue"):
    """
    locates the value defined of the dict defined in the job_star_dict dictionary so it can be displayed and edited.

    Input:
    job_name = job name as str as it's stated in the job_star_dict ("importmovies", "motioncorr", "ctffind")
    var = name of variable/parameter that should be changed (parameters as defined in the job.star files)
    job_dict = dataframe that should be accessed inside the job defined in job_name (standard input is the df containing the parameters)
    column_variable = column in the dataframe containing the parameters (standard input is the correct name)
    column_value = column in the dataframe containing the values assigned to each parameter (standard input is the correct name)

    Output:
    val = value that is currently assigned to the defined parameter of the defined job
    """
    val = job_star_dict[job_name][job_dict].loc[job_star_dict[job_name][job_dict][column_variable] == var, column_value].values[0]
    return val

def write_star(scheme_name, path_and_name):
  """
  reads a pd df and turns it into a .star file.

  Input:
  scheme_name = dataframe with the information of the star file.
  path_and_name = path and name to where the new file should be saved.

  Output:
  df_as_star = star file at the given path.

  """
  df_as_star = starfile.write(scheme_name, path_and_name)
  return df_as_star


# create Sphinx documentation: sphinx-build -M html docs/ docs/
# remove everything in the _build: make clean
# update Sphinx documentation: make html