""" Data context """

from typing import List

from dataclasses import dataclass

from PyQt6.QtSql import QSqlQueryModel, QSqlTableModel
from PyQt6.QtCore import QModelIndex, QObject, Qt, pyqtSignal

from adjutant.context.settings_context import SettingsContext
from adjutant.context.database_context import DatabaseContext


@dataclass
class HeaderRoles:
    """Stores data for the roles of a table header"""

    display: str
    tooltip: str


def setup_header_data(model: QSqlQueryModel, roles: List[HeaderRoles]):
    """Setup header data roles"""
    col = 0
    for role in roles:
        model.setHeaderData(
            col, Qt.Orientation.Horizontal, role.display, Qt.ItemDataRole.DisplayRole
        )
        model.setHeaderData(
            col, Qt.Orientation.Horizontal, role.tooltip, Qt.ItemDataRole.ToolTipRole
        )
        col += 1


class ModelContext:
    """Context for models"""

    def __init__(self):
        self.bases_model = None
        self.tags_model = None
        self.base_tags_model = None
        self.searches_model = None

    def load(self):
        """load the models from the database"""
        self.bases_model = self.__setup_bases_model()
        self.tags_model = self.__setup_tags_model()
        self.base_tags_model = QSqlTableModel()
        self.base_tags_model.setTable("base_tags")
        self.searches_model = QSqlTableModel()
        self.searches_model.setTable("searches")
        self.searches_model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)

        self.refresh_models()

    def refresh_models(self) -> None:
        """Reselects rows on all models"""
        self.bases_model.select()
        self.tags_model.select()
        self.base_tags_model.select()
        self.searches_model.select()

    def __setup_bases_model(self) -> QSqlTableModel:
        """Initialize and setup the bases model"""
        model = QSqlTableModel()
        model.setTable("bases")
        setup_header_data(
            model,
            [
                HeaderRoles("ID", "Unique ID for this base/model"),
                HeaderRoles("Name", "How you refer to this base"),
                HeaderRoles("Scale", "The miniature's scale (28mm, 1/72, etc)"),
                HeaderRoles("Base", "The style of base (square, round, etc)"),
                HeaderRoles("Width", "The width of the base looking at the front"),
                HeaderRoles("Depth", "The width of the base looking at the side"),
                HeaderRoles("Figures", "The number of miniatures on the base"),
                HeaderRoles("Material", "What the miniatures are made from"),
                HeaderRoles("Sculptor", "Who designed the miniatures"),
                HeaderRoles("Manufacturer", "The company who makes the miniatures"),
                HeaderRoles("Retailer", "Where the miniatures were bought"),
                HeaderRoles("Price", "How much this base cost"),
                HeaderRoles("Added", "When this base was added to Adjutant"),
                HeaderRoles("Acquired", "When the miniatures in this base were bought"),
                HeaderRoles("Finished", "When the work on this base was completed"),
                HeaderRoles("Completed", "Whether this base is ready for games"),
                HeaderRoles("Damaged", "Is there any damage on this base?"),
                HeaderRoles("Notes", "General notes about this base"),
                HeaderRoles("Custom ID", "How you refer to this base"),
                HeaderRoles("Storage", "Where this base is kept"),
                # HeaderRoles("Tags", "All tags associated with this base"),
            ],
        )
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        return model

    def __setup_tags_model(self) -> QSqlTableModel:
        """Set up the tags model"""
        model = QSqlTableModel()
        model.setTable("tags")
        setup_header_data(
            model,
            [
                HeaderRoles("ID", "Internal ID of the tag"),
                HeaderRoles("Name", "The name of the tag"),
                HeaderRoles("Category", "Which category the tag belongs to"),
                HeaderRoles("Custom", "Whether this tag was defined by you"),
            ],
        )
        return model


class SignalContext(QObject):
    """Collects all pan-application signals"""

    edit_base = pyqtSignal(QModelIndex)
    add_base = pyqtSignal()
    delete_base = pyqtSignal(QModelIndex)
    delete_bases = pyqtSignal(list)
    duplicate_base = pyqtSignal(QModelIndex, int)
    update_bases = pyqtSignal()

    save_search = pyqtSignal()
    load_search = pyqtSignal(int)
    apply_filter = pyqtSignal(int, object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)


class Context:
    """Data Context"""

    def __init__(self) -> None:
        self.settings = SettingsContext()
        self.signals = SignalContext()
        self.database = DatabaseContext()
        self.models = ModelContext()

    def load_database(self, filename: str) -> None:
        """Load a database file"""
        self.database.open_database(filename)
        self.database.migrate(self.settings)
        self.models.load()
