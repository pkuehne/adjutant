""" Test for the ForeignKeyCombobox"""

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtGui import QValidator
from pytestqt.qtbot import QtBot
from adjutant.widgets.foreign_key_combobox import (
    ForeignKeyCombobox,
    ModelContentValidator,
)
from tests.conftest import RelationalModel


def test_add_button_hidden(qtbot: QtBot):
    """The add button is hidden initially"""
    # Given
    box = ForeignKeyCombobox()
    qtbot.addWidget(box)

    # Then
    assert box.add_button.isHidden() is True


def test_add_button_not_shown_without_callback(
    qtbot: QtBot, relational_model: RelationalModel
):
    """When setting model, the add_button remains hidden if no callback is given"""
    # Given
    box = ForeignKeyCombobox()
    qtbot.addWidget(box)

    # When
    box.set_model(relational_model)

    # Then
    assert box.add_button.isHidden() is True


def test_add_button_shown_with_callback(
    qtbot: QtBot, relational_model: RelationalModel
):
    """When setting model, the add_button is shown if a callback is given"""
    # Given
    box = ForeignKeyCombobox()
    qtbot.addWidget(box)

    # When
    box.set_model(relational_model, lambda: False)

    # Then
    assert box.add_button.isHidden() is False


def test_callback_called_when_button_clicked(
    qtbot: QtBot, relational_model: RelationalModel
):
    """When a callback is set, pressing the button calls it"""
    # Given
    box = ForeignKeyCombobox()
    qtbot.addWidget(box)
    pressed = False

    def callback():
        nonlocal pressed
        pressed = True

    box.set_model(relational_model, callback)

    # When
    box.add_button.pressed.emit()

    # Then
    assert pressed is True


def test_set_model_column_passes_to_combobox(
    qtbot: QtBot, relational_model: RelationalModel
):
    """When a callback is set, pressing the button calls it"""
    # Given
    box = ForeignKeyCombobox()
    qtbot.addWidget(box)
    box.set_model(relational_model)

    # When
    box.set_model_column(3)

    # Then
    assert box.combobox.modelColumn() == 3


def test_validator_accepts_existing_string():
    """The validator accepts a string that's in the model"""
    # Given
    model = QStandardItemModel(4, 1)
    model.setItem(0, 0, QStandardItem("Foo"))
    model.setItem(1, 0, QStandardItem("Bar"))
    model.setItem(2, 0, QStandardItem("Test"))
    model.setItem(3, 0, QStandardItem("Baz"))

    validator = ModelContentValidator(model, 0)

    # When
    (result, _, __) = validator.validate("Test", 1)

    # Then
    assert result == QValidator.State.Acceptable


def test_validator_accepts_partial_string():
    """The validator accepts a string that's partially in the model"""
    # Given
    model = QStandardItemModel(4, 1)
    model.setItem(0, 0, QStandardItem("Foo"))
    model.setItem(1, 0, QStandardItem("Bar"))
    model.setItem(2, 0, QStandardItem("Test"))
    model.setItem(3, 0, QStandardItem("Baz"))

    validator = ModelContentValidator(model, 0)

    # When
    (result, _, __) = validator.validate("Te", 1)

    # Then
    assert result == QValidator.State.Intermediate


def test_validator_rejects_invalid_string():
    """The validator rejects a string that's not in the model"""
    # Given
    model = QStandardItemModel(4, 1)
    model.setItem(0, 0, QStandardItem("Foo"))
    model.setItem(1, 0, QStandardItem("Bar"))
    model.setItem(2, 0, QStandardItem("Test"))
    model.setItem(3, 0, QStandardItem("Baz"))

    validator = ModelContentValidator(model, 0)

    # When
    (result, _, __) = validator.validate("Foops", 1)

    # Then
    assert result == QValidator.State.Invalid
