""" Paints Edit/Add dialog"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QLineEdit
from adjutant.context.context import Context
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget
from adjutant.widgets.foreign_key_combobox import ForeignKeyCombobox


class StepsEditDialog(AddEditDialog):
    """Add/Edit Dialog for paints"""

    dialog_reference = None

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(index, parent)
        self.context = context
        self.model = context.models.recipe_steps_model

        self.set_title("Recipe Step")

        paint_box = ForeignKeyCombobox()
        paint_box.setModel(self.context.models.paints_model)
        paint_box.setModelColumn(1)
        operation_box = ForeignKeyCombobox()
        operation_box.setModel(self.context.models.step_operations_model)
        operation_box.setModelColumn(1)
        recipe_edit = QLineEdit()
        recipe_edit.setText("0")
        self.hide_name_field()
        # self.do_not_submit()
        self.set_widgets(
            [
                MappedWidget("Recipe", recipe_edit, "recipes_id", hidden=True),
                MappedWidget("Paint", paint_box, "paints_id"),
                MappedWidget("Operation", operation_box, "operations_id"),
            ]
        )

        self.setup()

    def delete_function(self, indexes: List[QModelIndex]):
        """delete was called on this item"""
        self.model.removeRow(indexes[0].row())
        self.model.submitAll()
