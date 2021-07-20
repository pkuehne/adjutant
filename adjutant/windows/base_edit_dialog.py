""" Edit Window for a Base """

from dataclasses import dataclass
from PyQt5.QtCore import QModelIndex, QStringListModel, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QDataWidgetMapper,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)
from adjutant.context import Context


@dataclass
class MappedWidgets:
    """Holds the widgets that need to be data mapped"""

    id_label: QLabel
    name_edit: QLineEdit
    scale_edit: QLineEdit
    base_combobox: QComboBox
    width_edit: QSpinBox
    depth_edit: QSpinBox
    figures_edit: QSpinBox

    def __init__(self):
        self.id_label = QLabel()
        self.name_edit = QLineEdit()
        self.scale_edit = QLineEdit()
        self.base_combobox = QComboBox()
        self.width_edit = QSpinBox()
        self.depth_edit = QSpinBox()
        self.figures_edit = QSpinBox()


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

        self.ok_button = QPushButton(self.tr("OK"))
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
        if self.add_mode:
            form_layout.addRow("", QLabel(""))
            form_layout.addRow("Duplicates: ", self.duplicate_edit)

        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.delete_button)
        action_button_layout.addStretch()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.ok_button)

        central = QVBoxLayout()
        central.addLayout(form_layout)
        central.addLayout(action_button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """Sets up the widgets"""
        self.widgets.base_combobox.setModel(
            QStringListModel(["Round", "Oval", "Rectangle", "Square", "Vignette"])
        )

        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(self.mapper.ManualSubmit)
        self.mapper.addMapping(self.widgets.id_label, 0, b"text")
        self.mapper.addMapping(self.widgets.name_edit, 1)
        self.mapper.addMapping(self.widgets.scale_edit, 2)
        self.mapper.addMapping(self.widgets.base_combobox, 3, b"currentText")
        self.mapper.addMapping(self.widgets.width_edit, 4)
        self.mapper.addMapping(self.widgets.depth_edit, 5)
        self.mapper.addMapping(self.widgets.figures_edit, 6)

        self.mapper.setCurrentModelIndex(self.index)
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
        self.widgets.base_combobox.currentTextChanged.connect(
            self.base_combobox_changed
        )
        self.base_combobox_changed(self.widgets.base_combobox.currentText())

    def submit_changes(self):
        """Submits all changes and updates the model"""
        success = self.mapper.submit()
        if not success:
            print("Mapper Error: " + self.model.lastError().text())
        success = self.model.submitAll()
        if not success:
            print("Model Error: " + self.model.lastError().text())
        self.model.selectRow(self.index.row())

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
        cls.dialog_reference.exec_()
        # result = cls.dialog_reference.result
        cls.dialog_reference = None
        # return result

    @classmethod
    def add_base(cls, context, parent):
        """Wraps the adding of a base"""
        cls.dialog_reference = cls(context, QModelIndex(), parent)
        cls.dialog_reference.exec_()
        cls.dialog_reference = None
