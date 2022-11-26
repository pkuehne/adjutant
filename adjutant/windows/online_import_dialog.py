""" Dialog for user to choose from a list of files to import """

from dataclasses import dataclass
import logging
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from adjutant.context.url_loader import UrlLoader

BASE_URL = "https://raw.githubusercontent.com/pkuehne/adjutant"


@dataclass
class ManifestItem:
    """Holds an item from the manifest file"""

    name: str
    filename: str
    desc: str
    updated: str

    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.filename = data.get("filename", "")
        self.desc = data.get("desc", "")
        self.updated = data.get("updated", "")


class OnlineImportDialog(QDialog):
    """Allows import from data files in github"""

    def __init__(self, directory: str, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.directory = directory
        self.file_list = []
        self.return_list = []
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.ok_button = QPushButton(self.tr("OK"))
        self.item_table = QTableWidget()

        self.setFixedSize(QGuiApplication.primaryScreen().availableSize() * 0.3)
        self.setWindowTitle("Online Import")
        self.setup_layout()
        self.setup_widgets()
        self.setup_signals()

        filename = f"{BASE_URL}/main/data/{directory}/manifest.yaml"
        UrlLoader.load_yaml_from_url(filename, self.load_manifest)

    def load_manifest(self, yaml_data):
        """Load the manifest"""
        if yaml_data is None:
            logging.error("Parsing failure")
            return
        self.file_list = [ManifestItem(i) for i in yaml_data.get("files", [])]
        if self.file_list == []:
            logging.warning("No files in manifest")
            return
        self.item_table.setRowCount(len(self.file_list))

        for row, item in enumerate(self.file_list):
            desc_item = QTableWidgetItem(item.desc)
            desc_item.setToolTip(item.desc)
            self.item_table.setItem(row, 0, QTableWidgetItem(item.name))
            self.item_table.setItem(row, 1, desc_item)
            self.item_table.setItem(row, 2, QTableWidgetItem(item.updated))
        self.item_table.setCurrentCell(0, 0)
        self.ok_button.setEnabled(True)

    def setup_layout(self):
        """Set up the layout"""
        action_button_layout = QHBoxLayout()
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.ok_button)

        central = QVBoxLayout()
        central.addWidget(self.item_table)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def setup_signals(self):
        """Setup signals"""
        self.ok_button.pressed.connect(self.load_selected_file)
        self.cancel_button.pressed.connect(self.reject)

    def setup_widgets(self):
        """Setup the widgets"""
        self.ok_button.setDisabled(True)
        headers = ["Name", "Description", "Last Updated"]
        self.item_table.setColumnCount(len(headers))
        self.item_table.verticalHeader().hide()
        self.item_table.setHorizontalHeaderLabels(headers)
        self.item_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.item_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.item_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.item_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.item_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.item_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def load_selected_file(self):
        """Loads the items in the selected file"""
        item = self.file_list[self.item_table.currentRow()]
        filename = f"{BASE_URL}/main/data/{self.directory}/{item.filename}"

        def set_return_list(content: dict):
            """Set the return list from yaml"""
            self.return_list = content.get(self.directory, [])
            self.accept()

        UrlLoader.load_yaml_from_url(filename, set_return_list)

    @classmethod
    def show(cls, directory: str, parent, **kwargs):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(directory, parent, **kwargs)
        cls.dialog_reference.exec()
        return_list = cls.dialog_reference.return_list
        cls.dialog_reference = None
        return return_list
