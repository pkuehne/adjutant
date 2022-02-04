""" Combobox that respects foreign key relationships"""

from typing import Callable
from PyQt6.QtCore import pyqtProperty
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QComboBox, QWidget, QPushButton, QHBoxLayout, QSizePolicy


class ForeignKeyCombobox(QWidget):
    """A Combobox that respects foreign keys"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)
        self.combobox = QComboBox()
        self.combobox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
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

    def set_model(self, model, add_callback: Callable = None):
        """Set the combobox model"""
        self.combobox.setModel(model)
        self.combobox.setModelColumn(1)

        if add_callback is not None:
            self.add_button.setHidden(False)
            self.add_button.pressed.connect(add_callback)

    def set_model_column(self, column: int):
        """Override the model column"""
        self.combobox.setModelColumn(column)

    @pyqtProperty(int, user=True)
    def current(self) -> int:
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
