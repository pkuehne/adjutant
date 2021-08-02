""" Tests for the Manage Tags dialog"""

from PyQt6.QtCore import Qt
from adjutant.context.context import Context
from adjutant.windows.manage_tags_dialog import ManageTagsDialog


def test_rename_button_is_disabled_by_default(qtbot, context: Context):
    """On startun the rename button should be disabled"""
    # Given

    # When
    dialog = ManageTagsDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.rename_button.isEnabled() is False


def test_delete_button_is_disabled_by_default(qtbot, context: Context):
    """On startun the delete button should be disabled"""
    # Given

    # When
    dialog = ManageTagsDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.delete_button.isEnabled() is False


def test_close_button_accepts(qtbot, context: Context):
    """The close button should accept the dialog"""
    # Given
    dialog = ManageTagsDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    with qtbot.waitSignal(dialog.accepted, timeout=10):
        qtbot.mouseClick(dialog.close_button, Qt.MouseButton.LeftButton)

    # Then
    assert dialog.delete_button.isEnabled() is False


def test_selecting_tag_enables_buttons(qtbot, context: Context):
    """Selecting a tag enables the rename and delete buttons"""
    # Given
    dialog = ManageTagsDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    dialog.tag_selected([])

    # Then
    assert dialog.rename_button.isEnabled()
    assert dialog.delete_button.isEnabled()
