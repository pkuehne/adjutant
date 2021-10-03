""" Combobox that respects foreign key relationships"""

from PyQt6.QtWidgets import QComboBox, QWidget
from PyQt6.QtCore import pyqtProperty


class ForeignKeyCombobox(QComboBox):
    """A Combobox that respects foreign keys"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)

    @pyqtProperty(int, user=True)
    def current(self) -> int:
        """Retrieve the ID of the currently selected row"""
        row = self.currentIndex()
        value = self.model().index(row, 0).data()
        return value

    @current.setter
    def current(self, value: str):
        """Set the currently selected row to the one with the given ID"""
        for row in range(self.model().rowCount()):
            if self.model().index(row, 0).data() == value:
                self.setCurrentIndex(row)
