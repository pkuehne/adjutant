""" Tests for the database context"""

from unittest.mock import MagicMock
import pytest
from pytest import MonkeyPatch
from tests.conftest import (
    BasesRecord,
    Models,
)
from adjutant.context import Context
from adjutant.context.database_context import (
    DatabaseContext,
    add_tag_to_base,
    generate_uuid,
    get_tag_count,
    remove_scheme_components,
)
from adjutant.context.exceptions import (
    DatabaseIsNewer,
    DatabaseNeedsMigration,
    NoDatabaseFileFound,
)
import adjutant.context.database_migrations


def test_uuid_generates_random():
    """When generate_uuid is run twice, it returns different results"""
    # Given

    # When
    id1 = generate_uuid()
    id2 = generate_uuid()

    # Then
    assert id1 != id2


def test_version_returns_zero_for_empty_file():
    """When there is no database, the version() function should return 0"""
    # Given
    database = DatabaseContext()
    database.database.close()

    # When
    version = database.version()

    # Then
    assert version == 0


def test_open_raises_if_database_version_higher(monkeypatch: MonkeyPatch):
    """open database raises exception if database version higher than app version"""
    # Given
    database = DatabaseContext()
    command_mock = MagicMock()
    monkeypatch.setattr(database, "version", lambda: 2)
    monkeypatch.setattr(database, "execute_sql_command", command_mock)
    monkeypatch.setattr(adjutant.context.database_context, "LATEST_DATABASE_VERSION", 1)

    # When
    with pytest.raises(DatabaseIsNewer):
        database.open_database()

    # Then


def test_open_raises_if_database_needs_migration(monkeypatch: MonkeyPatch):
    """open database raises exception if database version lower than app version"""
    # Given
    database = DatabaseContext()
    command_mock = MagicMock()
    monkeypatch.setattr(database, "version", lambda: 1)
    monkeypatch.setattr(database, "execute_sql_command", command_mock)
    monkeypatch.setattr(adjutant.context.database_context, "LATEST_DATABASE_VERSION", 2)

    # When
    with pytest.raises(DatabaseNeedsMigration):
        database.open_database()

    # Then


def test_open_raises_if_database_doesnt_exist(monkeypatch: MonkeyPatch):
    """open database raises exception if database doesn't exist"""
    # Given
    database = DatabaseContext()
    command_mock = MagicMock()
    monkeypatch.setattr(database, "version", lambda: 0)
    monkeypatch.setattr(database, "execute_sql_command", command_mock)
    monkeypatch.setattr(adjutant.context.database_context, "LATEST_DATABASE_VERSION", 1)

    # When
    with pytest.raises(NoDatabaseFileFound):
        database.open_database()

    # Then


def test_tag_count_is_zero_no_usage(context: Context, models: Models):
    """When there is a tag, but it is not used, the tag count should be zero"""
    # Given
    models.add_tag("Foo")
    tag_index = context.models.tags_model.index(0, 0)

    # When
    count = get_tag_count(context.database, tag_index.data())

    # Then
    assert count == 0


def test_tag_count_returns_zero_on_error(context: Context, monkeypatch: MonkeyPatch):
    """When there is an error in the sql, the return value should be zero"""
    # Given
    monkeypatch.setattr(context.database, "execute_sql_command", lambda *args: False)

    # When
    count = get_tag_count(context.database, None)

    # Then
    assert count == 0


def test_tag_count_when_used(
    context: Context,
    models: Models,
):
    """When there is a tag, and it is used by a base, the tag count should be one"""
    # Given
    models.add_tag("Foo")
    tag_index = context.models.tags_model.index(0, 0)
    models.add_base(BasesRecord(name="Foobar"))
    base_index = context.models.bases_model.index(0, 0)

    models.add_tag_use(base_index.data(), tag_index.data())

    # When
    count = get_tag_count(context.database, tag_index.data())

    # Then
    assert count == 1


def test_add_tag_to_base(
    context: Context,
    models: Models,
):
    """add_tag_to_base adds entry to the bases_tags table"""
    # Given
    models.add_empty_bases(1)
    base_id = context.models.bases_model.index(0, 0).data()
    models.add_tag("Foo")
    tag_id = context.models.tags_model.index(0, 0).data()

    # When
    add_tag_to_base(context.database, base_id, tag_id)

    # Then
    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 1


def test_add_tag_to_base_invalid_id(
    context: Context,
    models: Models,
    monkeypatch: MonkeyPatch,
):
    """add_tag_to_base adds entry to the bases_tags table"""
    # Given
    models.add_empty_bases(1)
    base_id = context.models.bases_model.index(0, 0).data()
    models.add_tag("Foo")
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
