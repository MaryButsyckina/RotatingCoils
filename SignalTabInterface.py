import Libs

from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Qt

from Style import Fonts, GraphLines


class SignalTab(QDialog):
    def __init__(self, signal):
        super(SignalTab, self).__init__()

        self.Signal = signal
        self.angle = signal
        self.main_layout = QGridLayout()
        self.coil_zero = QPushButton('First Coil')
        self.coil_one = QPushButton('Second Coil')
        self.coil_two = QPushButton('Third Coil')
        self.clear = QPushButton('Clear')
        self.Chart = QChart()
        self.ChartView = QChartView(self.Chart)
        self.g = None

        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        self.series = [QLineSeries() for i in range(3)]

        self.window()
        self.style_buttons()


    def window(self):
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

        self.Chart.setMinimumSize(600, 600)
        self.main_layout.addWidget(self.ChartView, 0, 1, 10, 1)

        self.setLayout(self.main_layout)


    def style_buttons(self):
        self.coil_zero.setFont(Fonts.button_text())
        self.coil_one.setFont(Fonts.button_text())
        self.coil_two.setFont(Fonts.button_text())
        self.clear.setFont(Fonts.button_text())


    def chart(self, j, g):
        for i in range(len(self.Signal[j][1][g])):
            self.series[j].append([QPointF(self.angle[j][0][g][i], self.Signal[j][1][g][i])])
        # for i in range(len(self.Signal[j][g])):
        #     self.series[j].append([QPointF(i, self.Signal[j][g][i])])

        if j == 0:
            self.series[j].setName('First Coil')
            self.series[j].setPen(GraphLines.green())
        elif j == 1:
            self.series[j].setName('Second Coil')
            self.series[j].setPen(GraphLines.red())
        elif j == 2:
            self.series[j].setName('Third Coil')
            self.series[j].setPen(GraphLines.purple())

        if len(self.Chart.legend().markers()) > 3:
            for i in range(3, len(self.Chart.legend().markers())+1):
                self.Chart.legend().markers()[i-3].setVisible(False)

        self.Chart.addSeries(self.series[j])
        self.x_axis.setRange(self.angle[j][0][g][0], self.angle[j][0][g][-1])
        # self.x_axis.setRange(0, len(self.Signal[j][g]))
        self.x_axis.setTitleText('angle, degrees')
        self.Chart.addAxis(self.x_axis, Qt.AlignBottom)
        self.series[j].attachAxis(self.x_axis)

        self.y_axis.setRange(min(self.Signal[j][1][g]), max(self.Signal[j][1][g]))
        # self.y_axis.setRange(min(self.Signal[j][g]), max(self.Signal[j][g]))
        self.y_axis.setTitleText('Voltage, V')
        self.Chart.addAxis(self.y_axis, Qt.AlignLeft)
        for i in range(j):
            self.series[i].attachAxis(self.y_axis)

        self.style_chart()


    def style_chart(self):
        self.Chart.legend().setFont(Fonts.small_headers())
        self.Chart.legend().setMaximumSize(300, 50)
        self.Chart.legend().setAlignment(Qt.AlignTop)
        self.Chart.legend().setBackgroundVisible(True)
        self.Chart.legend().setColor(0x867E79)
        self.x_axis.setTitleFont(Fonts.big_headers())
        self.y_axis.setTitleFont(Fonts.big_headers())


    def first_coil(self):
        self.chart(0, self.g)


    def second_coil(self):
        self.chart(1, self.g)


    def third_coil(self):
        self.chart(2, self.g)


    def clear_chart(self):
        for j in range(3):
            self.series[j].clear()


    def return_selected_meas(self, g):
        self.clear_chart()
        self.g = g
        self.first_coil()
        self.second_coil()
        self.third_coil()
