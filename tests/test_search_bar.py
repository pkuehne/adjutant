""" Tests for the search bar"""

from tests.conftest import Context, Models
from adjutant.widgets.bases_table import BasesTable


def test_load_button_menu_has_all_searches(qtbot, context: Context, models: Models):
    """The menu on the load button should include all searches"""
    # Given
    models.add_search("Foo")
    models.add_search("Bar")

    table = BasesTable(context)
    qtbot.addWidget(table)

    # When
    table.create_load_menu()

    # Then
    assert len(table.load_button.menu().actions()) == 2


def test_load_button_menu_updates(qtbot, context: Context, models: Models):
    """The menu on the load button should update with new searches"""
    # Given
    models.add_search("Foo")
    models.add_search("Bar")

    table = BasesTable(context)
    qtbot.addWidget(table)
    table.create_load_menu()

    # When
    models.add_search("Baz")
    # Not calling create_load_menu() explicitly

    # Then
    assert len(table.load_button.menu().actions()) == 3


def test_load_button_no_searches_disables(qtbot, context: Context):
    """The load button should be disabled if there are no searches"""
    # Given
    table = BasesTable(context)
    qtbot.addWidget(table)

    # When
    table.create_load_menu()

    # Then
    assert table.load_button.isEnabled() is False
