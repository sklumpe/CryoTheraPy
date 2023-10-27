
import yaml

def readConfig(filename):
  """
  read a configuration file in yaml format

  :arguments: filename 
  :returns: dictioanry with paramName and data
  """
  with open(filename) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    
  return data    
