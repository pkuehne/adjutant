""" Tests for the preferences dialog """

from tests.conftest import Context
from adjutant.windows.preferences_dialog import PreferencesDialog


def test_combobox_set_to_current_value(qtbot, context: Context):
    """The combobox should default to the current font_size"""
    # Given
    font_size = 12
    index = context.models.settings_model.index(
        0, context.models.settings_model.fieldIndex("font_size")
    )
    context.models.settings_model.setData(index, font_size)
    context.models.settings_model.submitAll()

    # When
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.font_size.currentText() == str(font_size)


def test_combobox_changing_combobox_updates_model(qtbot, context: Context):
    """The combobox should default to the current font_size"""
    # Given
    font_size = 12
    index = context.models.settings_model.index(
        0, context.models.settings_model.fieldIndex("font_size")
    )
    context.models.settings_model.setData(index, font_size)
    context.models.settings_model.submitAll()
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    dialog.font_size.setCurrentIndex(1)
    dialog.font_size_changed()

    # Then
    assert index.data() != font_size
