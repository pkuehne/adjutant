""" PDF report for a Colour Scheme"""

from typing import List
from PyQt6.QtSql import QSqlRecord
from adjutant.reports.base_report import BaseReport, InputValues
from adjutant.context import Context


class ColourSchemeReport(BaseReport):
    """Report for a colour scheme"""

    def __init__(self, context: Context, inputs: InputValues) -> None:
        super().__init__(context, inputs)

        self.scheme_id = inputs.colour_scheme_id
        self.title = "Colour Scheme Report - "
        self.model = self.context.models.colour_schemes_model

    def prepare(self):
        """Prepare the report by loading all data and generating the document"""
        record = self.model.record_by_id(self.scheme_id)
        self.title += record.value("name")

    def print_colour_recipe(self, recipe: QSqlRecord) -> str:
        """Print a colour recipe"""
        retval = ""
        retval += recipe.value("notes")
        retval += "<ol>"
        steps: List[QSqlRecord] = []
        for row in range(self.context.models.recipe_steps_model.rowCount()):
            step = self.context.models.recipe_steps_model.record(row)
            if step.value("recipes_id") != recipe.value("id"):
                continue
            steps.append(step)
        steps.sort(key=lambda s: s.value("priority"))

        for step in steps:
            paint = self.context.models.paints_model.record_by_id(
                step.value("paints_id")
            )
            paint_name = paint.value("name")
            colour_box = f"<font color='{paint.value('hexvalue')}'>■</font>"
            oper = self.context.models.step_operations_model.record_by_id(
                step.value("operations_id")
            )
            oper_name = oper.value("name")
            retval += f"<li>{colour_box} {paint_name} ({oper_name})</li>"
        retval += "</ol>"
        return retval

    def print_usage(self) -> str:
        """Generates the usage section"""
        usage = """
        <h2>Usage</h2>
        """
        usage_map = {}
        for row in range(self.context.models.bases_model.rowCount()):
            base = self.context.models.bases_model.record(row)
            if base.value("schemes_id") != self.scheme_id:
                continue
            usage_map[base.value("name")] = usage_map.get(base.value("name"), 0) + 1

        usage += "<ul>"
        for key, count in usage_map.items():
            usage += f"<li>{count}x {key}</li>"
        usage += "</ul>"
        return usage

    def print_components(self) -> str:
        """Print the usage section"""
        components = """
        <h2>Components</h2>
        """
        for row in range(self.context.models.scheme_components_model.rowCount()):
            component = self.context.models.scheme_components_model.record(row)
            if component.value("schemes_id") != self.scheme_id:
                continue
            component_name = component.value("name")
            recipe = self.context.models.recipes_model.record_by_id(
                component.value("recipes_id")
            )
            recipe_name = recipe.value("name")
            components += f"<h3>{component_name} - {recipe_name}</h3>"
            components += self.print_colour_recipe(recipe)
        return components

    def print_notes(self) -> str:
        """Print the notes section"""
        scheme = self.model.record_by_id(self.scheme_id)
        notes = f"""
        <h2>Notes</h2>
        {scheme.value("notes")}
        """
        return notes

    def body(self) -> str:
        """Generates the content of the report"""
        body = ""
        body += self.print_notes()
        body += self.print_usage()
        body += self.print_components()
        return body
