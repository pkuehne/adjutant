""" Tests for the main window"""

from pytestqt.qtbot import QtBot
from adjutant.windows.main_window import MainWindow


def test_title_includes_adjutant(qtbot: QtBot):
    """The title should include adjutant"""
    # Given
    win = MainWindow()
    qtbot.addWidget(win)

    # Then
    assert "Adjutant" in win.windowTitle()
