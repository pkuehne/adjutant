""" Tests for the Online Import Dialog"""

import pytest
from pytestqt.qtbot import QtBot

from adjutant.context.url_loader import UrlLoader
from adjutant.windows.online_import_dialog import OnlineImportDialog


@pytest.fixture(name="win")
def fixture_dialog(monkeypatch: pytest.MonkeyPatch, qtbot: QtBot):
    """Helper to construct the dialog"""
    monkeypatch.setattr(UrlLoader, "load_yaml_from_url", lambda *args: None)
    dialog = OnlineImportDialog("foo")
    qtbot.addWidget(dialog)
    return dialog


def test_title_is_set(win: OnlineImportDialog):
    """The title should include adjutant"""
    # Given
    # Then
    assert win.windowTitle() != ""


def test_parse_failure_logs_error(
    win: OnlineImportDialog, caplog: pytest.LogCaptureFixture
):
    """When an empty yaml is passed back, don't try to load the list"""
    # Given

    # When
    win.load_manifest(None)

    # Then
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
    assert win.item_table.rowCount() == 0


def test_empty_yaml_data_logs_warning(
    win: OnlineImportDialog, caplog: pytest.LogCaptureFixture
):
    """When an empty yaml is passed back, don't try to load the list"""
    # Given

    # When
    win.load_manifest({})

    # Then
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert win.item_table.rowCount() == 0


def test_loading_manifest_adds_row_per_file(win: OnlineImportDialog):
    """For a valid yaml, load the corresponding files"""
    # Given

    # When
    win.load_manifest({"files": [{"name": "foo", "desc": "bar"}]})

    # Then
    assert win.item_table.rowCount() == 1
