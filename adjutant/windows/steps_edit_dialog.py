""" Steps Edit/Add dialog"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QLineEdit
from adjutant.context.context import Context
from adjutant.models.row_zero_filter_model import RowZeroFilterModel
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget
from adjutant.widgets.foreign_key_combobox import ForeignKeyCombobox


class StepsEditDialog(AddEditDialog):
    """Add/Edit Dialog for Steps"""

    dialog_reference = None

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.recipe_steps_model

        self.set_title("Recipe Step")

        paint_box = ForeignKeyCombobox()
        paint_box.set_model(
            self.context.models.paints_model,
            lambda: self.context.signals.show_add_dialog.emit("paint", {}),
        )
        operation_box = ForeignKeyCombobox()
        model = RowZeroFilterModel()
        model.setSourceModel(self.context.models.step_operations_model)
        operation_box.set_model(
            model
            # , lambda: self.context.signals.show_add_dialog.emit("operation", {}),
        )
        recipe_edit = QLineEdit()
        step_edit = QLineEdit()

        self.hide_name_field()
        self.set_widgets(
            [
                MappedWidget(
                    "Recipe",
                    recipe_edit,
                    "recipes_id",
                    hidden=True,
                    default=kwargs.get("link_id", 0),
                ),
                MappedWidget(
                    "Priority",
                    step_edit,
                    "priority",
                    hidden=True,
                    default=kwargs.get("priority", 0),
                ),
                MappedWidget("Paint", paint_box, "paints_id"),
                MappedWidget("Operation", operation_box, "operations_id"),
            ]
        )

    def delete_function(self, indexes: List[QModelIndex]):
        """delete was called on this item"""
        self.context.controller.delete_records(self.model, indexes, "steps")
