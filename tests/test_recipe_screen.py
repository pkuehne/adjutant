""" Tests for the Recipe Screen """

from adjutant.windows.recipe_screen import RecipeScreen
from tests.conftest import Context


def test_model_is_set(qtbot, context: Context):
    """The model should be set"""
    # Given
    screen = RecipeScreen(context)
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.table.model() is not None
