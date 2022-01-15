""" The Bases Screen Search Bar """

import functools

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QToolButton,
    QHBoxLayout,
    QLabel,
    QMenu,
)

from adjutant.context.context import Context


class SearchBar(QWidget):
    """The Search bar"""

    def __init__(self, context: Context, parent: QWidget = None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.filter_edit = QLineEdit()
        self.clear_button = QPushButton(self.tr("Clear Filters"))
        self.save_button = QPushButton(self.tr("Save Search"))
        self.load_button = QToolButton()

        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()

    def _setup_layout(self):
        self.setContentsMargins(0, 0, 0, 0)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel(self.tr("Filter: ")))
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(self.clear_button)
        filter_layout.addWidget(self.save_button)
        filter_layout.addWidget(self.load_button)

        self.setLayout(filter_layout)

    def _setup_widgets(self):
        self.load_button.setText(self.tr("Load Search"))
        self.load_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.create_load_menu()

    def _setup_signals(self):
        self.clear_button.pressed.connect(lambda: self.filter_edit.setText(""))

        self.context.models.searches_model.data_updated.connect(self.create_load_menu)
        self.load_button.pressed.connect(self.load_button.showMenu)

    def create_load_menu(self):
        """Re-create the load menu"""

        self.load_button.setEnabled(self.context.models.searches_model.rowCount() > 0)
        load_menu = QMenu(self)
        for row in range(self.context.models.searches_model.rowCount()):
            search = self.context.models.searches_model.record(row)
            load_action = QAction(search.value("name"), self)
            load_action.triggered.connect(
                functools.partial(self.context.signals.load_search.emit, row)
            )
            load_menu.addAction(load_action)
        self.load_button.setMenu(load_menu)

    def load_search(self, search_text: str):
        """Restore a saved search"""
        self.filter_edit.blockSignals(True)
        self.filter_edit.setText(search_text)
        self.filter_edit.blockSignals(False)
