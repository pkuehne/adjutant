""" Tests for the Row Zero Filter Model"""

from adjutant.context.context import Context
from adjutant.models.row_zero_filter_model import RowZeroFilterModel
from tests.conftest import Models


def test_row_zero_is_filtered(context: Context, models: Models):
    """Row zero should not be shown"""
    # Given
    models.add_scheme("Foo")
    assert context.models.colour_schemes_model.rowCount() == 2
    model = RowZeroFilterModel()

    # When
    model.setSourceModel(context.models.colour_schemes_model)

    # Then
    assert model.rowCount() == 1
    assert model.index(0, 0).data() != 0
