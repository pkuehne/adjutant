""" The overlying filter model for use with the Bases table """

from dataclasses import dataclass
from typing import Dict, List
import yaml
from PyQt5.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QIcon


@dataclass
class FilterWrapper:
    """Wraps Filters for encoding/decoding"""

    regex: str
    column_filters: Dict[int, List[str]]


class BasesFilterModel(QSortFilterProxyModel):
    """Provides filtering for the Bases Model"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.column_filters: Dict[int, List[str]] = {}

    def set_column_filter(self, column: int, values: List[str]) -> None:
        """Set the filter for a given column"""
        self.column_filters[column] = values
        self.invalidateFilter()
        self.headerDataChanged.emit(Qt.Horizontal, column, column)

    def get_column_filter(self, column: int) -> List[str]:
        """Get the list of filter for the column"""
        return self.column_filters.get(column, [])

    def clear_all_column_filters(self) -> None:
        """Removes any set column filters"""
        for column in range(self.columnCount()):
            self.set_column_filter(column, [])

    def encode_filters(self) -> str:
        """Encode the filters in a binary format"""
        wrapper = {}
        wrapper["regex"] = self.filterRegExp().pattern()
        wrapper["column_filters"] = self.column_filters
        return yaml.dump(wrapper)

    def decode_filters(self, encoded: str):
        """Decode the filters from binary format"""
        wrapper: dict = yaml.safe_load(encoded)
        self.setFilterRegExp(wrapper["regex"])
        self.column_filters = wrapper["column_filters"]
        self.invalidateFilter()

    # pylint: disable=invalid-name
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """Override to set filter icon"""
        if role == Qt.DecorationRole:
            image = (
                ":/icons/filter-available.png"
                if self.column_filters.get(section, []) == []
                else ":/icons/filter-applied.png"
            )
            return QIcon(image)
        return super().headerData(section, orientation, role=role)

    def filterAcceptsRow(self, source_row: int, parent: QModelIndex = None) -> bool:
        """returns True if the row should be shown"""
        for column in range(self.sourceModel().columnCount()):
            filter_list = self.column_filters.get(column, [])
            value = self.sourceModel().index(source_row, column).data()
            if value in filter_list:
                return False

        return super().filterAcceptsRow(source_row, parent)
