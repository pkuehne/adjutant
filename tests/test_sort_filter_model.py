""" Tests for the SortFilterModel """


from adjutant.context.context import Context
from adjutant.models.sort_filter_model import SortFilterModel
from tests.conftest import BasesRecord, AddBaseFunc, AddEmptyBasesFunc


def test_id_filtering(context: Context, add_empty_bases: AddEmptyBasesFunc):
    """Test that items are filtered out when a filter is set"""
    # Given
    filter_model = SortFilterModel()
    filter_model.setSourceModel(context.models.bases_model)
    add_empty_bases(6)
    filter_list = [2, 4, 6, 8]

    # When
    filter_model.set_column_filter(0, filter_list)

    # Then
    assert filter_model.rowCount() > 0
    assert filter_model.rowCount() != context.models.bases_model.rowCount()
    for row in range(filter_model.rowCount()):
        print(filter_model.index(row, 0).data())
        assert filter_model.index(row, 0).data() in filter_list


def test_setting_getting_filters():
    """Test setting and getting filters works"""
    # Given
    filter_model = SortFilterModel()
    filter_list = ["foo", "bar", "baz"]

    # When
    filter_model.set_column_filter(5, filter_list)

    # Then
    assert filter_model.get_column_filter(5) == filter_list


def test_filters_are_applied(context: Context, add_base: AddBaseFunc):
    """Test that filters are applied to items"""
    # Given
    filter_model = SortFilterModel()
    filter_model.setSourceModel(context.models.bases_model)
    filter_list = ["foo", "bar"]
    add_base(
        [BasesRecord(name="foo"), BasesRecord(name="bar"), BasesRecord(name="baz")]
    )

    # When
    filter_model.set_column_filter(1, filter_list)

    # Then
    assert filter_model.rowCount() > 0
    assert filter_model.rowCount() != context.models.bases_model.rowCount()
    for row in range(filter_model.rowCount()):
        assert filter_model.index(row, 1).data() in filter_list


def test_multiple_filters_are_applied(context: Context, add_base: AddBaseFunc):
    """Test that multiple filters are applied to items"""
    # Given
    filter_model = SortFilterModel()
    filter_model.setSourceModel(context.models.bases_model)
    filter_list_name = ["foo"]
    filter_list_scale = ["28mm"]
    add_base(
        [
            BasesRecord(name="foo", scale="28mm"),
            BasesRecord(name="bar", scale="32mm"),
            BasesRecord(name="baz", scale="28mm"),
        ]
    )

    # When
    filter_model.set_column_filter(1, filter_list_name)
    filter_model.set_column_filter(2, filter_list_scale)

    # Then
    assert filter_model.rowCount() > 0
    assert filter_model.rowCount() != context.models.bases_model.rowCount()
    for row in range(filter_model.rowCount()):
        assert filter_model.index(row, 1).data() in filter_list_name
        assert filter_model.index(row, 2).data() in filter_list_scale


def test_setting_fixed_string_emit_signal(qtbot):
    """When a fixed string is set, a signal is emitted"""
    # Given
    filter_model = SortFilterModel()

    # When
    with qtbot.waitSignal(filter_model.filter_changed, timeout=10):
        filter_model.setFilterFixedString("Foo")

    # Then


def test_clear_filters_does_that(context: Context):
    """When the celar filters function is called, all filters are removed"""
    # Given

    filter_model = SortFilterModel()
    filter_model.setSourceModel(context.models.bases_model)
    filter_model.column_filters[0] = [0, 1, 2, 3, 4]
    filter_model.column_filters[3] = ["foo"]
    filter_model.column_filters[5] = ["a", "b"]

    # When
    filter_model.clear_all_column_filters()

    # Then
    for col in range(context.models.bases_model.rowCount()):
        assert filter_model.column_filters[col] is None