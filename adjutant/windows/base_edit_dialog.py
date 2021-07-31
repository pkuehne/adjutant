""" Edit Window for a Base """

from dataclasses import dataclass
from PyQt6.QtCore import QModelIndex, QStringListModel, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QCompleter,
    QDataWidgetMapper,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)
from adjutant.context import Context
from adjutant.context.database_context import get_tags_for_base


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    def __init__(self):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.scale_edit = QLineEdit()
        self.base_combobox = QComboBox()
        self.width_edit = QSpinBox()
        self.depth_edit = QSpinBox()
        self.figures_edit = QSpinBox()
        self.material_combobox = QComboBox()
        self.sculptor_edit = QLineEdit()
        self.manufacturer_edit = QLineEdit()
        self.retailer_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.date_acquired = QDateEdit()
        self.completed = QCheckBox()
        self.damaged = QCheckBox()
        self.notes_edit = QTextEdit()
        self.custom_id_edit = QLineEdit()
        self.tag_list = QListWidget()
        self.tag_edit = QComboBox()


class BaseEditDialog(QDialog):
    """Dialog to show edit fields for a base"""

    dialog_reference = None
    duplicate_base = pyqtSignal(QModelIndex, int)

    def __init__(self, context: Context, index: QModelIndex, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.index = index
        self.add_mode = index == QModelIndex()
        self.model = self.context.models.bases_model

        self.mapper = QDataWidgetMapper()
        self.widgets = MappedWidgets()

        self.duplicate_edit = QSpinBox()

        self.ok_button = QPushButton(self.tr("OK"), self)
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.delete_button = QPushButton(self.tr("Delete"))

        self.setWindowTitle("Edit Base")
        if self.add_mode:
            self.model.insertRow(self.model.rowCount())
            self.index = self.model.index(self.model.rowCount() - 1, 0)
            self.setWindowTitle("Add Base")

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Sets up the layout"""
        form_layout = QFormLayout()
        if not self.add_mode:
            form_layout.addRow("ID: ", self.widgets.id_label)
        form_layout.addRow("Name: ", self.widgets.name_edit)
        form_layout.addRow("Scale: ", self.widgets.scale_edit)
        form_layout.addRow("Base Style: ", self.widgets.base_combobox)
        form_layout.addRow("Width: ", self.widgets.width_edit)
        form_layout.addRow("Depth: ", self.widgets.depth_edit)
        form_layout.addRow("Figures: ", self.widgets.figures_edit)
        form_layout.addRow("Material", self.widgets.material_combobox)
        form_layout.addRow("Sculptor: ", self.widgets.sculptor_edit)
        form_layout.addRow("Manufacturer: ", self.widgets.manufacturer_edit)
        form_layout.addRow("Retailer: ", self.widgets.retailer_edit)
        form_layout.addRow("Price: ", self.widgets.price_edit)
        form_layout.addRow("Acquired: ", self.widgets.date_acquired)
        form_layout.addRow("Completed: ", self.widgets.completed)
        form_layout.addRow("Damaged", self.widgets.damaged)
        form_layout.addRow("Notes: ", self.widgets.notes_edit)
        form_layout.addRow("Custom ID: ", self.widgets.custom_id_edit)

        if self.add_mode:
            form_layout.addRow("", QLabel(""))
            form_layout.addRow("Duplicates: ", self.duplicate_edit)

        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.delete_button)
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.ok_button)

        tag_layout = QVBoxLayout()
        tag_layout.addWidget(QLabel("Tagging"))
        tag_layout.addWidget(self.widgets.tag_edit)
        tag_layout.addWidget(self.widgets.tag_list)
        edit_widget_layout = QHBoxLayout()
        edit_widget_layout.addLayout(form_layout)
        edit_widget_layout.addLayout(tag_layout)

        central = QVBoxLayout()
        central.addLayout(edit_widget_layout)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Sets up the widgets"""

        # Edit widgets & Mapper

        self.widgets.base_combobox.setModel(
            QStringListModel(["Round", "Oval", "Rectangle", "Square", "Vignette"])
        )
        self.widgets.material_combobox.setModel(
            QStringListModel(["Plastic", "Resin", "Metal"])
        )
        self.widgets.date_acquired.setCalendarPopup(True)

        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(self.mapper.SubmitPolicy.ManualSubmit)
        self.mapper.addMapping(self.widgets.id_label, self.field("id"), b"text")
        self.mapper.addMapping(self.widgets.name_edit, self.field("name"))
        self.mapper.addMapping(self.widgets.scale_edit, self.field("scale"))
        self.mapper.addMapping(
            self.widgets.base_combobox, self.field("base"), b"currentText"
        )
        self.mapper.addMapping(self.widgets.width_edit, self.field("width"))
        self.mapper.addMapping(self.widgets.depth_edit, self.field("depth"))
        self.mapper.addMapping(self.widgets.figures_edit, self.field("figures"))
        self.mapper.addMapping(self.widgets.material_combobox, self.field("material"))
        self.mapper.addMapping(self.widgets.sculptor_edit, self.field("sculptor"))
        self.mapper.addMapping(
            self.widgets.manufacturer_edit, self.field("manufacturer")
        )
        self.mapper.addMapping(self.widgets.retailer_edit, self.field("retailer"))
        self.mapper.addMapping(self.widgets.price_edit, self.field("price"))
        self.mapper.addMapping(self.widgets.date_acquired, self.field("date_acquired"))
        self.mapper.addMapping(self.widgets.completed, self.field("completed"))
        self.mapper.addMapping(self.widgets.damaged, self.field("damaged"))
        self.mapper.addMapping(
            self.widgets.notes_edit, self.field("notes"), b"plainText"
        )
        self.mapper.addMapping(self.widgets.custom_id_edit, self.field("custom_id"))

        self.mapper.setCurrentModelIndex(self.index)

        # Tag List
        completer = QCompleter(self.context.models.tags_model)
        completer.setCompletionColumn(1)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(completer.CompletionMode.InlineCompletion)
        self.widgets.tag_edit.setEditable(True)
        self.widgets.tag_edit.setCompleter(completer)
        self.widgets.tag_edit.setModel(self.context.models.tags_model)
        self.widgets.tag_edit.setModelColumn(1)
        self.widgets.tag_edit.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.widgets.tag_edit.setCurrentText("")
        self.widgets.tag_edit.activated.connect(self.tag_selected)

        self.widgets.tag_list.itemDoubleClicked.connect(self.tag_removed)
        self._load_tag_list()

        # Buttons
        self.ok_button.setDefault(True)
        if self.add_mode:
            self.delete_button.setDisabled(True)

    def _load_tag_list(self):
        """Load the tag list with the base's tags"""
        tags = get_tags_for_base(
            self.context.database, self.index.siblingAtColumn(0).data()
        )
        for tag in tags:
            self.add_tag_to_list(tag.tag_name, tag.tag_id)

    def add_tag_to_list(self, tag_name: str, tag_id: int):
        """Adds the given tag to the tag list"""
        item = QListWidgetItem(tag_name)
        item.setData(Qt.ItemDataRole.UserRole + 1, tag_id)
        self.widgets.tag_list.addItem(item)

    def tag_selected(self, row: int):
        """Add the tag to the list"""
        self.widgets.tag_edit.setCurrentText("")

        model = self.widgets.tag_edit.model()
        tag_id = model.index(row, 0).data()
        tag_name = model.index(row, 1).data()

        items = self.widgets.tag_list.findItems(tag_name, Qt.MatchFlag.MatchExactly)
        if items:
            # Don't add to the list, it's already there
            return

        self.add_tag_to_list(tag_name, tag_id)

    def tag_removed(self, _: QListWidgetItem):
        """Remove tag from list"""
        row = self.widgets.tag_list.selectedIndexes()[0].row()
        self.widgets.tag_list.takeItem(row)

    def field(self, name: str) -> int:
        """Shortcut to get the field number from the name"""
        return self.model.fieldIndex(name)

    def _setup_signals(self):
        """Setup signals on widgets"""
        self.accepted.connect(self.submit_changes)
        self.rejected.connect(self.model.revertAll)
        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)
        self.delete_button.pressed.connect(self.delete_button_pressed)
        self.widgets.base_combobox.currentTextChanged.connect(
            self.base_combobox_changed
        )
        self.base_combobox_changed(self.widgets.base_combobox.currentText())

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

        tags = []
        for row in range(self.widgets.tag_list.count()):
            item = self.widgets.tag_list.item(row)
            tags.append(item.data(Qt.ItemDataRole.UserRole + 1))
        self.context.controller.set_tags(self.index, tags)

        if self.add_mode and self.duplicate_edit.value() > 0:
            self.context.signals.duplicate_base.emit(
                self.index, self.duplicate_edit.value()
            )

    def delete_button_pressed(self):
        """Delete the current index"""
        self.context.signals.delete_bases.emit([self.index])
        self.reject()

    def base_combobox_changed(self, text: str):
        """When the base style combobox is changed"""
        self.widgets.depth_edit.setDisabled(text == "Round")
        if text == "Round":
            self.widgets.depth_edit.setValue(0)

    @classmethod
    def edit_base(cls, context, index, parent):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, index, parent)
        # cls.dialog_reference.summary.setFocus()
        cls.dialog_reference.exec()
        # result = cls.dialog_reference.result
        cls.dialog_reference = None
        # return result

    @classmethod
    def add_base(cls, context, parent):
        """Wraps the adding of a base"""
        cls.dialog_reference = cls(context, QModelIndex(), parent)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
