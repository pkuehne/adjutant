""" Tests for the completion chart window """

from pytestqt.qtbot import QtBot
from adjutant.context.context import Context
from adjutant.windows.completion_chart_window import CompletionChartWindow
from tests.conftest import BasesRecord, Models


def test_load_adds_years_to_combobox(qtbot: QtBot, context: Context, models: Models):
    """Load should add each year to the combobox once and in ascending order"""
    # Given
    models.add_base(BasesRecord(completed="2021-01-01"))
    models.add_base(BasesRecord(completed="2022-01-01"))
    models.add_base(BasesRecord(completed="2022-01-02"))
    models.add_base(BasesRecord(completed=""))

    win = CompletionChartWindow(context, None)
    qtbot.add_widget(win)

    # When
    win.load_data()

    # Then
    assert win.widgets.year_select.count() == 2
    assert win.widgets.year_select.itemText(0) == "2021"
    assert win.widgets.year_select.itemText(1) == "2022"


def test_load_counts_completions_per_year_and_month(
    qtbot: QtBot, context: Context, models: Models
):
    """Load should add each year to the combobox once and in ascending year order"""
    # Given
    models.add_base(BasesRecord(completed="2022-01-01"))
    models.add_base(BasesRecord(completed="2022-01-02"))
    models.add_base(BasesRecord(completed="2021-01-01"))

    win = CompletionChartWindow(context, None)
    qtbot.add_widget(win)

    # When
    win.load_data()

    # Then
    assert win.data.completion["2022"]["01"] == 2
    assert win.data.completion["2021"]["01"] == 1
