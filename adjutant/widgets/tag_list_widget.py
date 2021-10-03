""" Tag List Widget """

from typing import List
import operator
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtProperty
from adjutant.context.dataclasses import Tag


class TagListWidget(QListWidget):
    """Tag List Widget"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    # @property
    @pyqtProperty(list, user=True)
    def tag_list(self) -> List[Tag]:
        """Retrieve the tag list"""
        tags: List[Tag] = []
        for row in range(self.count()):
            item = self.item(row)
            tag_id = item.data(Qt.ItemDataRole.UserRole + 1)
            tag_name = item.data(Qt.ItemDataRole.DisplayRole)
            tags.append(Tag(tag_id, tag_name))
        return sorted(tags, key=operator.attrgetter("tag_name"))

    @tag_list.setter
    def tag_list(self, tags: List[Tag]):
        """Set the given tags"""
        for tag in tags:
            item = QListWidgetItem(tag.tag_name)
            item.setData(Qt.ItemDataRole.UserRole + 1, tag.tag_id)
            self.addItem(item)
