""" Tests for the recipe component dialog"""
from unittest import mock

import pytest
from pytestqt.qtbot import QtBot

from PyQt6.QtCore import QModelIndex

from adjutant.context.context import Context
from adjutant.windows.component_edit_dialog import ComponentEditDialog


def test_name_is_set(qtbot: QtBot, context: Context):
    """Test that the name is set"""
    # Given
    win = ComponentEditDialog(context, QModelIndex())
    qtbot.add_widget(win)

    # Then
    assert "Component" in win.windowTitle()


def test_delete_function_implemented(
    qtbot: QtBot,
    context: Context,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that the delete function is implemented"""
    # Given
    win = ComponentEditDialog(context, QModelIndex())
    qtbot.add_widget(win)
    controller = mock.Mock()
    monkeypatch.setattr(context, "controller", controller)

    # When
    win.delete_function([])

    # Then
    assert len(caplog.records) == 0
    controller.assert_not_called()
