"""Dialog to manage importing paints"""

from dataclasses import dataclass
import logging

from PyQt6.QtCore import Qt
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
    QFileDialog,
    QGroupBox,
    QCheckBox,
)

from adjutant.context.context import Context
from adjutant.context.database_context import generate_uuid
from adjutant.windows.online_import_dialog import OnlineImportDialog
from adjutant.context.url_loader import parse_yaml


@dataclass
class PaintItem:
    """Represents a paint from an import file"""

    name: str
    range: str
    manufacturer: str
    hexvalue: str

    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.range = data.get("range", "")
        self.manufacturer = data.get("manufacturer", "")
        self.hexvalue = data.get("hexvalue", "")


class ImportPaintsDialog(QDialog):
    """Dialog to choose which paints to import"""

    @dataclass
    class Widgets:
        """Widgets for the import paints dialog"""

        cancel_button: QPushButton
        ok_button: QPushButton
        from_file_button: QPushButton
        from_online_button: QPushButton
        option_skip_existing: QCheckBox
        option_add_note: QCheckBox

    def __init__(self, parent: QWidget, context: Context) -> None:
        super().__init__(parent)
        self.context = context
        self.paints = []
        self.item_table = QTableWidget()
        self.widgets = self.Widgets(
            QPushButton(self.tr("Cancel")),
            QPushButton(self.tr("OK")),
            QPushButton(self.tr("Import From File")),
            QPushButton(self.tr("Import From Internet")),
            QCheckBox(self.tr("Skip Existing Paints")),
            QCheckBox(self.tr("Add note")),
        )
        self.setFixedSize(QGuiApplication.primaryScreen().availableSize() * 0.3)
        self.setWindowTitle("Import Paints")
        self.setup_layout()
        self.setup_widgets()
        self.setup_signals()

    def setup_layout(self):
        """Set up the layout"""
        import_button_layout = QHBoxLayout()
        import_button_layout.addWidget(self.widgets.from_file_button)
        import_button_layout.addSpacing(10)
        import_button_layout.addWidget(self.widgets.from_online_button)
        source_group = QGroupBox(self.tr("Import Source"))
        source_group.setLayout(import_button_layout)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.widgets.option_skip_existing)
        options_layout.addWidget(self.widgets.option_add_note)
        options_group = QGroupBox(self.tr("Import Options"))
        options_group.setLayout(options_layout)

        action_button_layout = QHBoxLayout()
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.widgets.cancel_button)
        action_button_layout.addWidget(self.widgets.ok_button)

        central = QVBoxLayout()
        central.addWidget(source_group)
        central.addWidget(self.item_table)
        central.addWidget(options_group)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def setup_signals(self):
        """Setup signals"""
        self.widgets.ok_button.pressed.connect(self.accept)
        self.widgets.cancel_button.pressed.connect(self.reject)
        self.widgets.from_online_button.pressed.connect(self.load_from_online)
        self.widgets.from_file_button.pressed.connect(self.load_from_file)
        self.accepted.connect(self.import_paints)

    def setup_widgets(self):
        """Setup the widgets"""
        self.item_table.setColumnCount(3)
        self.item_table.verticalHeader().hide()
        self.item_table.setHorizontalHeaderLabels(["Name", "Range", "Manufacturer"])
        self.item_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.item_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.item_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.item_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.item_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.item_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.widgets.option_skip_existing.setToolTip(
            self.tr(
                "When checked, will skip any paints during import "
                "that have the exact same name as an already existing paint"
            )
        )
        self.widgets.option_skip_existing.setChecked(True)
        self.widgets.option_add_note.setToolTip(
            self.tr(
                "When checked, will add a note saying 'Imported' to all imported paints"
            )
        )
        self.widgets.option_add_note.setChecked(True)

    def load_from_online(self):
        """Opens the Online Import Dialog"""
        paints = OnlineImportDialog.show("paints", self)
        if len(paints) == 0:
            return
        self.paints = [PaintItem(p) for p in paints]
        self.load_table()

    def load_from_file(self):
        """Asks user for a file and then loads the paints from it"""
        filename = QFileDialog.getOpenFileName(
            self, "Open File", filter=self.tr("YAML File (*.yaml)")
        )[0]
        if filename == "":
            return

        with open(filename) as file:
            yaml_data = parse_yaml(file.read())
        self.paints = [PaintItem(p) for p in yaml_data.get("paints", [])]
        self.load_table()

    def load_table(self):
        """Load paints into the table"""
        self.item_table.clearContents()
        self.item_table.setRowCount(len(self.paints))
        row = 0
        for paint in self.paints:
            name_item = QTableWidgetItem(paint.name)
            name_item.setCheckState(Qt.CheckState.Checked)
            self.item_table.setItem(row, 0, name_item)
            self.item_table.setItem(row, 1, QTableWidgetItem(paint.range))
            self.item_table.setItem(row, 2, QTableWidgetItem(paint.manufacturer))
            row += 1

    def selected_paints(self):
        """Returns the list of paints that are checked"""
        return [
            p
            for i, p in enumerate(self.paints)
            if self.item_table.item(i, 0).checkState() == Qt.CheckState.Checked
        ]

    def name_exists(self, name: str) -> bool:
        """Checks whether the given name already exists in the database"""
        model = self.context.models.paints_model
        for row in range(model.rowCount()):
            if model.field_data(row, "name").casefold() == name.casefold():
                return True
        return False

    def import_paints(self):
        """Import selected paints into model"""
        model = self.context.models.paints_model
        for paint in self.selected_paints():
            if self.widgets.option_skip_existing.isChecked():
                if self.name_exists(paint.name):
                    continue
            record = model.record()
            record.setValue("id", generate_uuid())
            record.setValue("name", paint.name)
            record.setValue("manufacturer", paint.manufacturer)
            record.setValue("range", paint.range)
            record.setValue("hexvalue", paint.hexvalue)
            if self.widgets.option_add_note.isChecked():
                record.setValue("notes", "Imported")
            else:
                record.setValue("notes", "")
            model.insertRecord(-1, record)
        model.submitAll()
        logging.info(
            "Loaded %s paints out of %s", len(self.selected_paints()), len(self.paints)
        )

    @classmethod
    def show(cls, parent, context, **kwargs):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(parent, context, **kwargs)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
