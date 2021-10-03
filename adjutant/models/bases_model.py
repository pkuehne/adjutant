""" Bases Model"""

from PyQt6.QtCore import QModelIndex, Qt
from adjutant.models.relational_model import RelationalModel


class BasesModel(RelationalModel):
    """Subclass QSqlTableModel"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    # def select(self) -> bool:
    #     """Reload all data from the database"""
    #     return super().select()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Flags for the items"""
        if index.column() < super().columnCount():
            return super().flags(index)
        return super().flags(index.siblingAtColumn(0))

    def column_id_tags(self):
        """Returns the column id for the tags column"""
        return self.columnCount() - 1
