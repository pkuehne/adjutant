""" Popup filter for the bases table header """

from typing import cast
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from adjutant.models.bases_filter_model import BasesFilterModel


class FilterPopup(QDialog):
    """Pops up when clicking on the Bases table header"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        self.clear_button = QPushButton(self.tr("Clear Filter"))
        self.ok_button = QPushButton(self.tr("Apply"))
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.list_widget = QListView()
        self.list_model = QStandardItemModel()
        self.index = QModelIndex()

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""
        self.setFixedSize(500, 600)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        central = QVBoxLayout()
        central.addWidget(self.clear_button)
        central.addWidget(self.list_widget)
        central.addLayout(button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Configure the widgets"""
        self.list_widget.setModel(self.list_model)

    def _setup_signals(self):
        """Connect signals"""
        self.list_widget.selectionModel().selectionChanged.connect(
            lambda __, _: self.update_model_check_state()
        )
        self.clear_button.pressed.connect(self.clear_filters)
        self.cancel_button.pressed.connect(self.reject)
        self.ok_button.pressed.connect(self.accept)
        self.accepted.connect(self.update_filters)

    def set_source_index(self, index: QModelIndex) -> None:
        """Retrieves unique items from model at that column"""
        self.index = index
        column = index.column()
        filter_model = cast(BasesFilterModel, index.model())
        current_filters = filter_model.get_column_filter(column)
        model = filter_model.sourceModel()

        items = []
        for row in range(model.rowCount()):
            items.append(model.index(row, column).data())
        unique = list(set(items))

        for value in unique:
            item = QStandardItem(str(value))
            item.setCheckable(True)
            item.setCheckState(value not in current_filters)
            item.setData(value, Qt.UserRole + 1)
            self.list_model.appendRow(item)

    def update_model_check_state(self):
        """Update the model when an item is selected"""
        indexes = self.list_widget.selectionModel().selectedIndexes()
        if not indexes:
            return
        item = self.list_model.item(indexes[0].row(), indexes[0].column())
        item.setCheckState(not item.checkState())

    def clear_filters(self):
        """Clear all set filters"""
        model = cast(BasesFilterModel, self.index.model())
        model.set_column_filter(self.index.column(), [])
        self.reject()

    def update_filters(self):
        """Update the filters for this column on the filter model"""
        filter_list = []
        for row in range(self.list_model.rowCount()):
            item = self.list_model.item(row, 0)
            if not item.checkState():
                filter_list.append(item.data(Qt.UserRole + 1))

        model = cast(BasesFilterModel, self.index.model())
        model.set_column_filter(self.index.column(), filter_list)
