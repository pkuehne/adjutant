""" Main screen for the Bases layout """

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from adjutant.context import Context
from adjutant.widgets.bases_table import BasesTable
from adjutant.widgets.search_bar import SearchBar

from adjutant.windows.base_edit_dialog import BaseEditDialog


class BasesScreen(QWidget):
    """Main widget for all bases-related content"""

    row_count_changed = pyqtSignal(int)

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.search_bar = SearchBar(self.context)
        self.table = BasesTable(self.context)
        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Layout widgets"""

        central = QVBoxLayout()
        central.addWidget(self.search_bar)
        central.addWidget(self.table)
        self.setLayout(central)

    def _setup_signals(self):
        """Setup the signals"""
        self.search_bar.filter_edit.textChanged.connect(
            self.table.filter_model.setFilterFixedString
        )
        self.search_bar.clear_button.pressed.connect(self.table.clear_all_filters)
        self.search_bar.save_button.pressed.connect(self.table.save_search)

        self.table.filter_model.filter_changed.connect(
            lambda: self.row_count_changed.emit(self.table.filter_model.rowCount())
        )
        self.context.signals.load_search.connect(self.load_search)
        self.context.signals.save_search.connect(self.save_search)

        self.context.signals.show_add_base_dialog.connect(
            lambda: BaseEditDialog.add_base(self.context, self)
        )
        self.table.item_added.connect(self.context.signals.show_add_base_dialog.emit)
        self.context.signals.show_edit_base_dialog.connect(
            lambda index: BaseEditDialog.edit_base(self.context, index, self)
        )
        self.table.item_edited.connect(self.context.signals.show_edit_base_dialog.emit)
        self.table.item_deleted.connect(self.context.controller.delete_bases)

    def save_search(self):
        """Save the current search"""
        self.table.save_search()

    def load_search(self, row: int):
        """Load the search and pass to the table and search bar"""
        self.table.load_search(row)
        self.search_bar.load_search(
            self.table.filter_model.filterRegularExpression().pattern()
        )
