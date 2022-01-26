""" Tests fo the RecipeSteps Widget"""

from pytestqt.qtbot import QtBot
from adjutant.widgets.recipe_steps_link import RecipeStepsLink
from tests.conftest import Context


def test_link_id_is_set_to_zero(qtbot: QtBot, context: Context):
    """Adding a recipe step extends the list"""
    # Given
    widget = RecipeStepsLink(context, None)
    qtbot.addWidget(widget)

    # When

    # Then
    assert widget.link_id == 0
