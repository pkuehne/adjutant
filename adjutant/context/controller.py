""" Context for the controller """

from typing import List
import logging
import yaml
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from PyQt6.QtCore import QModelIndex, QObject, Qt, QUrl
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox, QFileDialog
from PyQt6.QtSql import QSqlTableModel
from adjutant.context.url_loader import UrlLoader
from adjutant.context.settings_context import SettingsContext
from adjutant.context.signal_context import SignalContext
from adjutant.context.model_context import ModelContext
from adjutant.context.database_context import (
    DatabaseContext,
    remove_all_tags_for_base,
    remove_scheme_components,
)
from adjutant.context.dataclasses import SchemeComponent, Tag


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
        if index.model() == self.models.tags_sort_model:
            index = self.models.tags_sort_model.mapToSource(index)
        return index

    def create_record(
        self, model: QSqlTableModel, desc: str = "records", default: str = ""
    ):
        """Creates a record in the given model and sets name field"""
        name, success = QInputDialog.getText(
            None, f"New {desc}", f"Please enter a name for the {desc}", text=default
        )

        if name == "" or not success:
            return

        record = model.record()
        record.setNull("id")
        record.setValue("name", name)
        model.insertRecord(-1, record)
        model.submitAll()

    def rename_record(self, model: QSqlTableModel, index: QModelIndex):
        """Rename the given record"""
        previous = index.data()
        name, success = QInputDialog.getText(
            None, "New tag", f"Rename tag '{previous}' to:", text=previous
        )

        if name == "" or not success:
            return

        model.setData(index, name)
        model.submitAll()

    def delete_records(
        self, model: QSqlTableModel, indexes: List[QModelIndex], desc="records"
    ):
        """Removes records from the model with confirmation"""
        result = QMessageBox.warning(
            None,
            "Confirm deletion",
            f"Are you sure you want to delete {len(indexes)} {desc}?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if result == QMessageBox.StandardButton.Cancel:
            return
        for index in indexes:
            model.removeRow(index.row())
        model.submitAll()

    def set_font_size(self, font_size: int):
        """Set the applications font size"""
        if font_size < 5:
            logging.error("Invalid font size: %s", font_size)
            return

        app: QApplication = QApplication.instance()
        font = app.font()
        font.setPointSize(font_size)
        app.setFont(font)

        self.settings.font_size = font_size
        self.settings.save()

    def delete_bases(self, indexes: List[QModelIndex]):
        """Delete all currently selected rows"""
        self.delete_records(self.models.bases_model, indexes, "bases")

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
        self.create_record(self.models.tags_model, "tag", default)

    def rename_tag(self, index: QModelIndex):
        """Rename the given tag"""
        index = self.convert_index(index)
        self.rename_record(self.models.tags_model, index.siblingAtColumn(1))

    def delete_tag(self, index: QModelIndex):
        """Delete the given tag"""
        index = self.convert_index(index)
        self.delete_records(self.models.tags_model, [index])

    def apply_field_to_bases(self, source: QModelIndex, destination: List[QModelIndex]):
        """Apply the data from the source index to the same field in the destination list"""
        for index in destination:
            index = self.convert_index(index)
            self.models.bases_model.setData(
                index.siblingAtColumn(source.column()),
                source.data(Qt.ItemDataRole.EditRole),
            )
        self.models.bases_model.submitAll()

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
        tags: List[Tag] = index.siblingAtColumn(tag_column).data(
            Qt.ItemDataRole.EditRole
        )

        num_rows = self.models.bases_model.rowCount()
        for step in range(num):
            idx = self.models.bases_model.index(num_rows - 1 - step, tag_column)
            self.models.bases_model.setData(idx, tags)
        return self.models.bases_model.submitAll()

    def delete_search(self, index: QModelIndex):
        """Delete the given search"""
        self.delete_records(self.models.searches_model, [index])

    def rename_search(self, index: QModelIndex):
        """Rename the given search"""
        self.rename_record(self.models.searches_model, index.siblingAtColumn(1))

    def edit_storage(self, index: QModelIndex):
        """Edit a storage location"""

    def delete_storages(self, indexes: List[QModelIndex]):
        """Delete all passed-in storages"""
        self.delete_records(self.models.storage_model, indexes, "storage locations")

    def create_status(self):
        """Creates a new status"""
        self.create_record(self.models.statuses_model, "status")

    def rename_status(self, index: QModelIndex):
        """Rename a status"""
        self.rename_record(self.models.statuses_model, index)

    def delete_status(self, index: QModelIndex):
        """Delete a status"""
        old_status = index.siblingAtColumn(0).data()
        self.delete_records(self.models.statuses_model, [index], "status")

        for row in range(self.models.bases_model.rowCount()):
            index = self.models.bases_model.index(
                row, self.models.bases_model.fieldIndex("status_id")
            )
            if index.data(Qt.ItemDataRole.EditRole) == old_status:
                self.models.bases_model.setData(index, 0)

    def delete_paints(self, indexes: List[QModelIndex]):
        """Deletes a given paint"""
        self.delete_records(self.models.paints_model, indexes, "paint")

    def delete_recipes(self, indexes: List[QModelIndex]):
        """Deleted a given colour recipe"""
        for index in indexes:
            recipe_id = index.siblingAtColumn(0).data()
            self.delete_recipe_steps(recipe_id)
        self.delete_records(self.models.recipes_model, indexes, "colour recipe")

    def delete_recipe_steps(self, recipe_id: int):
        """Add a new recipe step"""
        model = self.models.recipe_steps_model
        for row in range(model.rowCount()):
            record = model.record(row)
            if record.value("recipes_id") == recipe_id:
                model.removeRow(row)
        model.submitAll()

    def delete_schemes(self, indexes: List[QModelIndex]):
        """Deleted a given colour recipe"""
        for index in indexes:
            scheme_id = index.siblingAtColumn(0).data()
            self.replace_scheme_components(scheme_id, [])
        self.delete_records(self.models.colour_schemes_model, indexes, "colour scheme")

    def replace_scheme_components(
        self, scheme_id: int, components: List[SchemeComponent]
    ):
        """Add a new recipe step"""
        model = self.models.scheme_components_model
        remove_scheme_components(self.database, scheme_id)
        model.select()
        for component in components:
            record = model.record()
            record.setNull("id")
            record.setValue("schemes_id", scheme_id)
            record.setValue("name", component.name)
            record.setValue("recipes_id", component.recipe_id)
            model.insertRecord(-1, record)
        model.submitAll()

    def import_paints(self):
        """Ask for file and import it into the paints table"""
        filename: QUrl = QFileDialog.getOpenFileUrl(caption="Paints File")[0]
        if not filename.isValid():
            return

        if filename.isLocalFile():
            with open(filename.toLocalFile()) as file:
                self.load_paints_from_string(file.read())
        else:
            thread = UrlLoader(self, filename.toString())
            thread.content_loaded.connect(self.load_paints_from_string)
            thread.finished.connect(thread.deleteLater)
            thread.start()

    def load_paints_from_string(self, file_contents):
        """load the actual data into the paints table"""
        yaml_data = None
        try:
            yaml_data = yaml.safe_load(file_contents)
        except (ScannerError, ParserError) as exc:
            QMessageBox.critical(
                None,
                "Invalid File Format",
                f"Cannot parse the file:\n{exc.problem}\n{exc.problem_mark}",
            )
            return

        # print(yaml_data)

        paints = yaml_data.get("paints", [])
        for paint in paints:
            paint_name = paint.get("name", "")
            if paint_name == "":
                logging.warning("Invalid paint entry with no name")
                continue
            record = self.models.paints_model.record()
            record.setNull("id")
            record.setValue("name", paint.get("name", ""))
            record.setValue("manufacturer", paint.get("manufacturer", ""))
            record.setValue("range", paint.get("range", ""))
            record.setValue("hexvalue", paint.get("hexvalue", ""))
            record.setValue("notes", paint.get("notes", ""))
            self.models.paints_model.insertRecord(-1, record)
        self.models.paints_model.submitAll()
        logging.info("Loaded %s paints", len(paints))

    def load_latest_version(self, callback):
        """Load version from github repo"""
        url = "https://raw.githubusercontent.com/pkuehne/adjutant/main/adjutant/context/version.py"
        thread = UrlLoader(self, url)
        thread.content_loaded.connect(lambda text: callback(text.split("\n")))
        thread.finished.connect(thread.deleteLater)
        thread.start()
