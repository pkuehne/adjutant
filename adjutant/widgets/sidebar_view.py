""" Sidebar Tree View """

from typing import List
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTreeView

from adjutant.context import Context
from adjutant.models.sidebar_model import SidebarModel, Section


class SidebarView(QTreeView):
    """Sidebar tree"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.sidebar_model = SidebarModel()
        self.sidebar_model.add_section(Section("All", None, "remove_all_filters"))
        self.sidebar_model.add_section(
            Section(
                "Saved Searches", self.context.models.searches_model, "filter_by_search"
            )
        )

        self.setModel(self.sidebar_model)
        self.resizeColumnToContents(0)
        self.setFixedWidth(self.columnWidth(0) * 1.5)
        self.setHeaderHidden(True)
        self.setSelectionBehavior(self.SelectRows)
        self.selectionModel().selectionChanged.connect(
            lambda sel, _: self.item_selected(sel.indexes())
        )

        # self.setFixedWidth(150)

    def item_selected(self, indexes: List[QModelIndex]):
        """Item selected in view"""
        if not indexes:
            return

        index = indexes[0]
        if index.parent() == QModelIndex():
            section: Section = self.sidebar_model.sections[index.row()]
            getattr(self, section.signal)(QModelIndex())
            return
        section: Section = self.sidebar_model.sections[index.parent().row()]
        getattr(self, section.signal)(index)

    def remove_all_filters(self, _: QModelIndex):
        """Removes all filters"""
        self.context.signals.load_search.emit(-1)

    def filter_by_search(self, index: QModelIndex):
        """Filters by the given search"""
        if index == QModelIndex():
            return
        self.context.signals.load_search.emit(index.row())
