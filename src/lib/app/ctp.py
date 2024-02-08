import sys
import os
import subprocess
import pandas as pd
import yaml
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QApplication, QMainWindow, QDialog, QComboBox, QTabWidget, QWidget
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

"""
script_path = os.path.abspath(__name__)
script_dir = os.path.dirname(script_path)
"""
current_dir = os.path.dirname(os.path.abspath(__name__))
# change the path to be until src
src_dir = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(src_dir)

#from lib.functions import get_value_from_tab
from lib.read_write import scheme_star_dict, job_star_dict, jobs_in_scheme, get_alias, get_alias_reverse, load_config, read_mdoc, read_header, write_star

class MainUI(QMainWindow):
    """
    Main window of the UI.
    """
    def __init__(self):
        """
        Setting up the buttons in the code and connecting them to their respective functions.
        """ 
        super(MainUI, self).__init__()
        loadUi("ctp.ui", self)
        self.btn_makeJobTabs.clicked.connect(self.makeJobTabs)
        self.groupBox_in_paths.setEnabled(False)
        # have now put to textChanged --> every key entered updates it. If it takes too long to iterate every
        # time, change to editingFinished
        self.line_path_movies.textChanged.connect(self.loadPathMovies)
        self.line_path_mdoc.textChanged.connect(self.loadPathMdoc)
        self.btn_use_movie_path.clicked.connect(self.mdoc_use_movie_path)
        self.dropDown_config.addItem("Choose Microscope Set-Up")
        self.dropDown_config.addItem("Titan Krios 4")
        self.dropDown_config.addItem("Titan Krios 5")
        self.dropDown_config.activated.connect(self.loadConfig)
        self.btn_changeStarValues.clicked.connect(self.changeDf)
        self.btn_writeStar.clicked.connect(self.writeStar)


    def makeJobTabs(self):
        """
        insert a new tab for every job and place a table with the parameters found in the respective job.star
        file in the ["joboptions_values"] df.
        """
        # define where the new tabs should be inserted so all tabs can be used in order             
        first_insert_position = 1
        # loop through the jobs and create a tab for each job
        for job in jobs_in_scheme:
            # arguments: insertTab(index where it's inserted, widget that's inserted, name of tab)
            self.tabWidget.insertTab(first_insert_position, QWidget(), job)
            # build a table with the dataframe containinng the parameters for the respective job in the tab
            self.df = (job_star_dict[job]["joboptions_values"])
            nRows, nColumns = self.df.shape
            # create empty table with the dimensions of the df
            self.table = QTableWidget(self)
            self.table.setColumnCount(nColumns)
            self.table.setRowCount(nRows)
            self.table.setHorizontalHeaderLabels(("Parameter", "Value"))
            # this doesn't work yet...:
            #self.table.setMinimumSize(1500, 400)            
            # populate the table with the values of the df
            for row in range(nRows):
                for col in range(nColumns):
                    # set the value that should be added to the respective col/row combination in the df containing the parameters
                    current_value = self.df.iloc[row, col]
                    # see whether there is an alias for the parameter (only for the Parameters column)
                    if col == 0:
                        alias = get_alias(job, current_value)
                        # if there is an alias, set the widgetItem to this alias, else, do as normal
                        if alias != None:
                            self.table.setItem(row, col, QTableWidgetItem(alias))
                        else:
                            self.table.setItem(row, col, QTableWidgetItem(current_value))
                        # set the flag for this field as not editable --> people cannot accidentally change the 
                        # name of a parameter, inhibiting Relion later
                        self.table.item(row, col).setFlags(self.table.item(row, col).flags() & ~Qt.ItemFlag.ItemIsEditable)
                    else:
                        self.table.setItem(row, col, QTableWidgetItem(current_value))
            # set where this table should be placed
            tab_layout = QVBoxLayout(self.tabWidget.widget(first_insert_position))
            tab_layout.addWidget(self.table)
            #self.table.setMinimumSize(1500, 400)            
            first_insert_position += 1
        # make groupBox_in_paths available so it can only be used after the tabs are created (--> can load in data)
        self.groupBox_in_paths.setEnabled(True)


    def loadPathMovies(self):
        """
        set the parameter path to files in the importmovies job to the link provided here. Then, look into the 
        header of the movies provided and copy the respective information to the respective parameters too.
        """
        # save the input of the field as variable
        params_dict_movies = {"movie_files": self.line_path_movies.text() + "*.eer"}

        # reading the header doesn't work yet!
        """
        # look into the header and save all parameters as variables
        try:
            header_eers = read_header(params_dict_movies["movie_files"])

            index_import = jobs_in_scheme[jobs_in_scheme == "importmovies"].index

            self.tabWidget.setCurrentIndex(index_import.item())
            table_widget = self.tabWidget.currentWidget().findChild(QTableWidget)
            nRows = table_widget.rowCount()
            for row in range(nRows):
                current_param = table_widget.item(row, 0).text()
                # if the param we are looking for is equal to the param in the row in the table, change the
                # value in that table to the value to the value of the dict (path or header information).
                # Additionally, change the colour of the field to clarify that this has been automatically set.
                if current_param == "Pixel in A":
                    pixel_size = table_widget.item(row, 1).text()

                # exposure time and dose per ang in mdoc

               exposure_times, dose_per_angstrom, eer_sections
            # dose per frame from input if I want to change
            eer_sections = calculate_dose_rate_per_pixel(pixel_size, header_eers)

            params_dict_movies[""] = eer_sections
            print(header_eers)
        except:
            pass
        # create a combined dict to iterate over
        #params_dict_movies.update(header_params)
        """
        # go to the importmovies tab by getting the index where importmovies is
        # if header also has parameters for other jobs, have to loop through here
        index_import = jobs_in_scheme[jobs_in_scheme == "importmovies"].index  
        self.tabWidget.setCurrentIndex(index_import.item())
        # find the  copy the text of the input field to the path to file, check for aliases of the field, and
        # iterate over the parameters of the header to input them too
        table_widget = self.tabWidget.currentWidget().findChild(QTableWidget)
        nRows = table_widget.rowCount()
        for param, value in params_dict_movies.items():
            # look for any aliases for the params and if one is present, set the param to this alias
            for job in jobs_in_scheme:
                original_param_name = get_alias(job, param)
                if original_param_name != None:
                    param = original_param_name
                # go through the rows in the table and look for the parameter to be set  
                for row in range(nRows):
                    current_param = table_widget.item(row, 0).text()
                    # if the param we are looking for is equal to the param in the row in the table, change the
                    # value in that table to the value to the value of the dict (path or header information).
                    # Additionally, change the colour of the field to clarify that this has been automatically set.
                    if current_param == param:
                        table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
                        table_widget.item(row, 1).setBackground(QColor(200, 200, 200))
                        # could also change colour depending on origin of data --> could identify
                        #table_widget.item(row, 1).setBackground(QColor(0, 200, 0))

        # go back to setup tab
        self.tabWidget.setCurrentIndex(0)


    def loadPathMdoc(self):
        """
        set the parameter path to mdoc in the importmovies job to the link provided here. Then, look into the 
        mdoc file and copy the respective information to the respective parameters too.
        """
        # save the input of the field as variable
        params_dict_mdoc = {"mdoc_files": self.line_path_mdoc.text() + "*.mdoc"}
        # look into the mdoc file and save all parameters as variables
        try:
            params_dict_mdoc.update(read_mdoc(params_dict_mdoc["mdoc_files"]))
        except:
            pass
        # go to the importmovies tab by getting the index where importmovies is
        # if mdoc also has parameters for other jobs, have to loop through here
        for current_tab in jobs_in_scheme:
            index_import = jobs_in_scheme[jobs_in_scheme == current_tab].index
            self.tabWidget.setCurrentIndex(index_import.item())
            # find the  copy the text of the input field to the path to file, check for aliases of the field, and
            # iterate over the parameters of the header to input them too
            table_widget = self.tabWidget.currentWidget().findChild(QTableWidget)
            nRows = table_widget.rowCount()
            for param, value in params_dict_mdoc.items():
                # look for any aliases for the params and if one is present, set the param to this alias
                for job in jobs_in_scheme:
                    original_param_name = get_alias(job, param)
                    if original_param_name != None:
                        param = original_param_name
                    # go through the rows in the table and look for the parameter to be set  
                    for row in range(nRows):
                        current_param = table_widget.item(row, 0).text()
                        # if the param we are looking for is equal to the param in the row in the table, change the
                        # value in that table to the value to the value of the dict (path or header information).
                        # Additionally, change the colour of the field to clarify that this has been automatically set.
                        if current_param == param:
                            table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
                            table_widget.item(row, 1).setBackground(QColor(200, 200, 200))
                            # could also change colour depending on origin of data --> could identify
                            #table_widget.item(row, 1).setBackground(QColor(200, 0, 0))

        # go back to setup tab
        self.tabWidget.setCurrentIndex(0)


    def mdoc_use_movie_path(self):
        self.line_path_mdoc.setText(self.line_path_movies.text())


    def loadConfig(self):
        """
        go through all parameters of all tabs and see whether any parameter is in the config_microscopes file
        (= contains all parameters that are solely dependent on the setup) under the chosen setup. If a parameter
        is found, its value is set to the value defined in the config_microscopes for this parameter.
        """
        microscope = self.dropDown_config.currentText()
        # only do something if a microscope is chosen
        if microscope != "Choose Microscope Set-Up":
            microscope_parameters = load_config(microscope)
            # exclude the first tab (= set up)
            for job_tab_index in range(1, len(jobs_in_scheme) + 1):
                #job_name = self.tabWidget.tabText(job_tab)
                # go to the tabs based on their index
                self.tabWidget.setCurrentIndex(job_tab_index)
                # access the TableWidget in the currently open TabWidget
                table_widget = self.tabWidget.currentWidget().findChild(QTableWidget)
                nRows = table_widget.rowCount()
                # iterate through the table and access each row
                for row in range(nRows):
                    # set current_param to the parameter in the current row
                    current_param = table_widget.item(row, 0).text()
                    # microscope_parameters is a list of dicts so have to access these dicts first.
                    for dicts in microscope_parameters:
                        # iterate over the parameters and values of the config file. If the param is the same as the 
                        # current param, set the according value in the table to the value set in the config file.
                        for param, value in dicts.items():
                            if param == current_param:
                                # PyQt/QTableWidgetItem can only set str
                                table_widget.setItem(row, 1, QTableWidgetItem(str(value))) 
                                table_widget.item(row, 1).setBackground(QColor(200, 200, 200))
            # in the end, go back to the start tab from where the command was started
            self.tabWidget.setCurrentIndex(0)


    def changeDf(self):
        """
        go through all tabs that were created using the makeJobTabs function, select the table that is in that tab
        and iterate through the columns and rows of that table, checking whether there is an alias (and reverting
        it if there is) and then writing the value into the df for the job.star file at the same position as it 
        is in the table (table is created based on this df so it should always be the same position and name). 
        """
        # exclude the first tab (= set up)
        for job_tab_index in range(1, len(jobs_in_scheme) + 1):
            # save the name of the job based on the index (tabs also created in order of the index --> is the same)
            job = jobs_in_scheme[job_tab_index]
            #job_name = self.tabWidget.tabText(job_tab)
            # go to the tabs based on their index
            self.tabWidget.setCurrentIndex(job_tab_index)
            # access the TableWidget in the currently open TabWidget
            table_widget = self.tabWidget.currentWidget().findChild(QTableWidget)

            nRows = table_widget.rowCount()
            nColumns = table_widget.columnCount()
            # iterate through the table and access each row
            for row in range(nRows):
                for col in range(nColumns):
                    # set the value to the text in the respective field (determined by row and col index)
                    value = table_widget.item(row, col).text()
                    # check whether there is an alias for a parameter name and if yes, change back to original name 
                    if col == 0:
                        original_param_name = get_alias_reverse(job, value)
                        if original_param_name != None:
                            # param_name = original_param_name
                            value = original_param_name     
                    # insert value at the position defined by the index of the table
                    job_star_dict[job]["joboptions_values"].iloc[row, col] = value

        # in the end, go back to the start relion tab from where the command was started (range excludes last entry)
        self.tabWidget.setCurrentIndex(len(jobs_in_scheme) + 1)


    def writeStar(self):
        """
        write the star file with the coordinates given and with the values of job_star_dict.
        so far works only if the directory doesn't exist yet.
        can be made into a pop-up window later.
        """
        # set the location for the new project to the link set in the respective field
        self.path_to_new_project = self.line_path_new_project.text()

        # create the master_scheme dict (where all other jobs are in) at the position set
        path_scheme_star = os.path.join(self.path_to_new_project, "Schemes/master_scheme/scheme.star")
        # make a directory with this path and raise an error if such a directory already exists
        os.makedirs(path_scheme_star, exist_ok=False)
        write_star(scheme_star_dict, path_scheme_star)

        # repeat for all jobs, creating a job.star file in these directories
        for job in jobs_in_scheme:
            path = os.path.join(self.path_to_new_project, f"Schemes/master_scheme/{job}/job.star")
            os.makedirs(path, exist_ok=False)
            job_star = job_star_dict[job]
            write_star(job_star, path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec()