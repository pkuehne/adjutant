""" Main screen for the Colours layout """

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from adjutant.widgets.sort_filter_table import SortFilterTable
from adjutant.context import Context


class SchemeScreen(QWidget):
    """Main widget for all colour schemes"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.table = SortFilterTable(self)

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Layout widgets"""

        central = QVBoxLayout()
        central.addWidget(self.table)
        self.setLayout(central)

    def _setup_widgets(self):
        """Set up the widgets"""
        self.table.setModel(self.context.models.colour_schemes_model)
        self.table.hideRow(0)

    def _setup_signals(self):
        """Setup the signals"""
        self.table.item_added.connect(
            lambda: self.context.signals.show_add_dialog.emit("scheme", {})
        )
        self.table.item_edited.connect(
            lambda idx: self.context.signals.show_edit_dialog.emit("scheme", idx, {})
        )
        self.table.item_deleted.connect(self.context.controller.delete_schemes)
