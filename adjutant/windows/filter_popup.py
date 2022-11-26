""" Popup filter for the bases table header """

from dataclasses import dataclass
from typing import Any, List
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QCursor, QStandardItem, QStandardItemModel, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)
from adjutant.context.dataclasses import Tag
from adjutant.models.sort_filter_model import SortFilterModel


@dataclass(eq=True, frozen=True)
class FilterValue:
    """Filter text and data value"""

    text: str
    value: Any

    def __lt__(self, other):
        return self.text < other.text


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

        self.buttons = {
            "select_all": QPushButton(self.tr("Select all")),
            "unselect_all": QPushButton(self.tr("Unselect all")),
            "sort_ascending": QPushButton(
                QIcon("icons:sort_asc.png"), self.tr("Sort Ascending")
            ),
            "sort_descending": QPushButton(
                QIcon("icons:sort_dsc.png"), self.tr("Sort Descending")
            ),
            "apply": QPushButton(self.tr("Apply")),
            "cancel": QPushButton(self.tr("Cancel")),
        }
        self.filter = QLineEdit()

        self.list_widget = QListView()
        self.list_model = QStandardItemModel()
        self.sort_model = QSortFilterProxyModel()
        self.model = model
        self.column = column

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""
        self.setFixedSize(250, 350)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.buttons["cancel"])
        button_layout.addWidget(self.buttons["apply"])

        select_button_layout = QHBoxLayout()
        select_button_layout.addWidget(self.buttons["select_all"])
        select_button_layout.addWidget(self.buttons["unselect_all"])

        central = QVBoxLayout()
        central.addWidget(self.buttons["sort_ascending"])
        central.addWidget(self.buttons["sort_descending"])
        central.addWidget(QWidget())
        central.addLayout(select_button_layout)
        central.addWidget(self.filter)
        central.addWidget(self.list_widget)
        central.addLayout(button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Configure the widgets"""
        self.sort_model.setSourceModel(self.list_model)
        self.sort_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.list_widget.setModel(self.sort_model)

        self.buttons["sort_ascending"].setCheckable(True)
        self.buttons["sort_descending"].setCheckable(True)
        if self.model.sortColumn() == self.column:
            self.buttons["sort_ascending"].setChecked(
                self.model.sortOrder() == Qt.SortOrder.AscendingOrder
            )
            self.buttons["sort_descending"].setChecked(
                self.model.sortOrder() == Qt.SortOrder.DescendingOrder
            )
        self.filter.setClearButtonEnabled(True)

    def _setup_signals(self):
        """Connect signals"""
        self.list_widget.selectionModel().selectionChanged.connect(
            lambda __, _: self.update_model_check_state()
        )
        self.filter.textChanged.connect(self.sort_model.setFilterRegularExpression)
        self.buttons["select_all"].pressed.connect(self.select_all)
        self.buttons["unselect_all"].pressed.connect(self.unselect_all)
        self.buttons["cancel"].pressed.connect(self.reject)
        self.buttons["apply"].pressed.connect(self.accept)
        self.accepted.connect(self.update_filters)
        self.buttons["sort_ascending"].toggled.connect(self._ascending_clicked)
        self.buttons["sort_descending"].toggled.connect(self._descending_clicked)

    def _ascending_clicked(self, checked: bool):
        """When ascneding button is clicked"""
        if checked:
            self.buttons["sort_descending"].setChecked(False)
            self.model.sort(self.column, Qt.SortOrder.AscendingOrder)
        else:
            self.model.sort(-1, Qt.SortOrder.AscendingOrder)

    def _descending_clicked(self, checked: bool):
        """When the descending button is clicked"""
        if checked:
            self.buttons["sort_ascending"].setChecked(False)
            self.model.sort(self.column, Qt.SortOrder.DescendingOrder)
        else:
            self.model.sort(-1, Qt.SortOrder.DescendingOrder)

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
                items.append(FilterValue(str(display), value))
        unique = list(set(items))
        unique.sort()

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
        index = self.sort_model.mapToSource(indexes[0])
        item = self.list_model.item(index.row(), index.column())
        item.setCheckState(invert_check_state(item.checkState()))

    def unselect_all(self):
        """Uncheck all items"""
        for row in range(self.sort_model.rowCount()):
            index = self.sort_model.index(row, 0)
            item = self.list_model.item(self.sort_model.mapToSource(index).row(), 0)
            item.setCheckState(Qt.CheckState.Unchecked)

    def select_all(self):
        """Check all items"""
        for row in range(self.sort_model.rowCount()):
            index = self.sort_model.index(row, 0)
            item = self.list_model.item(self.sort_model.mapToSource(index).row(), 0)
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
