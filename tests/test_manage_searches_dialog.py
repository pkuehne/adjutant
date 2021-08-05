""" Tests for the Manage Searches dialog"""

from PyQt6.QtCore import Qt
from adjutant.context.context import Context
from adjutant.windows.manage_searches_dialog import ManageSearchesDialog


def test_rename_button_is_disabled_by_default(qtbot, context: Context):
    """On startun the rename button should be disabled"""
    # Given

    # When
    dialog = ManageSearchesDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.rename_button.isEnabled() is False


def test_delete_button_is_disabled_by_default(qtbot, context: Context):
    """On startun the delete button should be disabled"""
    # Given

    # When
    dialog = ManageSearchesDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.delete_button.isEnabled() is False


def test_close_button_accepts(qtbot, context: Context):
    """The close button should accept the dialog"""
    # Given
    dialog = ManageSearchesDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    with qtbot.waitSignal(dialog.accepted, timeout=10):
        qtbot.mouseClick(dialog.close_button, Qt.MouseButton.LeftButton)

    # Then
    assert dialog.delete_button.isEnabled() is False


def test_selecting_tag_enables_buttons(qtbot, context: Context):
    """Selecting a tag enables the rename and delete buttons"""
    # Given
    dialog = ManageSearchesDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    dialog.search_selected([])

    # Then
    assert dialog.rename_button.isEnabled()
    assert dialog.delete_button.isEnabled()
