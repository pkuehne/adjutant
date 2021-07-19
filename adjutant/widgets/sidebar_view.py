""" Sidebar Tree View """

from typing import List
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QSizePolicy, QTreeView

from adjutant.context import Context
from adjutant.models.sidebar_model import SidebarModel, Section


class SidebarView(QTreeView):
    """Sidebar tree"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.sidebar_model = SidebarModel()
        self.sidebar_model.add_section(Section("All", None, ""))
        self.sidebar_model.add_section(
            Section("Saved Searches", self.context.models.searches_model, "")
        )

        self.setModel(self.sidebar_model)
        self.setHeaderHidden(True)
        self.setSelectionBehavior(self.SelectRows)
        self.resizeColumnToContents(0)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.selectionModel().selectionChanged.connect(
            lambda sel, _: self.item_selected
        )

    def item_selected(self, indexes: List[QModelIndex]):
        """Item selected in view"""
