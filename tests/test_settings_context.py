""" Test the context classes """

from adjutant.context.settings_context import SettingsContext


def test_version_string_number_split():
    """When a version string is set, it should be split correctly"""
    # Given
    context = SettingsContext()

    # When
    context.set_version("1.2.3")

    # Then
    assert context.version_major == 1
    assert context.version_minor == 2
    assert context.version_patch == 3
    assert context.version_stage == ""


def test_version_string_stage_split():
    """When a version string has a stage set, it should be split correctly"""
    # Given
    context = SettingsContext()

    # When
    context.set_version("1.2.3-alpha")

    # Then
    assert context.version_major == 1
    assert context.version_minor == 2
    assert context.version_patch == 3
    assert context.version_stage == "alpha"
