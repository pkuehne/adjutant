""" Main screen for the Bases layout """

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from adjutant.context import Context
from adjutant.widgets.bases_table import BasesTable
from adjutant.widgets.search_bar import SearchBar


class BasesScreen(QWidget):
    """Main widget for all bases-related content"""

    row_count_changed = pyqtSignal(int)

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.search_bar = SearchBar(self.context)
        self.bases_table = BasesTable(self.context)
        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Layout widgets"""

        central = QVBoxLayout()
        central.addWidget(self.search_bar)
        central.addWidget(self.bases_table)
        self.setLayout(central)

    def _setup_signals(self):
        """Setup the signals"""
        self.search_bar.filter_edit.textChanged.connect(
            self.bases_table.table.filter_model.setFilterFixedString
        )
        self.search_bar.clear_button.pressed.connect(self.bases_table.clear_all_filters)
        self.search_bar.save_button.pressed.connect(self.bases_table.save_search)

        self.bases_table.table.filter_model.filter_changed.connect(
            lambda: self.row_count_changed.emit(
                self.bases_table.table.filter_model.rowCount()
            )
        )
        self.context.signals.load_search.connect(self.load_search)
        self.context.signals.save_search.connect(self.save_search)

    def save_search(self):
        """Save the current search"""
        self.bases_table.save_search()

    def load_search(self, row: int):
        """Load the search and pass to the table and search bar"""
        self.bases_table.load_search(row)
        self.search_bar.load_search(
            self.bases_table.table.filter_model.filterRegularExpression().pattern()
        )
