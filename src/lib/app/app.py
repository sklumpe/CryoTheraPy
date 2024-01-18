# have to be able to import new scheme.star files too so an already started (but stopped) run can be resumed
# should also change it so it doesn't crash everytime there is something going on that doesn't work. Maybe just write an error instead aborting. For that, I have to wrap everything into a try: ... else:  loop, so every error is cought by the else and I can just say pritn error there
import sys
import os
import subprocess
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog

current_dir = os.path.dirname(os.path.abspath(__name__))
src_dir = os.path.abspath(os.path.join(current_dir, '../..'))
# change the path to be until src
sys.path.append(src_dir)

from lib.read_write import write_star, job_star_dict, locate_val, jobs_in_scheme, param_names

class MainUI(QMainWindow):
    """
    Main window of the UI.
    """
    def __init__(self):
        """
        Setting up the buttons in the code and connecting them to their respective functions.
        """ 
        super(MainUI, self).__init__()
        loadUi("cryotheraPy.ui", self)
        self.btn_readStar.clicked.connect(self.readStar)
        self.btn_changeStarValues.clicked.connect(self.changeStarValues)
        self.btn_writeStar.clicked.connect(self.writeStar)
        #these two don't work yet bc the schemer requires a different version of python
        #self.btn_start.clicked.connect(self.start_relion)
        #self.btn_python2.clicked.connect(self.switch_python)

    def readStar(self):
        """
        Populate the line edits based on the values in the dataframe.
        """
        #self.lbl_path.setText(locate_val("importmovies", "movie_files", column_value= "rlnJobOptionVariable"))
        #self.line_imp_pix_size.setText(locate_val("importmovies", "angpix"))
        #self.line_imp_path.setText(locate_val("importmovies", "movie_files"))
        #self.line_imp_meta.setText(locate_val("importmovies", "mdoc_files"))
        #self.line_imp_qsub.setText(locate_val("importmovies", "qsubscript"))
        #self.line_motioncorr_1.setText(locate_val("motioncorr", "qsubscript"))
        #self.line_motioncorr_2.setText(locate_val("motioncorr", "eer_grouping"))
        
        for job_name in jobs_in_scheme:
            for i, (index, param) in enumerate(job_star_dict[job_name]["joboptions_values"]["rlnJobOptionVariable"].items()):
                label_name = f"lbl_{job_name}_{i + 1}"
                line_name = f"line_{job_name}_{i + 1}"
                try:
                    label = getattr(self, label_name)
                    if param in param_names:
                        param = param_names[param]
                    label.setText(locate_val(job_name, f"{param}", column_value="rlnJobOptionVariable"))
                    line = getattr(self, line_name)
                    line.setText(locate_val(job_name, f"{param}"))
                except:
                    print(f"could not import label {label_name} {param}")
                    print(f"could not import value {line_name} {param}")
                    raise AssertionError("not all parameters could be loaded")
                
    def changeStarValues(self):
        """
        function to change the value of the given parameter in the given job.
        Currently, one line has to be written for each parameter that's supposed to be changed.
        """
        def coor(self, job, param, value):
            index = job_star_dict[job]["joboptions_values"].index[job_star_dict[job]["joboptions_values"]["rlnJobOptionVariable"] == param]
            job_star_dict[job]["joboptions_values"].iloc[index, 1] = value
            return job_star_dict
        value_angpix = self.line_imp_pix_size.text()
        coor(self, "importmovies", "angpix", value_angpix)
        value_movie_files = self.line_imp_path.text()
        coor(self, "importmovies", "movie_files", value_movie_files)
        value_mdoc_files = self.line_imp_meta.text()
        coor(self, "importmovies", "mdoc_files", value_mdoc_files)
        value_qsub = self.line_imp_qsub.text()
        coor(self, "importmovies", "qsubscript", value_qsub)

        coor(self, "motioncorr", "qsubscript", value_qsub)
        value_eer_grouping = self.line_mcorr_eer.text()
        coor(self, "motioncorr", "eer_grouping", value_eer_grouping)
        
        print(job_star_dict)

    def writeStar(self):
        """
        write the star file with the coordinates given and with the values of job_star_dict.
        so far works only if the directory doesn't exist yet.
        can be made into a pop-up window later.
        """
        self.path_to_new_project = self.line_path_new_project.text()
        
        path_scheme_star = os.path.join(self.path_to_new_project, "Schemes/master_scheme/scheme.star")
        path_import = os.path.join(self.path_to_new_project, "Schemes/master_scheme/importmovies/job.star")
        os.makedirs(path_import, exist_ok=True)
        path_motioncorr = os.path.join(self.path_to_new_project, "Schemes/master_scheme/motioncorr/job.star")
        os.makedirs(path_motioncorr, exist_ok=True)
        path_ctffind = os.path.join(self.path_to_new_project, "Schemes/master_scheme/ctffind/job.star")
        os.makedirs(path_ctffind, exist_ok=True)
        scheme_star = job_star_dict["scheme_star"]
        job_star_import = job_star_dict["importmovies"]
        job_star_motioncorr = job_star_dict["motioncorr"]
        job_star_ctffind = job_star_dict["ctffind"]
        write_star(scheme_star, path_scheme_star)
        write_star(job_star_import, path_import)
        write_star(job_star_motioncorr, path_motioncorr)
        write_star(job_star_ctffind, path_ctffind)
"""
    def switch_python(self):
        subprocess.run("module load ANACONDA/2/2019.10", shell=True)

    def start_relion(self):
        subprocess.run("rm -rf .relion_lock_master_scheme")
        subprocess.run("relion_schemer --scheme master_scheme --reset")
        subprocess.run("relion_schemer --scheme master_scheme --set_current_node WAIT")
        subprocess.run("relion_schemer --scheme master_scheme --run --pipeline_control Schemes/master_scheme/ >> Schemes/master_scheme/run.out 2>> Schemes/master_scheme/run.err")
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec()
