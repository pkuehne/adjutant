""" Tests for the recipe edit dialog """

from PyQt6.QtCore import QModelIndex
from adjutant.windows.recipe_edit_dialog import RecipeEditDialog
from tests.conftest import Context


def test_dont_show_delete_button_in_add_mode(qtbot, context: Context):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    dialog = RecipeEditDialog(context, QModelIndex())
    qtbot.addWidget(dialog)

    # When

    # Then
    assert dialog.delete_button.isEnabled() is False
