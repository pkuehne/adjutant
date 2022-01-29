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

    def source_record(self, row: int) -> QSqlRecord:
        """Return the record from source model for given row"""
        source_row = self.mapToSource(self.index(row, 0)).row()
        source: RelationalModel = self.sourceModel()
        return source.record(source_row)

    def set_source_record(self, row: int, record: QSqlRecord) -> None:
        """Update given record in the source model"""
        source_row = self.mapToSource(self.index(row, 0)).row()
        source: RelationalModel = self.sourceModel()
        source.setRecord(source_row, record)
        # source.submitAll()

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
        operation_id = model.record(source_row).value("operations_id")
        if recipe_id != self.filter_id or operation_id == 0:
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """Used for sorting model by priority"""
        model: RelationalModel = self.sourceModel()
        left_num = model.record(left.row()).value("priority")
        right_num = model.record(right.row()).value("priority")

        return left_num < right_num

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
        self.buttons = {
            "add": QPushButton(self.tr("Add")),
            "up": QPushButton(self.tr("Up")),
            "down": QPushButton(self.tr("Down")),
        }

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
        self.model.sort(1)
        self.step_list.setModel(self.model)
        self.step_list.setModelColumn(1)
        self.step_list.setEditTriggers(QListView.EditTrigger.NoEditTriggers)

        self.buttons["up"].setEnabled(False)
        self.buttons["down"].setEnabled(False)

    def _setup_layout(self):
        """Set up the layout"""
        buttons = QVBoxLayout()
        buttons.addWidget(self.buttons["add"])
        buttons.addStretch()
        buttons.addWidget(self.buttons["up"])
        buttons.addWidget(self.buttons["down"])
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
        self.step_list.selectionModel().currentChanged.connect(
            self.list_selection_changed
        )
        self.buttons["add"].pressed.connect(self.show_step_add_dialog)
        self.buttons["up"].pressed.connect(lambda: self.move_step(-1))
        self.buttons["down"].pressed.connect(lambda: self.move_step(1))

    def show_step_add_dialog(self):
        """Show the step add dialog"""

        if self.model.rowCount() == 0:
            priority = 1
        else:
            record = self.model.source_record(self.model.rowCount() - 1)
            priority = record.value("priority") + 1

        args = {"link_id": self.link_id, "priority": priority}
        self.context.signals.show_add_dialog.emit("step", args)

    def list_selection_changed(self, current: QModelIndex, __):
        """Selection has changed"""
        is_not_first = current.row() != 0
        is_not_last = current.row() != self.model.rowCount() - 1
        self.buttons["up"].setEnabled(current.isValid() and is_not_first)
        self.buttons["down"].setEnabled(current.isValid() and is_not_last)

    def move_step(self, direction: int):
        """Move step up or down"""
        selected_row = self.step_list.selectionModel().currentIndex().row()
        other_row = selected_row + direction

        # Now swap
        selected_record = self.model.source_record(selected_row)
        other_record = self.model.source_record(other_row)

        temp_step = selected_record.value("priority")
        selected_record.setValue("priority", other_record.value("priority"))
        other_record.setValue("priority", temp_step)

        self.model.set_source_record(selected_row, selected_record)
        self.model.set_source_record(other_row, other_record)

        self.source_model.submitAll()
        # self.step_list.selectionModel().setCurrentIndex(
        #     self.model.index(other_row, 0),
        #     self.step_list.selectionModel().SelectionFlag.ClearAndSelect,
        # )

    def save_current_steps(self):
        """Save the steps now, so they can be reverted to later"""
        for row in range(self.source_model.rowCount()):
            record = self.source_model.record(row)
            if record.value("recipes_id") == self.link_id:
                self.current_steps.append(record)

    def submit_changes(self, link_id: int):
        """Accept the changes"""
        # Nothing needs to be done if all steps already have the right recipe_id
        if self.link_id == link_id:
            return
        for row in range(self.source_model.rowCount()):
            record = self.source_model.record(row)
            if record.value("recipes_id") == self.link_id:
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
            if record.value("recipes_id") == self.link_id:
                self.source_model.removeRow(row)
        for record in self.current_steps:
            self.source_model.insertRecord(-1, record)
        success = self.source_model.submitAll()
        if not success:
            print("Model Error: " + self.source_model.lastError().text())
