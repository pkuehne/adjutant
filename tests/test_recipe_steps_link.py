""" Tests fo the RecipeSteps Widget"""

from pytestqt.qtbot import QtBot
from adjutant.widgets.recipe_steps_link import RecipeStepsLink
from tests.conftest import Context, Models


def test_link_id_is_set_to_zero(qtbot: QtBot, context: Context):
    """Adding a recipe step extends the list"""
    # Given
    widget = RecipeStepsLink(context, None)
    qtbot.addWidget(widget)

    # When

    # Then
    assert widget.link_id == 0


def test_list_only_shows_relevant_steps(qtbot: QtBot, context: Context, models: Models):
    """List should only show steps pertaining to current recipe"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)
    models.add_step(3, 2, 4)
    models.add_step(1, 2, 5)

    # When
    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    # Then
    assert widget.step_list.model().rowCount() == 3


def test_set_selection_enables_up_down(qtbot: QtBot, context: Context, models: Models):
    """If an index is not the first or last, allow both buttons"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    # When
    widget.list_selection_changed(widget.step_list.model().index(1, 0), None)

    # Then
    assert widget.buttons["up"].isEnabled() is True
    assert widget.buttons["down"].isEnabled() is True


def test_set_selection_disbles_up(qtbot: QtBot, context: Context, models: Models):
    """If an index is the first, allow the up button"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    # When
    widget.list_selection_changed(widget.step_list.model().index(0, 0), None)

    # Then
    assert widget.buttons["up"].isEnabled() is False
    assert widget.buttons["down"].isEnabled() is True


def test_set_selection_disbles_down(qtbot: QtBot, context: Context, models: Models):
    """If an index is the last, allow the down button"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    # When
    widget.list_selection_changed(widget.step_list.model().index(2, 0), None)

    # Then
    assert widget.buttons["up"].isEnabled() is True
    assert widget.buttons["down"].isEnabled() is False


def test_show_add_dialog(qtbot: QtBot, context: Context, models: Models):
    """If an index is the last, allow the down button"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    # When
    with qtbot.wait_signal(context.signals.show_add_dialog) as signal:
        widget.show_step_add_dialog()

    # Then
    assert len(signal.args) == 2
    assert signal.args[0] == "step"
    assert "link_id" in signal.args[1]


def test_move_swaps_step_num(qtbot: QtBot, context: Context, models: Models):
    """If an index is the last, allow the down button"""
    # Given
    models.add_step(1, 1, 1)
    models.add_step(2, 1, 2)
    models.add_step(3, 1, 3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    widget.step_list.selectionModel().setCurrentIndex(
        widget.step_list.model().index(1, 0),
        widget.step_list.selectionModel().SelectionFlag.ClearAndSelect,
    )

    # When
    widget.move_step(1)

    # Then
    assert context.models.recipe_steps_model.field_data(1, "step_num") == 3
    assert context.models.recipe_steps_model.field_data(2, "step_num") == 2


def test_revert_restores_recipe_steps(qtbot: QtBot, context: Context):
    """When reverting changes, all recipe-related steps are reverted to their original"""
    # Given
    step_1 = context.models.recipe_steps_model.record()
    step_1.setValue("recipes_id", 1)
    step_1.setValue("paints_id", 5)
    context.models.recipe_steps_model.insertRecord(-1, step_1)
    step_2 = context.models.recipe_steps_model.record()
    step_2.setValue("recipes_id", 1)
    step_2.setValue("paints_id", 6)
    context.models.recipe_steps_model.insertRecord(-1, step_2)
    step_3 = context.models.recipe_steps_model.record()
    step_3.setValue("recipes_id", 2)
    step_3.setValue("paints_id", 10)
    context.models.recipe_steps_model.insertRecord(-1, step_3)

    widget = RecipeStepsLink(context, 1)
    qtbot.addWidget(widget)

    record = context.models.recipe_steps_model.record(0)
    record.setValue("paints_id", 2)
    context.models.recipe_steps_model.setRecord(0, record)
    context.models.recipe_steps_model.submitAll()

    record = context.models.recipe_steps_model.record(2)
    record.setValue("paints_id", 11)
    context.models.recipe_steps_model.setRecord(2, record)
    context.models.recipe_steps_model.submitAll()

    context.models.recipe_steps_model.removeRow(1)
    context.models.recipe_steps_model.submitAll()

    # When
    widget.revert_changes()

    # Then
    assert context.models.recipe_steps_model.rowCount() == 3
    record = context.models.recipe_steps_model.record(0)
    assert record.value("paints_id") == 11
    assert record.value("recipes_id") == 2
    record = context.models.recipe_steps_model.record(1)
    assert record.value("paints_id") == 5
    assert record.value("recipes_id") == 1
    record = context.models.recipe_steps_model.record(2)
    assert record.value("paints_id") == 6
    assert record.value("recipes_id") == 1
