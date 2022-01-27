""" Recipe Edit/Add dialog"""

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QTextEdit
from adjutant.context.context import Context
from adjutant.widgets.recipe_steps_link import RecipeStepsLink
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget


class RecipeEditDialog(AddEditDialog):
    """Add/Edit Dialog for recipes"""

    dialog_reference = None

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.recipes_model

        self.set_title("Recipe")
        self.set_widgets(
            [
                MappedWidget("Notes", QTextEdit(), "notes", b"plainText"),
            ],
            RecipeStepsLink(self.context, index.data()),
        )

        self.setup()

    def delete_function(self, indexes):
        """delete was called on this item"""
        self.context.controller.delete_recipes(indexes)
