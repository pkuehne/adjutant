""" Wrapper for the Bases Table """

import functools
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QWidget

from adjutant.context import Context

from adjutant.windows.base_edit_dialog import BaseEditDialog
from adjutant.widgets.sort_filter_table import SortFilterTable


class BasesTable(QWidget):
    """Wrapper for Bases Table"""

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.table = SortFilterTable(self)
        self.filter_edit = QLineEdit()
        self.clear_button = QPushButton(self.tr("Clear Filters"))
        self.save_button = QPushButton(self.tr("Save Search"))

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel(self.tr("Filter: ")))
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(self.clear_button)
        filter_layout.addWidget(self.save_button)

        central = QVBoxLayout()
        central.addLayout(filter_layout)
        central.addWidget(self.table)

        self.setLayout(central)

    def _setup_widgets(self):
        """Initialize and configure widgets"""
        self.table.setModel(self.context.models.bases_model)

    def _setup_signals(self):
        self.filter_edit.textChanged.connect(
            self.table.filter_model.setFilterFixedString
        )
        self.clear_button.pressed.connect(self.clear_all_filters)
        self.save_button.pressed.connect(self.save_search)

        self.table.item_edited.connect(self.context.signals.show_edit_base_dialog)
        self.table.item_deleted.connect(self.context.controller.delete_bases)
        self.table.context_menu_launched.connect(self.context_menu)

        self.context.signals.show_add_base_dialog.connect(
            lambda: BaseEditDialog.add_base(self.context, self)
        )
        self.context.signals.show_edit_base_dialog.connect(
            lambda index: BaseEditDialog.edit_base(self.context, index, self)
        )
        self.context.signals.load_search.connect(self.load_search)
        self.context.signals.save_search.connect(self.save_search)

    def search_loaded(self):
        """Restore a saved search"""
        self.filter_edit.blockSignals(True)
        self.filter_edit.setText(
            self.table.filter_model.filterRegularExpression().pattern()
        )
        self.filter_edit.blockSignals(False)

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_edit.setText("")
        self.table.filter_model.clear_all_column_filters()

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
            lambda: self.context.controller.delete_bases(self.table.selected_indexes())
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
        for column in range(1, self.table.model().columnCount()):
            apply_action = QAction(generate_title(column), apply_menu)
            apply_action.triggered.connect(
                functools.partial(
                    self.context.controller.apply_field_to_bases,
                    index.siblingAtColumn(column),
                    self.table.selected_indexes(),
                )
            )
            apply_menu.addAction(apply_action)

        filter_menu = QMenu(self.tr("Filter to Selection"), self)
        for column in range(1, self.table.model().columnCount()):
            filter_action = QAction(generate_title(column), filter_menu)
            filter_action.triggered.connect(
                functools.partial(
                    self.table.filter_model.set_column_filter,
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
        source = self.table.model().index(row, column)
        selection = self.table.selected_indexes()
        self.context.controller.apply_field_to_bases(source, selection)

    def save_search(self):
        """Save the current search"""
        name, success = QInputDialog.getText(None, "Save Search", "Name of search")
        if not success or not name:
            return
        searches = self.context.models.searches_model
        search = self.table.filter_model.encode_filters()
        record = searches.record()
        record.setNull("id")
        record.setValue("name", name)
        record.setValue("encoded", search)
        success = searches.insertRecord(-1, record)
        searches.submitAll()

    def load_search(self, row: int):
        """Restore a saved search"""
        self.table.filter_model.clear_all_column_filters()

        if row == -1:
            self.table.filter_model.setFilterFixedString("")
            self.search_loaded()
            return

        record = self.context.models.searches_model.record(row)
        self.table.filter_model.decode_filters(record.value("encoded"))
        self.search_loaded()
