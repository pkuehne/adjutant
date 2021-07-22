""" Model for the sidebar Tree on Bases Screen"""

from dataclasses import dataclass
from typing import List

from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtSql import QSqlTableModel


@dataclass
class Section:
    """Section within the Sidebar"""

    title: str
    model: QSqlTableModel
    signal: str
    row: int = -1


class SidebarModel(QAbstractItemModel):
    """Model for sidebar"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.sections: List[Section] = []

    def add_section(self, section: Section):
        """Add a section to the sidebar"""
        section.row = len(self.sections)
        self.sections.append(section)
        if section.model:
            section.model.layoutChanged.connect(self.layoutChanged.emit)
            section.model.rowsInserted.connect(self.rowsInserted.emit)
            section.model.rowsRemoved.connect(self.rowsRemoved.emit)

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        """Return index at given coordinates"""
        if not parent.isValid():
            return self.createIndex(row, 0, None)
        return self.createIndex(row, column, self.sections[parent.row()])

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Parent of given index"""
        if not index.isValid():
            return QModelIndex()
        section: Section = index.internalPointer()
        if section is None:
            return QModelIndex()  # root nodes
        return self.createIndex(section.row, 0, None)

    def data(self, index: QModelIndex, role: int):
        """Data stored at index"""
        section: Section = index.internalPointer()
        if section is None:
            if role != Qt.ItemDataRole.DisplayRole:
                return None
            return self.sections[index.row()].title

        return section.model.index(index.row(), 1).data(role)

    # pylint: disable=invalid-name, no-self-use
    def hasChildren(self, parent: QModelIndex) -> bool:
        """Whether the given index has children"""
        if not parent.isValid():
            return True
        section: Section = parent.internalPointer()
        if section is not None:
            return False
        section = self.sections[parent.row()]
        if section.model is not None:
            return section.model.rowCount() > 0
        return False

    def rowCount(self, parent: QModelIndex) -> int:
        """Number of rows"""
        if not parent.isValid():
            return len(self.sections)

        section: Section = parent.internalPointer()
        if section is not None:
            return 0

        section = self.sections[parent.row()]
        if section.model is not None:

            return section.model.rowCount()
        return 0

    def columnCount(self, _: QModelIndex) -> int:
        """Number of columns"""
        return 1
