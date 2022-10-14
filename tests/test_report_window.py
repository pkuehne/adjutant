""" Tests for the report window """

import pytest
from pytestqt.qtbot import QtBot
from adjutant.windows.report_window import ReportWindow
from adjutant.context import Context


@pytest.fixture(name="win")
def fixture_dialog(qtbot: QtBot, context: Context):
    """Helper to construct the dialog"""
    dialog = ReportWindow(context)
    qtbot.addWidget(dialog)
    return dialog


def test_title_is_set(win: ReportWindow):
    """The title should include adjutant"""
    # Given
    # Then
    assert win.windowTitle() != ""

def test_export_only_enabled_after_generation(win: ReportWindow):
    """ The export button is only enabled after the generate button was clicked"""
    # Given
    assert win.widgets.export_button.isEnabled() is False

    # When
    win.generate_report()

    # Then
    assert win.widgets.export_button.isEnabled() is True