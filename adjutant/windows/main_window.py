""" The Main Window """

import sys
from typing import List
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox

from adjutant.context import Context
from adjutant.context.exceptions import (
    DatabaseNeedsMigration,
    NoDatabaseFileFound,
    NoSettingsFileFound,
    SettingsFileCorrupt,
)
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
        self.context = Context()
        self.load_context()

        if self.context.models.bases_model.rowCount() == 0:
            self.context.database.execute_sql_file("populate_test_data.sql")
        self.context.models.refresh_models()

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
        self.setStatusBar(MainWindowStatusBar(self, self.context))

        self.bases.row_count_changed.connect(self.statusBar().update_row_count)
        self.statusBar().update_row_count(self.bases.table.filter_model.rowCount())
        self.check_version()

    def load_context(self):
        """Load the context from files/etc"""
        try:
            self.context.settings.load()
        except NoSettingsFileFound:
            self.context.settings.save()
        except SettingsFileCorrupt as exc:
            QMessageBox.critical(self, "Settings File Error", exc.args[0])
            sys.exit(1)

        try:
            self.context.database.open_database("adjutant.db")
        except NoDatabaseFileFound:
            self.context.database.migrate()
        except DatabaseNeedsMigration:
            # Check with user first?
            self.context.database.migrate()
        except RuntimeError as exc:
            QMessageBox.critical(self, "Database Error", exc.args[0])
            sys.exit(1)

        try:
            self.context.models.load()
        except RuntimeError as exc:
            QMessageBox.critical(self, "Model Error", exc.args[0])
            sys.exit(1)

    def check_version(self):
        """Check version against latest online"""

        def compare_and_alert(lines: List[str]):
            if lines == [""]:
                print("Failed to get version")
                return
            try:
                major = int(lines[0].split("=")[1])
                minor = int(lines[1].split("=")[1])
                patch = int(lines[2].split("=")[1])
            except IndexError:
                print("Failed to parse version")
                return
            if major > V_MAJOR or minor > V_MINOR or patch > V_PATCH:
                QMessageBox.information(
                    self, "New version", "A new version of ajdutant has just released!"
                )
                return
            # print("No new version")

        self.context.controller.load_latest_version(compare_and_alert)
