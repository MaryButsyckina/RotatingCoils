import Libs

from PySide6.QtWidgets import QDialog, QWidget, QGridLayout, QPushButton, QLabel, QListWidget, QAbstractItemView
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from Style import StyleSheets, Fonts, WarningLabels
from SaveConfigurationData import SavingTemplate
from SaveMeasurements import GraphTemplate, MeasTemplate, WordUtkinSextuple


class TemplatesWindow(QDialog):
    def __init__(self, meas_items, a_coef_volts, b_coef_volts, a_coef, b_coef, field, comments, is_sextuple):
        super(TemplatesWindow, self).__init__()

        self.a_coef_volts = a_coef_volts
        self.b_coef_volts = b_coef_volts
        self.a_coef = a_coef
        self.b_coef = b_coef
        self.field = field
        self.comments = comments
        self.is_sextuple = is_sextuple
        self.sextuple_utkin_data = {}

        self.central_widget = QWidget()
        self.main_layout = QGridLayout(self.central_widget)
        self.setLayout(self.main_layout)

        self.first_template = QPushButton()
        self.second_template = QPushButton()
        self.third_template = QPushButton()
        self.first_template_label = QLabel('Measurements')
        self.first_template_label.setFont(Fonts.small_headers())
        self.second_template_label = QLabel('Graph')
        self.second_template_label.setFont(Fonts.small_headers())
        self.third_template_label = QLabel('Passport for Utkin Sextuple')
        self.third_template_label.setFont(Fonts.small_headers())

        self.meas_list = QListWidget()
        self.error_status_label = QLabel('Error status')
        self.error_status_output = QLabel()
        self.back_button = QPushButton()

        self.main_layout.addWidget(self.first_template, 0, 0)
        self.main_layout.addWidget(self.second_template, 0, 1)
        self.main_layout.addWidget(self.third_template, 0, 2)
        self.main_layout.addWidget(self.first_template_label, 1, 0)
        self.main_layout.addWidget(self.second_template_label, 1, 1)
        self.main_layout.addWidget(self.third_template_label, 1, 2)
        self.main_layout.addWidget(self.meas_list, 0, 3, 4, 3)
        self.main_layout.addWidget(self.error_status_label, 3, 0)
        self.main_layout.addWidget(self.error_status_output, 4, 0)
        self.main_layout.addWidget(self.back_button, 4, 3)

        self.error_status_label.setFont(Fonts.small_headers())
        self.error_status_output.setFont(Fonts.small_headers())
        WarningLabels.style_1(self.error_status_label)
        WarningLabels.style_2(self.error_status_output)

        self.back_button.setIcon(QIcon('rightarrow.png'))
        self.back_button.setMinimumSize(100, 30)
        self.back_button.setMaximumSize(100, 30)
        self.back_button.clicked.connect(self.save_meas)

        self.meas_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.meas_list.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_central_widget(self)
        self.setWindowTitle('Templates')

        self.get_template(self.first_template, 'Saving_template1.PNG', 'Meas')
        self.get_template(self.second_template, 'Saving_templates2.PNG', 'Graph')
        self.get_template(self.third_template, 'Saving_templates2.PNG', 'Utkin_Sextuple')

        self.get_measurements(meas_items)


    def get_template(self, template, icon_path, template_name):
        template.setMinimumSize(250, 250)
        template.setMaximumSize(250, 250)
        template.setIcon(QIcon(icon_path))
        template.setIconSize(QSize(245, 245))
        StyleSheets.stylesheet_saving_template(template)
        template.clicked.connect(lambda: self.highlight_selected_template(template_name, template))


    def get_measurements(self, meas_items):
        for i in range(len(meas_items)):
            self.meas_list.addItem(meas_items[i])


    def highlight_selected_template(self, template_name, template):
        self.return_selected_template(template_name)
        StyleSheets.stylesheet_saving_template(self.first_template)
        StyleSheets.stylesheet_saving_template(self.second_template)
        StyleSheets.stylesheet_highlighted_template(template)

    @staticmethod
    def return_selected_template(template_name):
        SavingTemplate(template_name)


    def return_selected_meas(self):
        selected_meas = []
        for i in range(len(self.meas_list.selectedItems())):
            selected_meas.append(self.meas_list.row(self.meas_list.selectedItems()[i]))

        return selected_meas


    def collect_sextuple_utkin_data(self, x=0.0, y=0.0, i=0, angle=0.0, a=(), b=(), amp=()):
        parameters = {}
        measurements = {}
        self.sextuple_utkin_data['Parameters'] = parameters
        self.sextuple_utkin_data['Measurements'] = measurements

        def write_parameters():
            parameters['Lens_length'] = 12
            parameters['Radius'] = 1.5
            parameters['x'] = x
            parameters['y'] = y
            parameters['I'] = i
            parameters['Angle'] = angle

        def write_measurements():
            harms = {}
            measurements['Harm'] = harms

            def write_measurement(branch, n):
                branch['A'] = a[n]
                branch['B'] = b[n]
                branch['Amp'] = amp[n]
                branch['Rel'] = amp[n] / amp[2]

            for i in range(14):
                harms[i+1] = {}
                write_measurement(harms[i+1], i)


        write_parameters()
        write_measurements()


    def save_meas(self):
        template = None
        selected_meas = self.return_selected_meas()

        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        for elem in root[2].iter('SavingTemplate'):
            template = elem.text

        if template == 'Graph':
            GraphTemplate(selected_meas, self.a_coef_volts, self.b_coef_volts, self.comments, self.is_sextuple)
        elif template == 'Meas':
            MeasTemplate(selected_meas, self.a_coef, self.b_coef, self.field, self.comments, self.is_sextuple)
        elif template == 'Utkin_Sextuple':
            WordUtkinSextuple(self.sextuple_utkin_data)

        self.close()
