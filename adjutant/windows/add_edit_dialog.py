""" Common base class for all Add/Edit dialogs """
from dataclasses import dataclass
from typing import Dict, List
from PyQt6.QtWidgets import (
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QModelIndex, QByteArray

from adjutant.context.context import Context
from adjutant.models.relational_model import RelationalModel


@dataclass
class MappedWidget:
    """Holds widget<->database field mappings"""

    title: str
    widget: QWidget
    field: str
    property: QByteArray = None


@dataclass
class Buttons:
    """Holds action buttons for the dialog"""

    ok_button = QPushButton
    cancel_button = QPushButton
    delete_button = QPushButton

    def __init__(self, ok_button, cancel_button, delete_button):
        self.ok_button = ok_button
        self.cancel_button = cancel_button
        self.delete_button = delete_button


class AddEditDialog(QDialog):
    """Base class for all add/edit dialogs"""

    def __init__(self, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.index = index
        self.mapper = QDataWidgetMapper()
        self.widgets: Dict[str, MappedWidget] = {}
        self.model: RelationalModel = None
        self.form_layout = QFormLayout()
        self.is_add_mode = self.index == QModelIndex()

        self.buttons = Buttons(
            QPushButton(self.tr("OK"), self),
            QPushButton(self.tr("Cancel")),
            QPushButton(self.tr("Delete")),
        )

        self.setup_layout()

    def set_title(self, title: str) -> None:
        """Update the dialog title"""
        if self.is_add_mode:
            self.setWindowTitle(f"Add {title}")
        else:
            self.setWindowTitle(f"Edit {title}")

    def set_widgets(self, widgets: List[MappedWidget]):
        """Load and set the widgets"""
        widgets.insert(0, MappedWidget("Name", QLineEdit(), "name"))
        if not self.is_add_mode:
            widgets.insert(0, MappedWidget("ID", QLabel(), "id"))

        for widget in widgets:
            self.widgets[widget.title] = widget

    def setup(self):
        """Setup the dialog"""
        if self.is_add_mode:
            self.model.insertRow(self.model.rowCount())
            self.index = self.model.index(self.model.rowCount() - 1, 0)

        self.setup_form_layout()
        self.setup_widgets()
        self._setup_signals()

    def setup_layout(self):
        """Setup the widget layout on the dialog"""
        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.buttons.delete_button)
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.buttons.cancel_button)
        action_button_layout.addWidget(self.buttons.ok_button)

        edit_widget_layout = QHBoxLayout()
        edit_widget_layout.addLayout(self.form_layout)

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def setup_form_layout(self):
        """Add the widgets to the form layout"""
        for widget in self.widgets.values():
            self.form_layout.addRow(widget.title, widget.widget)

    def setup_widgets(self):
        """Setup the mapper and buttons"""
        if not self.is_add_mode:
            (self.widgets["ID"].widget).setText(
                str(self.index.siblingAtColumn(0).data())
            )

        # Mapper
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(self.mapper.SubmitPolicy.ManualSubmit)
        for widget in self.widgets.values():
            field_index = self.model.fieldIndex(widget.field)
            if widget.property is not None:
                self.mapper.addMapping(widget.widget, field_index, widget.property)
            else:
                self.mapper.addMapping(widget.widget, field_index)
        self.mapper.setCurrentModelIndex(self.index)

        # Buttons
        self.buttons.ok_button.setDefault(True)
        if self.is_add_mode:
            self.buttons.delete_button.setDisabled(True)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.model.revertAll)
        self.buttons.ok_button.pressed.connect(self.accept)
        self.buttons.cancel_button.pressed.connect(self.reject)
        self.buttons.delete_button.pressed.connect(self.delete_button_pressed)

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

    def delete_function(self, indexes):
        """overridable delete function"""
        print(f"No delete function defined for {indexes} - {self.index}")

    def delete_button_pressed(self):
        """Delete the current index"""
        self.delete_function([self.index])
        self.reject()

    @classmethod
    def edit(cls, context: Context, index, parent):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, index, parent)
        cls.dialog_reference.exec()
        cls.dialog_reference = None

    @classmethod
    def add(cls, context: Context, parent):
        """Wraps the adding of a colour"""
        cls.dialog_reference = cls(context, QModelIndex(), parent)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
