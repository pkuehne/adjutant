""" Tests for the Paints Screen """

from adjutant.windows.paints_screen import PaintsScreen
from tests.conftest import Context


def test_paints_model_set(qtbot, context: Context):
    """The paints model should be set"""
    # Given
    screen = PaintsScreen(context)
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.table.model() is not None
