""" Status bar for the main window"""

from PyQt6.QtWidgets import QLabel, QStatusBar

from adjutant.context import Context


class MainWindowStatusBar(QStatusBar):
    """Main Window Status Bar"""

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context

        self.row_count = QLabel()

        self.addPermanentWidget(self.row_count)

        self.context.models.bases_filter_model.filter_changed.connect(
            self.update_row_count
        )
        self.update_row_count()

    def update_row_count(self):
        """Set the row count on the widget"""
        print("Updating")
        self.row_count.setText(
            f"Rows: {self.context.models.bases_filter_model.rowCount()}"
        )
