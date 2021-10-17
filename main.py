"""
Program entry
"""
import sys
from os import path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from adjutant.windows.main_window import MainWindow


def main(argv):
    """The main"""
    QApplication.setStyle("windows")

    icons_path = path.abspath(path.join(path.dirname(__file__), "resources/icons"))
    QDir.addSearchPath("icons", icons_path)

    app = QApplication(argv)

    window = MainWindow()
    window.setMinimumSize(app.screens()[0].size() * 0.75)

    window.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv)
