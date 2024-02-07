# have to be able to import new scheme.star files too so an already started (but stopped) run can be resumed
# should also change it so it doesn't crash everytime there is something going on that doesn't work. Maybe just write an error instead aborting. For that, I have to wrap everything into a try: ... else:  loop, so every error is cought by the else and I can just say pritn error there
import sys
import os
import subprocess
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QComboBox, QTabWidget

current_dir = os.path.dirname(os.path.abspath(__name__))
src_dir = os.path.abspath(os.path.join(current_dir, '../..'))
# change the path to be until src
sys.path.append(src_dir)

from lib.read_write import job_star_dict, locate_val, jobs_in_scheme, param_names, update_job_star_dict, load_config, write_star
from lib.config import titan_krios_4, titan_krios_5

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
        dropDown_config = QComboBox(self)
        self.dropDown_config.addItem("Choose Microscope Set-Up")
        self.dropDown_config.addItem("Titan Krios 4")
        self.dropDown_config.addItem("Titan Krios 5")
        self.dropDown_config.activated.connect(self.loadConfig)

        #these two don't work yet bc the schemer requires a different version of python
        #self.btn_start.clicked.connect(self.start_relion)
        #self.btn_python2.clicked.connect(self.switch_python)

    def readStar(self):
        """
        Populate the line edits based on the values in the dataframe.
        """        
        for job_name in jobs_in_scheme:
            # iterate over all parameters in a job.star file
            for i, (index, param) in enumerate(job_star_dict[job_name]["joboptions_values"]["rlnJobOptionVariable"].items()):
                # accessing the respective label and line
                label_name = f"lbl_{job_name}_{i}"
                line_name = f"line_{job_name}_{i}"
                line = getattr(self, line_name)
                # set the value in the line to the current value in the job.star file associated to the repective parameter
                line.setText(locate_val(job_name, f"{param}"))
                label = getattr(self, label_name)
                try:
                    # see if there is a label name in the param_names dict (increases clarity for the user as eg. "qsub_extra1" doesn't tell the user what the input should be)
                    if param in param_names[job_name]:
                        param = param_names[job_name][param]
                    label.setText(param)
                except:
                    try:
                        # set the respective label to the respective parameter name
                        label.setText(locate_val(job_name, f"{param}", column_value="rlnJobOptionVariable"))
                    except:
                        # print the parameter name and the parameter if it has not been loaded into the ui (i.e. is missing)
                        print(f"could not import label {label_name} {param}")
                        print(f"could not import value {line_name} {param}")
                        #raise AssertionError("not all parameters could be loaded")
            # change values based on microscope used to respective values

    def loadConfig(self):
        """
        load in the values for the corresponding microscope depending on the option selected from the drop-down
        """
        #load_config("Titan Krios 4")
        #load_confg(titan_krios_4)     
        # make this all into a function and have only the dict name as input --> can easily add new
        if self.dropDown_config.currentText() == "Titan Krios 4":
            for param, value in titan_krios_4.items():
                #print(param)
                for job_name in job_star_dict.keys():
                    if job_name != "scheme_star":
                        # iterate over the number of parameters in each job to check every label (one label was set for each param)
                        for i in range(0, 2):
                            current_lbl = f"lbl_{job_name}_{i}"
                            current_label = getattr(self, current_lbl)
                            current_label_text = current_label.text()
                            #print(current_label_text)
                            #print(param)
                            if current_label_text == param:
                                line_name = f"line_{job_name}_{i}"
                                line = getattr(self, line_name)
                                line.setText(value)
                                break

        elif self.dropDown_config.currentText() == "Titan Krios 5":
            for param, value in titan_krios_5.items():
                #print(param)
                for job_name in job_star_dict.keys():
                    if job_name != "scheme_star":
                        # iterate over the number of parameters in each job to check every label (one label was set for each param)
                        for i in range(0, 2):
                            current_lbl = f"lbl_{job_name}_{i}"
                            current_label = getattr(self, current_lbl)
                            current_label_text = current_label.text()
                            #print(current_label_text)
                            #print(param)
                            if current_label_text == param:
                                line_name = f"line_{job_name}_{i}"
                                line = getattr(self, line_name)
                                line.setText(value)
                                break

    def changeStarValues(self):
        """
        function to change the value of the given parameter in the given job.
        """
        for job_name in jobs_in_scheme:
            for i in range(0, len(job_star_dict[job_name]["joboptions_values"])):
                # accessing the respective labels
                current_lbl = f"lbl_{job_name}_{i}"
                current_label = getattr(self, current_lbl)
                current_label_text = current_label.text()
                #print(current_label_text)
                # checks to which parameter in the job.star file the label refers to by looking for the key (= original name of parameter in the job.star file) associated to the value (= given/displayed name of label) in the param_names dict
                # --> after this step, al the labels should be their original name again
                if current_label_text in param_names[job_name].values():
                        for key, value in param_names[job_name].items():
                            if value == current_label_text:
                                current_label_text = key
                                #print(current_label_text)
                # the same as for the labels is done for the values too, excluding the changing of names
                current_ln = f"line_{job_name}_{i}"
                current_line = getattr(self, current_ln)
                current_line_text = current_line.text()
                #print(current_line_text)
                update_job_star_dict(job_name, current_label_text, current_line_text)
        #print(job_star_dict)
                

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
