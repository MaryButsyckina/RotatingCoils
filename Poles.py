from PySide6.QtWidgets import QDialog, QTableWidget, QGridLayout, QTableWidgetItem, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Qt

from Style import StyleSheets, Fonts, GraphLines
from Mathematics import Hyperbola


class Poles(QDialog):
    def __init__(self):
        super(Poles, self).__init__()
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.table_first_coil_deviation = QTableWidget(4, 1)
        self.table_second_coil_deviation = QTableWidget(4, 1)
        self.table_third_coil_deviation = QTableWidget(4, 1)
        self.table_first_coil_harm = QTableWidget(3, 2)
        self.table_second_coil_harm = QTableWidget(3, 2)
        self.table_third_coil_harm = QTableWidget(3, 2)
        self.Chart = QChart()
        self.ChartView = QChartView(self.Chart)
        self.series_ex_one = QLineSeries()
        self.series_ex_two = QLineSeries()
        self.series_ex_three = QLineSeries()
        self.series_ex_four = QLineSeries()
        self.series_real_one = QLineSeries()
        self.series_real_two = QLineSeries()
        self.series_real_three = QLineSeries()
        self.series_real_four = QLineSeries()
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()

        self.table_layout = QGridLayout()
        self.button_layout = QVBoxLayout()
        self.question_layout_1 = QGridLayout()

        self.first_coil = QPushButton('First Coil')
        self.second_coil = QPushButton('Second Coil')
        self.third_coil = QPushButton('Third Coil')

        self.question_1 = QPushButton('?')
        self.question_2 = QPushButton('?')
        self.question_3 = QPushButton('?')

        self.j = 1
        self.deviation = None
        self.distance = None
        self.g = None

        self.window()
        self.style_table()


    def window(self):
        self.table_first_coil_deviation.setHorizontalHeaderLabels(['First Coil: Deviation of distance between poles'])
        self.table_first_coil_deviation.setVerticalHeaderLabels(['1st-2nd Poles', '2nd-3rd Poles', '3rd-4th Poles', '4th-1st Poles'])
        self.table_layout.addWidget(self.table_first_coil_deviation, 0, 0)

        self.table_first_coil_deviation.setToolTip("The deviation of distance between poles from the ideal construction in microns.")
        self.table_first_coil_deviation.setToolTipDuration(30000)

        self.table_second_coil_deviation.setHorizontalHeaderLabels(['Second Coil: Deviation of distance between poles'])
        self.table_second_coil_deviation.setVerticalHeaderLabels(['1st-2nd Poles', '2nd-3rd Poles', '3rd-4th Poles', '4th-1st Poles'])
        self.table_layout.addWidget(self.table_second_coil_deviation, 1, 0)
        self.table_second_coil_deviation.setToolTip("The deviation of distance between poles from the ideal construction in microns.")
        self.table_second_coil_deviation.setToolTipDuration(30000)

        self.table_third_coil_deviation.setHorizontalHeaderLabels(['Third Coil: Deviation of distance between poles'])
        self.table_third_coil_deviation.setVerticalHeaderLabels(['1st-2nd Poles', '2nd-3rd Poles', '3rd-4th Poles', '4th-1st poles'])
        self.table_layout.addWidget(self.table_third_coil_deviation, 2, 0)
        self.table_third_coil_deviation.setToolTip("The deviation of distance between poles from the ideal construction in microns.")
        self.table_third_coil_deviation.setToolTipDuration(30000)

        self.table_first_coil_harm.setHorizontalHeaderLabels(['Difference in microns', 'Harmonic in Gs'])
        self.table_first_coil_harm.setVerticalHeaderLabels(['Between Vertical and Horizontal Poles', 'Between Verticals Poles', 'Between Horizontal Poles'])
        self.table_layout.addWidget(self.table_first_coil_harm, 3, 0)

        self.table_second_coil_harm.setHorizontalHeaderLabels(['Difference in microns', 'Harmonic in Gs'])
        self.table_second_coil_harm.setVerticalHeaderLabels(['Between Vertical and Horizontal Poles', 'Between Verticals Poles', 'Between Horizontal Poles'])
        self.table_layout.addWidget(self.table_second_coil_harm, 4, 0)

        self.table_third_coil_harm.setHorizontalHeaderLabels(['Difference in microns', 'Harmonic in Gs'])
        self.table_third_coil_harm.setVerticalHeaderLabels(['Between Vertical and Horizontal Poles', 'Between Verticals Poles', 'Between Horizontal Poles'])
        self.table_layout.addWidget(self.table_third_coil_harm, 5, 0)

        self.first_coil.setMaximumSize(100, 30)
        self.second_coil.setMaximumSize(100, 30)
        self.third_coil.setMaximumSize(100, 30)
        self.first_coil.setMinimumSize(100, 30)
        self.second_coil.setMinimumSize(100, 30)
        self.third_coil.setMinimumSize(100, 30)

        self.first_coil.clicked.connect(self.get_first_coil)
        self.second_coil.clicked.connect(self.get_second_coil)
        self.third_coil.clicked.connect(self.get_third_coil)

        self.first_coil.setFont(Fonts.button_text())
        self.second_coil.setFont(Fonts.button_text())
        self.third_coil.setFont(Fonts.button_text())

        self.button_layout.addWidget(self.first_coil)
        self.button_layout.addWidget(self.second_coil)
        self.button_layout.addWidget(self.third_coil)

        self.main_layout.addLayout(self.button_layout, 0, 0)
        self.main_layout.addWidget(self.ChartView, 0, 1, 3, 1)
        self.main_layout.addLayout(self.table_layout, 0, 2, 3, 2)


    def full_table(self, deviation, g, a_coef, b_coef):
        for i in range(4):
            self.table_first_coil_deviation.setItem(i, 0, QTableWidgetItem(f'{round(deviation[0][g][i], 3)}'))
            self.table_second_coil_deviation.setItem(i, 0, QTableWidgetItem(f'{round(deviation[1][g][i], 3)}'))
            self.table_third_coil_deviation.setItem(i, 0, QTableWidgetItem(f'{round(deviation[2][g][i], 3)}'))

        self.table_first_coil_harm.setItem(0, 0, QTableWidgetItem(f'{round(deviation[0][g][0]+deviation[0][g][2] - deviation[0][g][1] - deviation[0][g][3], 2)/2}'))
        self.table_second_coil_harm.setItem(0, 0, QTableWidgetItem(f'{round(deviation[1][g][0]+deviation[1][g][2] - deviation[1][g][1] - deviation[1][g][3], 2)/2}'))
        self.table_third_coil_harm.setItem(0, 0, QTableWidgetItem(f'{round(deviation[2][g][0]+deviation[2][g][2] - deviation[2][g][1] - deviation[2][g][3], 2)/2}'))
        self.table_first_coil_harm.setItem(0, 1, QTableWidgetItem(f'b4 = {round(b_coef[0][g][3], 5)}'))
        self.table_second_coil_harm.setItem(0, 1, QTableWidgetItem(f'b4 = {round(b_coef[1][g][3], 5)}'))
        self.table_third_coil_harm.setItem(0, 1, QTableWidgetItem(f'b4 = {round(b_coef[2][g][3], 5)}'))

        self.table_first_coil_harm.setItem(1, 0, QTableWidgetItem(f'{round(deviation[0][g][0] - deviation[0][g][2], 2) / 2}'))
        self.table_second_coil_harm.setItem(1, 0, QTableWidgetItem(f'{round(deviation[1][g][0] - deviation[1][g][2], 2) / 2}'))
        self.table_third_coil_harm.setItem(1, 0, QTableWidgetItem(f'{round(deviation[2][g][0] - deviation[2][g][2], 2) / 2}'))
        self.table_first_coil_harm.setItem(1, 1, QTableWidgetItem(f'a3 = {round(a_coef[0][g][2], 5)}'))
        self.table_second_coil_harm.setItem(1, 1, QTableWidgetItem(f'a3 = {round(a_coef[1][g][2], 5)}'))
        self.table_third_coil_harm.setItem(1, 1, QTableWidgetItem(f'a3 = {round(a_coef[2][g][2], 5)}'))

        self.table_first_coil_harm.setItem(2, 0, QTableWidgetItem(f'{round(deviation[0][g][1] - deviation[0][g][3], 2) / 2}'))
        self.table_second_coil_harm.setItem(2, 0, QTableWidgetItem(f'{round(deviation[1][g][1] - deviation[1][g][3], 2) / 2}'))
        self.table_third_coil_harm.setItem(2, 0, QTableWidgetItem(f'{round(deviation[2][g][1] - deviation[2][g][3], 2) / 2}'))
        self.table_first_coil_harm.setItem(2, 1, QTableWidgetItem(f'b3 = {round(b_coef[0][g][2], 5)}'))
        self.table_second_coil_harm.setItem(2, 1, QTableWidgetItem(f'b3 = {round(b_coef[1][g][2], 5)}'))
        self.table_third_coil_harm.setItem(2, 1, QTableWidgetItem(f'b3 = {round(b_coef[2][g][2], 5)}'))


    def style_table(self):
        StyleSheets.stylesheet_table(self.table_first_coil_deviation)
        self.table_first_coil_deviation.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_table(self.table_second_coil_deviation)
        self.table_second_coil_deviation.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_table(self.table_third_coil_deviation)
        self.table_third_coil_deviation.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_table(self.table_first_coil_harm)
        self.table_first_coil_harm.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_table(self.table_second_coil_harm)
        self.table_second_coil_harm.setFont(Fonts.plain_text())

        StyleSheets.stylesheet_table(self.table_third_coil_harm)
        self.table_third_coil_harm.setFont(Fonts.plain_text())

        self.table_first_coil_deviation.setColumnWidth(0, 340)
        self.table_second_coil_deviation.setColumnWidth(0, 340)
        self.table_third_coil_deviation.setColumnWidth(0, 340)

        self.table_first_coil_deviation.setMaximumSize(425, 150)
        self.table_second_coil_deviation.setMaximumSize(425, 150)
        self.table_third_coil_deviation.setMaximumSize(425, 150)
        self.table_first_coil_deviation.setMinimumSize(425, 150)
        self.table_second_coil_deviation.setMinimumSize(425, 150)
        self.table_third_coil_deviation.setMinimumSize(425, 150)

        self.table_first_coil_harm.setColumnWidth(0, 160)
        self.table_second_coil_harm.setColumnWidth(0, 160)
        self.table_third_coil_harm.setColumnWidth(0, 160)
        self.table_first_coil_harm.setColumnWidth(1, 160)
        self.table_second_coil_harm.setColumnWidth(1, 160)
        self.table_third_coil_harm.setColumnWidth(1, 160)

        self.table_first_coil_harm.setMaximumSize(565, 120)
        self.table_second_coil_harm.setMaximumSize(565, 120)
        self.table_third_coil_harm.setMaximumSize(565, 120)
        self.table_first_coil_harm.setMinimumSize(565, 120)
        self.table_second_coil_harm.setMinimumSize(565, 120)
        self.table_third_coil_harm.setMinimumSize(565, 120)


    def chart_ex(self, deviation, dist_between_poles, g):
        self.series_ex_one.clear()
        self.series_ex_two.clear()
        self.series_ex_three.clear()
        self.series_ex_four.clear()

        x_ex = []
        y_ex = []

        for i in range(0, 4):
            h = Hyperbola(deviation, dist_between_poles, g, self.j, i, hyperbola='ex')
            x_y = h.rotate_hyperbola()
            x_ex.append(x_y[0])
            y_ex.append(x_y[1])

        for i in range(len(y_ex[0])):
            self.series_ex_one.append([QPointF(x_ex[0][i], y_ex[0][i])])
            self.series_ex_two.append([QPointF(x_ex[1][i], y_ex[1][i])])
            self.series_ex_three.append([QPointF(x_ex[2][i], y_ex[2][i])])
            self.series_ex_four.append([QPointF(x_ex[3][i], y_ex[3][i])])

        self.Chart.addSeries(self.series_ex_one)
        self.Chart.addSeries(self.series_ex_two)
        self.Chart.addSeries(self.series_ex_three)
        self.Chart.addSeries(self.series_ex_four)

        self.x_axis.setRange(-3*dist_between_poles, 3*dist_between_poles)
        self.y_axis.setRange(-3 * dist_between_poles, 3 * dist_between_poles)
        self.Chart.addAxis(self.x_axis, Qt.AlignBottom)
        self.Chart.addAxis(self.y_axis, Qt.AlignLeft)

        self.series_ex_one.attachAxis(self.x_axis)
        self.series_ex_two.attachAxis(self.x_axis)
        self.series_ex_three.attachAxis(self.x_axis)
        self.series_ex_four.attachAxis(self.x_axis)
        self.series_ex_one.attachAxis(self.y_axis)
        self.series_ex_two.attachAxis(self.y_axis)
        self.series_ex_three.attachAxis(self.y_axis)
        self.series_ex_four.attachAxis(self.y_axis)


    def chart_real(self, deviation, dist_between_poles, g):
        self.series_real_one.clear()
        self.series_real_two.clear()
        self.series_real_three.clear()
        self.series_real_four.clear()

        x_real = []
        y_real = []

        for i in range(0, 4):
            h = Hyperbola(deviation, dist_between_poles, g, self.j, i, hyperbola='real')
            x_y = h.rotate_hyperbola()
            x_real.append(x_y[0])
            y_real.append(x_y[1])

        for i in range(len(y_real[0])):
            self.series_real_one.append([QPointF(x_real[0][i], y_real[0][i])])
            self.series_real_two.append([QPointF(x_real[1][i], y_real[1][i])])
            self.series_real_three.append([QPointF(x_real[2][i], y_real[2][i])])
            self.series_real_four.append([QPointF(x_real[3][i], y_real[3][i])])

        self.Chart.addSeries(self.series_real_one)
        self.Chart.addSeries(self.series_real_two)
        self.Chart.addSeries(self.series_real_three)
        self.Chart.addSeries(self.series_real_four)

        self.series_real_one.attachAxis(self.x_axis)
        self.series_real_two.attachAxis(self.x_axis)
        self.series_real_three.attachAxis(self.x_axis)
        self.series_real_four.attachAxis(self.x_axis)
        self.series_real_one.attachAxis(self.y_axis)
        self.series_real_two.attachAxis(self.y_axis)
        self.series_real_three.attachAxis(self.y_axis)
        self.series_real_four.attachAxis(self.y_axis)


    def style_chart(self):
        self.series_ex_one.setPen(GraphLines.gray())
        self.series_ex_two.setPen(GraphLines.gray())
        self.series_ex_three.setPen(GraphLines.gray())
        self.series_ex_four.setPen(GraphLines.gray())

        self.series_real_one.setPen(GraphLines.green())
        self.series_real_two.setPen(GraphLines.red())
        self.series_real_three.setPen(GraphLines.purple())
        self.series_real_four.setPen(GraphLines.light_blue())

        self.series_real_one.setName('1st Pole')
        self.series_real_two.setName('2nd Pole')
        self.series_real_three.setName('3rd Pole')
        self.series_real_four.setName('4th Pole')

        self.Chart.legend().markers(self.series_ex_one)[0].setVisible(False)
        self.Chart.legend().markers(self.series_ex_two)[0].setVisible(False)
        self.Chart.legend().markers(self.series_ex_three)[0].setVisible(False)
        self.Chart.legend().markers(self.series_ex_four)[0].setVisible(False)
        self.Chart.legend().setFont(Fonts.small_headers())
        self.Chart.legend().setMaximumSize(450, 40)
        self.Chart.legend().setAlignment(Qt.AlignTop)
        self.Chart.legend().setBackgroundVisible(True)
        self.Chart.legend().setColor(0x867E79)


    def clear_table(self):
        while True:
            if self.table_first_coil_deviation.rowCount() == 0:
                break
            else:
                self.table_first_coil_deviation.removeRow(0)

            if self.table_second_coil_deviation.rowCount() == 0:
                break
            else:
                self.table_second_coil_deviation.removeRow(0)

            if self.table_third_coil_deviation.rowCount() == 0:
                break
            else:
                self.table_third_coil_deviation.removeRow(0)

            if self.table_first_coil_harm.rowCount() == 0:
                break
            else:
                self.table_first_coil_harm.removeRow(0)

            if self.table_second_coil_harm.rowCount() == 0:
                break
            else:
                self.table_second_coil_harm.removeRow(0)

            if self.table_third_coil_harm.rowCount() == 0:
                break
            else:
                self.table_third_coil_harm.removeRow(0)


    def return_selected_meas(self, deviation, dist_between_poles, g, a_coef, b_coef):
        self.distance = dist_between_poles / 2 * 10 ** 5
        self.deviation = deviation
        self.g = g

        self.full_table(deviation, g, a_coef, b_coef)
        self.chart_ex(deviation, self.distance, g)
        self.chart_real(deviation, self.distance, g)
        self.style_chart()


    def get_first_coil(self):
        self.j = 0
        self.chart_ex(self.deviation, self.distance, self.g)
        self.chart_real(self.deviation, self.distance, self.g)


    def get_second_coil(self):
        self.j = 1
        self.chart_ex(self.deviation, self.distance, self.g)
        self.chart_real(self.deviation, self.distance, self.g)


    def get_third_coil(self):
        self.j = 2
        self.chart_ex(self.deviation, self.distance, self.g)
        self.chart_real(self.deviation, self.distance, self.g)
