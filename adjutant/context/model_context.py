""" Context for models"""

from typing import List
from dataclasses import dataclass

from PyQt6.QtSql import QSqlQueryModel, QSqlTableModel
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from adjutant.models.bases_model import BasesModel
from adjutant.context.dataclasses import ManyToManyRelationship, OneToManyRelationship


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
        self.tags_sort_model = None
        self.base_tags_model = None
        self.searches_model = None
        self.storage_model = None
        self.statuses_model = None

    def load(self):
        """load the models from the database"""
        self.bases_model = self.__setup_bases_model()

        self.tags_model = self.__setup_tags_model()
        self.tags_sort_model = QSortFilterProxyModel()
        self.tags_sort_model.setSourceModel(self.tags_model)
        self.tags_sort_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.tags_sort_model.sort(
            self.tags_model.fieldIndex("name"), Qt.SortOrder.AscendingOrder
        )

        self.base_tags_model = QSqlTableModel()
        self.base_tags_model.setTable("bases_tags")
        self.base_tags_model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)

        self.searches_model = QSqlTableModel()
        self.searches_model.setTable("searches")
        self.searches_model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)

        self.storage_model = self._setup_storage_model()
        self.statuses_model = self._setup_statuses_model()

        self.refresh_models()

    def refresh_models(self) -> None:
        """Reselects rows on all models"""
        self.bases_model.select()
        self.tags_model.select()
        self.base_tags_model.select()
        self.searches_model.select()
        self.storage_model.select()
        self.statuses_model.select()

    def __setup_bases_model(self) -> BasesModel:
        """Initialize and setup the bases model"""
        model = BasesModel()
        model.setTable("bases")
        model.set_many_to_many_relationship(ManyToManyRelationship("tags", "name"))
        model.set_one_to_many_relationship(
            model.fieldIndex("storage_id"),
            OneToManyRelationship("storage", "id", "name"),
        )
        model.set_one_to_many_relationship(
            model.fieldIndex("status_id"),
            OneToManyRelationship("statuses", "id", "name"),
        )

        model.boolean_fields.append(model.fieldIndex("completed"))
        model.boolean_fields.append(model.fieldIndex("damaged"))
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
                HeaderRoles("Completed", "Whether this base is ready for games"),
                HeaderRoles("Damaged", "Is there any damage on this base?"),
                HeaderRoles("Notes", "General notes about this base"),
                HeaderRoles("Custom ID", "How you refer to this base"),
                HeaderRoles("Storage", "Where this base is kept"),
                HeaderRoles("Status", "What status this base is in"),
                HeaderRoles("Tags", "All tags associated with this base"),
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
            ],
        )
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        return model

    def _setup_storage_model(self) -> QSqlTableModel:
        """Setup the storage model"""
        model = QSqlTableModel()
        model.setTable("storage")
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        setup_header_data(
            model,
            [
                HeaderRoles("ID", "Internal ID of the storage container"),
                HeaderRoles("Name", "The name of the container"),
                HeaderRoles("Location", "Where the container is located"),
                HeaderRoles("Height", "How tall your mini can be at most"),
                HeaderRoles(
                    "Magnetized", "Whether this container will take magnetized minis"
                ),
                HeaderRoles("Full", "Whether there's space in this box or not"),
                HeaderRoles("Notes", "Notes about this storage location"),
            ],
        )
        return model

    def _setup_statuses_model(self) -> QSqlTableModel:
        """Setup the statuses model"""
        model = QSqlTableModel()
        model.setTable("statuses")
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        setup_header_data(model, [HeaderRoles("Name", "What this status represents")])
        return model
