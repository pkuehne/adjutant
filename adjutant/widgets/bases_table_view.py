""" TableView for Bases model"""

import functools
from typing import cast
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QAction, QContextMenuEvent, QCursor, QKeyEvent
from PyQt6.QtWidgets import QMenu, QTableView

from adjutant.context.context import Context


class BasesTableView(QTableView):
    """Bases Table View"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self._setup_widget()

    def _setup_widget(self):
        """Initialize and configure widgets"""
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(BasesTableView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(BasesTableView.SelectionBehavior.SelectRows)
        self.installEventFilter(self)

        self.doubleClicked.connect(self.context.signals.show_edit_base_dialog.emit)

    def contextMenuEvent(
        self, event: QContextMenuEvent
    ):  # pylint: disable=invalid-name
        """When right-click context menu is requested"""
        row = self.rowAt(event.y())
        col = self.columnAt(event.x())
        if row == -1 or col == -1:
            return
        index = self.model().index(row, 1)

        edit_action = QAction(self.tr("Edit Base"), self)
        edit_action.triggered.connect(
            lambda: self.context.signals.show_edit_base_dialog.emit(index)
        )
        add_action = QAction(self.tr("Add Base"), self)
        add_action.triggered.connect(self.context.signals.show_add_base_dialog.emit)
        delete_action = QAction(self.tr("Delete Bases"), self)
        delete_action.triggered.connect(
            lambda: self.context.controller.delete_bases(
                self.selectionModel().selectedRows()
            )
        )

        duplicate_menu = QMenu(self.tr("Duplicate Base"), self)
        for n in range(1, 11):
            duplicate_action = QAction(str(n) + self.tr(" times"), duplicate_menu)
            duplicate_action.triggered.connect(
                functools.partial(self.context.controller.duplicate_base, index, n)
            )
            duplicate_menu.addAction(duplicate_action)

        def generate_title(column: int):
            title_idx = index.siblingAtColumn(column)
            header = index.model().headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            return f"{header} → {title_idx.data()}"

        apply_menu = QMenu(self.tr("Apply to Selection"), self)
        for column in range(1, self.model().columnCount()):
            apply_action = QAction(generate_title(column), apply_menu)
            apply_action.triggered.connect(
                functools.partial(self.apply_field_to_selection, row, column)
            )
            apply_menu.addAction(apply_action)

        filter_menu = QMenu(self.tr("Filter to Selection"), self)
        for column in range(1, self.model().columnCount()):
            filter_action = QAction(generate_title(column), filter_menu)
            filter_action.triggered.connect(
                functools.partial(self.filter_to_selection, row, column)
            )
            filter_menu.addAction(filter_action)

        menu = QMenu(self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addMenu(duplicate_menu)
        menu.addSeparator()
        menu.addMenu(apply_menu)
        menu.addMenu(filter_menu)
        menu.addSeparator()
        menu.addAction(add_action)
        menu.popup(QCursor.pos())

    def apply_field_to_selection(self, row: int, column: int):
        """Apply the field at index(row, column) to all selected indexes"""
        source = self.model().index(row, column)
        selection = self.selectionModel().selectedRows()

        for index in selection:
            self.model().setData(index.siblingAtColumn(column), source.data())
        self.context.models.bases_model.submitAll()

    def filter_to_selection(self, row: int, column: int):
        """Filter by the selected column"""
        source = self.model().index(row, column)
        self.context.controller.apply_filter(column, source.data())

    def eventFilter(
        self, source: QObject, event: QEvent
    ):  # pylint: disable=invalid-name
        """Capture delete/backspace key sent to table"""
        if source != self or event.type() != QEvent.Type.KeyPress:
            return super().eventFilter(source, event)

        key = cast(QKeyEvent, event).key()
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            self.context.controller.delete_bases(self.selectionModel().selectedRows())
        elif key == Qt.Key.Key_Return:
            indexes = self.selectionModel().selectedRows()
            if indexes:
                self.context.signals.show_edit_base_dialog.emit(indexes[0])
        else:
            super().keyPressEvent(event)
        return True
