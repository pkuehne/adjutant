""" Tests for the SortFilterTable"""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QContextMenuEvent, QKeyEvent
from adjutant.widgets.sort_filter_table import SortFilterTable
from adjutant.context import Context
from tests.conftest import AddBaseFunc, AddEmptyBasesFunc, BasesRecord


def test_set_model_sets_filter(qtbot, context: Context):
    """When the model is set, the filter model should be set too"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)

    # When
    table.setModel(context.models.bases_model)

    # Then
    assert table.filter_model is not None
    assert table.filter_model != context.models.bases_model
    assert table.model() == table.filter_model


def test_context_menu_is_fired(qtbot, context: Context, add_base: AddBaseFunc):
    """When the context menu event is fired, a signal is raised"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_base([BasesRecord()])
    table.setModel(context.models.bases_model)
    event = QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(5, 5))

    # When
    with qtbot.waitSignal(table.context_menu_launched, timeout=10) as blocker:
        table.contextMenuEvent(event)

    # Then
    assert blocker.args == [context.models.bases_model.index(0, 0)]


def test_context_menu_is_not_fired(qtbot, context: Context, add_base: AddBaseFunc):
    """When the context menu event is fired, the signal is not raised if no item is selected"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_base([BasesRecord()])
    table.setModel(context.models.bases_model)
    event = QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(9999, 999))

    # When
    with qtbot.assertNotEmitted(table.context_menu_launched):
        table.contextMenuEvent(event)

    # Then


def test_selected_returns_orig_model_index(
    qtbot, context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """Selected indexes returns the original model's index"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_empty_bases(2)
    table.setModel(context.models.bases_model)
    table.selectRow(0)

    # When
    indexes = table.selected_indexes()

    # Then
    assert indexes
    assert indexes[0].isValid()
    assert indexes[0].model() == context.models.bases_model


def test_backspace_deletes_item(
    qtbot, context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """backspace on selected item deletes the row"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_empty_bases(10)
    table.setModel(context.models.bases_model)
    table.selectRow(1)

    # When
    with qtbot.waitSignal(table.item_deleted, timeout=10) as blocker:
        table.eventFilter(
            table,
            QKeyEvent(
                QKeyEvent.Type.KeyPress,
                Qt.Key.Key_Backspace,
                Qt.KeyboardModifier.NoModifier,
                0,
                0,
                0,
            ),
        )

    # Then
    indexes = blocker.args[0]
    assert indexes
    assert indexes[0].isValid()
    assert indexes[0].model() == context.models.bases_model


def test_delete_deletes_item(
    qtbot, context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """delete on selected item deletes the row"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_empty_bases(10)
    table.setModel(context.models.bases_model)
    table.selectRow(1)

    # When
    with qtbot.waitSignal(table.item_deleted, timeout=10) as blocker:
        table.eventFilter(
            table,
            QKeyEvent(
                QKeyEvent.Type.KeyPress,
                Qt.Key.Key_Delete,
                Qt.KeyboardModifier.NoModifier,
                0,
                0,
                0,
            ),
        )

    # Then
    indexes = blocker.args[0]
    assert indexes
    assert indexes[0].isValid()
    assert indexes[0].model() == context.models.bases_model


def test_return_edits_item(qtbot, context: Context, add_empty_bases: AddEmptyBasesFunc):
    """return on selected item edits the row"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_empty_bases(10)
    table.setModel(context.models.bases_model)
    table.selectRow(1)

    # When
    with qtbot.waitSignal(table.item_edited, timeout=10) as blocker:
        table.eventFilter(
            table,
            QKeyEvent(
                QKeyEvent.Type.KeyPress,
                Qt.Key.Key_Return,
                Qt.KeyboardModifier.NoModifier,
                0,
                0,
                0,
            ),
        )

    # Then
    assert blocker.args
    index = blocker.args[0]
    assert index.isValid()
    assert index.model() == context.models.bases_model


def test_other_keys_do_nothing(
    qtbot, context: Context, add_empty_bases: AddEmptyBasesFunc
):
    """return on selected item edits the row"""
    # Given
    table = SortFilterTable()
    qtbot.addWidget(table)
    add_empty_bases(10)
    table.setModel(context.models.bases_model)
    table.selectRow(1)

    # When
    with qtbot.assertNotEmitted(table.item_edited, wait=10):
        with qtbot.assertNotEmitted(table.item_deleted, wait=10):
            table.eventFilter(
                table,
                QKeyEvent(
                    QKeyEvent.Type.KeyPress,
                    Qt.Key.Key_Right,
                    Qt.KeyboardModifier.NoModifier,
                    0,
                    0,
                    0,
                ),
            )

    # Then
