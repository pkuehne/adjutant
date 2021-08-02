""" Dialog to manage tags"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QListView, QPushButton, QVBoxLayout

from adjutant.context import Context


class ManageTagsDialog(QDialog):
    """Dialog to show edit fields for a base"""

    dialog_reference = None

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.setWindowTitle("Manage tags")

        self.tag_list = QListView()
        self.create_button = QPushButton(self.tr("Create tag"))
        self.rename_button = QPushButton(self.tr("Rename tag"))
        self.delete_button = QPushButton(self.tr("Delete tag"))
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
        central.addWidget(self.tag_list)
        central.addLayout(button_layout)

        self.setLayout(central)

    def _setup_widgets(self):
        """Set up the widgets"""
        self.rename_button.setDisabled(True)
        self.delete_button.setDisabled(True)

        self.tag_list.setModel(self.context.models.tags_sort_model)
        self.tag_list.setModelColumn(self.context.models.tags_model.fieldIndex("name"))
        self.tag_list.setSelectionMode(self.tag_list.SelectionMode.SingleSelection)
        self.tag_list.setEditTriggers(self.tag_list.EditTrigger.NoEditTriggers)

    def _setup_signals(self):
        """Setup the signals"""
        self.close_button.pressed.connect(self.accept)
        self.create_button.pressed.connect(self.context.controller.create_tag)
        self.rename_button.pressed.connect(
            lambda: self.context.controller.rename_tag(
                self.tag_list.selectionModel().selectedIndexes()[0]
            )
        )
        self.delete_button.pressed.connect(
            lambda: self.context.controller.delete_tag(
                self.tag_list.selectionModel().selectedIndexes()[0]
            )
        )
        self.tag_list.selectionModel().selectionChanged.connect(
            lambda sel, _: self.tag_selected(sel.indexes())
        )

    def tag_selected(self, _: List[QModelIndex]):
        """Fired whena  tag is selected"""
        self.rename_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    @classmethod
    def show(cls, parent, context):
        """Show the dialog"""
        cls.dialog_reference = cls(parent, context)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
