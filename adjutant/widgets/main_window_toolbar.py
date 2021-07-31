""" Toolbar for the main window """


from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QToolBar
from adjutant.context.context import Context


class MainWindowToolbar(QToolBar):
    """Toolbar for the main window"""

    def __init__(self, context: Context, parent):
        super().__init__(parent)
        self.context = context
        self.setMovable(False)

        self._add_actions()

    def _add_actions(self):
        """Add actions to toolbar"""
        add_base_action = QAction(QIcon("icons:add_base.png"), "Add Base", self)
        add_base_action.triggered.connect(self.context.signals.show_add_base_dialog)

        save_search_action = QAction(
            QIcon("icons:save_search.png"), "Save Search", self
        )
        save_search_action.triggered.connect(self.context.controller.save_search)

        # Align buttons here
        self.addAction(add_base_action)
        # self.addAction(save_search_action)
