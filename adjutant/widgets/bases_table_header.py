""" Custom header view for the base table """

from typing import Dict, cast
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QHeaderView, QWidget
from adjutant.windows.filter_popup import FilterPopup
from adjutant.models.bases_filter_model import BasesFilterModel


class HeaderView(QHeaderView):
    """Headerview with filter indicator"""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(Qt.Horizontal, parent=parent)
        self.filter_status: Dict[int, bool] = {}
        self.setSectionsClickable(True)
        self.sectionClicked.connect(self.section_clicked)

    def section_clicked(self, column: int) -> None:
        """Respond to clicks on the header"""
        popup = FilterPopup(self)
        cursor = QCursor().pos()
        popup.setGeometry(cursor.x(), cursor.y(), popup.width(), popup.height())
        popup.set_source_index(self.model().index(0, column))
        popup.exec_()
        self.update_filter_indicator(column)

    def update_all_filter_indicators(self) -> None:
        """Updates the state of the column's filter indicator"""
        for column in range(self.model().columnCount()):
            self.update_filter_indicator(column)
        self.repaint()

    def update_filter_indicator(self, column: int) -> None:
        """Updates the state of the column's filter indicator"""
        filter_model = cast(BasesFilterModel, self.model())
        self.filter_status[column] = filter_model.get_column_filter(column) != []
