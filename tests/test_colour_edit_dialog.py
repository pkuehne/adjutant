""" Tests for the Paints Add/Edit dialog"""

from unittest.mock import MagicMock
from PyQt6.QtCore import QModelIndex
from adjutant.context.context import Context
from adjutant.windows.paints_edit_dialog import PaintEditDialog
from tests.conftest import AddPaintFunc


def test_dont_show_delete_button_in_add_mode(qtbot, context: Context):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    dialog = PaintEditDialog(context, QModelIndex())
    qtbot.addWidget(dialog)

    # When

    # Then
    assert dialog.delete_button.isEnabled() is False


def test_values_submitted_on_add(qtbot, context: Context):
    """When the dialog is submitted, the values should be set on the record"""

    # Given
    dialog = PaintEditDialog(context, QModelIndex())
    qtbot.addWidget(dialog)
    name = "foo"

    # When
    dialog.widgets.name_edit.setText(name)
    dialog.submit_changes()

    # Then
    assert context.models.paints_model.rowCount() == 1
    index = context.models.paints_model.index(0, dialog.field("name"))
    assert index.data() == name


def test_values_submitted_on_edit(qtbot, context: Context, add_paint: AddPaintFunc):
    """When the dialog is submitted, the values should be set on the record"""

    # Given
    add_paint("Foo")
    dialog = PaintEditDialog(context, context.models.paints_model.index(0, 0))
    qtbot.addWidget(dialog)
    name = "Bar"

    # When
    dialog.widgets.name_edit.setText(name)
    dialog.submit_changes()

    # Then
    assert context.models.paints_model.rowCount() == 1
    index = context.models.paints_model.index(0, dialog.field("name"))
    assert index.data() == name


def test_delete_button_calls_controller(
    qtbot, context: Context, add_paint: AddPaintFunc
):
    """When the delete button is pressed, the record is deleted"""
    # Given
    add_paint("Foo")
    add_paint("Bar")
    dialog = PaintEditDialog(context, context.models.paints_model.index(1, 0))
    qtbot.addWidget(dialog)

    context.controller.delete_paints = MagicMock()

    # When
    dialog.delete_button_pressed()

    # Then
    assert context.controller.delete_paints.call_count == 1
