""" Dialog to manage tags"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QListView, QPushButton, QVBoxLayout

from adjutant.context import Context
from adjutant.models.row_zero_filter_model import RowZeroFilterModel


class ManageStatusesDialog(QDialog):
    """Dialog to show and manage available statuses"""

    dialog_reference = None

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.setWindowTitle("Manage statuses")

        self.model = RowZeroFilterModel(self)
        self.item_list = QListView()
        self.create_button = QPushButton(self.tr("Create Status"))
        self.rename_button = QPushButton(self.tr("Rename Status"))
        self.delete_button = QPushButton(self.tr("Delete Status"))
        self.close_button = QPushButton(self.tr("Close"))

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup layouts"""
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        central = QHBoxLayout()
        central.addWidget(self.item_list)
        central.addLayout(button_layout)

        self.setLayout(central)

    def _setup_widgets(self):
        """Set up the widgets"""
        self.rename_button.setDisabled(True)
        self.delete_button.setDisabled(True)

        self.model.setSourceModel(self.context.models.statuses_model)
        self.item_list.setModel(self.model)
        self.item_list.setModelColumn(self.context.models.tags_model.fieldIndex("name"))
        self.item_list.setSelectionMode(self.item_list.SelectionMode.SingleSelection)
        self.item_list.setEditTriggers(self.item_list.EditTrigger.NoEditTriggers)

    def _setup_signals(self):
        """Setup the signals"""
        self.close_button.pressed.connect(self.accept)
        self.create_button.pressed.connect(self.context.controller.create_status)
        self.rename_button.pressed.connect(
            lambda: self.context.controller.rename_status(
                self.model.mapToSource(
                    self.item_list.selectionModel().selectedIndexes()[0]
                )
            )
        )
        self.delete_button.pressed.connect(
            lambda: self.context.controller.delete_status(
                self.model.mapToSource(
                    self.item_list.selectionModel().selectedIndexes()[0]
                )
            )
        )
        self.item_list.selectionModel().selectionChanged.connect(
            lambda sel, _: self.item_selected(sel.indexes())
        )

    def item_selected(self, _: List[QModelIndex]):
        """Fired when an item is selected"""
        self.rename_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    @classmethod
    def show(cls, parent, context):
        """Show the dialog"""
        cls.dialog_reference = cls(parent, context)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
