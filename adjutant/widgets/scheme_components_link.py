""" Widget encompassing management of colour scheme cmoponents"""

from PyQt6.QtCore import QModelIndex
from adjutant.context import Context
from adjutant.models.relational_model import RelationalModel
from adjutant.widgets.relational_link import RelationalLink


def stringify_component(index: QModelIndex) -> str:
    """Stringifies a step record"""
    model: RelationalModel = index.model()
    name = model.field_index(index.row(), "name").data()
    recipe = model.field_index(index.row(), "recipes_id").data()
    return f"{name} - {recipe}"


class SchemeComponentsLink(RelationalLink):
    """Colour Schemes Link Widget"""

    def __init__(self, context: Context, link_id: int, parent=None) -> None:
        super().__init__(context, link_id, parent)
        self.source_model = self.context.models.scheme_components_model
        self.link_field = "schemes_id"
        self.add_edit_dialog = "component"

        self.model.null_check_field = "recipes_id"
        self.model.set_string_func(stringify_component)

        self._setup()
