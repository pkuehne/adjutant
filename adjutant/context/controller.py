""" Context for the controller """

from typing import List
from PyQt6.QtCore import QModelIndex, QObject
from adjutant.context import Context
from adjutant.context.database_context import remove_all_tags_for_base


class Controller(QObject):
    """Controller Context"""

    def __init__(self, parent, context: Context) -> None:
        super().__init__(parent=parent)
        self.context = context

        self.context.signals.add_tags.connect(self.add_tags)
        self.context.signals.remove_tags.connect(self.remove_tags)
        self.context.signals.set_tags.connect(self.set_tags)

    def add_tags(self, index: QModelIndex, tags: List[int]):
        """Add the tags to the given base"""
        model = self.context.models.base_tags_model
        for tag in tags:
            record = model.record()
            record.setNull("id")
            record.setValue("base_id", index.siblingAtColumn(0).data())
            record.setValue("tag_id", tag)
            model.insertRecord(-1, record)

        model.submitAll()

    def remove_tags(self, index: QModelIndex, tags: List[int]):
        """Remome tags"""

    def set_tags(self, index: QModelIndex, tags: List[int]):
        """Remove all tags and set to parameter"""
        # Remove all tags
        base_id = index.siblingAtColumn(0).data()
        remove_all_tags_for_base(self.context.database, base_id)
        self.context.models.base_tags_model.select()

        self.add_tags(index, tags)
