""" Widget encompassing management of recipe steps"""

from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QWidget

from adjutant.context.dataclasses import RecipeStep


class RecipeStepsWidget(QWidget):
    """Recipe Steps Widget"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.step_list = QListWidget()

        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Set up the layout"""
        self.step_list.setDragEnabled(True)
        self.step_list.setDragDropMode(self.step_list.DragDropMode.InternalMove)

        central = QHBoxLayout()
        central.addWidget(self.step_list)
        central.addStretch()
        central.setContentsMargins(0, 0, 0, 0)

        self.setLayout(central)

    def _setup_signals(self):
        """Connect signals to handlers"""
        self.step_list.itemDoubleClicked.connect(
            lambda item: self.step_list.takeItem(self.step_list.row(item))
        )

    def add_step(self, step: RecipeStep) -> None:
        """Add a new step"""
        item = QListWidgetItem(f"{step.operation_name} - {step.colour_name}")
        item.setData(Qt.ItemDataRole.UserRole + 1, step)
        item.setData(Qt.ItemDataRole.DecorationRole, QColor(f"{step.hexvalue}"))
        self.step_list.addItem(item)

    def get_steps(self) -> List[RecipeStep]:
        """Return the list of steps"""
        steps = []
        item: QListWidgetItem

        for row in range(self.step_list.count()):
            item = self.step_list.item(row)
            steps.append(item.data(Qt.ItemDataRole.UserRole + 1))
        return steps
