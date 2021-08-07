""" Main screen for the Bases layout """

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from adjutant.context import Context
from adjutant.widgets.bases_table import BasesTable
from adjutant.widgets.sidebar_view import SidebarView


class BasesScreen(QWidget):
    """Main widget for all bases-related content"""

    row_count_changed = pyqtSignal(int)

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.sidebar_view = SidebarView(self.context, self)
        self.bases_table = BasesTable(self.context)
        self.base_detail = QWidget(self)

        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Layout widgets"""

        central = QHBoxLayout()
        central.addWidget(self.sidebar_view)
        central.addStretch()
        central.addWidget(self.bases_table)
        central.addWidget(self.base_detail)
        central.setStretchFactor(self.bases_table, 1)
        self.setLayout(central)

    def _setup_signals(self):
        """Setup the signals"""
        self.sidebar_view.apply_filter.connect(
            self.bases_table.table.filter_model.set_column_filter
        )
        self.bases_table.table.filter_model.filter_changed.connect(
            lambda: self.row_count_changed.emit(
                self.bases_table.table.filter_model.rowCount()
            )
        )
