""" Tests for the RelationalModel"""

from PyQt6.QtCore import Qt
from tests.conftest import AddEmptyBasesFunc, AddTagFunc, AddTagUseFunc
from adjutant.context.dataclasses import ManyToManyRelationship, Tag
from adjutant.models.relational_model import OneToManyRelationship, RelationalModel
from adjutant.context.context import Context


def test_setting_id_column_does_nothing(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """Trying to update the ID column should succeed but do nothing"""
    # Given
    add_empty_bases(5)
    index = relational_model.index(2, 0)

    # When
    success = relational_model.setData(index, 99)

    # Then
    assert success
    assert index.data() == 3  # This shouldn't be flaky because of the autoincrement


def test_boolean_column_returns_text_value(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """A column marked as boolean should return Yes/No instead of 1/0"""

    # Given
    relational_model.boolean_fields.append(relational_model.fieldIndex("completed"))
    add_empty_bases(1)

    # When
    completed = relational_model.index(
        0, relational_model.fieldIndex("completed")
    ).data(Qt.ItemDataRole.DisplayRole)

    damaged = relational_model.index(0, relational_model.fieldIndex("damaged")).data(
        Qt.ItemDataRole.DisplayRole
    )

    # Then
    assert completed == "No"
    assert damaged == 0


def test_boolean_column_returns_boolean_for_edit_role(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """A column marked as boolean should return 1/0 for edit role"""

    # Given
    relational_model.boolean_fields.append(relational_model.fieldIndex("completed"))
    add_empty_bases(1)

    # When
    completed = relational_model.index(
        0, relational_model.fieldIndex("completed")
    ).data(Qt.ItemDataRole.EditRole)

    # Then
    assert completed == 0


def test_relationship_returns_own_value_for_edit(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """A relational column should return it's actual value when requesting via edit role"""

    # Given
    relationship = OneToManyRelationship("storage", "id", "name")
    relational_model.set_one_to_many_relationship(
        relational_model.fieldIndex("storage_id"), relationship
    )
    add_empty_bases(1)

    # When
    value = relational_model.index(0, relational_model.fieldIndex("storage_id")).data(
        Qt.ItemDataRole.EditRole
    )

    # Then
    assert value == 0


def test_relationship_returns_foreign_value_for_display(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """
    A relational column should return it's foreign table value when requesting via display role
    """

    # Given
    relationship = OneToManyRelationship("storage", "id", "name")
    relational_model.set_one_to_many_relationship(
        relational_model.fieldIndex("storage_id"), relationship
    )
    add_empty_bases(1)

    # When
    value = relational_model.index(0, relational_model.fieldIndex("storage_id")).data(
        Qt.ItemDataRole.DisplayRole
    )

    # Then
    assert isinstance(value, str)
    assert value is not None


def test_relationship_returns_none_for_error(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """A relational column should return None if it set up incorrectly"""

    # Given
    relationship = OneToManyRelationship("", "id", "name")
    relational_model.set_one_to_many_relationship(
        relational_model.fieldIndex("storage_id"), relationship
    )
    add_empty_bases(1)

    # When
    value = relational_model.index(0, relational_model.fieldIndex("storage_id")).data(
        Qt.ItemDataRole.DisplayRole
    )

    # Then
    assert value is None


def test_adding_m2m_relationship_adds_one_to_column_count(
    relational_model: RelationalModel,
):
    """Each many to many relationship adds an extra column"""
    # Given
    inital_count = relational_model.columnCount()
    relationship = ManyToManyRelationship("tags", "name")

    # When
    relational_model.set_many_to_many_relationship(relationship)

    # Then
    assert relational_model.columnCount() == inital_count + 1


def test_m2m_relationship_returns_none_for_unsupported_role(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """When requesting an unsupported role for m2m relational data field, return None"""
    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)

    # When
    value = relational_model.index(0, relational_model.columnCount() - 1).data(
        Qt.ItemDataRole.ForegroundRole
    )

    # Then
    assert value is None


def test_m2m_relationship_returns_stringified_tags_for_display_data(
    relational_model: RelationalModel,
    add_empty_bases: AddEmptyBasesFunc,
    add_tag: AddTagFunc,
    add_tag_use: AddTagUseFunc,
):
    """A many-to-many relationship column returns all tags as a string for the display role"""

    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)
    add_tag("Foo")
    add_tag("Bar")
    add_tag_use(1, 1)
    add_tag_use(1, 2)

    # When
    tags = relational_model.index(0, relational_model.columnCount() - 1).data(
        Qt.ItemDataRole.DisplayRole
    )

    # Then
    assert tags == "Foo,Bar"


def test_m2m_relationship_returns_lists_tags_for_edit_data(
    relational_model: RelationalModel,
    add_empty_bases: AddEmptyBasesFunc,
    add_tag: AddTagFunc,
    add_tag_use: AddTagUseFunc,
):
    """A many-to-many relationship column returns all tags as a list for the edit role"""

    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)
    add_tag("Foo")
    add_tag("Bar")
    add_tag_use(1, 1)
    add_tag_use(1, 2)

    # When
    tags = relational_model.index(0, relational_model.columnCount() - 1).data(
        Qt.ItemDataRole.EditRole
    )

    # Then
    assert isinstance(tags, list)
    assert len(tags) == 2


def test_m2m_set_other_than_edit_does_nothing(
    relational_model: RelationalModel, add_empty_bases: AddEmptyBasesFunc
):
    """Trying to set a DisplayRole on a m2m column does nothing"""
    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)
    index = relational_model.index(0, relational_model.columnCount() - 1)

    # When
    success = relational_model.setData(index, "Foo", Qt.ItemDataRole.DisplayRole)

    # Then
    assert not success


def test_m2m_set_tags_adds_them(
    relational_model: RelationalModel,
    add_empty_bases: AddEmptyBasesFunc,
    add_tag: AddTagFunc,
    context: Context,
):
    """When setting on an m2m column, like tags, it adds the tags to the intermediate table"""
    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)
    add_tag("Foo")
    add_tag("Bar")

    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 0

    index = relational_model.index(0, relational_model.columnCount() - 1)
    tags = [Tag(1, "")]

    # When
    success = relational_model.setData(index, tags)

    # Then
    assert success
    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 1


def test_m2m_set_tags_removes_old(
    relational_model: RelationalModel,
    add_empty_bases: AddEmptyBasesFunc,
    add_tag: AddTagFunc,
    add_tag_use: AddTagUseFunc,
    context: Context,
):
    """When settings on an m2m column, it removes the old association first"""
    # Given
    relationship = ManyToManyRelationship("tags", "name")
    relational_model.set_many_to_many_relationship(relationship)
    add_empty_bases(1)
    add_tag("Foo")
    add_tag("Bar")
    add_tag_use(1, 1)

    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 1

    index = relational_model.index(0, relational_model.columnCount() - 1)
    tags = []

    # When
    success = relational_model.setData(index, tags)

    # Then
    assert success
    context.models.base_tags_model.select()
    assert context.models.base_tags_model.rowCount() == 0