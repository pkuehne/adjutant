""" TableView for Bases model"""

from typing import List, cast
from PyQt6.QtCore import (
    QAbstractItemModel,
    QEvent,
    QModelIndex,
    QObject,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import QContextMenuEvent, QKeyEvent
from PyQt6.QtWidgets import QTableView

from adjutant.widgets.sort_filter_header import SortFilterHeader
from adjutant.models.sort_filter_model import SortFilterModel


class SortFilterTable(QTableView):
    """Bases Table View"""

    item_edited = pyqtSignal(QModelIndex)
    item_deleted = pyqtSignal(list)
    context_menu_launched = pyqtSignal(QModelIndex)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._setup_widget()
        self.filter_model = SortFilterModel()

    def _setup_widget(self):
        """Initialize and configure widgets"""
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.installEventFilter(self)
        self.setHorizontalHeader(SortFilterHeader(self))

        self.doubleClicked.connect(
            lambda: self.item_edited.emit(self.selected_indexes()[0])
        )

    def _map_index(self, index: QModelIndex):
        """Maps a filter model index to source"""
        return self.filter_model.mapToSource(index)

    def _map_indexes(self, indexes: List[QModelIndex]):
        """Maps indexes to source"""
        return [self._map_index(x) for x in indexes]

    def selected_indexes(self) -> List[QModelIndex]:
        """Returns the currently selected indexes"""
        return self._map_indexes(self.selectionModel().selectedRows())

    # pylint: disable=invalid-name
    def setModel(self, model: QAbstractItemModel) -> None:
        """Set the source model for the table"""
        self.filter_model.setSourceModel(model)
        self.filter_model.setFilterKeyColumn(-1)  # All columns
        self.filter_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        super().setModel(self.filter_model)
        self.resizeColumnsToContents()

    def contextMenuEvent(self, event: QContextMenuEvent):
        """When right-click context menu is requested"""
        row = self.rowAt(event.y())
        col = self.columnAt(event.x())
        if row == -1 or col == -1:
            return
        index = self.model().index(row, 0)
        self.context_menu_launched.emit(self._map_index(index))

    def eventFilter(self, source: QObject, event: QEvent):
        """Capture delete/backspace key sent to table"""
        if source != self or event.type() != QEvent.Type.KeyPress:
            return super().eventFilter(source, event)

        key = cast(QKeyEvent, event).key()
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            self.item_deleted.emit(self.selected_indexes())
        elif key == Qt.Key.Key_Return:
            indexes = self.selected_indexes()
            if indexes:
                self.item_edited.emit(indexes[0])
        else:
            super().keyPressEvent(event)
        return True
