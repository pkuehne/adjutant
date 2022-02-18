""" TableView for Bases model"""

import functools
from typing import List, cast
from PyQt6.QtCore import (
    QAbstractItemModel,
    QEvent,
    QModelIndex,
    QObject,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import QContextMenuEvent, QKeyEvent, QCursor, QAction
from PyQt6.QtWidgets import QTableView, QMenu
from adjutant.context.context import Context
from adjutant.models.relational_model import RelationalModel
from adjutant.models.sort_filter_model import SortFilterModel
from adjutant.widgets.sort_filter_header import SortFilterHeader


def apply_field_to_index_list(source: QModelIndex, destination: List[QModelIndex]):
    """Apply the data from the source index to the same field in the destination list"""
    model: RelationalModel = source.model()
    for index in destination:
        model.setData(
            index.siblingAtColumn(source.column()),
            source.data(Qt.ItemDataRole.EditRole),
        )
    model.submitAll()


class SortFilterTable(QTableView):
    """Bases Table View"""

    item_edited = pyqtSignal(QModelIndex)
    item_deleted = pyqtSignal(list)
    item_added = pyqtSignal()

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.filter_model = SortFilterModel()
        self._setup_widget()

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

    def additional_context_menu_items(self, index: QModelIndex, menu: QMenu):
        """Overridable for subclasses"""

    def generate_title(self, index: QModelIndex, column: int):
        """Generate title for Filter/Apply menu items"""
        title_idx = index.siblingAtColumn(column)
        header = index.model().headerData(
            column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
        )
        return f"{header} → {title_idx.data()}"

    def setup_filter_selection_menu(self, index: QModelIndex) -> QMenu:
        """Setup the "Filter to Selection" menu"""
        filter_menu = QMenu(self.tr("Filter to Selection"), self)
        for column in range(1, self.model().columnCount()):
            filter_action = QAction(self.generate_title(index, column), filter_menu)
            filter_action.triggered.connect(
                functools.partial(
                    self.filter_model.set_column_filter,
                    column,
                    [index.siblingAtColumn(column).data(role=Qt.ItemDataRole.EditRole)],
                )
            )
            filter_menu.addAction(filter_action)
        return filter_menu

    def setup_apply_selection_menu(self, index: QModelIndex) -> QMenu:
        """Setup the "Apply to Selection" menu"""
        apply_menu = QMenu(self.tr("Apply to Selection"), self)
        for column in range(1, self.model().columnCount()):
            apply_action = QAction(self.generate_title(index, column), apply_menu)
            apply_action.triggered.connect(
                functools.partial(
                    apply_field_to_index_list,
                    index.siblingAtColumn(column),
                    self.selected_indexes(),
                )
            )
            apply_menu.addAction(apply_action)
        return apply_menu

    def contextMenuEvent(self, event: QContextMenuEvent):
        """When right-click context menu is requested"""
        row = self.rowAt(event.y())
        col = self.columnAt(event.x())
        if row == -1 or col == -1:
            return
        index = self._map_index(self.model().index(row, 0))
        name = "'" + index.siblingAtColumn(1).data() + "'"  # 1 is always the name

        add_action = QAction(self.tr("Add New"), self)
        add_action.triggered.connect(self.item_added.emit)
        edit_action = QAction(self.tr(f"Edit {name}"), self)
        edit_action.triggered.connect(lambda: self.item_edited.emit(index))
        delete_action = QAction(self.tr(f"Delete {name}"), self)
        delete_action.triggered.connect(
            lambda: self.item_deleted.emit(self.selected_indexes())
        )
        menu = QMenu(self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addSeparator()
        menu.addMenu(self.setup_filter_selection_menu(index))
        menu.addMenu(self.setup_apply_selection_menu(index))
        menu.addSeparator()

        # Hand over to subclasses
        self.additional_context_menu_items(index, menu)

        menu.addSeparator()
        menu.addAction(add_action)
        menu.popup(QCursor.pos())

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
