""" Sidebar Tree View """

from PyQt6.QtCore import QModelIndex, QPoint
from PyQt6.QtGui import QAction, QContextMenuEvent, QCursor
from PyQt6.QtWidgets import QMenu, QTreeView

from adjutant.context import Context
from adjutant.context.database_context import get_bases_for_tag
from adjutant.models.sidebar_model import SidebarModel, Section


class SidebarView(QTreeView):
    """Sidebar tree"""

    def __init__(self, context: Context, parent=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.sidebar_model = SidebarModel()
        self.sidebar_model.add_section(Section("All", None, "remove_all_filters", None))
        self.sidebar_model.add_section(
            Section(
                "Saved Searches",
                self.context.models.searches_model,
                "filter_by_search",
                self.searches_context_menu,
            )
        )
        self.sidebar_model.add_section(
            Section("Tags", self.context.models.tags_model, "filter_by_tag", None)
        )

        self.setModel(self.sidebar_model)
        self.resizeColumnToContents(0)
        self.setFixedWidth(self.columnWidth(0) * 1.5)
        self.setHeaderHidden(True)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.clicked.connect(self.item_selected)

    def section_from_index(self, index: QModelIndex) -> Section:
        """Get the section for the given index"""
        if index.parent() == QModelIndex():
            section: Section = self.sidebar_model.sections[index.row()]
        else:
            section: Section = self.sidebar_model.sections[index.parent().row()]
        return section

    def item_selected(self, index: QModelIndex):
        """Item selected in view"""
        section: Section = self.section_from_index(index)
        if index.parent() == QModelIndex():
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

        getattr(self, section.signal)(index)

    def remove_all_filters(self, _: QModelIndex):
        """Removes all filters"""
        self.context.controller.load_search(-1)

    def filter_by_search(self, index: QModelIndex):
        """Filters by the given search"""
        if index.parent() == QModelIndex():
            return
        self.context.controller.load_search(index.row())

    def filter_by_tag(self, index: QModelIndex):
        """Filter by the given tag"""
        if index.parent() == QModelIndex():
            # Filter by those that don't have any tags
            return
        tag_id = self.context.models.tags_model.index(index.row(), 0).data()
        bases = get_bases_for_tag(self.context.database, tag_id)
        self.context.signals.filter_by_id.emit(bases)

    def contextMenuEvent(
        self, event: QContextMenuEvent
    ):  # pylint: disable=invalid-name
        """When right-click context menu is requested"""
        index = self.indexAt(QPoint(event.x(), event.y()))
        if not index.isValid():
            return

        section: Section = self.section_from_index(index)
        menu = section.context_menu
        if callable(menu):
            menu = section.context_menu(index)
        if menu is None:
            return
        menu.popup(QCursor.pos())

    def searches_context_menu(self, index):
        """Create the context menu for the searches"""

        if index.parent() == QModelIndex():
            # Top level search doesn't get a context menu
            return None

        rename_action = QAction(self.tr("Rename Search"), self)
        rename_action.triggered.connect(
            lambda: self.context.controller.rename_search(index.row())
        )

        delete_action = QAction(self.tr("Delete Search"), self)
        delete_action.triggered.connect(
            lambda: self.context.controller.delete_search(index.row())
        )

        menu = QMenu(self)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        return menu
