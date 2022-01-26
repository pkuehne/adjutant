""" Storage Edit/Add dialog"""

from dataclasses import dataclass
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import (
    QCompleter,
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QFrame,
)

from adjutant.context.context import Context
from adjutant.models.row_zero_filter_model import RowZeroFilterModel
from adjutant.widgets.recipe_steps_link import RecipeStepsLink


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    def __init__(self, context: Context, recipe_id: int):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        # self.operations_combobox = QComboBox()
        # self.paints_combobox = QComboBox()
        self.steps_widget = RecipeStepsLink(context, recipe_id)
        # self.add_button = QPushButton()


class RecipeEditDialog(QDialog):
    """Add/Edit Dialog for Recipes"""

    dialog_reference = None

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.widgets = MappedWidgets(self.context, index.data())
        self.index = index.siblingAtColumn(0)
        self.add_mode = index == QModelIndex()
        self.model = context.models.recipes_model

        self.mapper = QDataWidgetMapper()

        self.ok_button = QPushButton(self.tr("OK"), self)
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.delete_button = QPushButton(self.tr("Delete"))

        self.setWindowTitle("Edit Colour Recipe")
        if self.add_mode:
            self.model.insertRow(self.model.rowCount())
            self.index = self.model.index(self.model.rowCount() - 1, 0)
            self.setWindowTitle("Add Colour Recipe")

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Sets up the layout"""
        form_layout = QFormLayout()
        if not self.add_mode:
            form_layout.addRow("ID: ", self.widgets.id_label)
        form_layout.addRow("Name: ", self.widgets.name_edit)
        form_layout.addRow("Notes: ", self.widgets.notes_edit)

        combobox_layout = QHBoxLayout()
        # combobox_layout.addWidget(self.widgets.operations_combobox)
        # combobox_layout.addWidget(self.widgets.paints_combobox)
        # combobox_layout.addWidget(self.widgets.add_button)

        steps_layout = QVBoxLayout()
        steps_layout.addLayout(combobox_layout)
        steps_layout.addWidget(self.widgets.steps_widget)

        edit_widget_layout = QHBoxLayout()
        edit_widget_layout.addLayout(form_layout)
        edit_widget_layout.addLayout(steps_layout)

        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.delete_button)
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.ok_button)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.HLine)
        # frame.setFrameShadow(QFrame.Shadow.Sunken)

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addWidget(frame)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Sets up the widgets"""
        completer = QCompleter(self.context.models.paints_model)
        completer.setCompletionColumn(1)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(completer.CompletionMode.InlineCompletion)

        model = RowZeroFilterModel()
        model.setSourceModel(self.context.models.step_operations_model)

        self.widgets.id_label.setText(str(self.index.data()))
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(self.mapper.SubmitPolicy.ManualSubmit)
        self.mapper.addMapping(self.widgets.name_edit, self.field("name"))
        self.mapper.addMapping(
            self.widgets.notes_edit, self.field("notes"), b"plainText"
        )

        self.mapper.setCurrentModelIndex(self.index)

        # Buttons
        self.ok_button.setDefault(True)
        if self.add_mode:
            self.delete_button.setDisabled(True)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.revert_changes)
        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)
        self.delete_button.pressed.connect(self.delete_button_pressed)

    def submit_changes(self):
        """Submits all changes and updates the model"""
        success = self.mapper.submit()
        if not success:
            print("Mapper Error: " + self.model.lastError().text())
        success = self.model.submitAll()
        if not success:
            print("Model Error: " + self.model.lastError().text())
        self.model.selectRow(self.index.row())
        recipe_id = self.index.siblingAtColumn(0).data()
        self.widgets.steps_widget.submit_changes(recipe_id)

    def revert_changes(self):
        """Revert"""
        self.model.revertAll()
        self.widgets.steps_widget.revert_changes()

    def delete_button_pressed(self):
        """Delete the current index"""
        self.context.controller.delete_recipes([self.index])
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
