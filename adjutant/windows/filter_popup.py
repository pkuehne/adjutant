""" Popup filter for the bases table header """

from dataclasses import dataclass
from typing import Any, List
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QCursor, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from adjutant.context.dataclasses import Tag
from adjutant.models.sort_filter_model import SortFilterModel


@dataclass(eq=True, frozen=True)
class FilterValue:
    """Filter text and data value"""

    text: str
    value: Any


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

    def __init__(self, parent: QWidget, model: SortFilterModel, column: int) -> None:
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
        current_filters = self.model.get_column_filter(self.column)
        model = self.model.sourceModel()

        items: List[FilterValue] = []
        for row in range(model.rowCount()):
            index = model.index(row, self.column)
            value = index.data(Qt.ItemDataRole.EditRole)
            display = index.data(Qt.ItemDataRole.DisplayRole)

            if isinstance(value, list):
                value: List[Tag] = value
                for tag in value:
                    items.append(FilterValue(tag.tag_name, tag.tag_id))
            else:
                items.append(FilterValue(display, value))
        unique = list(set(items))

        for filter_ in unique:
            item = QStandardItem(filter_.text)
            item.setCheckable(True)
            checked = not (
                current_filters is not None and filter_.value not in current_filters
            )
            item.setCheckState(to_check_state(checked))
            item.setData(filter_.value, Qt.ItemDataRole.UserRole + 1)
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
        self.model.set_column_filter(self.column, filter_list)

    @classmethod
    def show(cls, parent: QWidget, model: QSortFilterProxyModel, column: int):
        """Show the dialog"""
        cls.dialog_reference = cls(parent, model, column)
        cursor = QCursor().pos()
        cls.dialog_reference.setGeometry(
            cursor.x(),
            cursor.y(),
            cls.dialog_reference.width(),
            cls.dialog_reference.height(),
        )
        cls.dialog_reference.setup_filter()
        cls.dialog_reference.exec()
        cls.dialog_reference = None
