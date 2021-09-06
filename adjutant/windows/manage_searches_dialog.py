""" Manage searches dialog"""

from typing import List
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QListView, QPushButton, QVBoxLayout

from adjutant.context.context import Context


class ManageSearchesDialog(QDialog):
    """Dialog to manage searches"""

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.setWindowTitle("Manage searches")

        self.searches_list = QListView()
        self.rename_button = QPushButton(self.tr("Rename search"))
        self.delete_button = QPushButton(self.tr("Delete search"))
        self.close_button = QPushButton(self.tr("Close"))

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        central = QHBoxLayout()
        central.addWidget(self.searches_list)
        central.addLayout(button_layout)

        self.setLayout(central)

    def _setup_widgets(self):
        """Setup the widgets"""
        self.rename_button.setDisabled(True)
        self.delete_button.setDisabled(True)

        self.searches_list.setModel(self.context.models.searches_model)
        self.searches_list.setModelColumn(
            self.context.models.searches_model.fieldIndex("name")
        )
        self.searches_list.setSelectionMode(
            self.searches_list.SelectionMode.SingleSelection
        )
        self.searches_list.setEditTriggers(
            self.searches_list.EditTrigger.NoEditTriggers
        )

    def _setup_signals(self):
        """Setup the signals"""
        self.close_button.pressed.connect(self.accept)
        self.rename_button.pressed.connect(
            lambda: self.context.controller.rename_search(
                self.searches_list.selectionModel().selectedIndexes()[0]
            )
        )
        self.delete_button.pressed.connect(
            lambda: self.context.controller.delete_search(
                self.searches_list.selectionModel().selectedIndexes()[0]
            )
        )
        self.searches_list.selectionModel().selectionChanged.connect(
            lambda sel, _: self.search_selected(sel.indexes())
        )

    def search_selected(self, _: List[QModelIndex]):
        """Fired whena  tag is selected"""
        self.rename_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    @classmethod
    def show(cls, parent, context):
        """Show the dialog"""
        cls.dialog_reference = cls(parent, context)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
