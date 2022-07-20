""" Widget encompassing management of recipe steps"""

from PyQt6.QtCore import QModelIndex
from adjutant.context import Context
from adjutant.models.relational_model import RelationalModel
from adjutant.widgets.relational_link import RelationalLink


def stringify_step(index: QModelIndex) -> str:
    """Stringifies a step record"""
    model: RelationalModel = index.model()
    paint = model.field_index(index.row(), "paints_id").data()
    operation = model.field_index(index.row(), "operations_id").data()
    return f"{operation} - {paint}"


class RecipeStepsLink(RelationalLink):
    """Recipe Steps Widget"""

    def __init__(self, context: Context, link_id: str, parent=None) -> None:
        super().__init__(context, link_id, parent)
        self.source_model = self.context.models.recipe_steps_model
        self.link_field = "recipes_id"
        self.add_edit_dialog = "step"
        self.allow_reordering = True
        self.model.null_check_field = "operations_id"
        self.model.set_string_func(stringify_step)

        self._setup()
