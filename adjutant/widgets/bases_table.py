""" Wrapper for the Bases Table """

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QWidget

from adjutant.context import Context

from adjutant.windows.base_edit_dialog import BaseEditDialog
from adjutant.widgets.sort_filter_header import SortFilterHeader
from adjutant.widgets.bases_table_view import BasesTableView


class BasesTable(QWidget):
    """Wrapper for Bases Table"""

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.table = BasesTableView(self.context)
        self.header = SortFilterHeader()
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
        self.save_button.pressed.connect(self.context.controller.save_search)

        self.context.signals.show_add_base_dialog.connect(self.show_add_base_dialog)
        self.context.signals.show_edit_base_dialog.connect(self.show_edit_base_dialog)
        self.context.signals.search_loaded.connect(self.search_loaded)

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

    def search_loaded(self):
        """Restore a saved search"""
        self.filter_edit.blockSignals(True)
        self.filter_edit.setText(
            self.context.models.bases_filter_model.filterRegularExpression().pattern()
        )
        self.filter_edit.blockSignals(False)

    def clear_all_filters(self):
        """Clear all filters applied to the table"""
        self.filter_edit.setText("")
        self.context.models.bases_filter_model.clear_all_column_filters()
