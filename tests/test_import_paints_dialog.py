""" Tests for the Online Import Dialog"""

from pathlib import Path
import pytest
from pytestqt.qtbot import QtBot

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

from adjutant.context.context import Context
from adjutant.context.url_loader import UrlLoader
from adjutant.windows.import_paints_dialog import ImportPaintsDialog, PaintItem
from adjutant.windows.online_import_dialog import OnlineImportDialog


@pytest.fixture(name="win")
def fixture_dialog(monkeypatch: pytest.MonkeyPatch, qtbot: QtBot, context: Context):
    """Helper to construct the dialog"""
    monkeypatch.setattr(UrlLoader, "load_yaml_from_url", lambda *args: None)
    dialog = ImportPaintsDialog(None, context)
    qtbot.addWidget(dialog)
    return dialog


def test_title_is_set(win: ImportPaintsDialog):
    """The title should include adjutant"""
    # Given
    # Then
    assert win.windowTitle() != ""


def test_load_from_online_adds_row_per_paint(
    win: ImportPaintsDialog, monkeypatch: pytest.MonkeyPatch
):
    """For each paint returned from online import, add a row"""
    # Given
    paints = [
        {"name": "foo", "desc": "test range", "manufacturer": "Someone"},
        {"name": "bar", "range": "test range", "manufacturer": "Someone"},
        {"name": "baz", "range": "other range", "manufacturer": "Else"},
    ]
    monkeypatch.setattr(OnlineImportDialog, "show", lambda *args: paints)

    # When
    win.load_from_online()

    # Then
    assert len(win.paints) == len(paints)
    assert win.item_table.rowCount() == len(paints)


def test_load_from_online_does_nothing_on_empty_list(
    win: ImportPaintsDialog, monkeypatch: pytest.MonkeyPatch
):
    """For each paint returned from online import, add a row"""
    # Given
    win.paints = [
        {"name": "foo", "desc": "test range", "manufacturer": "Someone"},
        {"name": "bar", "range": "test range", "manufacturer": "Someone"},
        {"name": "baz", "range": "other range", "manufacturer": "Else"},
    ]
    monkeypatch.setattr(OnlineImportDialog, "show", lambda *args: [])

    # When
    win.load_from_online()

    # Then
    assert len(win.paints) == 3
    assert win.item_table.rowCount() == 0


def test_load_from_file_adds_row_per_paint(
    win: ImportPaintsDialog, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """For each paint returned from file import, add a row"""
    # Given
    content = """
    paints:
      - name: "Abaddon Black"
        range: "Base"
        manufacturer: "Citadel"
        hexvalue: "#231F20"
      - name: "Averland Sunset"
        range: "Base"
        manufacturer: "Citadel"
        hexvalue: "#FDB825"
      - name: "Balthasar Gold (Metal)"
        range: "Base"
        manufacturer: "Citadel"
        hexvalue: "#A47552"
    """
    file = tmp_path / "paints.yaml"
    file.write_text(content)
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda *args, **kwargs: [str(file), None]
    )

    # When
    win.load_from_file()

    # Then
    assert len(win.paints) == 3
    assert win.item_table.rowCount() == 3


def test_load_from_file_does_nothing_on_cancel(
    win: ImportPaintsDialog, monkeypatch: pytest.MonkeyPatch
):
    """When user cancels file dialog, nothing is loaded"""
    # Given
    win.paints = [
        PaintItem({"name": "foo", "desc": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "bar", "range": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "baz", "range": "other range", "manufacturer": "Else"}),
    ]
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda *args, **kwargs: ["", None]
    )

    # When
    win.load_from_file()

    # Then
    assert len(win.paints) == 3  # isn't overwritten
    assert win.item_table.rowCount() == 0  # but also not loaded into table


def test_selected_paints_does_not_include_unchecked(win: ImportPaintsDialog):
    """When calling selected_paints(), those not checked in the list are not included"""
    # Given
    win.paints = [
        PaintItem({"name": "foo", "desc": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "bar", "range": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "baz", "range": "other range", "manufacturer": "Else"}),
    ]
    win.load_table()
    win.item_table.item(1, 0).setCheckState(Qt.CheckState.Unchecked)

    # When
    result = win.selected_paints()

    # Then
    assert len(result) == 2


def test_import_adds_selected_to_model(win: ImportPaintsDialog, context: Context):
    """When importing, the selected paints are added to the right model"""
    # Given
    win.paints = [
        PaintItem({"name": "foo", "desc": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "bar", "range": "test range", "manufacturer": "Someone"}),
        PaintItem({"name": "baz", "range": "other range", "manufacturer": "Else"}),
    ]
    win.load_table()
    win.item_table.item(1, 0).setCheckState(Qt.CheckState.Unchecked)

    # When
    win.import_paints()

    # Then
    assert context.models.paints_model.rowCount() == 2
