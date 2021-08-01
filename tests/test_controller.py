""" Tests for the Controller class"""

from PyQt6.QtWidgets import QMessageBox

from tests.conftest import AddBaseFunc, AddEmptyBasesFunc, BasesRecord
from adjutant.context.context import Context


def test_convert_index_filter_model(
    context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """If a filter_model index is passed, the base model index should be returned"""
    # Given
    add_empty_bases(5)
    index = context.models.bases_filter_model.index(0, 0)

    # When
    retval = context.controller.convert_index(index)

    # Then
    assert index.model() != retval.model()
    assert retval.model() == context.models.bases_model


def test_convert_index_bases_model(
    context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """If a filter_model index is passed, the base model index should be returned"""
    # Given
    add_empty_bases(5)
    index = context.models.bases_model.index(0, 0)

    # When
    retval = context.controller.convert_index(index)

    # Then
    assert index.model() == retval.model()
    assert retval.model() == context.models.bases_model


def test_delete_confirmation_required(
    context: Context, add_empty_bases: AddEmptyBasesFunc, monkeypatch
):
    """Check that delete requires confirmation"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Cancel
    )
    num_rows = 5
    add_empty_bases(num_rows)

    # When
    context.controller.delete_bases(
        [context.models.bases_model.index(0, 0), context.models.bases_model.index(1, 0)]
    )

    # Then
    assert context.models.bases_model.rowCount() == num_rows


def test_delete_removes_selected_indexes(
    context: Context, add_empty_bases: AddEmptyBasesFunc, monkeypatch
):
    """Check that delete removes the requested indexes"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )
    num_rows = 5
    add_empty_bases(num_rows)
    index1 = context.models.bases_model.index(2, 0)
    id1 = index1.data()
    index2 = context.models.bases_model.index(4, 0)
    id2 = index2.data()

    # When
    context.controller.delete_bases([index1, index2])

    # Then
    assert context.models.bases_model.rowCount() == num_rows - 2
    for row in range(context.models.bases_model.rowCount()):
        assert context.models.bases_model.index(row, 0).data() != id1
        assert context.models.bases_model.index(row, 0).data() != id2


def test_delete_does_nothing_for_no_indexes(
    context: Context, add_empty_bases: AddEmptyBasesFunc, monkeypatch
):
    """Check that delete removes the requested indexes"""
    # Given
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: QMessageBox.StandardButton.Ok
    )
    num_rows = 5
    add_empty_bases(num_rows)

    # When
    context.controller.delete_bases([])

    # Then
    assert context.models.bases_model.rowCount() == num_rows


def test_duplicate_bases_does_that(context: Context, add_base: AddBaseFunc):
    """When duplicating, exact copties are created"""
    # Given
    model = context.models.bases_model
    add_base([BasesRecord(None, name="Foo Name", figures=5)])
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


def test_duplicate_bases_zero_does_nothing(context: Context, add_base: AddBaseFunc):
    """When duplicating 0 times, nothing happens"""
    # Given
    model = context.models.bases_model
    add_base([BasesRecord(None, name="Foo Name", figures=5)])
    index = model.index(0, 0)

    # When
    success = context.controller.duplicate_base(index, 0)

    # Then
    assert success
    assert model.rowCount() == 1
