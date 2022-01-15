""" Tests for the search bar"""

from pytestqt.qtbot import QtBot
from tests.conftest import Context, Models
from adjutant.widgets.search_bar import SearchBar


def test_load_button_menu_has_all_searches(
    qtbot: QtBot, context: Context, models: Models
):
    """The menu on the load button should include all searches"""
    # Given
    models.add_search("Foo")
    models.add_search("Bar")

    search_bar = SearchBar(context)
    qtbot.addWidget(search_bar)

    # When
    search_bar.create_load_menu()

    # Then
    assert len(search_bar.load_button.menu().actions()) == 2


def test_load_button_menu_updates(qtbot: QtBot, context: Context, models: Models):
    """The menu on the load button should update with new searches"""
    # Given
    models.add_search("Foo")
    models.add_search("Bar")

    search_bar = SearchBar(context)
    qtbot.addWidget(search_bar)
    search_bar.create_load_menu()

    # When
    models.add_search("Baz")
    # Not calling create_load_menu() explicitly

    # Then
    assert len(search_bar.load_button.menu().actions()) == 3


def test_load_button_no_searches_disables(qtbot: QtBot, context: Context):
    """The load button should be disabled if there are no searches"""
    # Given
    search_bar = SearchBar(context)
    qtbot.addWidget(search_bar)

    # When
    search_bar.create_load_menu()

    # Then
    assert search_bar.load_button.isEnabled() is False


def test_load_search_sets_edit_text(qtbot: QtBot, context: Context):
    """Load search"""
    # Given
    search_bar = SearchBar(context)
    qtbot.addWidget(search_bar)

    # When
    with qtbot.assert_not_emitted(search_bar.filter_edit.textChanged):
        search_bar.load_search("Foo")

    # Then
    assert search_bar.filter_edit.text() == "Foo"
