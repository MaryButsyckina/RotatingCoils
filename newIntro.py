import sys

from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QPushButton, QListWidget, QTextEdit, QLineEdit, QWidget, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon

from Style import Labels, StyleSheets, Fonts, WarningLabels


class IntroWindowInterface(object):
    def setWidget(self, IntroWindow):
        super(IntroWindowInterface, self).__init__()

        self.central_widget = QWidget(IntroWindow)
        IntroWindow.setCentralWidget(self.central_widget)

        self.open_file_button = QToolButton()

        self.open_file_layout = QHBoxLayout()
        self.left_layout = QGridLayout()
        self.right_layout = QVBoxLayout()
        self.select_meas = QGridLayout()
        self.main_layout = QGridLayout(self.central_widget)
        self.open_config_layout = QHBoxLayout()

        self.main_layout.addLayout(self.left_layout, 0, 0)
        self.main_layout.addLayout(self.right_layout, 0, 1)

        self.left_layout.addLayout(self.open_file_layout, 0, 0)

        self.open_file_layout.addWidget(self.open_file_button)

        self.open_file_label = QLabel('Open File')
        self.open_file_layout.addWidget(self.open_file_label)

        self.path_file_output = QLabel()
        self.left_layout.addWidget(self.path_file_output, 1, 0)

        self.coil_parameter_label = QLabel('Coils Parameters')
        self.left_layout.addWidget(self.coil_parameter_label, 2, 0)

        self.open_config_button = QToolButton()
        self.open_config_layout.addWidget(self.open_config_button)

        self.open_config_label = QLabel('Configuration File')
        self.open_config_layout.addWidget(self.open_config_label)

        self.left_layout.addLayout(self.open_config_layout, 3, 0)

        self.open_config_output = QLabel()
        self.left_layout.addWidget(self.open_config_output, 4, 0)

        self.new_config_button = QPushButton('Create new config file')
        self.left_layout.addWidget(self.new_config_button, 5, 0)

        self.ok_button = QPushButton('Ok')
        self.left_layout.addWidget(self.ok_button, 6, 0)

        self.is_sextuple = QCheckBox('Sextuple')
        self.left_layout.addWidget(self.is_sextuple, 7, 0)

        self.empty_label = QLabel()
        self.left_layout.addWidget(self.empty_label, 8, 0, 10, 0)

        self.meas_list_label = QLabel('Select measurement')
        self.right_layout.addWidget(self.meas_list_label)

        self.meas_list = QListWidget()
        self.select_meas.addWidget(self.meas_list, 0, 0, 5, 3)

        self.meas_comments = QTextEdit('Comment:')
        self.select_meas.addWidget(self.meas_comments, 0, 3, 1, 4)

        self.start_label = QLabel('Start with')
        self.select_meas.addWidget(self.start_label, 1, 3)
        self.right_layout.addLayout(self.select_meas)

        self.last_label = QLabel('End with')
        self.select_meas.addWidget(self.last_label, 2, 3)

        self.step = QLabel('Step')
        self.select_meas.addWidget(self.step, 3, 3)

        self.start_input = QLineEdit()
        self.select_meas.addWidget(self.start_input, 1, 4)

        self.last_input = QLineEdit()
        self.select_meas.addWidget(self.last_input, 2, 4)

        self.step_input = QLineEdit()
        self.select_meas.addWidget(self.step_input, 3, 4)

        self.submit_button = QPushButton('Ok')
        self.select_meas.addWidget(self.submit_button, 4, 3)

        self.select_all = QPushButton('Select All')
        self.select_meas.addWidget(self.select_all, 4, 4)

        self.next_page_button = QPushButton()
        self.select_meas.addWidget(self.next_page_button, 5, 6)

        self.error_status_label = QLabel('Error Status')
        self.left_layout.addWidget(self.error_status_label, 15, 0)

        self.error_status_output = QLabel()
        self.left_layout.addWidget(self.error_status_output, 16, 0)

        self.style_window(IntroWindow)


    def style_window(self, IntroWindow):
        IntroWindow.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        IntroWindow.setGeometry(470, 300, 1000, 500)

        self.next_page_button.setIcon(QIcon('rightarrow.png'))

        StyleSheets.stylesheet_central_widget(IntroWindow)
        Labels.output(self.path_file_output)
        Labels.output(self.open_config_output)

        self.open_file_label.setMinimumSize(400, 25)
        self.open_file_label.setMaximumSize(400, 25)
        self.open_file_label.setFont(Fonts.small_headers())

        self.path_file_output.setMinimumSize(450, 25)
        self.path_file_output.setMaximumSize(450, 25)
        self.path_file_output.setFont(Fonts.plain_text())

        self.coil_parameter_label.setFont(Fonts.big_headers())
        self.coil_parameter_label.setMinimumSize(400, 25)
        self.coil_parameter_label.setMaximumSize(400, 25)

        self.open_config_label.setFont(Fonts.small_headers())
        self.open_config_label.setMinimumSize(400, 25)
        self.open_config_label.setMaximumSize(400, 25)

        self.open_config_output.setFont(Fonts.plain_text())
        self.open_config_output.setMinimumSize(450, 25)
        self.open_config_output.setMaximumSize(450, 25)

        self.new_config_button.setMaximumSize(150, 25)
        self.new_config_button.setMinimumSize(150, 25)
        self.new_config_button.setFont(Fonts.button_text())

        self.ok_button.setMaximumSize(80, 25)
        self.ok_button.setFont(Fonts.button_text())

        self.meas_list_label.setFont(Fonts.big_headers())

        self.meas_list.setFont(Fonts.plain_text())
        self.meas_list.setMinimumSize(300, 0)
        self.meas_list.setMaximumSize(300, 10000)

        self.meas_comments.setFont(Fonts.plain_text())

        self.start_label.setFont(Fonts.plain_text())
        self.last_label.setFont(Fonts.plain_text())
        self.step.setFont(Fonts.plain_text())

        self.start_label.setMaximumSize(60, 25)
        self.last_label.setMaximumSize(60, 25)
        self.step_input.setMaximumSize(60, 25)

        self.start_input.setMaximumSize(50, 25)
        self.last_input.setMaximumSize(50, 25)
        self.step_input.setMaximumSize(50, 25)

        self.start_input.setFont(Fonts.plain_text())
        self.last_input.setFont(Fonts.plain_text())
        self.step.setFont(Fonts.plain_text())

        self.submit_button.setFont(Fonts.button_text())
        self.submit_button.setMaximumSize(80, 25)

        self.open_config_button.setText('...')
        self.open_file_button.setText('...')

        self.error_status_label.setFont(Fonts.small_headers())
        WarningLabels.style_1(self.error_status_label)
        self.error_status_label.setMaximumSize(90, 25)

        self.error_status_output.setFont(Fonts.small_headers())
        WarningLabels.style_2(self.error_status_output)
        self.error_status_output.setMaximumSize(400, 25)

        self.select_all.setFont(Fonts.button_text())

        self.is_sextuple.setFont(Fonts.button_text())
