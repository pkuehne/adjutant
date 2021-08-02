""" Menu bar for the main window"""

from PyQt6.QtWidgets import QApplication, QMenuBar, QMessageBox
from PyQt6.QtGui import QAction

from adjutant.context import Context
from adjutant.windows.manage_tags_dialog import ManageTagsDialog


class MainWindowMenuBar(QMenuBar):
    """Menu Bar"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context

        self._setup_file_menu()
        self._setup_add_menu()
        self._setup_manage_menu()
        self._setup_help_menu()

    def _setup_file_menu(self):
        """Setup the file menu"""

        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        file_menu = self.addMenu("&File")
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def _setup_add_menu(self):
        """Setup the add menu"""
        bases_action = QAction("&Base", self)
        bases_action.triggered.connect(self.context.signals.show_add_base_dialog.emit)

        add_menu = self.addMenu("&Add")
        add_menu.addAction(bases_action)

    def _setup_manage_menu(self):
        """Setup the Manage menu"""
        tags_action = QAction("Manage &Tags", self)
        tags_action.triggered.connect(
            lambda: ManageTagsDialog.show(self.parent(), self.context)
        )

        manage_menu = self.addMenu("&Manage")
        manage_menu.addAction(tags_action)

    def _setup_help_menu(self):
        """Setup the help menu"""

        about_action = QAction("&About", self)
        about_text = f"Version: {self.context.settings.version_string}"
        about_text += "\nIcons by https://icons8.com"
        about_action.triggered.connect(
            lambda: QMessageBox.about(self, "Adjutant", about_text)
        )

        help_menu = self.addMenu("&Help")
        help_menu.addAction(about_action)
