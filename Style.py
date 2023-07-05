from PySide6.QtGui import QColor, QPen, QFont, QIcon
from PySide6.QtWidgets import QFrame

color_1 = 0x73B833
color_2 = 0xB83533
color_3 = 0x7833B8
color_4 = 0x33B6B8
color_5 = 0x4f4f4f
color_6 = 0x444444


class GraphLines:
    @staticmethod
    def green():
        s = QPen(color_1)
        s.setWidth(2)
        return s

    @staticmethod
    def red():
        s = QPen(color_2)
        s.setWidth(2)
        return s

    @staticmethod
    def purple():
        s = QPen(color_3)
        s.setWidth(2)
        return s

    @staticmethod
    def light_blue():
        s = QPen(color_4)
        s.setWidth(2)
        return s

    @staticmethod
    def gray():
        s = QPen(color_5)
        s.setWidth(1)
        return s

    @staticmethod
    def black():
        s = QPen(color_6)
        s.setWidth(2)
        return s


class Colours:
    @staticmethod
    def green():
        return QColor(color_1)

    @staticmethod
    def red():
        return QColor(color_2)

    @staticmethod
    def purple():
        return QColor(color_3)


class WarningLabels:
    @staticmethod
    def style_1(label):
        label.setFrameShape(QFrame.WinPanel)
        label.setFrameShadow(QFrame.Raised)
        return label

    @staticmethod
    def style_2(label):
        label.setFrameShape(QFrame.Panel)
        label.setFrameShadow(QFrame.Plain)


class Labels:
    @staticmethod
    def output(label):
        label.setFrameShape(QFrame.Panel)
        label.setFrameShadow(QFrame.Raised)
        label.setLineWidth(2)

    @staticmethod
    def simple_label(label):
        label.setFrameShape(QFrame.StyledPanel)
        label.setFrameShape(QFrame.NoFrame)


class StyleSheets:
    @staticmethod
    def stylesheet_central_widget(wind):
        wind.setStyleSheet('background-color: #444444; color: white;')
        wind.setWindowTitle('Rotating Coils')
        wind.setWindowIcon(QIcon('winIcon.png'))


    @staticmethod
    def stylesheet_tabwidget(wind):
        wind.setStyleSheet('''QTabWidget::pane {
                                    border: 1px;
                                    background-color: #5B5B5B;
                                }
                               QTabBar::tab {
                                    background-color: #5B5B5B;
                                    min-width: 28ex;
                                    mib-height: 18ex;
                                    margin-left: 2px;
                                    font-size: 14px;
                                    font-weight: bold;
                               }
                               QTabBar::tab:selected {
                                    background-color: #867E79;
                               }
                               QTabBar::tab:hover {
                                    background-color: #867E79;
                               }
                                ''')

    @staticmethod
    def stylesheet_table(wind):
        wind.setStyleSheet('''QHeaderView::section {
                                    background-color: #867E79;
                                    font-size: 13px;
                                    font-weight: bold;
                                }
                                QTableCornerButton::section {
                                    background-color: #867E79;
                                }
                                QToolTip {
                                    border: 2px;
                                    background-color: #867E79;
                                    color: black;
                                    border-style: groove;
                                    font-size: 14px;
                                }''')


    @staticmethod
    def stylesheet_tool_tip(wind):
        wind.setStyleSheet('''QToolTip {
                                    border: 2px;
                                    background-color: #867E79;
                                    color: black;
                                    border-style: groove;
                                    font-size: 14px;
                                }
                                ''')


    @staticmethod
    def stylesheet_saving_template(template):
        template.setStyleSheet('''QPushButton {
                                    border: 2px;
                                    border-color: black;
                                    border-width: 2px;
                                    border-style: groove;
                                    }
                                ''')


    @staticmethod
    def stylesheet_highlighted_template(template):
        template.setStyleSheet('''QPushButton {
                                    border: 3px;
                                    border-color: white;
                                    border-width: 3px;
                                    border-style: groove;
                                    }
                                ''')


class Fonts:
    @staticmethod
    def plain_text():
        font = QFont()
        font.setPixelSize(14)
        return font

    @staticmethod
    def small_headers():
        font = QFont()
        font.setPixelSize(14)
        font.setWeight(QFont.Weight.Bold)
        return font

    @staticmethod
    def big_headers():
        font = QFont()
        font.setPixelSize(16)
        font.setWeight(QFont.Weight.Bold)
        return font

    @staticmethod
    def bigger_headers():
        font = QFont()
        font.setPixelSize(18)
        font.setWeight(QFont.Weight.Bold)
        return font

    @staticmethod
    def button_text():
        font = QFont()
        font.setPixelSize(13)
        font.setWeight(QFont.Weight.Bold)
        return font
