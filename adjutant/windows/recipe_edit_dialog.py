""" Storage Edit/Add dialog"""

from dataclasses import dataclass
from PyQt6.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QCompleter,
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
)

from adjutant.context.context import Context
from adjutant.context.database_context import get_recipe_steps
from adjutant.context.dataclasses import RecipeStep
from adjutant.widgets.recipe_steps_widget import RecipeStepsWidget


class NoNoneFilterModel(QSortFilterProxyModel):
    """Proxy model to hide row 0"""

    # pylint: disable=invalid-name
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """Hides the 0 row"""
        if source_row == 0:
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    # pylint: enable=invalid-name


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    def __init__(self):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        self.operation_combobox = QComboBox()
        self.colour_combobox = QComboBox()
        self.steps_widget = RecipeStepsWidget()
        self.add_button = QPushButton()


class RecipeEditDialog(QDialog):
    """Add/Edit Dialog for Recipes"""

    dialog_reference = None

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.index = index.siblingAtColumn(0)
        self.add_mode = index == QModelIndex()
        self.model = context.models.recipes_model

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
        form_layout.addRow("Notes: ", self.widgets.notes_edit)

        combobox_layout = QHBoxLayout()
        combobox_layout.addWidget(self.widgets.operation_combobox)
        combobox_layout.addWidget(self.widgets.colour_combobox)
        combobox_layout.addWidget(self.widgets.add_button)

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

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Sets up the widgets"""
        steps = get_recipe_steps(self.context.database, self.index.data())
        for step in steps:
            self.widgets.steps_widget.add_step(step)

        completer = QCompleter(self.context.models.colours_model)
        completer.setCompletionColumn(1)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(completer.CompletionMode.InlineCompletion)

        self.widgets.colour_combobox.setModel(self.context.models.colours_model)
        self.widgets.colour_combobox.setModelColumn(1)
        self.widgets.colour_combobox.setEditable(True)
        self.widgets.colour_combobox.setInsertPolicy(
            self.widgets.colour_combobox.InsertPolicy.NoInsert
        )
        self.widgets.colour_combobox.setCompleter(completer)
        self.widgets.colour_combobox.setCurrentText("")

        model = NoNoneFilterModel()
        model.setSourceModel(self.context.models.step_operations_model)
        self.widgets.operation_combobox.setModel(model)
        self.widgets.operation_combobox.setModelColumn(1)

        self.widgets.add_button.setMinimumWidth(1)
        self.widgets.add_button.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
        self.widgets.add_button.setText("˅")

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
        self.widgets.colour_combobox.activated.connect(
            lambda _: self.widgets.add_button.setFocus()
        )
        self.widgets.add_button.pressed.connect(self.add_step)

        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.model.revertAll)
        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)
        self.delete_button.pressed.connect(self.delete_button_pressed)

    def add_step(self):
        """Add a new step to the list"""
        colour_row = self.widgets.colour_combobox.currentIndex()
        colour_index = self.context.models.colours_model.index(colour_row, 0)
        operations_row = self.widgets.operation_combobox.currentIndex()
        operations_index = self.widgets.operation_combobox.model().index(
            operations_row, 0
        )

        colour_id = colour_index.siblingAtColumn(0).data()
        colour_name = colour_index.siblingAtColumn(1).data()
        hexvalue = colour_index.siblingAtColumn(
            self.context.models.colours_model.fieldIndex("hexvalue")
        ).data()
        operation_id = operations_index.siblingAtColumn(0).data()
        operation_name = operations_index.siblingAtColumn(1).data()

        step = RecipeStep(
            colour_id, colour_name, operation_id, operation_name, hexvalue
        )
        self.widgets.steps_widget.add_step(step)
        self.widgets.colour_combobox.setCurrentText("")
        self.widgets.colour_combobox.setFocus()

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
        recipe_id = self.index.siblingAtColumn(0).data()
        self.context.controller.replace_recipe_steps(
            recipe_id, self.widgets.steps_widget.get_steps()
        )

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
