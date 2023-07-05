import Libs
from PySide6.QtWidgets import QMainWindow, QFileDialog, QAbstractItemView
from PySide6.QtCore import QItemSelectionModel

from Get_data import GetMainData, GetConfigData
from ConfigWindowInterface import ConfigWindow
from newIntro import IntroWindowInterface
from SaveConfigurationData import SavePathOfFile, SavePathOfConfigurationFile


class IntroWindow(QMainWindow):
    def __init__(self):
        super(IntroWindow, self).__init__()
        self.ui = IntroWindowInterface()
        self.ui.setWidget(self)

        self.ui.meas_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.N = None

        self.get_previous_path()
        self.add_functions()

        self.doc = None
        self.config_doc = None
        self.selected_meas = []
        self.sextuple = False


    def get_previous_path(self):
        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        for elem in root[0].iter('PathOfFile'):
            self.ui.path_file_output.setText(elem.text)
        for elem in root[1].iter('PathOfConfig'):
            self.ui.open_config_output.setText(elem.text)


    def add_functions(self):
        self.ui.open_file_button.clicked.connect(self.open_file)
        self.ui.open_file_button.clicked.connect(self.parse_file)

        self.ui.open_config_button.clicked.connect(self.open_config_file)
        self.ui.open_config_button.clicked.connect(self.parse_config_file)

        self.ui.select_all.clicked.connect(self.select_all_meas)
        self.ui.submit_button.clicked.connect(self.select_meas_with_range)
        self.ui.ok_button.clicked.connect(self.parse_file)
        self.ui.ok_button.clicked.connect(self.parse_config_file)
        self.ui.meas_list.itemClicked.connect(self.full_comment)

        self.ui.new_config_button.clicked.connect(self.create_config)


    def open_file(self):
        self.ui.error_status_output.setText('')
        PathOfFile, _ = QFileDialog.getOpenFileName(self)
        self.ui.path_file_output.setText(f'{PathOfFile}')
        SavePathOfFile(PathOfFile)


    def parse_file(self):
        PathOfFile = self.ui.path_file_output.text()
        self.doc = GetMainData.parse_data(PathOfFile)
        if type(self.doc) == str:
            self.ui.error_status_output.setText(self.doc)
        else:
            self.full_measlist()


    def open_config_file(self):
        PathOfConfigFile, _ = QFileDialog.getOpenFileName(self)
        self.ui.open_config_output.setText(f'{PathOfConfigFile}')
        SavePathOfConfigurationFile(PathOfConfigFile)


    def parse_config_file(self):
        PathOfConfigFile = self.ui.open_config_output.text()
        self.config_doc = GetConfigData.parse_config_data(PathOfConfigFile)
        if type(self.config_doc) == str:
            self.ui.error_status_label.setText(self.config_doc)


    def full_measlist(self):
        self.ui.meas_list.clear()
        self.N = GetMainData.get_num_of_meas(self.doc)
        for n in range(len(self.N)):
            self.ui.meas_list.addItem(f'{n+1}. {self.doc["Magnet"]["Measurements"][n]["Name"]}')


    def full_comment(self):
        for i in range(len(self.ui.meas_list.selectedItems())):
            self.ui.meas_comments.setText(f'Comment:\n{self.ui.meas_list.row(self.ui.meas_list.selectedItems()[i]) + 1}. {self.doc["Magnet"]["Measurements"][self.ui.meas_list.row(self.ui.meas_list.selectedItems()[i])]["Comments"]}')


    def select_all_meas(self):
        for i in range(len(self.N)):
            self.ui.meas_list.setCurrentRow(i, QItemSelectionModel.Select)


    def select_meas_with_range(self):
        self.ui.error_status_output.setText('')

        try:
            N_start = int(self.ui.start_input.text()) - 1
            N_last = int(self.ui.last_input.text()) - 1
            Step = int(self.ui.start_input.text())
        except ValueError:
            self.ui.error_status_output.setText('Meas number and step take only positive integers')
        else:
            if N_start > len(self.N) or N_last > len(self.N):
                self.ui.error_status_output.setText('Meas Number out of range')
            if N_start < 0 or N_last < 0 or Step < 0:
                self.ui.error_status_output.setText('Meas number and step take only positive integers')
            if N_start < N_last:
                if N_start+Step < N_last:
                    for i in range(N_start, N_last+1, Step):
                        self.ui.meas_list.setCurrentRow(i, QItemSelectionModel.Select)
                else:
                    self.ui.error_status_output.setText('Step is out the first-last meas border')
            elif N_start == N_last:
                self.ui.error_status_output.setText('Last meas equal to first meas')
            else:
                self.ui.error_status_output.setText('Last meas before first meas')


    def submit_meas(self):
        self.selected_meas = []
        items = self.ui.meas_list.selectedItems()
        for i in range(len(items)):
            self.selected_meas.append(self.ui.meas_list.row(self.ui.meas_list.selectedItems()[i]))


    def is_sextuple(self):
        self.sextuple = self.ui.is_sextuple.isChecked()


    @staticmethod
    def create_config():
        config_window = ConfigWindow()
        config_window.show()
        config_window.exec()


class Exceptions:
    @staticmethod
    def is_any_meas_selected(selected_meas):
        return False if not selected_meas else True

    @staticmethod
    def is_empty_file(selected_meas, doc):
        try:
            for i in selected_meas:
                index = i
                x = doc['Magnet']['Measurements'][i]['Data']['item'][1]['value']['ArrayOfMeasurementData'][
                                'MeasurementData'][0]['Data']
        except TypeError:
            return True, index + 1

        return False, None


    @staticmethod
    def is_config_file(window):
        try:
            window.parse_config_file()
        except FileNotFoundError:
            return False

        return True
