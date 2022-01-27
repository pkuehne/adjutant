""" Paints Edit/Add dialog"""

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QLineEdit, QTextEdit
from adjutant.context.context import Context
from adjutant.widgets.colour_pick import ColourPick
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget


class PaintEditDialog(AddEditDialog):
    """Add/Edit Dialog for paints"""

    dialog_reference = None

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.paints_model

        self.set_title("Paint")
        self.set_widgets(
            [
                MappedWidget("Manufacturer", QLineEdit(), "manufacturer"),
                MappedWidget("Range", QLineEdit(), "range"),
                MappedWidget("Hexvalue", ColourPick(), "hexvalue"),
                MappedWidget("Notes", QTextEdit(), "notes", b"plainText"),
            ]
        )

        self.setup()

    def delete_function(self, indexes):
        """delete was called on this item"""
        self.context.controller.delete_paints(indexes)
