""" The Main Window """

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from adjutant.context import Context
from adjutant.widgets.main_window_menubar import MainWindowMenuBar
from adjutant.widgets.main_window_toolbar import MainWindowToolbar
from adjutant.windows.bases_screen import BasesScreen


class MainWindow(QMainWindow):
    """The Main Window where we start"""

    def __init__(self):
        super().__init__()
        self.context = Context()
        self.context.settings.set_version("0.1.0-dev")
        self.context.load_database(":memory:")

        self.setWindowTitle("Adjutant - " + self.context.settings.version_string)
        self.setWindowIcon(QIcon(":/icons/adjutant.png"))
        self.bases = BasesScreen(self.context)
        self.setCentralWidget(self.bases)

        self.toolbar = MainWindowToolbar(self.context, self)
        self.addToolBar(self.toolbar)
        self.setMenuBar(MainWindowMenuBar(self.context, self))
