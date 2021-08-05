""" A date widget that respects None values

    Custom widget that includes a DateEdit as well as a checkbox to enable it
    * If the checkbox is unticked, the value is None
    * If the checkbox is ticked, the value is the DateEdit's value
"""

from datetime import date, datetime
from PyQt6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
)


def _value_from_str(value: str) -> datetime:
    if value == "":
        return None
    return datetime.fromisoformat(value)


class NullableDate(QWidget):
    """Custom widget that allows None as a valid date value"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.checkbox = QCheckBox()
        self.dateedit = QDateEdit()

        self._setup_layout()
        self._setup_signals()

        self.date = None

    def _setup_layout(self):
        """Lays out the checkbox and dateedit"""

        self.checkbox.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        self.dateedit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        central = QHBoxLayout()
        central.addWidget(self.checkbox)
        central.addWidget(self.dateedit)
        central.addStretch()
        central.setContentsMargins(0, 0, 0, 0)

        self.setLayout(central)

    def _setup_signals(self):
        """Setup signals"""
        self.checkbox.toggled.connect(self.dateedit.setVisible)

    @property
    def date(self) -> date:
        """Retrieve the given date"""
        if self.checkbox.isChecked():
            return self.dateedit.date()
        return None

    @date.setter
    def date(self, value: str):
        """Set the given date"""
        if isinstance(value, str):
            value = _value_from_str(value)
        self.checkbox.setChecked(value is not None)
        self.dateedit.setVisible(value is not None)

        if value is not None:
            self.dateedit.setDate(value)
