""" The Main Window """

import logging
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox

from adjutant.context import Context
from adjutant.context.exceptions import (
    DatabaseNeedsMigration,
    NoDatabaseFileFound,
    NoSettingsFileFound,
    SettingsFileCorrupt,
)
from adjutant.context.sample_data import SampleData
from adjutant.context.version import V_MAJOR, V_MINOR, V_PATCH
from adjutant.widgets.dialog_manager import DialogManager
from adjutant.widgets.main_window_menubar import MainWindowMenuBar
from adjutant.widgets.main_window_toolbar import MainWindowToolbar
from adjutant.widgets.main_window_status_bar import MainWindowStatusBar
from adjutant.windows.bases_screen import BasesScreen
from adjutant.windows.schemes_screen import SchemeScreen
from adjutant.windows.storage_screen import StorageScreen
from adjutant.windows.paints_screen import PaintsScreen
from adjutant.windows.recipe_screen import RecipeScreen


class MainWindow(QMainWindow):
    """The Main Window where we start"""

    def __init__(self):
        super().__init__()
        self.first_time = False
        logging.info("Adjutant v%s.%s.%s", V_MAJOR, V_MINOR, V_PATCH)
        self.context = Context()
        self.load_context()
        logging.info("Context loaded")

        if self.first_time:
            QTimer.singleShot(0, self.load_sample_data)

        self.setWindowTitle("Adjutant - " + self.context.settings.version_string)
        self.setWindowIcon(QIcon("icons:adjutant.png"))
        self.context.controller.set_font_size(self.context.settings.font_size)
        self.dialogs = DialogManager(self.context, self)

        self.bases = BasesScreen(self.context)
        self.storage = StorageScreen(self.context)
        self.paints = PaintsScreen(self.context)
        self.recipes = RecipeScreen(self.context)
        self.schemes = SchemeScreen(self.context)

        self.tabbar = QTabWidget(self)
        self.tabbar.addTab(self.bases, self.tr("Bases"))
        self.tabbar.addTab(self.storage, self.tr("Storages"))
        # self.tabbar.addTab(QWidget(), self.tr("Units"))
        # self.tabbar.addTab(QWidget(), self.tr("Forces"))
        self.tabbar.addTab(self.paints, self.tr("Paints"))
        self.tabbar.addTab(self.recipes, self.tr("Recipes"))
        self.tabbar.addTab(self.schemes, self.tr("Schemes"))

        self.setCentralWidget(self.tabbar)

        self.toolbar = MainWindowToolbar(self.context, self)
        self.addToolBar(self.toolbar)
        self.setMenuBar(MainWindowMenuBar(self.context, self))
        status_bar = MainWindowStatusBar(self, self.context)
        self.setStatusBar(status_bar)

        def status_bar_subscription(screen: BasesScreen):
            screen.table.filter_model.filter_changed.connect(
                lambda: status_bar.update_row_count(
                    screen.table.filter_model.rowCount()
                )
            )
            screen.table.selectionModel().selectionChanged.connect(
                lambda _, __: status_bar.update_select_count(
                    len(screen.table.selected_indexes())
                )
            )

        status_bar_subscription(self.bases)
        status_bar_subscription(self.storage)
        status_bar_subscription(self.paints)
        status_bar_subscription(self.recipes)
        status_bar_subscription(self.schemes)

        def update_from_current_widget(_):
            screen: BasesScreen = self.tabbar.currentWidget()
            status_bar.update_row_count(screen.table.filter_model.rowCount())
            status_bar.update_select_count(len(screen.table.selected_indexes()))

        self.tabbar.currentChanged.connect(update_from_current_widget)
        update_from_current_widget(None)

        self.check_version()

    def load_sample_data(self):
        """Load sample data after migration"""
        result = QMessageBox.question(
            self,
            "Load samples?",
            "Welcome to Adjutant!\n"
            "Would you like to load some sample data to see suggestions on how to use Adjutant?",
        )
        if result == QMessageBox.StandardButton.No:
            return

        sample_data = SampleData(self.context.models)
        sample_data.load_all()

    def load_context(self):
        """Load the context from files/etc"""
        logging.debug("Loading settings context")
        try:
            self.context.settings.load()
        except NoSettingsFileFound:
            self.context.settings.save()
        except SettingsFileCorrupt as exc:
            logging.fatal("Settings file is corrupt: %s", exc)
            QMessageBox.critical(self, "Settings File Error", exc.args[0])
            sys.exit(1)

        logging.debug("Loading database")
        try:
            self.context.database.open_database()
        except NoDatabaseFileFound:
            self.first_time = True
            self.context.database.migrate()
        except DatabaseNeedsMigration:
            # Check with user first?
            self.context.database.migrate()
        except RuntimeError as exc:
            logging.fatal("Database error encountered: %s", exc)
            QMessageBox.critical(self, "Database Error", exc.args[0])
            sys.exit(1)

        logging.debug("Loading models")
        try:
            self.context.models.load()
        except RuntimeError as exc:
            logging.fatal("Failed to load models: %s", exc)
            QMessageBox.critical(self, "Model Error", exc.args[0])
            sys.exit(1)

    def check_version(self):
        """Check version against latest online"""
        logging.debug("Checking for newer version")

        def compare_and_alert(html: str):
            if html == "" or html is None:
                logging.warning("Failed to get latest version")
                return
            lines = html.split("\n")
            try:
                major = int(lines[0].split("=")[1])
                minor = int(lines[1].split("=")[1])
                patch = int(lines[2].split("=")[1])
            except IndexError as exc:
                logging.warning("Failed to parse version: %s", exc)
                return
            if major > V_MAJOR or minor > V_MINOR or patch > V_PATCH:
                QMessageBox.information(
                    self, "New version", "A new version of ajdutant has just released!"
                )
                return
            logging.info("No new version")

        self.context.controller.load_latest_version(compare_and_alert)
