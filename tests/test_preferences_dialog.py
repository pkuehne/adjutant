""" Tests for the preferences dialog """

from pytestqt.qtbot import QtBot
from tests.conftest import Context
from adjutant.windows.preferences_dialog import PreferencesDialog


def test_combobox_set_to_current_value(qtbot: QtBot, context: Context):
    """The combobox should default to the current font_size"""
    # Given
    font_size = 12
    context.settings.font_size = font_size

    # When
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.font_size.currentText() == str(font_size)


def test_combobox_changing_combobox_updates_settings(qtbot: QtBot, context: Context):
    """Changing the combobox updates settings"""
    # Given
    font_size = 12
    context.settings.font_size = font_size
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    dialog.font_size.setCurrentIndex(1)
    dialog.font_size_changed()

    # Then
    assert context.settings.font_size != font_size
