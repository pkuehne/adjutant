""" Test the context classes """

from pathlib import Path
import pytest
from pytest import MonkeyPatch
from adjutant.context.settings_context import SettingsContext
from adjutant.context.exceptions import NoSettingsFileFound, SettingsFileCorrupt
import adjutant.context


def test_if_settings_file_not_found_raises(monkeypatch: MonkeyPatch, tmp_path: Path):
    """If the settings file is not found, an exception is raised"""
    # Given
    settings = SettingsContext()
    filename = tmp_path / "settings.yaml"
    monkeypatch.setattr(adjutant.context.settings_context, "SETTINGS_FILE", filename)

    # Given
    with pytest.raises(NoSettingsFileFound):
        settings.load()


def test_if_settings_file_bad_raises(monkeypatch: MonkeyPatch, tmp_path: Path):
    """If the settings file contains bad yaml, an exception is raised"""
    # Given
    settings = SettingsContext()
    filename = tmp_path / "settings.yaml"
    filename.write_text(":")
    monkeypatch.setattr(adjutant.context.settings_context, "SETTINGS_FILE", filename)

    # Given
    with pytest.raises(SettingsFileCorrupt):
        settings.load()


def test_load_sets_values_from_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    """During load, values are set from the file"""
    # Given
    settings = SettingsContext()
    filename = tmp_path / "settings.yaml"
    filename.write_text("font_size: 99\n")
    monkeypatch.setattr(adjutant.context.settings_context, "SETTINGS_FILE", filename)

    # Given
    settings.load()

    # Then
    assert settings.font_size == 99


def test_load_sets_values_from_defaults_if_not_set(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    """During load, if the value is not in file, uses the default"""
    # Given
    settings = SettingsContext()
    filename = tmp_path / "settings.yaml"
    filename.write_text("foo_val: 99\n")
    monkeypatch.setattr(adjutant.context.settings_context, "SETTINGS_FILE", filename)

    # Given
    settings.load()

    # Then
    assert settings.font_size == SettingsContext.font_size


def test_save_writes_to_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    """During load, if the value is not in file, uses the default"""
    # Given
    settings = SettingsContext()
    filename = tmp_path / "settings.yaml"
    filename.write_text("foo_val: 99\n")
    monkeypatch.setattr(adjutant.context.settings_context, "SETTINGS_FILE", filename)
    settings.font_size = 99

    # Given
    settings.save()

    # Then
    assert "99" in filename.read_text()
