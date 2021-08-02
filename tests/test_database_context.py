""" Tests for the database context"""

from tests.conftest import AddBaseFunc, AddTagFunc, AddTagUseFunc, BasesRecord
from adjutant.context import Context
from adjutant.context.database_context import get_tag_count


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
