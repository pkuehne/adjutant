"""
Program entry
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from adjutant.windows.main_window import MainWindow
import adjutant.resources  # pylint: disable=unused-import


def main(argv):
    """The main"""
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    app = QApplication(argv)
    app.setStyle("Windows")
    window = MainWindow()
    window.setFixedSize(app.screens()[0].size() * 0.5)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
