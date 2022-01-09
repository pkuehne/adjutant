""" Model to filter out row zero"""

from PyQt6.QtCore import QModelIndex, QSortFilterProxyModel


class RowZeroFilterModel(QSortFilterProxyModel):
    """Proxy model to hide row 0"""

    # pylint: disable=invalid-name
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """Hides the 0 row"""
        if source_row == 0:
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    # pylint: enable=invalid-name
