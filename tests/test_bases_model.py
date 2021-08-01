""" Testing the Bases Model and its quirks"""

from tests.conftest import AddEmptyBasesFunc
from adjutant.context.context import Context


def test_setting_id_column_does_nothing(
    context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """Trying to update the ID column should succeed but do nothing"""
    # Given
    add_empty_bases(5)
    index = context.models.bases_model.index(2, 0)

    # When
    success = context.models.bases_model.setData(index, 99)

    # Then
    assert success
    assert index.data() == 3  # This shouldn't be flaky because of the autoincrement
