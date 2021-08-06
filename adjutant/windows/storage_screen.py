""" Main screen for the Storage layout """

from PyQt6.QtWidgets import QTableView, QVBoxLayout, QWidget
from adjutant.context import Context


class StorageScreen(QWidget):
    """Main widget for all bases-related content"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.storage_table = QTableView(self)

        self._setup_layout()
        self._setup_widgets()

    def _setup_layout(self):
        """Layout widgets"""

        central = QVBoxLayout()
        central.addWidget(self.storage_table)
        self.setLayout(central)

    def _setup_widgets(self):
        """Set up the widgets"""
        self.storage_table.setModel(self.context.models.storage_model)

        self.storage_table.setAlternatingRowColors(True)
        self.storage_table.verticalHeader().setVisible(False)
        self.storage_table.setEditTriggers(
            self.storage_table.EditTrigger.NoEditTriggers
        )
        self.storage_table.setSelectionBehavior(
            self.storage_table.SelectionBehavior.SelectRows
        )
