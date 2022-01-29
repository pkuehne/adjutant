""" Tests for the add/edit dialog"""


from pytestqt.qtbot import QtBot
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QTextEdit
from adjutant.models.relational_model import RelationalModel
from adjutant.windows.add_edit_dialog import AddEditDialog, MappedWidget


def test_dont_show_delete_button_in_add_mode(qtbot: QtBot):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.model = RelationalModel()

    # When
    dialog.setup()

    # Then
    assert dialog.buttons.delete_button.isEnabled() is False


def test_dont_show_id_field_in_add_mode(qtbot: QtBot):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.model = RelationalModel()

    # When
    dialog.set_widgets([])
    dialog.setup()

    # Then
    assert dialog.widgets.get("ID", None) is None


def test_name_widget_is_added_by_default(qtbot: QtBot):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.model = RelationalModel()

    # When
    dialog.set_widgets([])
    dialog.setup()

    # Then
    assert dialog.widgets.get("Name", None) is not None


def test_in_edit_mode_id_is_set(qtbot: QtBot, relational_model: RelationalModel):
    """When the dialog is in add mode, the delete button should not be enabled"""

    # Given
    relational_model.insertRecord(-1, relational_model.record())
    relational_model.submitAll()
    dialog = AddEditDialog(relational_model.index(0, 0))
    qtbot.addWidget(dialog)
    dialog.model = relational_model

    # When
    dialog.set_widgets([])
    dialog.setup()

    # Then
    id_widget = dialog.widgets.get("ID", None)
    assert id_widget is not None
    assert id_widget.widget.text() != ""


def test_values_submitted_on_edit(qtbot: QtBot, relational_model: RelationalModel):
    """When the dialog is submitted, the values should be set on the record"""

    # Given
    record = relational_model.record()
    record.setValue("name", "Foo")
    relational_model.insertRecord(-1, record)
    relational_model.submitAll()

    dialog = AddEditDialog(relational_model.index(0, 0))
    qtbot.addWidget(dialog)
    dialog.model = relational_model
    dialog.set_widgets([])
    dialog.setup()
    name = "Bar"
    dialog.widgets["Name"].widget.setText(name)

    # When
    dialog.submit_changes()

    # Then
    assert relational_model.rowCount() == 1
    index = relational_model.field_index(0, "name")
    assert index.data() == name


def test_values_submitted_on_add(qtbot: QtBot, relational_model: RelationalModel):
    """When the dialog is submitted, the values should be set on the record"""

    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.model = relational_model
    dialog.set_widgets([])
    dialog.setup()
    name = "foo"
    dialog.widgets["Name"].widget.setText(name)

    # When
    dialog.submit_changes()

    # Then
    assert relational_model.rowCount() == 1
    index = relational_model.field_index(0, "name")
    assert index.data() == name


def test_set_title_add_includes_title(qtbot: QtBot):
    """When the title is set, the passed string should be included on add"""
    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)

    # When
    dialog.set_title("Foo")

    # Then
    assert "Foo" in dialog.windowTitle()


def test_set_title_edit_includes_title(qtbot: QtBot, relational_model: RelationalModel):
    """When the title is set, the passed string should be included on add"""
    # Given
    relational_model.insertRecord(-1, relational_model.record())
    relational_model.submitAll()
    dialog = AddEditDialog(relational_model.index(0, 0))
    qtbot.addWidget(dialog)

    # When
    dialog.set_title("Foo")

    # Then
    assert "Foo" in dialog.windowTitle()


def test_delete_button_does_nothing(qtbot: QtBot):
    """When the title is set, the passed string should be included on add"""
    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)

    # When
    with qtbot.assert_not_emitted(dialog.finished):
        dialog.delete_button_pressed()

    # Then


def test_custom_property_in_mapping(qtbot: QtBot, relational_model: RelationalModel):
    """When a custom property is set in the MappedWidgets, it should be applied"""
    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    widget = QTextEdit()
    mappings = [MappedWidget("Foo", widget, "foo", b"plainText")]
    dialog.set_widgets(mappings)
    dialog.model = relational_model

    # When
    dialog.setup()

    # Then
    assert dialog.mapper.mappedPropertyName(widget) == mappings[1].property


def test_hide_name_field(qtbot: QtBot, relational_model: RelationalModel):
    """When hide name field is set, the name field doesn't get added"""
    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.hide_name_field()
    dialog.set_widgets([])
    dialog.model = relational_model

    # When
    dialog.setup()

    # Then
    assert dialog.widgets.get("Name", None) is None


def test_revert_changes(qtbot: QtBot, relational_model: RelationalModel):
    """reject should revert changes"""
    # Given
    dialog = AddEditDialog(QModelIndex())
    qtbot.addWidget(dialog)
    dialog.set_widgets([])
    dialog.model = relational_model
    dialog.setup()
    dialog.model.insertRecord(-1, dialog.model.record())

    # When
    dialog.revert_changes()

    # Then
    assert not dialog.model.isDirty()
