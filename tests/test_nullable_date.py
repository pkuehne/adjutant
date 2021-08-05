""" Tests for the NullableDate widget """

from datetime import datetime
from adjutant.widgets.nullable_date import NullableDate


def test_widget_starts_with_none_value(qtbot):
    """By default the value of the widget is None"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)
    widget.show()

    # When
    value = widget.date

    # Then
    assert value is None
    assert widget.checkbox.isChecked() is False
    assert widget.dateedit.isVisible() is False


def test_date_returns_none_unchecked(qtbot):
    """When the checkbox is not checked, None should be returned by date()"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)
    widget.checkbox.setChecked(False)

    # When
    value = widget.date

    # Then
    assert value is None


def test_date_returns_date_checked(qtbot):
    """When the checkbox is checked, the date should be returned by date()"""
    # Given
    current_date = datetime.now()
    widget = NullableDate()
    qtbot.addWidget(widget)
    widget.checkbox.setChecked(True)
    widget.dateedit.setDate(current_date)

    # When
    value = widget.date

    # Then
    assert value is not None
    assert value == current_date


def test_setting_date_none(qtbot):
    """When setting a date, a none value unchecks the box"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)

    # When
    widget.date = None

    # Then
    assert widget.checkbox.isChecked() is False
    assert widget.dateedit.isVisible() is False


def test_setting_date_valid_value(qtbot):
    """When setting a date, a valid value checks the box"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)
    current_date = datetime.now()
    widget.show()

    # When
    widget.date = current_date

    # Then
    assert widget.checkbox.isChecked()
    assert widget.dateedit.isVisible()
    assert widget.dateedit.date() == current_date


def test_setting_date_empty_string(qtbot):
    """When setting a date, an empty string is same as None"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)
    widget.show()

    # When
    widget.date = ""

    # Then
    assert widget.checkbox.isChecked() is False
    assert widget.dateedit.isVisible() is False


def test_setting_date_iso_date_string(qtbot):
    """When setting a date, a string in iso format is ok"""
    # Given
    widget = NullableDate()
    qtbot.addWidget(widget)
    widget.show()

    # When
    widget.date = "2021-02-03"

    # Then
    assert widget.checkbox.isChecked()
    assert widget.dateedit.isVisible()
    assert widget.dateedit.date().year() == 2021
    assert widget.dateedit.date().month() == 2
    assert widget.dateedit.date().day() == 3
