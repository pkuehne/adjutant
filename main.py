"""
Program entry
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from adjutant.windows.main_window import MainWindow


def main(argv):
    """The main"""
    # QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setStyle("windows")

    QDir.addSearchPath("icons", "resources/icons")
    QDir.addSearchPath("migrations", "resources/migrations")

    app = QApplication(argv)

    window = MainWindow()
    window.setMinimumSize(app.screens()[0].size() * 0.75)

    window.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv)
