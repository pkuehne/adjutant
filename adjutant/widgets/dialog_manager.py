""" Holds and dispatches the right dialog"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QModelIndex
from adjutant.context import Context
from adjutant.windows.add_edit_dialog import AddEditDialog
from adjutant.windows.component_edit_dialog import ComponentEditDialog
from adjutant.windows.paints_edit_dialog import PaintEditDialog
from adjutant.windows.recipe_edit_dialog import RecipeEditDialog
from adjutant.windows.scheme_edit_dialog import SchemeEditDialog
from adjutant.windows.steps_edit_dialog import StepsEditDialog
from adjutant.windows.storage_edit_dialog import StorageEditDialog


def get_dialog(name: str) -> AddEditDialog:
    """Retrieve dialog by name"""
    return {
        "paint": PaintEditDialog,
        "recipe": RecipeEditDialog,
        "scheme": SchemeEditDialog,
        "step": StepsEditDialog,
        "storage": StorageEditDialog,
        "component": ComponentEditDialog,
    }[name]


class DialogManager(QWidget):
    """Holds dialogs"""

    def __init__(self, context: Context, parent) -> None:
        super().__init__(parent)
        self.context = context

        self.context.signals.show_add_dialog.connect(self.show_add_dialog)
        self.context.signals.show_edit_dialog.connect(self.show_edit_dialog)

    def show_add_dialog(self, name: str, kwargs):
        """Show the Add version of the Add/Edit Dialog"""
        dialog = get_dialog(name)
        dialog.add(self.context, self.parent(), **kwargs)

    def show_edit_dialog(self, name: str, index: QModelIndex, kwargs):
        """Show the Edit version of the Add/Edit Dialog"""
        dialog = get_dialog(name)
        dialog.edit(self.context, index, self.parent(), **kwargs)
