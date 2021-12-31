""" Tests for the recipe edit dialog """

# from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import Qt

from adjutant.windows.scheme_edit_dialog import SchemeEditDialog
from adjutant.context.dataclasses import SchemeComponent
from tests.conftest import Context, Models


def test_existing_components_are_loaded(qtbot, context: Context, models: Models):
    """When the dialog loads, existing components are added to the list"""

    # Given
    models.add_scheme("Foo")
    models.add_recipe("Bar")
    models.add_component(1, "Baz", 1)
    index = context.models.colour_schemes_model.index(1, 0)

    # When
    dialog = SchemeEditDialog(context, index)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.widgets.component_list.count() == 1
    assert "Bar" in dialog.widgets.component_list.item(0).text()
    assert "Baz" in dialog.widgets.component_list.item(0).text()


def test_add_component_from_widgets_adds_new_item_to_list(
    qtbot, context: Context, models: Models
):
    """When the dialog loads, existing components are added to the list"""

    # Given
    models.add_scheme("Scheme")
    models.add_recipe("Foo")
    models.add_recipe("Bar")
    index = context.models.colour_schemes_model.index(1, 0)
    dialog = SchemeEditDialog(context, index)
    qtbot.addWidget(dialog)
    dialog.widgets.component_edit.setText("Comp")
    dialog.widgets.recipe_combobox.setCurrentIndex(1)

    # When
    dialog.add_component_from_widgets()

    # Then
    assert dialog.widgets.component_list.count() == 1
    assert "Bar" in dialog.widgets.component_list.item(0).text()
    assert "Comp" in dialog.widgets.component_list.item(0).text()


def test_submit_adds_components_to_scheme(qtbot, context: Context, models: Models):
    """When the dialog loads, existing components are added to the list"""

    # Given
    models.add_scheme("Scheme")
    models.add_recipe("Foo")
    models.add_recipe("Bar")
    models.add_component(1, "Comp", 1)

    index = context.models.colour_schemes_model.index(1, 0)
    dialog = SchemeEditDialog(context, index)
    qtbot.addWidget(dialog)
    item = QListWidgetItem()
    item.setData(Qt.ItemDataRole.UserRole + 1, SchemeComponent("Comp2", 2))
    dialog.widgets.component_list.addItem(item)

    # When
    dialog.submit_changes()

    # Then
    assert context.models.scheme_components_model.rowCount() == 2
