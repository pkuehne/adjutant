""" Main screen for the Bases layout """

from PyQt5.QtWidgets import QHBoxLayout, QWidget
from adjutant.context import Context
from adjutant.widgets.bases_table import BasesTable


class BasesScreen(QWidget):
    """Main widget for all bases-related content"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.filter_selection = QWidget(self)
        self.bases_table = BasesTable(self.context)
        self.base_detail = QWidget(self)

        self._setup_layout()

    def _setup_layout(self):
        """Layout widgets"""

        central = QHBoxLayout()
        central.addWidget(self.filter_selection)
        central.addWidget(self.bases_table)
        central.addWidget(self.base_detail)
        self.setLayout(central)
