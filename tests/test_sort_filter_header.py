""" Tests for the SortFilterHeader widget"""

from adjutant.widgets.sort_filter_header import SortFilterHeader
from adjutant.context import Context
from adjutant.windows.filter_popup import FilterPopup


def test_set_model_sets_filter(qtbot, context: Context, monkeypatch):
    """When a section is clicked the relevant Filter Popup is shown"""
    # Given
    model = None
    column = 0

    def save_args(mod, col):
        nonlocal model
        model = mod
        nonlocal column
        column = col

    header = SortFilterHeader()
    qtbot.addWidget(header)
    header.setModel(context.models.storage_model)
    monkeypatch.setattr(FilterPopup, "show", lambda _, m, c: save_args(m, c))

    # When
    header.section_clicked(2)

    # Then
    assert model == header.model()
    assert column == 2
