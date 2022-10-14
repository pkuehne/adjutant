""" Menu bar for the main window"""

from PyQt6.QtWidgets import QApplication, QMenu, QMenuBar, QMessageBox, QFileDialog
from PyQt6.QtGui import QAction

from adjutant.context import Context
from adjutant.context.import_export import write_models_to_yaml, read_models_from_yaml
from adjutant.windows.completion_chart_window import CompletionChartWindow
from adjutant.windows.import_paints_dialog import ImportPaintsDialog
from adjutant.windows.manage_operations_dialog import ManageOperationsDialog
from adjutant.windows.manage_statuses_dialog import ManageStatusesDialog
from adjutant.windows.manage_tags_dialog import ManageTagsDialog
from adjutant.windows.manage_searches_dialog import ManageSearchesDialog
from adjutant.windows.preferences_dialog import PreferencesDialog
from adjutant.windows.report_window import ReportWindow


class MainWindowMenuBar(QMenuBar):
    """Menu Bar"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context

        self._setup_file_menu()
        self._setup_add_menu()
        self._setup_reports_menu()
        self._setup_tools_menu()
        self._setup_help_menu()

    def _setup_file_menu(self):
        """Setup the file menu"""

        def export_func():
            filename = QFileDialog.getSaveFileName(
                self, "Export data", filter=self.tr("YAML File (*.yaml)")
            )[0]
            if filename == "":
                return
            write_models_to_yaml(self.context.models.models, filename)
            QMessageBox.information(
                self,
                self.tr("Export complete"),
                self.tr("Export completed successfully!"),
            )

        def import_func():
            filename = QFileDialog.getOpenFileName(
                self, "Open File", filter=self.tr("YAML File (*.yaml)")
            )[0]
            if filename == "":
                return
            read_models_from_yaml(self.context.models.models, filename)
            QMessageBox.information(
                self,
                self.tr("Import complete"),
                self.tr("Import completed successfully!"),
            )

        export_action = QAction("&Export data", self)
        export_action.triggered.connect(export_func)

        import_action = QAction("&Import data", self)
        import_action.triggered.connect(import_func)

        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        file_menu = self.addMenu("&File")
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def _setup_add_menu(self):
        """Setup the add menu"""
        bases_action = QAction("&Base", self)
        bases_action.triggered.connect(self.context.signals.show_add_base_dialog)
        tags_action = QAction("&Tag", self)
        tags_action.triggered.connect(lambda _: self.context.controller.create_tag())
        storage_action = QAction("&Storage", self)
        storage_action.triggered.connect(
            lambda: self.context.signals.show_add_dialog.emit("storage", {})
        )
        paint_action = QAction("&Paint", self)
        paint_action.triggered.connect(
            lambda: self.context.signals.show_add_dialog.emit("paint", {})
        )
        recipe_action = QAction("&Recipe", self)
        recipe_action.triggered.connect(
            lambda: self.context.signals.show_add_dialog.emit("recipe", {})
        )
        scheme_action = QAction("&Scheme", self)
        scheme_action.triggered.connect(
            lambda: self.context.signals.show_add_dialog.emit("scheme", {})
        )

        add_menu = self.addMenu("&Add")
        add_menu.addAction(bases_action)
        add_menu.addAction(tags_action)
        add_menu.addAction(storage_action)
        add_menu.addAction(paint_action)
        add_menu.addAction(recipe_action)
        add_menu.addAction(scheme_action)

    def _setup_reports_menu(self):
        """Setup the Reports menu"""

        report_action = QAction("Generate Report", self)
        report_action.triggered.connect(lambda: ReportWindow.show(self.context))

        completion_chart_action = QAction("Completion Chart", self)
        completion_chart_action.triggered.connect(
            lambda: CompletionChartWindow.show(self.context, None)
        )

        reports_menu = self.addMenu("&Reports")
        reports_menu.addAction(report_action)
        reports_menu.addAction(completion_chart_action)

    def _setup_tools_menu(self):
        """Setup the Tools menu"""
        preferences_action = QAction("&Preferences", self)
        preferences_action.triggered.connect(
            lambda: PreferencesDialog.show(self.parent(), self.context)
        )

        tools_menu = self.addMenu("&Tools")
        manage_menu = tools_menu.addMenu("&Manage Data")
        self._setup_manage_menu(manage_menu)
        import_menu = tools_menu.addMenu("&Import Data")
        self._setup_import_menu(import_menu)

        tools_menu.addSeparator()
        tools_menu.addAction(preferences_action)

    def _setup_manage_menu(self, manage_menu: QMenu):
        """Setup the Manage menu"""
        tags_action = QAction("Manage &Tags", self)
        tags_action.triggered.connect(
            lambda: ManageTagsDialog.show(self.parent(), self.context)
        )
        searches_action = QAction("Manage &Searches", self)
        searches_action.triggered.connect(
            lambda: ManageSearchesDialog.show(self.parent(), self.context)
        )
        statuses_action = QAction("Manage S&tatuses", self)
        statuses_action.triggered.connect(
            lambda: ManageStatusesDialog.show(self.parent(), self.context)
        )
        operations_action = QAction("Manage &Operations", self)
        operations_action.triggered.connect(
            lambda: ManageOperationsDialog.show(self.parent(), self.context)
        )

        manage_menu.addAction(tags_action)
        manage_menu.addAction(searches_action)
        manage_menu.addAction(statuses_action)
        manage_menu.addAction(operations_action)
        return manage_menu

    def _setup_import_menu(self, menu: QMenu):
        """Setup the import menu"""
        paints_action = QAction("Paints", self)
        paints_action.triggered.connect(
            lambda: ImportPaintsDialog.show(self.parent(), self.context)
        )

        menu.addAction(paints_action)

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
