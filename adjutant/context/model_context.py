""" Context for models"""

from typing import List
from dataclasses import dataclass

from PyQt6.QtCore import QSortFilterProxyModel, Qt
from adjutant.models.bases_model import BasesModel
from adjutant.context.dataclasses import ManyToManyRelationship, OneToManyRelationship
from adjutant.models.relational_model import RelationalModel


@dataclass
class HeaderRoles:
    """Stores data for the roles of a table header"""

    display: str
    tooltip: str


def setup_header_data(model: RelationalModel, roles: List[HeaderRoles]):
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
        self.settings_model = None
        self.bases_model = None
        self.tags_model = None
        self.tags_sort_model = None
        self.base_tags_model = None
        self.searches_model = None
        self.storage_model = None
        self.statuses_model = None
        self.paints_model = None
        self.recipes_model = None
        self.recipe_steps_model = None
        self.step_operations_model = None
        self.colour_schemes_model = None
        self.scheme_components_model = None

    def load(self):
        """load the models from the database"""
        self._setup_settings_model()

        self.bases_model = self.__setup_bases_model()

        self.tags_model = self.__setup_tags_model()
        self.tags_sort_model = QSortFilterProxyModel()
        self.tags_sort_model.setSourceModel(self.tags_model)
        self.tags_sort_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.tags_sort_model.sort(
            self.tags_model.fieldIndex("name"), Qt.SortOrder.AscendingOrder
        )

        self.base_tags_model = RelationalModel()
        self.base_tags_model.setTable("bases_tags")
        self.base_tags_model.setEditStrategy(
            RelationalModel.EditStrategy.OnManualSubmit
        )

        self.searches_model = RelationalModel()
        self.searches_model.setTable("searches")
        self.searches_model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)

        self.storage_model = self._setup_storage_model()
        self.statuses_model = self._setup_statuses_model()

        self._setup_searches_model()
        self._setup_paints_model()
        self._setup_recipes_model()
        self._setup_recipe_steps_model()
        self._setup_step_operations_model()
        self._setup_colour_schemes_model()
        self._setup_scheme_components_model()

        self.refresh_models()

    def refresh_models(self) -> None:
        """Reselects rows on all models"""
        self.settings_model.select()
        self.bases_model.select()
        self.tags_model.select()
        self.base_tags_model.select()
        self.searches_model.select()
        self.storage_model.select()
        self.statuses_model.select()
        self.paints_model.select()
        self.recipes_model.select()
        self.recipe_steps_model.select()
        self.step_operations_model.select()
        self.colour_schemes_model.select()
        self.scheme_components_model.select()

    def _setup_settings_model(self) -> None:
        """Load settings model"""
        self.settings_model = RelationalModel()
        self.settings_model.setTable("settings")
        self.settings_model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)

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
        model.set_one_to_many_relationship(
            model.fieldIndex("schemes_id"),
            OneToManyRelationship("colour_schemes", "id", "name"),
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
                HeaderRoles("Colour Scheme", "The colour scheme for this mini"),
                HeaderRoles("Tags", "All tags associated with this base"),
            ],
        )
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        return model

    def __setup_tags_model(self) -> RelationalModel:
        """Set up the tags model"""
        model = RelationalModel()
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

    def _setup_searches_model(self) -> RelationalModel:
        """Setup the Searches Model"""
        self.searches_model = RelationalModel()
        self.searches_model.setTable("searches")
        self.searches_model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)

    def _setup_storage_model(self) -> RelationalModel:
        """Setup the storage model"""
        model = RelationalModel()
        model.setTable("storage")
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)

        model.boolean_fields.append(model.fieldIndex("magnetized"))
        model.boolean_fields.append(model.fieldIndex("full"))

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

    def _setup_statuses_model(self) -> RelationalModel:
        """Setup the statuses model"""
        model = RelationalModel()
        model.setTable("statuses")
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        setup_header_data(model, [HeaderRoles("Name", "What this status represents")])
        return model

    def _setup_paints_model(self) -> None:
        """Setup the paints models"""
        self.paints_model = RelationalModel()
        self.paints_model.setTable("paints")
        self.paints_model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)
        self.paints_model.colour_fields.append(self.paints_model.fieldIndex("hexvalue"))
        setup_header_data(
            self.paints_model,
            [
                HeaderRoles("ID", "The internal ID of the paint"),
                HeaderRoles("Name", "The name of this paint"),
                HeaderRoles(
                    "Manufacturer",
                    "The manufacturer of this paint (Citadel, Vallejo, etc)",
                ),
                HeaderRoles("Range", "What group this is (e.g. Layer, Model Air, etc)"),
                HeaderRoles(
                    "Hex Value", "The RGB values of this paint in hexadecimal notation"
                ),
                HeaderRoles("Notes", "General notes about this paint"),
            ],
        )

    def _setup_recipes_model(self) -> None:
        """Setup the recipes model"""
        self.recipes_model = RelationalModel()
        self.recipes_model.setTable("recipes")
        self.recipes_model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)
        setup_header_data(
            self.recipes_model,
            [
                HeaderRoles("ID", "Internal ID of the recipe"),
                HeaderRoles("Name", "The name for this colour recipe"),
                HeaderRoles("Notes", "General notes about this recipe"),
            ],
        )

    def _setup_recipe_steps_model(self) -> None:
        """Setup the recipe steps model"""
        self.recipe_steps_model = RelationalModel()
        self.recipe_steps_model.setTable("recipe_steps")
        self.recipe_steps_model.setEditStrategy(
            RelationalModel.EditStrategy.OnManualSubmit
        )

        self.recipe_steps_model.set_one_to_many_relationship(
            self.recipe_steps_model.fieldIndex("recipes_id"),
            OneToManyRelationship("recipes", "id", "name"),
        )

        self.recipe_steps_model.set_one_to_many_relationship(
            self.recipe_steps_model.fieldIndex("paints_id"),
            OneToManyRelationship("paints", "id", "name"),
        )
        self.recipe_steps_model.set_one_to_many_relationship(
            self.recipe_steps_model.fieldIndex("operations_id"),
            OneToManyRelationship("step_operations", "id", "name"),
        )
        setup_header_data(
            self.recipe_steps_model,
            [
                HeaderRoles("ID", "The internal ID of this recipe step"),
                HeaderRoles("Recipe", "The recipe this step belongs to"),
                HeaderRoles("Paint", "The paint to apply at this step"),
                HeaderRoles("Operation", "How to apply the paint"),
                HeaderRoles("Number", "Which step number this step is"),
            ],
        )

    def _setup_step_operations_model(self) -> None:
        """Setup the steps operation model"""
        self.step_operations_model = RelationalModel()
        self.step_operations_model.setTable("step_operations")
        self.step_operations_model.setEditStrategy(
            RelationalModel.EditStrategy.OnManualSubmit
        )
        setup_header_data(
            self.step_operations_model,
            [
                HeaderRoles("ID", "Internal ID of the operation"),
                HeaderRoles("Name", "The descriptive name for this operation"),
            ],
        )

    def _setup_colour_schemes_model(self) -> None:
        """Setup the colour schemes"""
        self.colour_schemes_model = RelationalModel()
        self.colour_schemes_model.setTable("colour_schemes")
        self.colour_schemes_model.setEditStrategy(
            RelationalModel.EditStrategy.OnManualSubmit
        )
        setup_header_data(
            self.colour_schemes_model,
            [
                HeaderRoles("ID", "Internal ID of the colour scheme"),
                HeaderRoles("Name", "The name for this colour scheme"),
                HeaderRoles("Notes", "General notes about this colour scheme"),
            ],
        )

    def _setup_scheme_components_model(self) -> None:
        """Setup the colour schemes"""
        self.scheme_components_model = RelationalModel()
        self.scheme_components_model.setTable("scheme_components")
        self.scheme_components_model.setEditStrategy(
            RelationalModel.EditStrategy.OnManualSubmit
        )
        self.scheme_components_model.set_one_to_many_relationship(
            self.scheme_components_model.fieldIndex("recipes_id"),
            OneToManyRelationship("recipes", "id", "name"),
        )
