""" Wrapper for the Bases Table """

from typing import List
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QWidget

from adjutant.context import Context
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
        self.clear_button = QPushButton(self.tr("Clear All Filters"))
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

        self.filter_model.setFilterKeyColumn(-1)  # All columns
        self.filter_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def _setup_signals(self):
        # self.table.selectionModel().selectionChanged.connect(
        #     lambda selected, __: print(selected)
        # )
        self.filter_edit.textChanged.connect(self.filter_model.setFilterRegExp)
        self.clear_button.pressed.connect(self.clear_all_filters)

        self.context.signals.add_base.connect(self.add_base)
        self.context.signals.edit_base.connect(self.edit_base)
        self.context.signals.delete_base.connect(lambda base: self.delete_bases([base]))
        self.context.signals.duplicate_base.connect(self.duplicate_base)
        self.context.signals.delete_bases.connect(self.delete_bases)

        self.context.signals.save_search.connect(self.save_search)
        self.context.signals.load_search.connect(self.load_search)

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
        self.filter_edit.setText(self.filter_model.filterRegExp().pattern())
        self.filter_edit.blockSignals(False)

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_edit.setText("")
        self.filter_model.clear_all_column_filters()
        self.header.update_all_filter_indicators()
