""" Widget encompassing management of recipe steps"""

from typing import List
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt6.QtSql import QSqlRecord
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QListView,
    QWidget,
    QPushButton,
)

from adjutant.context import Context
from adjutant.models.relational_model import RelationalModel


class RecipeStepsLinkModel(QSortFilterProxyModel):
    """Model to proxy the receipe steps"""

    def __init__(self) -> None:
        super().__init__()
        self.filter_id = 0
        self.string_func = lambda n: ""

    def set_filter_id(self, filter_id) -> None:
        """Update filter ID"""
        self.filter_id = filter_id

    def set_string_func(self, string_func) -> None:
        """Override the stringification function"""
        self.string_func = string_func

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        """Return same string for all fields"""
        if role != Qt.ItemDataRole.DisplayRole:
            return super().data(index, role)
        return self.string_func(self.mapToSource(index))

    # pylint: disable=invalid-name
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """Filter out rows that don't match filter_id"""

        model: RelationalModel = self.sourceModel()
        recipe_id = model.record(source_row).value("recipes_id")
        if recipe_id not in (0, self.filter_id):
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    # pylint: enable=invalid-name


class RecipeStepsLink(QWidget):
    """Recipe Steps Widget"""

    def __init__(self, context: Context, link_id: int, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.link_id = link_id if link_id is not None else 0
        self.model = RecipeStepsLinkModel()
        self.source_model = self.context.models.recipe_steps_model
        self.current_steps: List[QSqlRecord] = []
        self.step_list = QListView()
        self.add_button = QPushButton(self.tr("Add"))

        self._setup_widgets()
        self._setup_layout()
        self._setup_signals()

        self.save_current_steps()

    def _setup_widgets(self):
        """Set up the widgets"""

        def stringify_step(index: QModelIndex) -> str:
            """Stringifies a step record"""
            model: RelationalModel = index.model()
            paint = model.field_index(index.row(), "paints_id").data()
            operation = model.field_index(index.row(), "operations_id").data()
            return f"{operation} - {paint}"

        self.model.setSourceModel(self.source_model)
        self.model.set_filter_id(self.link_id)
        self.model.set_string_func(stringify_step)
        self.step_list.setModel(self.model)
        self.step_list.setModelColumn(1)
        self.step_list.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        # todo: handle re-ordering
        # self.step_list.setDragEnabled(True)
        # self.step_list.setDragDropMode(self.step_list.DragDropMode.InternalMove)

    def _setup_layout(self):
        """Set up the layout"""
        buttons = QVBoxLayout()
        buttons.addWidget(self.add_button)
        buttons.addStretch()

        central = QHBoxLayout()
        central.addWidget(self.step_list)
        central.addStretch()
        central.addLayout(buttons)
        central.setContentsMargins(0, 0, 0, 0)

        self.setLayout(central)

    def _setup_signals(self):
        """Connect signals to handlers"""
        self.step_list.doubleClicked.connect(
            lambda index: self.context.signals.show_edit_dialog.emit(
                "step", self.model.mapToSource(index), {}
            )
        )
        self.add_button.pressed.connect(
            lambda: self.context.signals.show_add_dialog.emit("step", {})
        )

    def save_current_steps(self):
        """Save the steps now, so they can be reverted to later"""
        for row in range(self.source_model.rowCount()):
            record = self.source_model.record(row)
            if record.value("recipes_id") == self.link_id:
                self.current_steps.append(record)

    def submit_changes(self, link_id: int):
        """Accept the changes"""
        for row in range(self.source_model.rowCount()):
            record = self.source_model.record(row)
            if record.value("recipes_id") == 0:
                record.setValue("recipes_id", link_id)
                self.source_model.setRecord(row, record)
        success = self.source_model.submitAll()
        if not success:
            print("Model Error: " + self.source_model.lastError().text())

    def revert_changes(self):
        """Revert all changes"""
        self.source_model.revertAll()
        for row in range(self.source_model.rowCount()):
            record = self.source_model.record(row)
            if record.value("recipes_id") in (0, self.link_id):
                self.source_model.removeRow(row)
        for record in self.current_steps:
            self.source_model.insertRecord(-1, record)
        success = self.source_model.submitAll()
        if not success:
            print("Model Error: " + self.source_model.lastError().text())
