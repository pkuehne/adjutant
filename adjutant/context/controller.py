""" Context for the controller """

from typing import List
from PyQt6.QtCore import QModelIndex, QObject, Qt
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from adjutant.context.settings_context import SettingsContext
from adjutant.context.signal_context import SignalContext
from adjutant.context.model_context import ModelContext
from adjutant.context.database_context import (
    DatabaseContext,
    TagResult,
    get_tag_count,
    remove_all_tags_for_base,
)


class Controller(QObject):
    """Controller Context"""

    def __init__(
        self,
        models: ModelContext,
        database: DatabaseContext,
        signals: SignalContext,
        settings: SettingsContext,
    ) -> None:
        super().__init__(parent=None)
        self.models = models
        self.database = database
        self.signals = signals
        self.settings = settings

    def convert_index(self, index: QModelIndex) -> QModelIndex:
        """Converts index reference to bases_table index"""
        if index.model() == self.models.bases_filter_model:
            index = self.models.bases_filter_model.mapToSource(index)
        if index.model() == self.models.tags_sort_model:
            index = self.models.tags_sort_model.mapToSource(index)
        return index

    def delete_bases(self, indexes: List[QModelIndex]):
        """Delete all currently selected rows"""
        result = QMessageBox.warning(
            None,
            "Confirm deletion",
            "Are you sure you want to delete these bases?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        for index in indexes:
            index = self.convert_index(index)
            self.models.bases_model.removeRow(index.row())
        self.models.bases_model.submitAll()

    def duplicate_base(self, index: QModelIndex, num: int) -> bool:
        """Duplicate the given base num times"""
        index = self.convert_index(index)
        for _ in range(num):
            record = self.models.bases_model.record(index.row())
            record.setNull("id")
            self.models.bases_model.insertRecord(-1, record)
        success = self.models.bases_model.submitAll()
        if not success:
            return False
        return self.duplicate_tags(index, num)

    def create_tag(self, default=""):
        """Create a new tag"""
        name, success = QInputDialog.getText(
            None, "New tag", "Please enter a name for the tag", text=default
        )

        if name == "" or not success:
            return

        record = self.models.tags_model.record()
        record.setNull("id")
        record.setValue("name", name)
        self.models.tags_model.insertRecord(-1, record)
        self.models.tags_model.submitAll()

    def rename_tag(self, index: QModelIndex):
        """Rename the given tag"""
        index = self.convert_index(index)
        index = index.siblingAtColumn(1)
        previous = index.data()
        name, success = QInputDialog.getText(
            None, "New tag", f"Rename tag '{previous}' to:", text=previous
        )

        if name == "" or not success:
            return

        self.models.tags_model.setData(index, name)
        self.models.tags_model.submitAll()

    def delete_tag(self, index: QModelIndex):
        """Delete the given tag"""
        index = self.convert_index(index)
        count = get_tag_count(self.database, index.siblingAtColumn(0).data())
        usage = f" It will be removed from {count} bases." if count else ""

        result = QMessageBox.warning(
            None,
            "Confirm deletion",
            "Are you sure you want to delete this tag?" + usage,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        self.models.tags_model.removeRow(index.row())
        self.models.tags_model.submitAll()

    def add_tags(self, index: QModelIndex, tags: List[int]):
        """Add the tags to the given base"""
        model = self.models.base_tags_model
        for tag in tags:
            record = model.record()
            record.setNull("id")
            record.setValue("bases_id", index.siblingAtColumn(0).data())
            record.setValue("tags_id", tag)
            model.insertRecord(-1, record)
        model.submitAll()
        self.signals.tags_updated.emit(index)

    def remove_tags(self, index: QModelIndex, _: List[int]):
        """Remome tags"""
        self.signals.tags_updated.emit(index)

    def set_tags(self, index: QModelIndex, tags: List[int]):
        """Remove all tags and set to parameter"""
        # Remove all tags
        base_id = index.siblingAtColumn(0).data()
        remove_all_tags_for_base(self.database, base_id)
        self.models.base_tags_model.select()

        self.add_tags(index, tags)

    def duplicate_tags(self, index: QModelIndex, num: int) -> bool:
        """Updates the same tags on the last 'num' rows same as index"""
        tag_column = self.models.bases_model.columnCount() - 1
        tags: List[TagResult] = index.siblingAtColumn(tag_column).data(
            Qt.ItemDataRole.EditRole
        )

        num_rows = self.models.bases_model.rowCount()
        for step in range(num):
            idx = self.models.bases_model.index(num_rows - 1 - step, tag_column)
            self.models.bases_model.setData(idx, tags)
        return self.models.bases_model.submitAll()

    def save_search(self):
        """Save the current search"""
        name, success = QInputDialog.getText(None, "Save Search", "Name of search")
        if not success or not name:
            return
        search = self.models.bases_filter_model.encode_filters()
        record = self.models.searches_model.record()
        record.setNull("id")
        record.setValue("name", name)
        record.setValue("encoded", search)
        success = self.models.searches_model.insertRecord(-1, record)
        self.models.searches_model.submitAll()

    def load_search(self, row: int):
        """Restore a saved search"""
        self.models.bases_filter_model.clear_all_column_filters()

        if row == -1:
            self.models.bases_filter_model.setFilterFixedString("")
            self.signals.search_loaded.emit()
            return

        record = self.models.searches_model.record(row)
        self.models.bases_filter_model.decode_filters(record.value("encoded"))
        self.signals.search_loaded.emit()

    def delete_search(self, row: int):
        """Delete the given search"""
        result = QMessageBox.warning(
            None,
            "Confirm deletion",
            "Are you sure you want to delete this search?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        self.models.searches_model.removeRow(row)
        self.models.searches_model.submitAll()

    def rename_search(self, row: int, name: str = None):
        """Rename the given search"""
        # index = self.models.searches_model.index(row, record.)
        success = True
        if name is None:
            name, success = QInputDialog.getText(
                None, "New name", "Please enter a new name for the search"
            )

        if name == "" or not success:
            return

        model = self.models.searches_model
        record = model.record(row)
        record.setValue("name", name)
        model.setRecord(row, record)
        model.submitAll()

    def apply_filter(self, column: int, value):
        """Apply the given filter to the given column"""
        # Get all unique items that are not the value passed in
        items = []
        for row in range(self.models.bases_filter_model.rowCount()):
            data = self.models.bases_filter_model.index(row, column).data()
            if data != value:
                continue
            items.append(data)
        unique = list(set(items))

        self.models.bases_filter_model.set_column_filter(column, unique)

    def filter_by_id(self, id_list: List[int]):
        """Filter the ID column by the supplied list"""
        self.models.bases_filter_model.set_column_filter(0, id_list)
