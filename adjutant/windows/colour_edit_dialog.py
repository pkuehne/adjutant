""" Storage Edit/Add dialog"""

from dataclasses import dataclass
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import (
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from adjutant.context.context import Context
from adjutant.widgets.colour_pick import ColourPick


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    def __init__(self):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.manufacturer_edit = QLineEdit()
        self.range_edit = QLineEdit()
        self.hexvalue_edit = ColourPick()


class ColourEditDialog(QDialog):
    """Add/Edit Dialog for colours"""

    dialog_reference = None

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.index = index
        self.add_mode = index == QModelIndex()
        self.model = context.models.colours_model

        self.mapper = QDataWidgetMapper()
        self.widgets = MappedWidgets()

        self.ok_button = QPushButton(self.tr("OK"), self)
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.delete_button = QPushButton(self.tr("Delete"))

        self.setWindowTitle("Edit Colour")
        if self.add_mode:
            self.model.insertRow(self.model.rowCount())
            self.index = self.model.index(self.model.rowCount() - 1, 0)
            self.setWindowTitle("Add Colour")

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Sets up the layout"""
        form_layout = QFormLayout()
        if not self.add_mode:
            form_layout.addRow("ID: ", self.widgets.id_label)
        form_layout.addRow("Name: ", self.widgets.name_edit)
        form_layout.addRow("Manufacturer: ", self.widgets.manufacturer_edit)
        form_layout.addRow("Range: ", self.widgets.range_edit)
        form_layout.addRow("Colour: ", self.widgets.hexvalue_edit)

        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.delete_button)
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.ok_button)

        edit_widget_layout = QHBoxLayout()
        edit_widget_layout.addLayout(form_layout)

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Sets up the widgets"""
        self.widgets.id_label.setText(str(self.index.siblingAtColumn(0).data()))
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(self.mapper.SubmitPolicy.ManualSubmit)
        self.mapper.addMapping(self.widgets.name_edit, self.field("name"))
        self.mapper.addMapping(
            self.widgets.manufacturer_edit, self.field("manufacturer")
        )
        self.mapper.addMapping(self.widgets.range_edit, self.field("range"))
        self.mapper.addMapping(self.widgets.hexvalue_edit, self.field("hexvalue"))

        self.mapper.setCurrentModelIndex(self.index)

        # Buttons
        self.ok_button.setDefault(True)
        if self.add_mode:
            self.delete_button.setDisabled(True)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.model.revertAll)
        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)
        self.delete_button.pressed.connect(self.delete_button_pressed)

    def submit_changes(self):
        """Submits all changes and updates the model"""
        # Submit Bases table change
        success = self.mapper.submit()
        if not success:
            print("Mapper Error: " + self.model.lastError().text())
        success = self.model.submitAll()
        if not success:
            print("Model Error: " + self.model.lastError().text())
        self.model.selectRow(self.index.row())

    def delete_button_pressed(self):
        """Delete the current index"""
        self.context.controller.delete_colour(self.index)
        self.reject()

    def field(self, name: str) -> int:
        """Shortcut to get the field number from the name"""
        return self.model.fieldIndex(name)

    @classmethod
    def edit(cls, context, index, parent):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, index, parent)
        cls.dialog_reference.exec()
        cls.dialog_reference = None

    @classmethod
    def add(cls, context, parent):
        """Wraps the adding of a colour"""
        cls.dialog_reference = cls(context, QModelIndex(), parent)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
