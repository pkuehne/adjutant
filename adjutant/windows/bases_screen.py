""" Main screen for the Bases layout """

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from adjutant.context import Context
from adjutant.widgets.bases_table import BasesTable


class BasesScreen(QWidget):
    """Main widget for all bases-related content"""

    row_count_changed = pyqtSignal(int)

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.bases_table = BasesTable(self.context)

        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Layout widgets"""

        central = QHBoxLayout()
        central.addWidget(self.bases_table)
        self.setLayout(central)

    def _setup_signals(self):
        """Setup the signals"""
        self.bases_table.table.filter_model.filter_changed.connect(
            lambda: self.row_count_changed.emit(
                self.bases_table.table.filter_model.rowCount()
            )
        )
