""" Main screen for the Recipes layout """

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from adjutant.widgets.sort_filter_table import SortFilterTable
from adjutant.context import Context


class RecipeScreen(QWidget):
    """Main widget for all colour recipes"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.table = SortFilterTable(context, self)

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
        self.table.setModel(self.context.models.recipes_model)

    def _setup_signals(self):
        """Setup the signals"""
        self.table.item_added.connect(
            lambda: self.context.signals.show_add_dialog.emit("recipe", {})
        )
        self.table.item_edited.connect(
            lambda idx: self.context.signals.show_edit_dialog.emit("recipe", idx, {})
        )
        self.table.item_deleted.connect(self.context.controller.delete_recipes)
