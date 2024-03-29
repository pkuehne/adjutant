""" Tests for the Controller class"""

from unittest import mock
from pytest import MonkeyPatch
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox

from tests.conftest import Models, BasesRecord

from adjutant.context.dataclasses import SchemeComponent
from adjutant.context.context import Context


def test_convert_index_tags_model(context: Context, models: Models):
    """If a filter_model index is passed, the base model index should be returned"""
    # Given
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 0)

    # When
    retval = context.controller.convert_index(index)

    # Then
    assert index.model() == retval.model()
    assert retval.model() == context.models.tags_model


def test_convert_index_tags_sort_model(context: Context, models: Models):
    """If a filter_model index is passed, the base model index should be returned"""
    # Given
    models.add_tag("Foo")
    index = context.models.tags_sort_model.index(0, 0)

    # When
    retval = context.controller.convert_index(index)

    # Then
    assert index.model() != retval.model()
    assert retval.model() == context.models.tags_model


###################################
# delete_records
###################################


def test_delete_confirmation_required(context: Context, models: Models):
    """Check that delete requires confirmation"""
    # Given
    context.controller.confirm_deletion = mock.Mock(return_value=False)
    num_rows = 5
    models.add_empty_bases(num_rows)

    # When
    context.controller.delete_records(
        context.models.bases_model,
        [
            context.models.bases_model.index(0, 0),
            context.models.bases_model.index(1, 0),
        ],
    )

    # Then
    assert context.models.bases_model.rowCount() == num_rows


def test_delete_removes_selected_indexes(context: Context, models: Models):
    """Check that delete removes the requested indexes"""
    # Given
    num_rows = 5
    models.add_empty_bases(num_rows)
    index1 = context.models.bases_model.index(2, 0)
    id1 = index1.data()
    index2 = context.models.bases_model.index(4, 0)
    id2 = index2.data()

    # When
    context.controller.delete_records(context.models.bases_model, [index1, index2])

    # Then
    assert context.models.bases_model.rowCount() == num_rows - 2
    for row in range(context.models.bases_model.rowCount()):
        assert context.models.bases_model.index(row, 0).data() != id1
        assert context.models.bases_model.index(row, 0).data() != id2


def test_delete_does_nothing_for_no_indexes(context: Context, models: Models):
    """Check that delete removes the requested indexes"""
    # Given
    num_rows = 5
    models.add_empty_bases(num_rows)

    # When
    context.controller.delete_records(context.models.bases_model, [])

    # Then
    assert context.models.bases_model.rowCount() == num_rows


###################################
# create_record
###################################


def test_create_record_requires_name(context: Context, monkeypatch):
    """When creating a record, a name is required"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("", True))

    # When
    context.controller.create_record(context.models.tags_model)

    # Then
    assert context.models.tags_model.rowCount() == 0


def test_create_record_requires_input(context: Context, monkeypatch):
    """When creating a record, user can't click cancel button"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("Foo", False))

    # When
    context.controller.create_record(context.models.tags_model)

    # Then
    assert context.models.tags_model.rowCount() == 0


def test_create_record(context: Context, monkeypatch):
    """When creating a record, a name is required"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("Foo", True))

    # When
    context.controller.create_record(context.models.tags_model)

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert context.models.tags_model.index(0, 1).data() == "Foo"
    assert context.models.tags_model.isDirty() is False


def test_create_record_uses_passed_default(context: Context, monkeypatch):
    """When creating a tag, a name is required"""
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: (kwargs["text"], kwargs["text"] == "Foobar"),
    )

    # When
    context.controller.create_record(context.models.tags_model, default="Foobar")

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert context.models.tags_model.index(0, 1).data() == "Foobar"
    assert context.models.tags_model.isDirty() is False


###################################
# rename_record
###################################


def test_rename_record_requires_name(context: Context, models: Models, monkeypatch):
    """When renaming a record, a non-empty string must be used"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("", True))
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.rename_record(context.models.tags_model, index)

    # Then
    assert index.data() == "Foo"


def test_rename_record_requires_input(context: Context, models: Models, monkeypatch):
    """When renaming a record, the user can't click cancel"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("Foo", False))
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.rename_record(context.models.tags_model, index)

    # Then
    assert index.data() == "Foo"


def test_rename_record(context: Context, models: Models, monkeypatch):
    """When renaming a record, the name value should change"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kawrgs: ("Bar", True))
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.rename_record(context.models.tags_model, index)

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert index.data() == "Bar"
    assert context.models.tags_model.isDirty() is False


def test_rename_record_uses_passed_default(
    context: Context, models: Models, monkeypatch
):
    """When renaming a record, a default name can be set"""
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: ("Foobar", kwargs["text"] == "Foo"),
    )
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.rename_record(context.models.tags_model, index)

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert context.models.tags_model.index(0, 1).data() == "Foobar"
    assert context.models.tags_model.isDirty() is False


###################################
# Settings
###################################


def test_font_size_not_less_than_5(context: Context):
    """Font size should be less than five"""
    # Given
    font_size = 3

    # When
    context.controller.set_font_size(font_size)

    # Then
    assert context.settings.font_size != font_size


def test_font_size_sets_value_in_db(
    context: Context, qapp: QApplication, monkeypatch: MonkeyPatch
):
    """Setting the font size should update the settings"""
    # Given
    font_size = 12
    monkeypatch.setattr(QApplication, "instance", lambda: qapp)

    # When
    context.controller.set_font_size(font_size)

    # Then
    assert context.settings.font_size == font_size
    assert qapp.font().pointSize() == font_size


###################################
# Bases
###################################


def test_duplicate_bases_does_that(context: Context, models: Models):
    """When duplicating, exact copties are created"""
    # Given
    model = context.models.bases_model
    models.add_base(BasesRecord(None, name="Foo Name", figures=5))
    index = model.index(0, 0)
    name_field = model.fieldIndex("name")
    figures_field = model.fieldIndex("figures")

    # When
    success = context.controller.duplicate_base(index, 2)

    # Then
    assert success
    assert model.rowCount() == 3
    assert model.index(1, 0).data() != 0
    assert model.index(2, 0).data() != 0
    assert model.index(1, name_field).data() == index.siblingAtColumn(name_field).data()
    assert (
        model.index(1, figures_field).data()
        == index.siblingAtColumn(figures_field).data()
    )
    assert model.index(2, name_field).data() == index.siblingAtColumn(name_field).data()
    assert (
        model.index(2, figures_field).data()
        == index.siblingAtColumn(figures_field).data()
    )
    assert model.isDirty() is False


def test_duplicate_bases_zero_does_nothing(context: Context, models: Models):
    """When duplicating 0 times, nothing happens"""
    # Given
    model = context.models.bases_model
    models.add_base(BasesRecord(None, name="Foo Name", figures=5))
    index = model.index(0, 0)

    # When
    success = context.controller.duplicate_base(index, 0)

    # Then
    assert success
    assert model.rowCount() == 1


def test_duplicate_bases_returns_false_when_submit_all_fails(
    context: Context, models: Models, monkeypatch
):
    """When duplicating a submit failure returns False"""
    # Given
    model = context.models.bases_model
    models.add_base(BasesRecord(None, name="Foo Name", figures=5))
    index = model.index(0, 0)
    monkeypatch.setattr(model, "submitAll", lambda: False)

    # When
    success = context.controller.duplicate_base(index, 2)

    # Then
    assert success is False


def test_apply_field_updates_bases(context: Context, models: Models):
    """Test that the field's value overwrites the selected indices"""
    # Given
    models.add_base(BasesRecord(name="Foo", figures=1))
    models.add_base(BasesRecord(name="Bar", figures=3))
    models.add_base(BasesRecord(name="Baz", figures=3))
    name_field = context.models.bases_model.fieldIndex("name")
    figures_field = context.models.bases_model.fieldIndex("figures")
    source = context.models.bases_model.index(0, name_field)
    destinations = [
        context.models.bases_model.index(1, figures_field),
        context.models.bases_model.index(1, figures_field),
    ]

    # When
    context.controller.apply_field_to_bases(source, destinations)

    # Then
    assert context.models.bases_model.isDirty() is False
    assert destinations[0].siblingAtColumn(name_field).data() == source.data()
    assert destinations[1].siblingAtColumn(name_field).data() == source.data()
    assert destinations[0].siblingAtColumn(
        figures_field
    ).data() != source.siblingAtColumn(figures_field)


######################
# Tags
######################
def test_create_tag(context: Context, monkeypatch):
    """When creating a tag, a name is required"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("Foo", True))

    # When
    context.controller.create_tag()

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert context.models.tags_model.index(0, 1).data() == "Foo"
    assert context.models.tags_model.isDirty() is False


def test_rename_tag(context: Context, models: Models, monkeypatch):
    """When renaming a tag, the name value should change"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kawrgs: ("Bar", True))
    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.rename_tag(index)

    # Then
    assert context.models.tags_model.rowCount() == 1
    assert index.data() == "Bar"
    assert context.models.tags_model.isDirty() is False


def test_delete_tag(context: Context, models: Models, monkeypatch):
    """Delete tag does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_tag("Foo")
    index = context.models.tags_model.index(0, 1)

    # When
    context.controller.delete_tag(index)

    # Then
    assert context.models.tags_model.rowCount() == 0
    assert context.models.tags_model.isDirty() is False
    assert index.isValid()


######################
# Searches
######################


def test_rename_search(context: Context, models: Models, monkeypatch):
    """When renaming a search, the name value should change"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kawrgs: ("Bar", True))
    models.add_search("Foo")
    index = context.models.searches_model.index(0, 1)

    # When
    context.controller.rename_search(index)

    # Then
    assert context.models.searches_model.rowCount() == 1
    assert index.data() == "Bar"
    assert context.models.searches_model.isDirty() is False


def test_delete_search(context: Context, models: Models, monkeypatch):
    """Delete search does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_search("Foo")
    index = context.models.searches_model.index(0, 1)

    # When
    context.controller.delete_search(index)

    # Then
    assert context.models.searches_model.rowCount() == 0
    assert context.models.searches_model.isDirty() is False
    assert index.isValid()


##############################
# Storage
##############################


def test_delete_storage(context: Context, models: Models, monkeypatch):
    """Delete recipe does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_storage("Foo")
    index = context.models.storages_model.index(1, 1)

    # When
    context.controller.delete_storages([index])

    # Then
    assert context.models.storages_model.rowCount() == 1
    assert context.models.storages_model.isDirty() is False
    assert index.isValid()


##############################
# Status
##############################


def test_create_status(context: Context, monkeypatch):
    """When creating a status, a name is required"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("Foo", True))

    # When
    context.controller.create_status()

    # Then
    assert context.models.statuses_model.rowCount() == 2
    assert context.models.statuses_model.index(1, 1).data() == "Foo"
    assert context.models.statuses_model.isDirty() is False


def test_rename_status(context: Context, models: Models, monkeypatch):
    """When renaming a status, the name value should change"""
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kawrgs: ("Bar", True))
    models.add_status("Foo")
    index = context.models.statuses_model.index(1, 1)

    # When
    context.controller.rename_status(index)

    # Then
    assert context.models.statuses_model.rowCount() == 2
    assert index.data() == "Bar"
    assert context.models.statuses_model.isDirty() is False


def test_delete_status(context: Context, models: Models, monkeypatch):
    """Delete status does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_status("Foo")
    index = context.models.statuses_model.index(1, 1)

    # When
    context.controller.delete_status(index)

    # Then
    assert context.models.statuses_model.rowCount() == 1
    assert context.models.statuses_model.isDirty() is False
    assert index.isValid()


def test_delete_status_reassigns_bases(context: Context, monkeypatch, models: Models):
    """When deleting a status, any bases using that status will be set to the default 0 value"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    status_id = models.add_status("Foo")
    status_index = context.models.statuses_model.index(1, 1)
    assert status_index.data() == "Foo"
    models.add_base(BasesRecord(name="Test", status=status_id))
    base_index = context.models.bases_model.index(
        0, context.models.bases_model.fieldIndex("status_id")
    )
    assert base_index.data(Qt.ItemDataRole.DisplayRole) == "Foo"

    # When
    context.controller.delete_status(status_index)

    # Then
    assert base_index.data(Qt.ItemDataRole.EditRole) == ""


##############################
# Paints
##############################
def test_delete_paint(context: Context, models: Models, monkeypatch):
    """Delete paint does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_paint("Foo")
    index = context.models.paints_model.index(0, 1)

    # When
    context.controller.delete_paints([index])

    # Then
    assert context.models.paints_model.lastError().text() == ""
    assert context.models.paints_model.rowCount() == 0
    assert context.models.paints_model.isDirty() is False
    assert index.isValid()


##############################
# Recipes
##############################
def test_delete_recipe(context: Context, models: Models, monkeypatch):
    """Delete recipe does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_recipe("Foo")
    index = context.models.recipes_model.index(0, 1)

    # When
    context.controller.delete_recipes([index])

    # Then
    assert context.models.recipes_model.rowCount() == 0
    assert context.models.recipes_model.isDirty() is False
    assert index.isValid()


def test_delete_recipe_removes_steps(context: Context, models: Models, monkeypatch):
    """Delete recipe does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    recipe_id = models.add_recipe("Foo")
    models.add_step(1, recipe_id, 0)
    models.add_step(1, "Foo", 1)
    index = context.models.recipes_model.index(0, 1)

    # When
    context.controller.delete_recipes([index])

    # Then
    assert context.models.recipe_steps_model.rowCount() == 1


def test_delete_recipe_steps_removes(context: Context, models: Models):
    """Delete removes all steps for given recipe"""
    # Given
    recipe_id = "Foo"
    models.add_step(9, recipe_id, 9)
    models.add_step(8, recipe_id, 8)
    models.add_step(7, "Bar", 7)

    # When
    context.controller.delete_recipe_steps(recipe_id)

    # Then
    assert context.models.recipe_steps_model.rowCount() == 1
    assert context.models.recipe_steps_model.isDirty() is False


##############################
# Schemes
##############################
def test_delete_scheme(context: Context, models: Models, monkeypatch):
    """Delete scheme does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )

    models.add_scheme("Foo")
    model = context.models.colour_schemes_model
    index = model.index(0, 1)

    # When
    context.controller.delete_schemes([index])

    # Then
    assert model.rowCount() == 1  # Always includes <None>
    assert model.isDirty() is False
    assert index.isValid()


def test_delete_scheme_removes_components(
    context: Context, models: Models, monkeypatch
):
    """Delete recipe does just that"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )
    model = context.models.colour_schemes_model

    models.add_scheme("Foo")
    models.add_component(1, "Bar", 0)
    models.add_component(1, "Baz", 1)
    index = model.index(0, 1)

    # When
    context.controller.delete_schemes([index])

    # Then
    assert model.rowCount() == 1  # Always <None>


def test_replace_scheme_components_add_new_ones(context: Context):
    """Adding a recipe step puts it into the model"""
    # Given
    scheme_id = 1
    components = [
        SchemeComponent("Foo", 1),
        SchemeComponent("Bar", 2),
    ]
    model = context.models.scheme_components_model

    # When
    context.controller.replace_scheme_components(scheme_id, components)

    # Then
    assert model.rowCount() == 2
    assert model.index(0, 3).data(Qt.ItemDataRole.EditRole) == "1"
    assert model.index(1, 3).data(Qt.ItemDataRole.EditRole) == "2"


def test_replace_scheme_components_removes_old(context: Context, models: Models):
    """Adding a recipe step puts it into the model"""
    # Given
    scheme_id = 1
    models.add_component(1, "Bar", 0)
    models.add_component(1, "Baz", 1)

    components = []

    # When
    context.controller.replace_scheme_components(scheme_id, components)

    # Then
    assert context.models.scheme_components_model.rowCount() == 0
