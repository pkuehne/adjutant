""" Preferences dialog"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from adjutant.context.context import Context


class PreferencesDialog(QDialog):
    """Dialog to manage searches"""

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.setWindowTitle("Preferences")

        self.font_size = QComboBox()
        self.close_button = QPushButton(self.tr("Close"))

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        """Setup the layout"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        form_layout = QFormLayout()
        form_layout.addRow("Font Size: ", self.font_size)
        form_layout.addRow("", None)

        central = QVBoxLayout()
        central.addLayout(form_layout)
        central.addLayout(button_layout)

        self.setLayout(central)

    def _setup_widgets(self):
        """Setup the widgets"""
        current_font_size = self.context.models.settings_model.record(0).value(
            "font_size"
        )
        for size in range(5, 48):
            self.font_size.addItem(str(size), size)
            if size == current_font_size:
                self.font_size.setCurrentIndex(size - 5)

    def _setup_signals(self):
        """Setup the signals"""
        self.close_button.pressed.connect(self.accept)

        self.font_size.activated.connect(self.font_size_changed)

    def font_size_changed(self):
        """Font size has been updated"""
        new_size = self.font_size.currentData(Qt.ItemDataRole.UserRole)
        self.context.controller.set_font_size(new_size)

    @classmethod
    def show(cls, parent, context):
        """Show the dialog"""
        cls.dialog_reference = cls(parent, context)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
