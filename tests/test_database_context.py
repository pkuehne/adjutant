""" Tests for the database context"""

from tests.conftest import (
    AddBaseFunc,
    AddEmptyBasesFunc,
    AddTagFunc,
    AddTagUseFunc,
    BasesRecord,
    Models,
)
from adjutant.context import Context
from adjutant.context.database_context import (
    add_tag_to_base,
    get_tag_count,
    remove_scheme_components,
)


def test_tag_count_is_zero_no_usage(context: Context, add_tag: AddTagFunc):
    """When there is a tag, but it is not used, the tag count should be zero"""
    # Given
    add_tag("Foo")
    tag_index = context.models.tags_model.index(0, 0)

    # When
    count = get_tag_count(context.database, tag_index.data())

    # Then
    assert count == 0


def test_tag_count_returns_zero_on_error(context: Context, monkeypatch):
    """When there is an error in the sql, the return value should be zero"""
    # Given
    monkeypatch.setattr(context.database, "execute_sql_command", lambda *args: False)

    # When
    count = get_tag_count(context.database, None)

    # Then
    assert count == 0


def test_tag_count_when_used(
    context: Context,
    add_tag: AddTagFunc,
    add_base: AddBaseFunc,
    add_tag_use: AddTagUseFunc,
):
    """When there is a tag, and it is used by a base, the tag count should be one"""
    # Given
    add_tag("Foo")
    tag_index = context.models.tags_model.index(0, 0)
    add_base([BasesRecord(name="Foobar")])
    base_index = context.models.bases_model.index(0, 0)

    add_tag_use(base_index.data(), tag_index.data())

    # When
    count = get_tag_count(context.database, tag_index.data())

    # Then
    assert count == 1


def test_add_tag_to_base(
    context: Context,
    add_tag: AddTagFunc,
    add_empty_bases: AddEmptyBasesFunc,
):
    """add_tag_to_base adds entry to the bases_tags table"""
    # Given
    add_empty_bases(1)
    base_id = context.models.bases_model.index(0, 0).data()
    add_tag("Foo")
    tag_id = context.models.tags_model.index(0, 0).data()

    # When
    add_tag_to_base(context.database, base_id, tag_id)

    # Then
    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 1


def test_add_tag_to_base_invalid_id(
    context: Context,
    add_tag: AddTagFunc,
    add_empty_bases: AddEmptyBasesFunc,
    monkeypatch,
):
    """add_tag_to_base adds entry to the bases_tags table"""
    # Given
    add_empty_bases(1)
    base_id = context.models.bases_model.index(0, 0).data()
    add_tag("Foo")
    tag_id = context.models.tags_model.index(0, 0).data()
    monkeypatch.setattr(context.database, "execute_sql_command", lambda *args: False)

    # When
    add_tag_to_base(context.database, base_id, tag_id)

    # Then
    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 0


def test_scheme_components_remove(context: Context, models: Models):
    """Steps are retrieved and converted"""
    # Given
    models.add_component(1, "Foo", 1)
    models.add_component(1, "Bar", 2)
    models.add_component(2, "Baz", 2)

    # When
    success = remove_scheme_components(context.database, 1)

    # Then
    assert success
    context.models.scheme_components_model.select()
    assert context.models.scheme_components_model.rowCount() == 1
