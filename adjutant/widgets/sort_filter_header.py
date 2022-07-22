""" Custom header view for the base table """

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QWidget
from adjutant.windows.filter_popup import FilterPopup


class SortFilterHeader(QHeaderView):
    """Handles the filter popup menu"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent=parent)
        self.setSectionsClickable(True)
        self.sectionClicked.connect(self.section_clicked)
        self.setStretchLastSection(True)
        self.setSortIndicatorShown(True)

    def section_clicked(self, column: int) -> None:
        """Respond to clicks on the header"""
        FilterPopup.show(self, self.model(), column)
