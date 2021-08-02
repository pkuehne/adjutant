""" The overlying filter model for use with the Bases table """

from dataclasses import dataclass
from typing import Any, Dict, List
import yaml
from PyQt6.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from PyQt6.QtGui import QIcon
from adjutant.models.bases_model import Tag


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

    def set_column_filter(self, column: int, values: List[Any]) -> None:
        """Set the filter for a given column"""
        self.column_filters[column] = values
        self.invalidateFilter()
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, column, column)

    def get_column_filter(self, column: int) -> List[str]:
        """Get the list of filter for the column"""
        return self.column_filters.get(column, None)

    def clear_all_column_filters(self) -> None:
        """Removes any set column filters"""
        for column in range(self.columnCount()):
            self.set_column_filter(column, None)

    def encode_filters(self) -> str:
        """Encode the filters in a binary format"""
        wrapper = {}
        wrapper["regex"] = self.filterRegularExpression().pattern()
        wrapper["column_filters"] = self.column_filters
        return yaml.dump(wrapper)

    def decode_filters(self, encoded: str):
        """Decode the filters from binary format"""
        wrapper: dict = yaml.safe_load(encoded)
        self.setFilterFixedString(wrapper["regex"])
        self.column_filters = wrapper["column_filters"]
        self.invalidateFilter()

    # pylint: disable=invalid-name
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """Override to set filter icon"""
        if role == Qt.ItemDataRole.DecorationRole:
            image = (
                "icons:filter-available.png"
                if self.column_filters.get(section, None) is None
                else "icons:filter-applied.png"
            )
            return QIcon(image)
        return super().headerData(section, orientation, role=role)

    def filterAcceptsRow(self, source_row: int, parent: QModelIndex = None) -> bool:
        """returns True if the row should be shown"""
        for column in range(self.sourceModel().columnCount()):
            filter_list = self.column_filters.get(column, None)
            value = (
                self.sourceModel()
                .index(source_row, column)
                .data(Qt.ItemDataRole.EditRole)
            )
            if isinstance(value, list):
                if filter_list is not None:
                    filter_set = set(filter_list)
                    value: List[Tag] = value
                    value_set = {tag.tag_id for tag in value}
                    if not filter_set and value_set:
                        # No filters, but tags
                        return False
                    if not filter_set.issubset(value_set):
                        return False
            else:
                if filter_list is not None and value not in filter_list:
                    return False

        return super().filterAcceptsRow(source_row, parent)
