""" Tests fo the RecipeSteps Widget"""

from PyQt6.QtCore import Qt
from adjutant.context.dataclasses import RecipeStep
from adjutant.widgets.recipe_steps_widget import RecipeStepsWidget


def test_add_step_adds_to_list(qtbot):
    """Adding a recipe step extends the list"""
    # Given
    widget = RecipeStepsWidget()
    qtbot.addWidget(widget)

    step = RecipeStep(0, "Foo", 0, "Bar", "#123456")

    # When
    widget.add_step(step)

    # Then
    assert widget.step_list.count() == 1
    assert "Foo" in widget.step_list.item(0).text()
    assert step == widget.step_list.item(0).data(Qt.ItemDataRole.UserRole + 1)
