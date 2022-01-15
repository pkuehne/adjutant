""" Wrapper for the Bases Table """

import functools
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import (
    QInputDialog,
    QMenu,
)

from adjutant.context import Context

from adjutant.windows.base_edit_dialog import BaseEditDialog
from adjutant.widgets.sort_filter_table import SortFilterTable


class BasesTable(SortFilterTable):
    """Special functionality for Bases Table"""

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.setModel(self.context.models.bases_model)

        self._setup_signals()

    def _setup_signals(self):

        self.item_edited.connect(self.context.signals.show_edit_base_dialog)
        self.item_deleted.connect(self.context.controller.delete_bases)
        self.context_menu_launched.connect(self.context_menu)

        self.context.signals.show_add_base_dialog.connect(
            lambda: BaseEditDialog.add_base(self.context, self)
        )
        self.context.signals.show_edit_base_dialog.connect(
            lambda index: BaseEditDialog.edit_base(self.context, index, self)
        )

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_model.clear_all_column_filters()

    def context_menu(self, index: QModelIndex):  # pylint: disable=invalid-name
        """When right-click context menu is requested"""
        edit_action = QAction(self.tr("Edit Base"), self)
        edit_action.triggered.connect(
            lambda: self.context.signals.show_edit_base_dialog.emit(index)
        )
        add_action = QAction(self.tr("Add Base"), self)
        add_action.triggered.connect(self.context.signals.show_add_base_dialog.emit)
        delete_action = QAction(self.tr("Delete Bases"), self)
        delete_action.triggered.connect(
            lambda: self.context.controller.delete_bases(self.selected_indexes())
        )

        duplicate_menu = QMenu(self.tr("Duplicate Base"), self)
        for dupes in range(1, 11):
            duplicate_action = QAction(str(dupes) + self.tr(" times"), duplicate_menu)
            duplicate_action.triggered.connect(
                functools.partial(self.context.controller.duplicate_base, index, dupes)
            )
            duplicate_menu.addAction(duplicate_action)

        def generate_title(column: int):
            title_idx = index.siblingAtColumn(column)
            header = index.model().headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            return f"{header} → {title_idx.data()}"

        apply_menu = QMenu(self.tr("Apply to Selection"), self)
        for column in range(1, self.model().columnCount()):
            apply_action = QAction(generate_title(column), apply_menu)
            apply_action.triggered.connect(
                functools.partial(
                    self.context.controller.apply_field_to_bases,
                    index.siblingAtColumn(column),
                    self.selected_indexes(),
                )
            )
            apply_menu.addAction(apply_action)

        filter_menu = QMenu(self.tr("Filter to Selection"), self)
        for column in range(1, self.model().columnCount()):
            filter_action = QAction(generate_title(column), filter_menu)
            filter_action.triggered.connect(
                functools.partial(
                    self.filter_model.set_column_filter,
                    column,
                    [index.siblingAtColumn(column).data()],
                )
            )
            filter_menu.addAction(filter_action)

        menu = QMenu(self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addMenu(duplicate_menu)
        menu.addSeparator()
        menu.addMenu(apply_menu)
        menu.addMenu(filter_menu)
        menu.addSeparator()
        menu.addAction(add_action)
        menu.popup(QCursor.pos())

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
