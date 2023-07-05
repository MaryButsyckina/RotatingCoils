from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QCategoryAxis
from PySide6.QtCore import Qt

from Style import Fonts, StyleSheets, Colours


class Harmonics(QDialog):
    def __init__(self, is_sextuple):
        super(Harmonics, self).__init__()

        self.main_layout = QGridLayout()
        self.Chart = QChart()
        self.ChartView = QChartView(self.Chart)
        self.coil_zero = QPushButton('First coil')
        self.coil_one = QPushButton('Second coil')
        self.coil_two = QPushButton('Third coil')
        self.clear = QPushButton('Clear')
        self.table = QTableWidget(15, 3)
        self.Field = None
        self.x_axis = QBarCategoryAxis()
        self.y_axis = QCategoryAxis()
        self.g = None
        self.question = QPushButton('?')
        self.description = None
        self.main_harm = 1
        if is_sextuple:
            self.main_harm = 2


        self.window()
        self.style_chart()
        self.style_table()
        self.style_buttons()

    def window(self):
        self.setLayout(self.main_layout)
        self.ChartView.setMinimumSize(600, 600)
        self.main_layout.addWidget(self.ChartView, 0, 1, 11, 1)

        self.coil_zero.setMinimumSize(100, 20)
        self.coil_zero.clicked.connect(self.first_coil)
        self.main_layout.addWidget(self.coil_zero, 0, 0)

        self.coil_one.setMinimumSize(100, 20)
        self.coil_one.clicked.connect(self.second_coil)
        self.main_layout.addWidget(self.coil_one, 1, 0)

        self.coil_two.setMinimumSize(100, 20)
        self.coil_two.clicked.connect(self.third_coil)
        self.main_layout.addWidget(self.coil_two, 2, 0)

        self.clear.setMinimumSize(100, 20)
        self.clear.clicked.connect(self.clear_chart)
        self.main_layout.addWidget(self.clear, 3, 0)

        self.table.setMinimumSize(325, 400)
        self.table.setMaximumSize(325, 10000)
        self.table.setHorizontalHeaderLabels(['First Coil', 'Second Coil', 'Third Coil'])
        self.table.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.main_layout.addWidget(self.table, 0, 2, 9, 2)

        self.question.setMaximumSize(20, 20)
        self.question.setToolTip("Field Harmonics in Gs")
        StyleSheets.stylesheet_tool_tip(self.question)
        self.question.setToolTipDuration(3000)
        self.main_layout.addWidget(self.question, 0, 4)

        self.x_axis.setTitleText('Harmonic number')
        self.y_axis.setTitleText('Hn/H2')


    def chart(self, j, g, field):
        self.Chart.removeAllSeries()
        self.Field = field
        barSet = QBarSet(f'H2 = {self.Field[j][g][1]}')
        k = []

        for i in range(15):
            k.append(0)
            while True:
                if round(self.Field[j][g][i]/self.Field[j][g][self.main_harm], k[i]) == 0:
                    pass
                else:
                    if self.Field[j][g][i]/self.Field[j][g][self.main_harm] * 10 ** (k[i]) < 1:
                        k[i] += 1
                        break
                    else:
                        break
                k[i] += 1

        for i in range(15):
            self.x_axis.append([f'{i+1}'])
            barSet.append(max(k) - k[i] + round(self.Field[j][g][i]/self.Field[j][g][self.main_harm] * 10**(k[i]-1), 3))
        bar = QBarSeries()
        if j == 0:
            barSet.setColor(Colours.green())
        elif j == 1:
            barSet.setColor(Colours.red())
        elif j == 2:
            barSet.setColor(Colours.purple())
        bar.append(barSet)

        self.Chart.addSeries(bar)

        self.Chart.addAxis(self.x_axis, Qt.AlignBottom)
        bar.attachAxis(self.x_axis)

        self.y_axis.setRange(0, max(k))
        self.y_axis.setStartValue(0)
        for i in range(max(k)+1):
            self.y_axis.append(f'10^-{max(k)-i+1}', i-1)
        self.Chart.addAxis(self.y_axis, Qt.AlignLeft)
        bar.attachAxis(self.y_axis)


    def style_chart(self):
        self.Chart.legend().setFont(Fonts.small_headers())
        self.Chart.legend().setMaximumSize(300, 40)
        self.Chart.legend().setAlignment(Qt.AlignTop)
        self.Chart.legend().setBackgroundVisible(True)
        self.Chart.legend().setColor(0x867E79)
        self.x_axis.setTitleFont(Fonts.big_headers())
        self.y_axis.setTitleFont(Fonts.big_headers())


    def style_buttons(self):
        self.coil_zero.setFont(Fonts.button_text())
        self.coil_two.setFont(Fonts.button_text())
        self.coil_one.setFont(Fonts.button_text())
        self.clear.setFont(Fonts.button_text())


    def style_table(self):
        StyleSheets.stylesheet_table(self.table)
        self.table.setFont(Fonts.plain_text())


    def full_table(self):
        for j in range(3):
            k = []
            for i in range(15):
                k.append(0)
                while True:
                    if round(self.Field[j][self.g][i], k[i]) == 0:
                        pass
                    else:
                        if self.Field[j][self.g][i] * 10**(k[i]) < 1:
                            k[i] += 1
                            break
                        else:
                            break
                    k[i] += 1
            for i in range(15):
                self.table.setItem(i, j, QTableWidgetItem(f'{round(self.Field[j][self.g][i] * 10**(k[i]), 3)}*10^-{k[i]}'))


    def return_selected_meas(self, g, field):
        self.g = g
        self.Field = field
        self.chart(1, self.g, self.Field)
        self.full_table()


    def first_coil(self):
        self.chart(0, self.g, self.Field)


    def second_coil(self):
        self.chart(1, self.g, self.Field)


    def third_coil(self):
        self.chart(2, self.g, self.Field)


    def clear_chart(self):
        self.Chart.removeAllSeries()
        self.Chart.removeAxis(self.x_axis)
        self.Chart.removeAxis(self.y_axis)
