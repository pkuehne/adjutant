""" Wrapper for the Bases Table """

from typing import Any, List
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QWidget

from adjutant.context import Context
from adjutant.context.database_context import remove_all_tags_for_base
from adjutant.models.bases_filter_model import BasesFilterModel
from adjutant.windows.base_edit_dialog import BaseEditDialog
from adjutant.widgets.bases_table_header import HeaderView
from adjutant.widgets.bases_table_view import BasesTableView


class BasesTable(QWidget):
    """Wrapper for Bases Table"""

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.table = BasesTableView(self.context)
        self.header = HeaderView()
        self.filter_edit = QLineEdit()
        self.clear_button = QPushButton(self.tr("Clear Filters"))
        self.save_button = QPushButton(self.tr("Save Search"))
        self.filter_model = BasesFilterModel()

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
        self.filter_model.setSourceModel(self.context.models.bases_model)
        self.table.setModel(self.filter_model)
        self.table.setHorizontalHeader(self.header)
        self.table.resizeColumnsToContents()
        self.table.hideColumn(self.context.models.bases_model.fieldIndex("storage"))

        self.filter_model.setFilterKeyColumn(-1)  # All columns
        self.filter_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def _setup_signals(self):
        # self.table.selectionModel().selectionChanged.connect(
        #     lambda selected, __: print(selected)
        # )
        self.filter_edit.textChanged.connect(self.filter_model.setFilterFixedString)
        self.clear_button.pressed.connect(self.clear_all_filters)
        self.save_button.pressed.connect(self.save_search)

        self.context.signals.add_base.connect(self.add_base)
        self.context.signals.edit_base.connect(self.edit_base)
        self.context.signals.delete_base.connect(lambda base: self.delete_bases([base]))
        self.context.signals.duplicate_base.connect(self.duplicate_base)
        self.context.signals.delete_bases.connect(self.delete_bases)
        self.context.signals.update_bases.connect(
            self.context.models.bases_model.submitAll
        )
        self.context.signals.add_tags.connect(self.add_tags)
        self.context.signals.remove_tags.connect(self.remove_tags)
        self.context.signals.set_tags.connect(self.set_tags)

        self.context.signals.save_search.connect(self.save_search)
        self.context.signals.load_search.connect(self.load_search)
        self.context.signals.delete_search.connect(self.delete_search)
        self.context.signals.rename_search.connect(self.rename_search)
        self.context.signals.apply_filter.connect(self.apply_filter)

    def convert_index(self, index: QModelIndex) -> QModelIndex:
        """Converts index reference to bases_table index"""
        if index.model() == self.filter_model:
            index = self.filter_model.mapToSource(index)
        return index

    def edit_base(self, index: QModelIndex) -> None:
        """Opens the edit dialog"""
        index = self.convert_index(index)
        BaseEditDialog.edit_base(self.context, index, self)

    def add_base(self) -> None:
        """Add a base"""
        BaseEditDialog.add_base(self.context, self)

    def delete_bases(self, indexes: List[QModelIndex]):
        """Delete all currently selected rows"""
        result = QMessageBox.warning(
            self,
            "Confirm deletion",
            "Are you sure you want to delete these bases?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        for index in indexes:
            index = self.convert_index(index)
            self.context.models.bases_model.removeRow(index.row())
        self.context.models.bases_model.submitAll()

    def duplicate_base(self, index: QModelIndex, num: int) -> None:
        """Duplicate the given base num times"""
        index = self.convert_index(index)
        for _ in range(num):
            record = self.context.models.bases_model.record(index.row())
            record.setNull("id")
            self.context.models.bases_model.insertRecord(-1, record)
        self.context.models.bases_model.submitAll()

    def add_tags(self, index: QModelIndex, tags: List[int]):
        """Add the tags to the given base"""
        model = self.context.models.base_tags_model
        for tag in tags:
            record = model.record()
            record.setNull("id")
            record.setValue("base_id", index.siblingAtColumn(0).data())
            record.setValue("tag_id", tag)
            model.insertRecord(-1, record)

        model.submitAll()

    def remove_tags(self, index: QModelIndex, tags: List[int]):
        """Remome tags"""

    def set_tags(self, index: QModelIndex, tags: List[int]):
        """Remove all tags and set to parameter"""
        # Remove all tags
        base_id = index.siblingAtColumn(0).data()
        remove_all_tags_for_base(self.context.database, base_id)
        self.context.models.base_tags_model.select()

        self.add_tags(index, tags)

    def save_search(self):
        """Save the current search"""
        name, success = QInputDialog.getText(
            self, self.tr("Save Search"), self.tr("Name of search")
        )
        if not success or not name:
            return
        search = self.filter_model.encode_filters()
        record = self.context.models.searches_model.record()
        record.setNull("id")
        record.setValue("name", name)
        record.setValue("encoded", search)
        success = self.context.models.searches_model.insertRecord(-1, record)
        self.context.models.searches_model.submitAll()

    def load_search(self, row: int):
        """Restore a saved search"""
        self.clear_all_filters()

        if row == -1:
            return
        record = self.context.models.searches_model.record(row)
        self.filter_model.decode_filters(record.value("encoded"))
        self.filter_edit.blockSignals(True)
        self.filter_edit.setText(self.filter_model.filterRegularExpression().pattern())
        self.filter_edit.blockSignals(False)

    def delete_search(self, row: int):
        """Delete the given search"""
        result = QMessageBox.warning(
            self,
            "Confirm deletion",
            "Are you sure you want to delete this search?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        self.context.models.searches_model.removeRow(row)
        self.context.models.searches_model.submitAll()

    def rename_search(self, row: int, name: str):
        """Rename the given search"""
        # index = self.context.models.searches_model.index(row, record.)
        model = self.context.models.searches_model
        record = model.record(row)
        record.setValue("name", name)
        model.setRecord(row, record)
        model.submitAll()

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_edit.setText("")
        self.filter_model.clear_all_column_filters()
        self.header.update_all_filter_indicators()

    def apply_filter(self, column: int, value: Any):
        """Apply the given filter to the given column"""
        # Get all unique items that are not the value passed in
        items = []
        for row in range(self.filter_model.rowCount()):
            data = self.filter_model.index(row, column).data()
            if data == value:
                continue
            items.append(data)
        unique = list(set(items))

        self.filter_model.set_column_filter(column, unique)
