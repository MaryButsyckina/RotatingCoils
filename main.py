import sys

from PySide6.QtWidgets import QApplication

from IntroWindowInterface import IntroWindow, Exceptions
from TabWindowInterface import TabWindow


def is_no_exception(intro_window, selected_meas, doc):
    if Exceptions.is_any_meas_selected(selected_meas):
        if not Exceptions.is_empty_file(selected_meas, doc)[0]:
            if Exceptions.is_config_file(intro_window):
                return True
            else:
                intro_window.ui.error_status_output.setText('No configuration file')
        else:
            intro_window.ui.error_status_output.setText(f'Empty measurement {Exceptions.is_empty_file(selected_meas, doc)[1]}')
    else:
        intro_window.ui.error_status_output.setText('Choose at least one meas')

    return False


def control_intro_window(window):
    window.ui.next_page_button.clicked.connect(window.submit_meas)
    window.ui.next_page_button.clicked.connect(window.is_sextuple)
    window.ui.next_page_button.clicked.connect(window.parse_config_file)
    window.ui.next_page_button.clicked.connect(lambda: open_tab_window(window, window.doc, window.config_doc, window.selected_meas, window.sextuple))


def control_tab_window(tab_window):
    tab_window.back_button.clicked.connect(lambda: open_intro_window(tab_window))


def open_tab_window(window, doc, config_doc, selected_meas, is_sextuple):
    if is_no_exception(window, selected_meas, doc):
        global tabWindow
        tabWindow = TabWindow(doc, config_doc, selected_meas, is_sextuple)
        window.hide()
        control_tab_window(tabWindow)
        tabWindow.show()


def open_intro_window(tab_window=None):
    window = IntroWindow()
    if tab_window:
        tab_window.hide()
    control_intro_window(window)
    window.show()


if __name__ == "__main__":
    app = QApplication()
    open_intro_window()
    sys.exit(app.exec())
