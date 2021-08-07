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

    def update_row_count(self, count: int):
        """Set the row count on the widget"""
        self.row_count.setText(self.tr("Rows: ") + f"{count}")
