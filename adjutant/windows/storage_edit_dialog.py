""" Storage Edit/Add dialog"""

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QCheckBox, QSpinBox
from adjutant.context.context import Context
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget


class StorageEditDialog(AddEditDialog):
    """Add/Edit Dialog for storage"""

    dialog_reference = None

    def __init__(
        self, context: Context, index: QModelIndex, parent=None, **kwargs
    ) -> None:
        super().__init__(index, parent, **kwargs)
        self.context = context
        self.model = context.models.storage_model

        self.set_title("Storage")
        self.set_widgets(
            [
                MappedWidget("Location", QLineEdit(), "location"),
                MappedWidget("Height", QSpinBox(), "height"),
                MappedWidget("Magnetized", QCheckBox(), "magnetized"),
                MappedWidget("Full", QCheckBox(), "full"),
                MappedWidget("Notes", QTextEdit(), "notes", b"plainText"),
            ]
        )

        self.setup()

    def delete_function(self, indexes):
        """delete was called on this item"""
        self.context.controller.delete_storages(indexes)
