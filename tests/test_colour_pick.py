""" Tests for the Colour Pick widget """

from unittest.mock import MagicMock
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QColorDialog
from adjutant.widgets.colour_pick import ColourPick


def test_getting_hexvalue_uses_set_value(qtbot):
    """When getting the hexvalue, use the widget's previously set value"""

    # Given
    pick = ColourPick()
    qtbot.addWidget(pick)
    expected = "#123456"

    # When
    pick.hexvalue = expected

    # Then
    assert pick.hexvalue == expected


def test_setting_hexvalue_updates_stylesheet(qtbot):
    """When setting the hexvalue, the widget's background color changes"""

    # Given
    pick = ColourPick()
    qtbot.addWidget(pick)
    expected = "#123456"

    # When
    pick.hexvalue = expected

    # Then
    assert expected in pick.styleSheet()


def test_clicking_opens_color_dialog_assigns_result(qtbot, monkeypatch):
    """
    When clicking on the widget, the color dialog is opened and its result used for the hexvalue
    """

    # Given
    pick = ColourPick()
    qtbot.addWidget(pick)
    expected = "#123456"
    monkeypatch.setattr(QColorDialog, "getColor", lambda _: QColor(expected))

    # When
    pick.mousePressEvent(None)

    # Then
    assert pick.hexvalue == expected


def test_color_dialog_opens_on_current(qtbot, monkeypatch):
    """
    When clicking on the widget, the color dialog is opened and its result used for the hexvalue
    """

    # Given
    pick = ColourPick()
    qtbot.addWidget(pick)
    initial = "#ff00ff"
    pick.hexvalue = initial
    mock = MagicMock()
    monkeypatch.setattr(QColorDialog, "getColor", mock)

    # When
    pick.mousePressEvent(None)

    # Then
    assert mock.call_count == 1
    assert mock.call_args[0][0].name() == initial
