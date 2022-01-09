""" Tests for the colour scheme report dialog"""

from adjutant.context.context import Context
from tests.conftest import Models
from adjutant.windows.colour_scheme_report_dialog import ColourSchemeReportDialog


def test_no_zero_row_in_combobox(qtbot, context: Context, models: Models):
    """The <None> record should not be in the combobox"""
    # Given
    models.add_scheme("Foo")

    # When
    dialog = ColourSchemeReportDialog(context, None)
    qtbot.addWidget(dialog)

    # Then
    assert dialog.scheme_combobox.count() == 1
    assert "None" not in dialog.scheme_combobox.itemText(0)
    assert (
        dialog.scheme_combobox.model()
        .index(dialog.scheme_combobox.currentIndex(), 0)
        .data()
        != 0
    )
