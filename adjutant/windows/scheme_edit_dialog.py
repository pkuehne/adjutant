""" Storage Edit/Add dialog"""

from dataclasses import dataclass
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
)

from adjutant.context.context import Context
from adjutant.context.dataclasses import SchemeComponent


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    def __init__(self):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        self.component_edit = QLineEdit()
        self.recipe_combobox = QComboBox()
        self.component_list = QListWidget()
        self.add_button = QPushButton()


class SchemeEditDialog(QDialog):
    """Add/Edit Dialog for Recipes"""

    dialog_reference = None

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.index = index.siblingAtColumn(0)
        self.add_mode = index == QModelIndex()
        self.model = context.models.colour_schemes_model

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
        combobox_layout.addWidget(self.widgets.component_edit)
        combobox_layout.addWidget(self.widgets.recipe_combobox)
        combobox_layout.addWidget(self.widgets.add_button)

        steps_layout = QVBoxLayout()
        steps_layout.addLayout(combobox_layout)
        steps_layout.addWidget(self.widgets.component_list)

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
        self._load_existing_steps()

        self.widgets.recipe_combobox.setModel(self.context.models.recipes_model)
        self.widgets.recipe_combobox.setModelColumn(1)

        self.widgets.add_button.setMinimumWidth(3)
        self.widgets.add_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
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

    def _load_existing_steps(self):
        """Load the steps for an existing scheme"""
        model = self.context.models.scheme_components_model
        for row in range(model.rowCount()):
            index = model.field_index(row, "schemes_id")
            if index.data() == self.index.data():
                name = index.siblingAtColumn(model.fieldIndex("name")).data()
                recipe_index = index.siblingAtColumn(model.fieldIndex("recipes_id"))
                component = SchemeComponent(
                    name, recipe_index.data(Qt.ItemDataRole.EditRole)
                )
                item = QListWidgetItem(f"{name} - {recipe_index.data()}")
                item.setData(Qt.ItemDataRole.UserRole + 1, component)
                self.widgets.component_list.addItem(item)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.widgets.recipe_combobox.activated.connect(
            lambda _: self.widgets.add_button.setFocus()
        )
        self.widgets.add_button.pressed.connect(self.add_component_from_widgets)

        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.model.revertAll)
        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)
        self.delete_button.pressed.connect(self.delete_button_pressed)

    def add_component_from_widgets(self):
        """Add a new step to the list"""
        row = self.widgets.recipe_combobox.currentIndex()
        index = self.context.models.recipes_model.index(row, 0)
        name = self.widgets.component_edit.text()
        component = SchemeComponent(name, index.data())
        item = QListWidgetItem(f"{name} - {index.siblingAtColumn(1).data()}")
        item.setData(Qt.ItemDataRole.UserRole + 1, component)
        self.widgets.component_list.addItem(item)

        self.widgets.component_edit.setText("")
        self.widgets.recipe_combobox.setFocus()

    def submit_changes(self):
        """Submits all changes and updates the model"""
        success = self.mapper.submit()
        if not success:
            print("Mapper Error: " + self.model.lastError().text())
        success = self.model.submitAll()
        if not success:
            print("Model Error: " + self.model.lastError().text())
        self.model.selectRow(self.index.row())

        scheme_id = self.index.data()
        components = []
        for row in range(self.widgets.component_list.count()):
            components.append(
                self.widgets.component_list.item(row).data(Qt.ItemDataRole.UserRole + 1)
            )
        self.context.controller.replace_scheme_components(scheme_id, components)

    def delete_button_pressed(self):
        """Delete the current index"""
        self.context.controller.delete_schemes([self.index])
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
