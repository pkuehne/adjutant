""" Common base class for all Add/Edit dialogs """

import logging
from dataclasses import dataclass
from typing import Dict, List
from PyQt6.QtWidgets import (
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QModelIndex, QByteArray, Qt

from adjutant.context.context import Context
from adjutant.context.database_context import generate_uuid
from adjutant.models.relational_model import RelationalModel
from adjutant.widgets.recipe_steps_link import RecipeStepsLink


@dataclass
class MappedWidget:
    """Holds widget<->database field mappings"""

    title: str
    widget: QWidget
    field: str
    property: QByteArray = None
    hidden: bool = False


@dataclass
class Buttons:
    """Holds action buttons for the dialog"""

    ok_button: QPushButton
    cancel_button: QPushButton
    delete_button: QPushButton

    def __init__(self, ok_button, cancel_button, delete_button):
        self.ok_button = ok_button
        self.cancel_button = cancel_button
        self.delete_button = delete_button


@dataclass
class Layouts:
    """Holds the layouts for this dialog"""

    form_layout: QFormLayout
    link_layout: QHBoxLayout

    def __init__(self):
        self.form_layout = QFormLayout()
        self.link_layout = QHBoxLayout()


@dataclass
class Features:
    """Holds feature toggles for the dialog"""

    is_add_mode: bool = False
    hide_name_field: bool = False


class AddEditDialog(QDialog):
    """Base class for all add/edit dialogs"""

    def __init__(self, index: QModelIndex, parent=None, **kwargs) -> None:
        super().__init__(parent)
        self.index = index
        self.mapper = QDataWidgetMapper()
        self.widgets: Dict[str, MappedWidget] = {}
        self.link_widget = None
        self.model: RelationalModel = None
        self.layouts = Layouts()
        self.features = Features()
        self.features.is_add_mode = self.index == QModelIndex()
        self.features.hide_name_field = kwargs.get("hide_name_field", False)

        self.buttons = Buttons(
            QPushButton(self.tr("OK"), self),
            QPushButton(self.tr("Cancel")),
            QPushButton(self.tr("Delete")),
        )

        self.setup_layout()

    def set_title(self, title: str) -> None:
        """Update the dialog title"""
        if self.features.is_add_mode:
            self.setWindowTitle(f"Add {title}")
        else:
            self.setWindowTitle(f"Edit {title}")

    def set_widgets(
        self, widgets: List[MappedWidget], link_widget: RecipeStepsLink = None
    ):
        """Load and set the widgets"""
        self.link_widget = link_widget

        if not self.features.hide_name_field:
            widgets.insert(0, MappedWidget("Name", QLineEdit(), "name"))
        if not self.features.is_add_mode:
            widgets.insert(0, MappedWidget("ID", QLabel(), "id"))

        for widget in widgets:
            self.widgets[widget.title] = widget

    def hide_name_field(self):
        """Hide the name field"""
        self.features.hide_name_field = True

    def setup(self):
        """Setup the dialog"""
        if self.features.is_add_mode:
            record = self.model.record()
            uuid = generate_uuid()
            record.setValue("id", uuid)
            self.model.insertRecord(-1, record)
            self.index = self.model.index(self.model.rowCount() - 1, 0)

        self.layout_widgets()
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
        edit_widget_layout.addLayout(self.layouts.form_layout)
        edit_widget_layout.addLayout(self.layouts.link_layout)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.HLine)
        frame.setFrameShadow(QFrame.Shadow.Sunken)

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addWidget(frame)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def layout_widgets(self):
        """Add the widgets to the form layout"""
        for widget in self.widgets.values():
            if not widget.hidden:
                column = self.model.fieldIndex(widget.field)
                tooltip = self.model.headerData(
                    column, Qt.Orientation.Horizontal, Qt.ItemDataRole.ToolTipRole
                )
                label = QLabel(widget.title)
                label.setToolTip(tooltip)
                self.layouts.form_layout.addRow(label, widget.widget)

        if self.link_widget:
            self.layouts.link_layout.addWidget(self.link_widget)

    def setup_widgets(self):
        """Setup the mapper and buttons"""
        if not self.features.is_add_mode:
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
        if self.features.is_add_mode:
            self.buttons.delete_button.setDisabled(True)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.revert_changes)
        self.buttons.ok_button.pressed.connect(self.accept)
        self.buttons.cancel_button.pressed.connect(self.reject)
        self.buttons.delete_button.pressed.connect(self.delete_button_pressed)

    def submit_changes(self):
        """Submits all changes and updates the model"""
        # Submit Bases table change
        success = self.mapper.submit()
        if not success:
            logging.error(
                "Add/Edit Submit Mapper Error: %s", self.model.lastError().text()
            )

        success = self.model.submitAll()
        if not success:
            logging.error(
                "Add/Edit Submit Model Error: %s", self.model.lastError().text()
            )
        self.model.selectRow(self.index.row())

        if self.link_widget is not None:
            link_id = self.index.siblingAtColumn(0).data()
            self.link_widget.submit_changes(link_id)

    def revert_changes(self):
        """Revert all changes and cancel"""
        self.model.revertAll()
        if self.link_widget is not None:
            self.link_widget.revert_changes()

    def delete_function(self, indexes):
        """overridable delete function"""
        logging.warning("No delete function defined for %s - %s", indexes, self.index)

    def delete_button_pressed(self):
        """Delete the current index"""
        self.delete_function([self.index])
        self.close()

    @classmethod
    def edit(cls, context: Context, index, parent, **kwargs):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, index, parent, **kwargs)
        cls.dialog_reference.exec()
        cls.dialog_reference = None

    @classmethod
    def add(cls, context: Context, parent, **kwargs):
        """Wraps the adding of a colour"""
        cls.dialog_reference = cls(context, QModelIndex(), parent, **kwargs)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
