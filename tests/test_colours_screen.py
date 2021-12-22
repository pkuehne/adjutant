""" Tests for the Colours Screen """

from adjutant.windows.colours_screen import ColoursScreen
from tests.conftest import Context


def test_colours_model_set(qtbot, context: Context):
    """The colours model should be set"""
    # Given
    screen = ColoursScreen(context)
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.table.model() is not None
