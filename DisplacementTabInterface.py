from PySide6.QtWidgets import QDialog, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCharts import QChart, QChartView, QScatterSeries, QValueAxis, QLineSeries
from PySide6.QtCore import Qt, QPointF

from Style import Fonts, StyleSheets, GraphLines, Colours


class DisplacementTab(QDialog):
    def __init__(self):
        super(DisplacementTab, self).__init__()
        self.f = Fonts()

        self.main_layout = QGridLayout()
        self.Chart = QChart()
        self.ChartView = QChartView(self.Chart)
        self.Table = QTableWidget(0, 4)
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        self.question = QPushButton('?')

        self.window()


    def window(self):
        self.setLayout(self.main_layout)

        self.ChartView.setMinimumSize(600, 600)
        self.main_layout.addWidget(self.ChartView, 0, 0, 10, 1)

        self.Table.setMinimumSize(333, 600)
        self.Table.setMaximumSize(333, 10000)
        self.Table.setHorizontalHeaderLabels(['x_left', 'y_left', 'x_right', 'y_right'])
        self.style_table()
        self.main_layout.addWidget(self.Table, 0, 1, 10, 1)

        self.question.setToolTip("Left and right deviation of the shaft's axis from the lens's axis in microns.")
        self.question.setMaximumSize(20, 20)
        StyleSheets.stylesheet_tool_tip(self.question)
        self.question.setToolTipDuration(3000)
        self.main_layout.addWidget(self.question, 0, 2)


    def chart(self, x_left, x_right, y_left, y_right):
        self.Chart.removeAllSeries()

        series_left = QScatterSeries()
        series_right = QScatterSeries()
        series_left.setName('Left')
        series_right.setName('Right')
        x_abs = []
        y_abs = []

        for i in range(len(x_left)):
            x_abs.append(abs(x_left[i]))
            x_abs.append(abs(x_right[i]))
            y_abs.append(abs(y_left[i]))
            y_abs.append(abs(y_right[i]))
            series_left.append([QPointF(x_left[i], y_left[i])])
            series_right.append([QPointF(x_right[i], y_right[i])])

        series_right.setPen(GraphLines.green())
        series_left.setPen(GraphLines.red())
        series_left.setColor(Colours.red())
        series_right.setColor(Colours.green())

        self.Chart.addSeries(series_left)
        self.Chart.addSeries(series_right)

        if max(x_abs) < 200:
            factor_x = 10
        elif 200 <= max(x_abs) < 500:
            factor_x = 50
        elif 500 <= max(x_abs) < 1000:
            factor_x = 100
        elif 1000 <= max(y_abs) < 3000:
            factor_x = 500
        else:
            factor_x = int(max(x_abs) / 10)

        if max(y_abs) < 100:
            factor_y = 10
        elif 100 <= max(y_abs) < 500:
            factor_y = 50
        elif 500 <= max(y_abs) < 1000:
            factor_y = 100
        elif 1000 <= max(y_abs) < 3000:
            factor_y = 500
        else:
            factor_y = int(max(y_abs) / 10)

        if round(max(x_abs)/factor_x) * factor_x < max(x_abs):
            x_max = round(max(x_abs)/factor_x) * factor_x + factor_x
        else:
            x_max = round(max(x_abs)/factor_x) * factor_x

        if round(max(y_abs)/factor_y) * factor_y < max(y_abs):
            y_max = round(max(y_abs)/factor_y) * factor_y + factor_y
        else:
            y_max = round(max(y_abs)/factor_y) * factor_y


        self.x_axis.setRange(-x_max, x_max)
        self.Chart.addAxis(self.x_axis, Qt.AlignBottom)
        series_right.attachAxis(self.x_axis)
        series_left.attachAxis(self.x_axis)

        self.y_axis.setRange(-y_max, y_max)
        self.Chart.addAxis(self.y_axis, Qt.AlignLeft)
        series_right.attachAxis(self.y_axis)
        series_left.attachAxis(self.y_axis)

        x_zero = QLineSeries()
        x_zero.append([QPointF(-x_max, 0), QPointF(x_max, 0)])
        self.Chart.addSeries(x_zero)
        x_zero.attachAxis(self.x_axis)
        x_zero.attachAxis(self.y_axis)
        x_zero.setPen(GraphLines.black())

        y_zero = QLineSeries()
        y_zero.append([QPointF(0, -y_max), QPointF(0, y_max)])
        self.Chart.addSeries(y_zero)
        y_zero.attachAxis(self.x_axis)
        y_zero.attachAxis(self.y_axis)
        y_zero.setPen(GraphLines.black())

        self.style_chart(x_max, y_max, x_zero, y_zero, factor_x, factor_y)

        self.table(x_left, x_right, y_left, y_right)


    def style_chart(self, x_max, y_max, x_zero, y_zero, factor_x, factor_y):
        self.Chart.setFont(Fonts.small_headers())
        self.Chart.legend().setMaximumSize(300, 40)
        self.Chart.legend().setAlignment(Qt.AlignTop)
        self.Chart.legend().setBackgroundVisible(True)
        self.Chart.legend().setColor(0x867E79)
        self.Chart.legend().markers(x_zero)[0].setVisible(False)
        self.Chart.legend().markers(y_zero)[0].setVisible(False)
        self.x_axis.setMinorTickCount(9)
        self.y_axis.setMinorTickCount(9)
        self.x_axis.setTickCount(2 * round(x_max / factor_x) + 1)
        self.y_axis.setTickCount(2 * round(y_max / factor_y) + 1)
        self.x_axis.setGridLineColor(0x4f4f4f)
        self.y_axis.setGridLineColor(0x4f4f4f)


    def table(self, x_left, x_right, y_left, y_right):
        while True:
            if self.Table.rowCount() == 0:
                break
            else:
                self.Table.removeRow(0)
        for i in range(len(x_left)):
            self.Table.insertRow(i)
            self.Table.setItem(i, 0, QTableWidgetItem(f'{round(x_left[i], 3)}'))
            self.Table.setItem(i, 1, QTableWidgetItem(f'{round(y_left[i], 3)}'))
            self.Table.setItem(i, 2, QTableWidgetItem(f'{round(x_right[i], 3)}'))
            self.Table.setItem(i, 3, QTableWidgetItem(f'{round(y_right[i], 3)}'))
        self.Table.setColumnWidth(0, 77)
        self.Table.setColumnWidth(1, 77)
        self.Table.setColumnWidth(2, 77)
        self.Table.setColumnWidth(3, 77)
        self.Table.setFont(Fonts.plain_text())


    def style_table(self):
        StyleSheets.stylesheet_table(self.Table)


    def return_selected_meas(self, x_left, x_right, y_left, y_right):
        self.chart(x_left, x_right, y_left, y_right)
