""" Wrapper for the Bases Table """

from typing import Any, List
from PyQt6.QtCore import QModelIndex
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
        self.table.setModel(self.context.models.bases_filter_model)
        self.table.setHorizontalHeader(self.header)
        self.table.resizeColumnsToContents()
        self.table.hideColumn(self.context.models.bases_model.fieldIndex("storage"))

    def _setup_signals(self):
        # self.table.selectionModel().selectionChanged.connect(
        #     lambda selected, __: print(selected)
        # )
        self.filter_edit.textChanged.connect(
            self.context.models.bases_filter_model.setFilterFixedString
        )
        self.clear_button.pressed.connect(self.clear_all_filters)
        self.save_button.pressed.connect(self.save_search)

        self.context.signals.show_add_base_dialog.connect(self.show_add_base_dialog)
        self.context.signals.show_edit_base_dialog.connect(self.show_edit_base_dialog)

        self.context.signals.save_search.connect(self.save_search)
        self.context.signals.load_search.connect(self.load_search)
        self.context.signals.delete_search.connect(self.delete_search)
        self.context.signals.rename_search.connect(self.rename_search)
        self.context.signals.apply_filter.connect(self.apply_filter)
        self.context.signals.filter_by_id.connect(self.filter_by_id)

    def convert_index(self, index: QModelIndex) -> QModelIndex:
        """Converts index reference to bases_table index"""
        if index.model() == self.context.models.bases_filter_model:
            index = self.context.models.bases_filter_model.mapToSource(index)
        return index

    def show_add_base_dialog(self) -> None:
        """Add a base"""
        BaseEditDialog.add_base(self.context, self)

    def show_edit_base_dialog(self, index: QModelIndex) -> None:
        """Opens the edit dialog"""
        index = self.convert_index(index)
        BaseEditDialog.edit_base(self.context, index, self)

    def save_search(self):
        """Save the current search"""
        name, success = QInputDialog.getText(
            self, self.tr("Save Search"), self.tr("Name of search")
        )
        if not success or not name:
            return
        search = self.context.models.bases_filter_model.encode_filters()
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
        self.context.models.bases_filter_model.decode_filters(record.value("encoded"))
        self.filter_edit.blockSignals(True)
        self.filter_edit.setText(
            self.context.models.bases_filter_model.filterRegularExpression().pattern()
        )
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
        self.context.models.bases_filter_model.clear_all_column_filters()

    def apply_filter(self, column: int, value: Any):
        """Apply the given filter to the given column"""
        # Get all unique items that are not the value passed in
        items = []
        for row in range(self.context.models.bases_filter_model.rowCount()):
            data = self.context.models.bases_filter_model.index(row, column).data()
            if data != value:
                continue
            items.append(data)
        unique = list(set(items))

        self.context.models.bases_filter_model.set_column_filter(column, unique)

    def filter_by_id(self, id_list: List[int]):
        """Filter the ID column by the supplied list"""
        self.context.models.bases_filter_model.set_column_filter(0, id_list)
