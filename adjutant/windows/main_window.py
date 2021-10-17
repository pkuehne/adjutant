""" The Main Window """

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget

from adjutant.context import Context
from adjutant.widgets.main_window_menubar import MainWindowMenuBar
from adjutant.widgets.main_window_toolbar import MainWindowToolbar
from adjutant.widgets.main_window_status_bar import MainWindowStatusBar
from adjutant.windows.bases_screen import BasesScreen
from adjutant.windows.storage_screen import StorageScreen


class MainWindow(QMainWindow):
    """The Main Window where we start"""

    def __init__(self):
        super().__init__()
        self.context = Context()
        self.context.settings.set_version("0.1.0-dev")
        self.context.settings.database_version = 1
        self.context.load_database("data.db")
        # self.context.load_database(":memory:")
        self.context.models.refresh_models()
        if self.context.models.bases_model.rowCount() == 0:
            self.context.database.execute_sql_file("populate_test_data.sql")
        self.context.models.refresh_models()

        self.setWindowTitle("Adjutant - " + self.context.settings.version_string)
        self.setWindowIcon(QIcon("icons:adjutant.png"))

        self.bases = BasesScreen(self.context)
        self.storage = StorageScreen(self.context)

        self.tabbar = QTabWidget(self)
        self.tabbar.addTab(self.bases, "Bases")
        self.tabbar.addTab(QWidget(), "Units")
        self.tabbar.addTab(QWidget(), "Forces")
        self.tabbar.addTab(self.storage, "Storage")

        self.setCentralWidget(self.tabbar)

        self.toolbar = MainWindowToolbar(self.context, self)
        self.addToolBar(self.toolbar)
        self.setMenuBar(MainWindowMenuBar(self.context, self))
        self.setStatusBar(MainWindowStatusBar(self, self.context))

        self.bases.row_count_changed.connect(self.statusBar().update_row_count)
        self.statusBar().update_row_count(
            self.bases.bases_table.table.filter_model.rowCount()
        )
