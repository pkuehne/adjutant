""" Tests for the main window"""

import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QMessageBox
from adjutant.windows.main_window import MainWindow


def test_title_includes_adjutant(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch):
    """The title should include adjutant"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.No
    )
    win = MainWindow()
    qtbot.addWidget(win)

    # Then
    assert "Adjutant" in win.windowTitle()


def test_sample_data_can_be_loaded(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch):
    """Sample data should be loaded if requested"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.No
    )
    win = MainWindow()
    qtbot.add_widget(win)

    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.Yes
    )

    # When
    win.load_sample_data()

    # Then
    assert win.context.models.bases_model.rowCount() > 0
    assert win.context.models.bases_model.isDirty() is False
