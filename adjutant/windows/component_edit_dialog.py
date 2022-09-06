""" Components Edit/Add dialog"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QLineEdit
from adjutant.context.context import Context
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget
from adjutant.widgets.foreign_key_combobox import ForeignKeyCombobox


class ComponentEditDialog(AddEditDialog):
    """Add/Edit Dialog for components"""

    dialog_reference = None

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.scheme_components_model

        self.set_title("Scheme Component")

        recipe_box = ForeignKeyCombobox()
        recipe_box.set_model(
            self.context.models.recipes_model,
            lambda: self.context.signals.show_add_dialog.emit("recipe", {}),
        )
        name_edit = QLineEdit()
        scheme_edit = QLineEdit()

        self.hide_name_field()
        self.set_widgets(
            [
                MappedWidget(
                    "Scheme",
                    scheme_edit,
                    "schemes_id",
                    hidden=False,
                    default=str(kwargs.get("link_id", 0)),
                ),
                MappedWidget("Name", name_edit, "name"),
                MappedWidget("Recipe", recipe_box, "recipes_id"),
            ]
        )

    def delete_function(self, indexes: List[QModelIndex]):
        """delete was called on this item"""
        self.context.controller.delete_records(self.model, indexes, "components")
