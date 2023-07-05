from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QTabWidget, QGridLayout, QListWidget, QPushButton, QHBoxLayout, QTextEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
import Libs

from Mathematics import SignalFromCoils, FieldCoefficients, Field, Displacement, PolesGeometry
from SignalTabInterface import SignalTab
from Harmonics import Harmonics
from DisplacementTabInterface import DisplacementTab
from Poles import Poles
from Style import StyleSheets, Fonts, Labels
from Get_data import GetConfigData
from SavingTemplates import TemplatesWindow


class TabWindow(QDialog):
    def __init__(self, doc, config_doc, selected_meas, is_sextuple):
        super(TabWindow, self).__init__()

        self.main_layout = QGridLayout()
        self.intro_window = None

        self.EMF = []
        self.Signal = []
        self.Field_A_Harmonics = []
        self.Field_B_Harmonics = []
        self.Coil_Type = None
        self.Field = []
        self.x_left = None
        self.x_right = None
        self.y_left = None
        self.y_right = None
        self.deviation = []
        self.comments = []

        self.selected_meas = selected_meas
        self.doc = doc
        self.config_doc = config_doc
        self.is_sextuple = is_sextuple

        self.st = None
        self.h = Harmonics(self.is_sextuple)
        self.d = DisplacementTab()
        self.p = Poles()
        self.Rref_name = QLabel('Reference radius, m')
        self.Rref_input = QLineEdit()
        self.MeasList = QListWidget()
        self.back_button = QPushButton()
        self.widget = QTabWidget()
        self.items = None

        self.meas_comments = QTextEdit('Comment:')

        self.dist_layout = QHBoxLayout()
        self.new_dist_layout = QHBoxLayout()
        self.dist_label = QLabel()
        self.dist_output = QLabel()
        self.dist_input = QLineEdit()
        self.new_dist_label = QLabel()
        self.distance = 0.04

        self.saving_templates = QPushButton('Save')

        self.r_ref = 0.01

        self.calc_signal()
        self.calc_harmonics(self.r_ref)
        self.calc_field()
        self.calc_displacement(self.r_ref)
        self.calc_deviation(self.distance)
        self.window_interface()
        self.style_window()
        self.style_labels()


    def window_interface(self):
        self.st = SignalTab(self.Signal)
        self.dist_label.setText('Distance between Poles:')
        self.dist_label.setFont(Fonts.small_headers())
        self.dist_label.setMaximumSize(170, 20)
        self.dist_layout.addWidget(self.dist_label)

        self.dist_output.setFont(Fonts.small_headers())
        self.dist_output.setText('0.04 m')
        Labels.output(self.dist_output)
        self.dist_output.setMaximumSize(80, 20)
        self.dist_layout.addWidget(self.dist_output)

        self.new_dist_label.setText('New Distance:')
        self.new_dist_label.setFont(Fonts.small_headers())
        self.new_dist_label.setMaximumSize(100, 20)
        self.new_dist_layout.addWidget(self.new_dist_label)

        self.dist_input.setFont(Fonts.plain_text())
        self.dist_input.editingFinished.connect(self.get_new_distance)
        self.dist_input.setMaximumSize(150, 20)
        self.new_dist_layout.addWidget(self.dist_input)

        self.Rref_name.setMaximumSize(250, 30)
        self.main_layout.addWidget(self.Rref_name, 0, 0)

        self.Rref_input.setMaximumSize(200, 30)
        self.Rref_input.editingFinished.connect(self.get_new_r_ref)
        self.main_layout.addWidget(self.Rref_input, 1, 0)

        self.main_layout.addLayout(self.dist_layout, 2, 0)
        self.main_layout.addLayout(self.new_dist_layout, 3, 0)

        self.MeasList.setMinimumSize(200, 600)
        self.MeasList.setMaximumSize(250, 10000)
        self.full_measlist()
        self.MeasList.itemClicked.connect(self.update_graph)
        self.main_layout.addWidget(self.MeasList, 4, 0)

        self.meas_comments.setMinimumSize(200, 200)
        self.meas_comments.setMaximumSize(250, 400)
        self.main_layout.addWidget(self.meas_comments, 5, 0)

        self.widget.addTab(self.st, 'Signal')
        self.widget.addTab(self.h, 'Harmonics')
        self.widget.addTab(self.d, 'Displacement')
        self.widget.addTab(self.p, 'Poles Geometry')
        self.main_layout.addWidget(self.widget, 0, 1, 6, 1)

        self.back_button.setMaximumSize(100, 30)
        self.back_button.setIcon(QIcon('leftarrow.png'))
        self.back_button.setIconSize(QSize(100, 20))
        self.main_layout.addWidget(self.back_button, 7, 0)

        self.saving_templates.clicked.connect(self.get_saving_templates)
        self.saving_templates.setMaximumSize(100, 30)
        self.saving_templates.setFont(Fonts.button_text())
        self.main_layout.addWidget(self.saving_templates, 6, 0)

        self.setLayout(self.main_layout)


    def style_window(self):
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        StyleSheets.stylesheet_central_widget(self)
        StyleSheets.stylesheet_tabwidget(self.widget)


    def style_labels(self):
        self.MeasList.setFont(Fonts.plain_text())
        self.Rref_name.setFont(Fonts.small_headers())


    def full_measlist(self):
        self.items = []
        for i in range(len(self.selected_meas)):
            self.items.append(f'{i+1}. {self.doc["Magnet"]["Measurements"][self.selected_meas[i]]["Name"]}')
            self.MeasList.addItem(f'{i+1}. {self.doc["Magnet"]["Measurements"][self.selected_meas[i]]["Name"]}')


    def calc_signal(self):
        self.EMF = []
        self.Signal = []
        self.calibr = GetConfigData.get_calibr(self.config_doc)
        for i in range(0, 3):
            sc = SignalFromCoils(self.doc, self.selected_meas, self.calibr)
            self.EMF.append(sc.spline_signal(i))

        for i in range(0, 3):
            sc = SignalFromCoils(self.doc, self.selected_meas, self.calibr)
            self.Signal.append(sc.return_spline(i))


    def calc_harmonics(self, r_ref):
        self.Field_A_Harmonics = []
        self.Field_B_Harmonics = []
        self.Coil_Type = GetConfigData.get_type(self.config_doc)
        for i in range(3):
            if self.Coil_Type[i] == 0:
                fc = FieldCoefficients(self.doc, self.config_doc, self.EMF, self.selected_meas, r_ref)
                Harm = FieldCoefficients.harmonics_for_coil(fc, i)
                self.Field_A_Harmonics.append(Harm[0])
                self.Field_B_Harmonics.append(Harm[1])
            else:
                fc = FieldCoefficients(self.doc, self.config_doc, self.EMF, self.selected_meas, r_ref)
                Harm = FieldCoefficients.harmonics_for_coil(fc, i)
                self.Field_A_Harmonics.append(Harm[0])
                self.Field_B_Harmonics.append(Harm[1])


    def calc_field(self):
        self.Field = []
        for j in range(3):
            fl = Field(self.selected_meas, self.Field_A_Harmonics[j], self.Field_B_Harmonics[j])
            self.Field.append(Field.field_harmonics(fl))


    def calc_displacement(self, r_ref):
        d_left = Displacement(0, self.Field_A_Harmonics, self.Field_B_Harmonics, self.Field, r_ref, self.is_sextuple)
        d_right = Displacement(1, self.Field_A_Harmonics, self.Field_B_Harmonics, self.Field, r_ref, self.is_sextuple)
        self.x_left = Displacement.calc_x(d_left)
        self.x_right = Displacement.calc_x(d_right)
        self.y_left = Displacement.calc_y(d_left)
        self.y_right = Displacement.calc_y(d_right)


    def calc_deviation(self, distance):
        self.deviation = []
        for i in range(3):
            pg = PolesGeometry(self.selected_meas, distance, self.Field_A_Harmonics, self.Field_B_Harmonics, i)
            self.deviation.append(pg.calc_deviation())


    def update_graph(self, field):
        g = self.MeasList.currentRow()
        SignalTab.return_selected_meas(self.st, g)
        DisplacementTab.return_selected_meas(self.d, self.x_left, self.x_right, self.y_left, self.y_right)
        Poles.return_selected_meas(self.p, self.deviation, self.distance, g, self.Field_A_Harmonics, self.Field_B_Harmonics)
        try:
            Harmonics.return_selected_meas(self.h, g, field)
        except TypeError:
            Harmonics.return_selected_meas(self.h, g, self.Field)

        self.get_comment_by_click()


    def get_new_r_ref(self):
        self.r_ref = float(self.Rref_input.text())
        self.calc_harmonics(self.r_ref)
        self.calc_field()
        self.calc_displacement(self.r_ref)
        self.calc_deviation(self.distance)
        self.update_graph(self.Field)


    def get_new_distance(self):
        self.distance = float(self.dist_input.text())
        self.dist_output.setText(f'{self.distance}')
        self.calc_deviation(self.distance)
        self.update_graph(self.Field)


    def get_comment_by_click(self):
        for i in range(len(self.MeasList.selectedItems())):
            text = self.meas_comments.toPlainText()
            self.meas_comments.setText(f'{text}\n{self.MeasList.row(self.MeasList.selectedItems()[i]) + 1}. {self.doc["Magnet"]["Measurements"][self.MeasList.row(self.MeasList.selectedItems()[i])]["Comments"]}')


    def get_all_comments(self):
        self.comments = []
        for i in range(len(self.selected_meas)):
            self.comments.append(
                self.doc["Magnet"]["Measurements"][self.selected_meas[i]]["Comments"])


    @staticmethod
    def get_template_name():
        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        template_name = None
        for elem in root[2].iter('SavingTemplate'):
            template_name = elem.text

        return template_name


    def get_saving_templates(self):
        self.get_all_comments()
        fc = FieldCoefficients(self.doc, self.config_doc, self.EMF, self.selected_meas, self.r_ref)
        a_coef = [[] for x in range(len(self.Field_B_Harmonics[0]))]
        b_coef = [[] for x in range(len(self.Field_B_Harmonics[1]))]
        field = [[] for x in range(len(self.Field[1]))]
        for g in range(len(self.Field[0])):
            # for k in range(15):
            #     a_coef[g].append((abs(self.Field_A_Harmonics[1][g][k]) + abs(self.Field_A_Harmonics[2][g][k]))/2)
            #     b_coef[g].append((abs(self.Field_B_Harmonics[1][g][k]) + abs(self.Field_B_Harmonics[2][g][k])) / 2)
            #     field[g].append((self.Field[1][g][k] + self.Field[2][g][k])/2)
            # for k in range(2, 15):
            #     a_coef[g].append(self.Field_A_Harmonics[2][g][k])
            #     b_coef[g].append(self.Field_B_Harmonics[2][g][k])
            #     field[g].append(self.Field[2][g][k])
            for k in range(15):
                a_coef[g].append(self.Field_A_Harmonics[0][g][k])
                b_coef[g].append(self.Field_B_Harmonics[0][g][k])
                field[g].append(self.Field[0][g][k])
        FFT_coef = fc.fft_coefficients(2)
        a_coef_volts = FFT_coef[0]
        b_coef_volts = FFT_coef[1]
        template_window = TemplatesWindow(self.items, a_coef_volts, b_coef_volts, a_coef, b_coef, field, self.comments, self.is_sextuple)
        template_window.collect_sextuple_utkin_data(
                                                    x=round((self.x_left[0] - self.x_right[0])/2 * 10**(-4), 5),
                                                    y=round((self.y_left[0] - self.y_right[0])/2 * 10**(-4), 5),
                                                    i=int(self.comments[0]),
                                                    a=list(map(lambda a: round(a, 5), a_coef[0])),
                                                    b=list(map(lambda b: round(b, 5), b_coef[0])),
                                                    amp=list(map(lambda f: round(f, 5), field[0]))
                                                    )
        template_window.show()
        template_window.exec()
