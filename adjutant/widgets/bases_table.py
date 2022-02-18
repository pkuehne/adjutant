""" Wrapper for the Bases Table """

import functools
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QInputDialog,
    QMenu,
)

from adjutant.context import Context
from adjutant.widgets.sort_filter_table import SortFilterTable


class BasesTable(SortFilterTable):
    """Special functionality for Bases Table"""

    def __init__(self, context: Context):
        super().__init__(context)
        self.context = context
        self.setModel(self.context.models.bases_model)

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_model.clear_all_column_filters()

    def additional_context_menu_items(self, index: QModelIndex, menu: QMenu):
        """When right-click context menu is requested"""
        duplicate_menu = QMenu(self.tr("Duplicate Base"), self)
        for dupes in range(1, 11):
            duplicate_action = QAction(str(dupes) + self.tr(" times"), duplicate_menu)
            duplicate_action.triggered.connect(
                functools.partial(self.context.controller.duplicate_base, index, dupes)
            )
            duplicate_menu.addAction(duplicate_action)

        menu.addMenu(duplicate_menu)

    def apply_field_to_selection(self, row: int, column: int):
        """Apply the field at index(row, column) to all selected indexes"""
        source = self.model().index(row, column)
        selection = self.selected_indexes()
        self.context.controller.apply_field_to_bases(source, selection)

    def save_search(self):
        """Save the current search"""
        name, success = QInputDialog.getText(None, "Save Search", "Name of search")
        if not success or not name:
            return
        searches = self.context.models.searches_model
        search = self.filter_model.encode_filters()
        record = searches.record()
        record.setNull("id")
        record.setValue("name", name)
        record.setValue("encoded", search)
        success = searches.insertRecord(-1, record)
        searches.submitAll()

    def load_search(self, row: int):
        """Restore a saved search"""
        self.filter_model.clear_all_column_filters()

        if row == -1:
            self.filter_model.setFilterFixedString("")
            return

        record = self.context.models.searches_model.record(row)
        self.filter_model.decode_filters(record.value("encoded"))
