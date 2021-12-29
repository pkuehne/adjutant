""" Tests for the preferences dialog """

from tests.conftest import Context
from adjutant.windows.preferences_dialog import PreferencesDialog


def test_combobox_set_to_current_value(qtbot, context: Context):
    """The combobox should default to the current font_size"""
    # Given
    font_size = 12
    record = context.models.settings_model.record(0)
    record.setValue("font_size", font_size)
    context.models.settings_model.setRecord(0, record)

    # When
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.font_size.currentText() == str(font_size)


def test_combobox_changing_combobox_updates_model(qtbot, context: Context):
    """The combobox should default to the current font_size"""
    # Given
    font_size = 12
    record = context.models.settings_model.record(0)
    record.setValue("font_size", font_size)
    context.models.settings_model.setRecord(0, record)
    dialog = PreferencesDialog(None, context)
    qtbot.addWidget(dialog)

    # When
    dialog.font_size.setCurrentIndex(1)
    dialog.font_size_changed()

    # Then
    assert context.models.settings_model.record(0).value("font_size") != font_size
