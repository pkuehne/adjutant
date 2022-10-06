""" Combobox that respects foreign key relationships"""

from typing import Callable, Tuple
from PyQt6.QtCore import pyqtProperty, QAbstractItemModel, QSortFilterProxyModel
from PyQt6.QtGui import QIcon, QValidator
from PyQt6.QtWidgets import (
    QComboBox,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)


class ModelContentValidator(QValidator):
    """Validator to ensure that a given string is in the model"""

    def __init__(self, model: QAbstractItemModel, column: int) -> None:
        super().__init__(None)
        self.model = model
        self.column = column

    def set_column(self, column: int):
        """Allows overriding the column to use for validation"""
        self.column = column

    def validate(self, string: str, pos: int) -> Tuple["QValidator.State", str, int]:
        """Validates the given string against the model's data"""
        retval = QValidator.State.Invalid

        for row in range(self.model.rowCount()):
            item: str = self.model.index(row, self.column).data()
            if item.startswith(string):
                retval = QValidator.State.Intermediate
            if item == string:
                retval = QValidator.State.Acceptable
        return (retval, string, pos)


class ForeignKeyCombobox(QWidget):
    """A Combobox that respects foreign keys"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)
        self.combobox = QComboBox()
        self.combobox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.validator = None
        self.add_button = QPushButton()
        self.add_button.setToolTip(self.tr("Add new"))
        self.add_button.setFixedHeight(self.combobox.sizeHint().height())
        self.add_button.setIcon(QIcon("icons:add.png"))
        self.add_button.setHidden(True)

        layout = QHBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.add_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

    def set_model(self, model: QAbstractItemModel, add_callback: Callable = None):
        """Set the combobox model"""
        sort_model = QSortFilterProxyModel(self)
        sort_model.setSourceModel(model)
        sort_model.sort(1)
        self.combobox.setModel(sort_model)
        self.combobox.setModelColumn(1)
        self.combobox.setEditable(True)
        self.combobox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.validator = ModelContentValidator(sort_model, 1)
        self.combobox.lineEdit().setValidator(self.validator)
        assert self.combobox.lineEdit().validator() is not None

        if add_callback is not None:
            self.add_button.setHidden(False)
            self.add_button.pressed.connect(add_callback)

    def set_model_column(self, column: int):
        """Override the model column"""
        self.combobox.setModelColumn(column)
        self.validator.set_column(column)

    @pyqtProperty(str, user=True)
    def current(self) -> str:
        """Retrieve the ID of the currently selected row"""
        row = self.combobox.currentIndex()
        value = self.combobox.model().index(row, 0).data()
        return value

    @current.setter
    def current(self, value: str):
        """Set the currently selected row to the one with the given ID"""
        for row in range(self.combobox.model().rowCount()):
            if self.combobox.model().index(row, 0).data() == value:
                self.combobox.setCurrentIndex(row)
