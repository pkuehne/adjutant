""" Tests for the Recipe Screen """

from adjutant.windows.schemes_screen import SchemeScreen
from tests.conftest import Context


def test_row_zero_is_hidden(qtbot, context: Context):
    """The zero'th row is <None> and should be hidden in the table"""
    # Given
    screen = SchemeScreen(context)
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.table.isRowHidden(0)
