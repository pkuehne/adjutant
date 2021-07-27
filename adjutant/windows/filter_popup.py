""" Popup filter for the bases table header """

from typing import cast
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from adjutant.models.bases_filter_model import BasesFilterModel


def from_check_state(value: Qt.CheckState) -> bool:
    """Convert CheckState -> Boolean"""
    return value == Qt.CheckState.Checked


def to_check_state(value: bool) -> Qt.CheckState:
    """Convert Boolean -> CHeckstate"""
    if value:
        return Qt.CheckState.Checked
    return Qt.CheckState.Unchecked


def invert_check_state(value: Qt.CheckState) -> Qt.CheckState:
    """Toggles the checkstate value"""
    if value == Qt.CheckState.Checked:
        return Qt.CheckState.Unchecked
    return Qt.CheckState.Checked


class FilterPopup(QDialog):
    """Pops up when clicking on the Bases table header"""

    def __init__(
        self, parent: QWidget, model: QSortFilterProxyModel, column: int
    ) -> None:
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)

        self.select_all_button = QPushButton(self.tr("Select all"))
        self.unselect_all_button = QPushButton(self.tr("Unselect all"))
        self.ok_button = QPushButton(self.tr("Apply"))
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.list_widget = QListView()
        self.list_model = QStandardItemModel()
        self.model = model
        self.column = column

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""
        self.setFixedSize(180, 300)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        central = QVBoxLayout()
        central.addWidget(self.select_all_button)
        central.addWidget(self.unselect_all_button)
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
        self.select_all_button.pressed.connect(self.select_all)
        self.unselect_all_button.pressed.connect(self.unselect_all)
        self.cancel_button.pressed.connect(self.reject)
        self.ok_button.pressed.connect(self.accept)
        self.accepted.connect(self.update_filters)

    def setup_filter(self) -> None:
        """Retrieves unique items from model at that column"""
        filter_model = cast(BasesFilterModel, self.model)
        current_filters = filter_model.get_column_filter(self.column)
        model = filter_model.sourceModel()

        items = []
        for row in range(model.rowCount()):
            items.append(model.index(row, self.column).data())
        unique = list(set(items))

        for value in unique:
            item = QStandardItem(str(value))
            item.setCheckable(True)
            checked = not (current_filters is not None and value not in current_filters)
            item.setCheckState(to_check_state(checked))
            item.setData(value, Qt.ItemDataRole.UserRole + 1)
            self.list_model.appendRow(item)

    def update_model_check_state(self):
        """Update the model when an item is selected"""
        indexes = self.list_widget.selectionModel().selectedIndexes()
        if not indexes:
            return
        item = self.list_model.item(indexes[0].row(), indexes[0].column())
        item.setCheckState(invert_check_state(item.checkState()))

    def unselect_all(self):
        """Uncheck all items"""
        for row in range(self.list_model.rowCount()):
            item = self.list_model.item(row, 0)
            item.setCheckState(Qt.CheckState.Unchecked)

    def select_all(self):
        """Uncheck all items"""
        for row in range(self.list_model.rowCount()):
            item = self.list_model.item(row, 0)
            item.setCheckState(Qt.CheckState.Checked)

    def update_filters(self):
        """Update the filters for this column on the filter model"""
        filter_list = []
        for row in range(self.list_model.rowCount()):
            item = self.list_model.item(row, 0)
            if from_check_state(item.checkState()):
                filter_list.append(item.data(Qt.ItemDataRole.UserRole + 1))

        if len(filter_list) == self.list_model.rowCount():
            filter_list = None
        model = cast(BasesFilterModel, self.model)
        model.set_column_filter(self.column, filter_list)
