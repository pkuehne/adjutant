""" Context for models"""

from typing import Dict, List
from dataclasses import dataclass

from PyQt6.QtCore import QSortFilterProxyModel, Qt
from adjutant.models.bases_model import BasesModel
from adjutant.context.dataclasses import ManyToManyRelationship, OneToManyRelationship
from adjutant.models.relational_model import RelationalModel


@dataclass
class HeaderData:
    """Stores data for the roles of a table header"""

    display: str
    tooltip: str


def setup_header_data(model: RelationalModel, roles: List[HeaderData]):
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
        self.models: Dict[str, RelationalModel] = {}
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

    def get(self, name: str) -> RelationalModel:
        """get a model by name"""
        return self.models.get(name, None)

    def setup_model(
        self, name: str, headers: List[HeaderData] = None
    ) -> RelationalModel:
        """Setup a model"""
        model = RelationalModel()
        model.setTable(name)
        model.setEditStrategy(RelationalModel.EditStrategy.OnManualSubmit)
        setup_header_data(model, headers if headers else [])

        self.models[name] = model
        model.select()

        return model

    def load(self):
        """load the models from the database"""

        self._setup_bases_model()
        self._setup_bases_tags_model()
        self._setup_colour_schemes_model()
        self._setup_paints_model()
        self._setup_recipe_steps_model()
        self._setup_recipes_model()
        self._setup_scheme_components_model()
        self._setup_searches_model()
        self._setup_settings_model()
        self._setup_step_operations_model()
        self._setup_statuses_model()
        self._setup_storage_model()
        self._setup_tags_model()

        self.tags_sort_model = QSortFilterProxyModel()
        self.tags_sort_model.setSourceModel(self.tags_model)
        self.tags_sort_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.tags_sort_model.sort(
            self.tags_model.fieldIndex("name"), Qt.SortOrder.AscendingOrder
        )

    def refresh_models(self) -> None:
        """Reselects rows on all models"""
        for model in self.models.values():
            model.select()

    def _setup_settings_model(self) -> None:
        """Load settings model"""
        self.settings_model = self.setup_model("settings")

    def _setup_bases_model(self) -> BasesModel:
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
                HeaderData("ID", "Unique ID for this base/model"),
                HeaderData("Name", "How you refer to this base"),
                HeaderData("Scale", "The miniature's scale (28mm, 1/72, etc)"),
                HeaderData("Base", "The style of base (square, round, etc)"),
                HeaderData("Width", "The width of the base looking at the front"),
                HeaderData("Depth", "The width of the base looking at the side"),
                HeaderData("Figures", "The number of miniatures on the base"),
                HeaderData("Material", "What the miniatures are made from"),
                HeaderData("Sculptor", "Who designed the miniatures"),
                HeaderData("Manufacturer", "The company who makes the miniatures"),
                HeaderData("Pack Code", "The code used by the retailer/manufacturer"),
                HeaderData("Retailer", "Where the miniatures were bought"),
                HeaderData("Price", "How much this base cost"),
                HeaderData("Added", "When this base was added to Adjutant"),
                HeaderData("Acquired", "When the miniatures in this base were bought"),
                HeaderData("Completed", "Whether this base is ready for games"),
                HeaderData("Damaged", "Is there any damage on this base?"),
                HeaderData("Notes", "General notes about this base"),
                HeaderData("Custom ID", "How you refer to this base"),
                HeaderData("Storage", "Where this base is kept"),
                HeaderData("Status", "What status this base is in"),
                HeaderData("Colour Scheme", "The colour scheme for this mini"),
                HeaderData("Tags", "All tags associated with this base"),
            ],
        )
        model.setEditStrategy(model.EditStrategy.OnManualSubmit)
        model.select()
        self.bases_model = model
        self.models["bases"] = model
        return model

    def _setup_tags_model(self) -> None:
        """Set up the tags model"""
        self.tags_model = self.setup_model(
            "tags",
            [
                HeaderData("ID", "Internal ID of the tag"),
                HeaderData("Name", "The name of the tag"),
            ],
        )

    def _setup_bases_tags_model(self) -> None:
        """Setup the bases_tags model"""
        self.base_tags_model = self.setup_model("bases_tags")

    def _setup_searches_model(self) -> None:
        """Setup the Searches Model"""
        self.searches_model = self.setup_model("searches")

    def _setup_storage_model(self) -> None:
        """Setup the storage model"""
        self.storage_model = self.setup_model(
            "storage",
            [
                HeaderData("ID", "Internal ID of the storage container"),
                HeaderData("Name", "The name of the container"),
                HeaderData("Location", "Where the container is located"),
                HeaderData("Height", "How tall your mini can be at most"),
                HeaderData(
                    "Magnetized", "Whether this container will take magnetized minis"
                ),
                HeaderData("Full", "Whether there's space in this box or not"),
                HeaderData("Notes", "Notes about this storage location"),
            ],
        )

        self.storage_model.boolean_fields.append(
            self.storage_model.fieldIndex("magnetized")
        )
        self.storage_model.boolean_fields.append(self.storage_model.fieldIndex("full"))

    def _setup_statuses_model(self) -> None:
        """Setup the statuses model"""
        self.statuses_model = self.setup_model(
            "statuses", [HeaderData("Name", "What this status represents")]
        )

    def _setup_paints_model(self) -> None:
        """Setup the paints models"""
        self.paints_model = self.setup_model(
            "paints",
            [
                HeaderData("ID", "The internal ID of the paint"),
                HeaderData("Name", "The name of this paint"),
                HeaderData(
                    "Manufacturer",
                    "The manufacturer of this paint (Citadel, Vallejo, etc)",
                ),
                HeaderData("Range", "What group this is (e.g. Layer, Model Air, etc)"),
                HeaderData(
                    "Hex Value", "The RGB values of this paint in hexadecimal notation"
                ),
                HeaderData("Notes", "General notes about this paint"),
            ],
        )
        self.paints_model.colour_fields.append(self.paints_model.fieldIndex("hexvalue"))

    def _setup_recipes_model(self) -> None:
        """Setup the recipes model"""
        self.recipes_model = self.setup_model(
            "recipes",
            [
                HeaderData("ID", "Internal ID of the recipe"),
                HeaderData("Name", "The name for this colour recipe"),
                HeaderData("Notes", "General notes about this recipe"),
            ],
        )

    def _setup_recipe_steps_model(self) -> None:
        """Setup the recipe steps model"""
        self.recipe_steps_model = self.setup_model(
            "recipe_steps",
            [
                HeaderData("ID", "The internal ID of this recipe step"),
                HeaderData("Recipe", "The recipe this step belongs to"),
                HeaderData("Paint", "The paint to apply at this step"),
                HeaderData("Operation", "How to apply the paint"),
                HeaderData("Priority", "Which order this step appears in"),
            ],
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

    def _setup_step_operations_model(self) -> None:
        """Setup the steps operation model"""
        self.step_operations_model = self.setup_model(
            "step_operations",
            [
                HeaderData("ID", "Internal ID of the operation"),
                HeaderData("Name", "The descriptive name for this operation"),
            ],
        )

    def _setup_colour_schemes_model(self) -> None:
        """Setup the colour schemes"""
        self.colour_schemes_model = self.setup_model(
            "colour_schemes",
            [
                HeaderData("ID", "Internal ID of the colour scheme"),
                HeaderData("Name", "The name for this colour scheme"),
                HeaderData("Notes", "General notes about this colour scheme"),
            ],
        )

    def _setup_scheme_components_model(self) -> None:
        """Setup the colour schemes"""
        self.scheme_components_model = self.setup_model("scheme_components")
        self.scheme_components_model.set_one_to_many_relationship(
            self.scheme_components_model.fieldIndex("recipes_id"),
            OneToManyRelationship("recipes", "id", "name"),
        )
