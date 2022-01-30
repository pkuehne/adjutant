""" Storage Edit/Add dialog"""

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QTextEdit

from adjutant.context.context import Context
from adjutant.widgets.scheme_components_link import SchemeComponentsLink
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget


class SchemeEditDialog(AddEditDialog):
    """Add/Edit Dialog for Colour Schemes"""

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.colour_schemes_model

        self.set_title("Recipe")
        self.set_widgets(
            [
                MappedWidget("Notes", QTextEdit(), "notes", b"plainText"),
            ],
            SchemeComponentsLink(self.context, index.data()),
        )

        self.setup()

    def delete_function(self, indexes):
        """delete was called on this item"""
        self.context.controller.delete_schemes(indexes)
