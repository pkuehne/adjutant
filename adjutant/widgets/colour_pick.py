""" Colour Pick Widget """

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QLabel, QColorDialog
from PyQt6.QtCore import pyqtProperty


class ColourPick(QLabel):
    """Takes/Returns a hexvalue and shows it as a coloured label"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._hexvalue = "FFFFFF"

    # @property
    @pyqtProperty(str, user=True)
    def hexvalue(self) -> str:
        """Retrieve the hexvalue of the colour"""
        return self._hexvalue

    @hexvalue.setter
    def hexvalue(self, hexvalue: str) -> None:
        """Set the given colour hexvalue"""
        self._hexvalue = hexvalue
        self.setStyleSheet(f"QLabel {{ background-color : {hexvalue}; }}")

    def mousePressEvent(self, _) -> None:  # pylint: disable=invalid-name
        """The label has been clicked"""
        colour = QColor(self._hexvalue)
        colour = QColorDialog.getColor(colour)
        self.hexvalue = colour.name()
