""" Main screen for the Colours layout """

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from adjutant.widgets.sort_filter_table import SortFilterTable
from adjutant.context import Context

from adjutant.windows.paints_edit_dialog import PaintEditDialog


class PaintsScreen(QWidget):
    """Main widget for all paints content"""

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
        self.table.setModel(self.context.models.paints_model)

    def _setup_signals(self):
        """Setup the signals"""
        self.context.signals.show_add_paint_dialog.connect(
            lambda: PaintEditDialog.add(self.context, self)
        )
        self.table.item_added.connect(self.context.signals.show_add_paint_dialog.emit)
        self.context.signals.show_edit_paint_dialog.connect(
            lambda idx: PaintEditDialog.edit(self.context, idx, self)
        )
        self.table.item_edited.connect(
            lambda idx: PaintEditDialog.edit(self.context, idx, self)
        )
        self.table.item_deleted.connect(self.context.controller.delete_paints)