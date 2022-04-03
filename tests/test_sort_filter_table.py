""" Tests for the SortFilterTable"""

from unittest.mock import MagicMock
from pytestqt.qtbot import QtBot
from pytest import MonkeyPatch
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QContextMenuEvent, QKeyEvent
from PyQt6.QtWidgets import QMenu
from adjutant.widgets.sort_filter_table import SortFilterTable
from adjutant.context import Context
from tests.conftest import Models, BasesRecord


def test_set_model_sets_filter(qtbot: QtBot, context: Context):
    """When the model is set, the filter model should be set too"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)

    # When
    table.setModel(context.models.bases_model)

    # Then
    assert table.filter_model is not None
    assert table.filter_model != context.models.bases_model
    assert table.model() == table.filter_model


def test_context_menu_is_fired(
    qtbot: QtBot, monkeypatch: MonkeyPatch, context: Context, models: Models
):
    """When the context menu event is fired, a signal is raised"""
    # Given
    popup_mock = MagicMock()
    monkeypatch.setattr(QMenu, "popup", popup_mock)
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_base(BasesRecord())
    table.setModel(context.models.bases_model)
    event = QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(5, 5))

    # When
    table.contextMenuEvent(event)

    # Then
    popup_mock.assert_called()


def test_context_menu_is_not_fired(
    qtbot: QtBot, monkeypatch: MonkeyPatch, context: Context, models: Models
):
    """When the context menu event is fired, the signal is not raised if no item is selected"""
    # Given
    popup_mock = MagicMock()
    monkeypatch.setattr(QMenu, "popup", popup_mock)
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_base(BasesRecord())
    table.setModel(context.models.bases_model)
    event = QContextMenuEvent(QContextMenuEvent.Reason.Mouse, QPoint(9999, 999))

    # When
    table.contextMenuEvent(event)

    # Then
    popup_mock.assert_not_called()


def test_selected_returns_orig_model_index(
    qtbot: QtBot, context: Context, models: Models
):
    """Selected indexes returns the original model's index"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_empty_bases(2)
    table.setModel(context.models.bases_model)
    table.selectRow(0)

    # When
    indexes = table.selected_indexes()

    # Then
    assert indexes
    assert indexes[0].isValid()
    assert indexes[0].model() == context.models.bases_model


def test_backspace_deletes_item(qtbot: QtBot, context: Context, models: Models):
    """backspace on selected item deletes the row"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_empty_bases(10)
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


def test_delete_deletes_item(qtbot: QtBot, context: Context, models: Models):
    """delete on selected item deletes the row"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_empty_bases(10)
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


def test_return_edits_item(qtbot: QtBot, context: Context, models: Models):
    """return on selected item edits the row"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_empty_bases(10)
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


def test_other_keys_do_nothing(qtbot: QtBot, context: Context, models: Models):
    """return on selected item edits the row"""
    # Given
    table = SortFilterTable(context)
    qtbot.addWidget(table)
    models.add_empty_bases(10)
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
