""" Test for the Filter Popup """

from typing import List
from pytestqt.qtbot import QtBot
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt
from adjutant.windows.filter_popup import (
    FilterPopup,
    from_check_state,
    invert_check_state,
    to_check_state,
)
from adjutant.models.sort_filter_model import SortFilterModel


def create_popup(items: List[str]):
    """Creates a popup with these items"""
    model = create_model(items)
    popup = FilterPopup(None, model, 0)
    return popup


def create_model(items: List[str]):
    """Creates the sort filter model"""
    base_model = QStandardItemModel()
    for item in items:
        base_model.appendRow(QStandardItem(item))
    model = SortFilterModel()
    model.setSourceModel(base_model)
    return model


def test_from_check_state():
    """From converts checkstate to boolean"""
    assert from_check_state(Qt.CheckState.Checked) is True
    assert from_check_state(Qt.CheckState.Unchecked) is False


def test_to_check_state():
    """To converts boolean to checkstate"""
    assert to_check_state(True) == Qt.CheckState.Checked
    assert to_check_state(False) == Qt.CheckState.Unchecked


def test_invert_check_state():
    """Invert converts checkstate to checkstate"""
    assert invert_check_state(Qt.CheckState.Unchecked) == Qt.CheckState.Checked
    assert invert_check_state(Qt.CheckState.Checked) == Qt.CheckState.Unchecked


def test_duplicates_are_removed(qtbot: QtBot):
    """Test that the list of items removes duplicates"""
    # Given
    popup = create_popup(["Foo", "Foo", "Bar", "Bar", "Baz"])
    qtbot.add_widget(popup)

    # When
    popup.setup_filter()

    # Then
    assert popup.list_model.rowCount() == 3


def test_all_items_checked_by_default(qtbot: QtBot):
    """Test that all items are checked if no filters set"""
    # Given
    popup = create_popup(["Foo", "Bar", "Baz"])
    qtbot.add_widget(popup)

    # When
    popup.setup_filter()

    # Then
    for row in range(popup.list_model.rowCount()):
        item = popup.list_model.item(row, 0)
        assert (
            item.checkState() == Qt.CheckState.Checked
        ), f"Item in row {row} is not checked"


def test_uncheck_all_items(qtbot: QtBot):
    """Test that all items can be unchecked"""
    # Given
    popup = create_popup(["Foo", "Bar", "Baz"])
    qtbot.add_widget(popup)
    popup.setup_filter()

    # When
    popup.unselect_all()

    # Then
    for row in range(popup.list_model.rowCount()):
        item = popup.list_model.item(row, 0)
        assert (
            item.checkState() == Qt.CheckState.Unchecked
        ), f"Item in row {row} is checked"


def test_check_all_items(qtbot: QtBot):
    """Test that all items are checked if no filters set"""
    # Given
    popup = create_popup(["Foo", "Bar", "Baz"])
    qtbot.add_widget(popup)
    popup.setup_filter()
    for row in range(popup.list_model.rowCount()):
        item = popup.list_model.item(row, 0)
        item.setCheckState(Qt.CheckState.Unchecked)

    # When
    popup.select_all()

    # Then
    for row in range(popup.list_model.rowCount()):
        item = popup.list_model.item(row, 0)
        assert (
            item.checkState() == Qt.CheckState.Checked
        ), f"Item in row {row} is not checked"


def test_asc_sort_button_set_when_sort_enabled(qtbot: QtBot):
    """When sorting is enabled on the model, the button is checked"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(0, Qt.SortOrder.AscendingOrder)
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)

    # When
    popup.setup_filter()

    # Then
    assert popup.buttons["sort_ascending"].isChecked()
    assert popup.buttons["sort_descending"].isChecked() is False


def test_desc_sort_button_set_when_sort_enabled(qtbot: QtBot):
    """When sorting is enabled on the model, the button is checked"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(0, Qt.SortOrder.DescendingOrder)
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)

    # When
    popup.setup_filter()

    # Then
    assert popup.buttons["sort_ascending"].isChecked() is False
    assert popup.buttons["sort_descending"].isChecked()


def test_no_sort_button_set_when_sort_disabled(qtbot: QtBot):
    """When sorting is disabled on the model, no button is checked"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(-1, Qt.SortOrder.AscendingOrder)  # Disable
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)

    # When
    popup.setup_filter()

    # Then
    assert popup.buttons["sort_ascending"].isChecked() is False
    assert popup.buttons["sort_descending"].isChecked() is False


def test_asc_sort_button_sorts_ascending(qtbot: QtBot):
    """The asc button should sort the model"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(-1, Qt.SortOrder.AscendingOrder)  # Disable
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)
    popup.setup_filter()

    # When
    qtbot.mouseClick(popup.buttons["sort_ascending"], Qt.MouseButton.LeftButton)

    # Then
    assert model.sortOrder() == Qt.SortOrder.AscendingOrder
    assert model.sortColumn() == 0


def test_asc_sort_button_unsorts_when_sorted(qtbot: QtBot):
    """When asc sort button is pressed while model is sorted, unsort it"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(0, Qt.SortOrder.AscendingOrder)  # Disable
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)
    popup.setup_filter()

    # When
    qtbot.mouseClick(popup.buttons["sort_ascending"], Qt.MouseButton.LeftButton)

    # Then
    assert model.sortOrder() == Qt.SortOrder.AscendingOrder
    assert model.sortColumn() == -1


def test_desc_sort_button_sorts_descending(qtbot: QtBot):
    """The asc button should sort the model"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(-1, Qt.SortOrder.AscendingOrder)  # Disable
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)
    popup.setup_filter()

    # When
    qtbot.mouseClick(popup.buttons["sort_descending"], Qt.MouseButton.LeftButton)

    # Then
    assert model.sortOrder() == Qt.SortOrder.DescendingOrder
    assert model.sortColumn() == 0


def test_desc_sort_button_unsorts_when_sorted(qtbot: QtBot):
    """When asc sort button is pressed while model is sorted, unsort it"""
    # Given
    model = create_model(["Foo", "Bar", "Baz"])
    model.sort(0, Qt.SortOrder.DescendingOrder)  # Disable
    popup = FilterPopup(None, model, 0)
    qtbot.add_widget(popup)
    popup.setup_filter()

    # When
    qtbot.mouseClick(popup.buttons["sort_descending"], Qt.MouseButton.LeftButton)

    # Then
    assert model.sortOrder() == Qt.SortOrder.DescendingOrder
    assert model.sortColumn() == -1


def test_update_filter_only_sets_checked(qtbot: QtBot):
    """The asc button should sort the model"""
    # Given
    popup = create_popup(["Foo", "Bar", "Baz"])
    qtbot.add_widget(popup)
    popup.setup_filter()

    for row in [1, 2]:
        item = popup.list_model.item(row, 0)
        item.setCheckState(Qt.CheckState.Unchecked)

    # When
    popup.update_filters()

    # Then
    assert len(popup.model.column_filters[0]) == 1
    assert popup.model.column_filters[0] == ["Bar"]


def test_update_filter_empyt_list_when_all_checked(qtbot: QtBot):
    """The asc button should sort the model"""
    # Given
    popup = create_popup(["Foo", "Bar", "Baz"])
    qtbot.add_widget(popup)
    popup.setup_filter()

    for row in range(popup.list_model.rowCount()):
        item = popup.list_model.item(row, 0)
        item.setCheckState(Qt.CheckState.Checked)

    # When
    popup.update_filters()

    # Then
    assert popup.model.column_filters[0] is None
