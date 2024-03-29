""" PDF report for a Colour Scheme"""

from PyQt6.QtSql import QSqlRecord
from adjutant.reports.base_report import BaseReport, InputValues, format_paint
from adjutant.context import Context


class PaintingGuideReport(BaseReport):
    """Report for a painting guide"""

    def __init__(self, context: Context, inputs: InputValues) -> None:
        super().__init__(context, inputs)

        self.base_id = inputs.base_id
        self.scheme_id = self.context.models.bases_model.record_by_id(self.base_id).value(
            "schemes_id"
        )
        self.title = "Painting Guide Report - "
        self.steps = {}

    def prepare_recipe(self, recipe: QSqlRecord) -> dict:
        """Prepares the recipe in operation order"""
        retval = {}
        for row in range(self.context.models.recipe_steps_model.rowCount()):
            step = self.context.models.recipe_steps_model.record(row)
            if step.value("recipes_id") != recipe.value("id"):
                continue
            operations_id = step.value("operations_id")
            listvalue = retval.get(operations_id, [])
            listvalue.append(step.value("paints_id"))
            retval[operations_id] = listvalue

        return retval

    def prepare(self):
        """Prepare the report by loading all data and generating the document"""
        base = self.context.models.bases_model.record_by_id(self.base_id)
        self.title += base.value("name")

        for row in range(self.context.models.scheme_components_model.rowCount()):
            component = self.context.models.scheme_components_model.record(row)
            if component.value("schemes_id") != self.scheme_id:
                continue
            component_name = component.value("name")
            recipe = self.context.models.recipes_model.record_by_id(
                component.value("recipes_id")
            )

            self.steps[component_name] = self.prepare_recipe(recipe)

    def print_notes(self) -> str:
        """Print the notes section"""
        scheme = self.context.models.colour_schemes_model.record_by_id(self.scheme_id)
        notes = f"""
        <h2>Notes</h2>
        {scheme.value("notes")}
        """
        return notes

    def print_steps(self) -> str:
        """Print the individual operations in order"""
        steps = """
        
        """

        for row in range(self.context.models.step_operations_model.rowCount()):
            operation = self.context.models.step_operations_model.record(row)
            oper_id = operation.value("id")
            steps += f"<h2>{operation.value('name')}</h2>"
            for key, value in self.steps.items():
                if oper_id not in value:
                    continue
                paint_list = value[oper_id]
                if len(paint_list) > 1:
                    steps += f"<b>{key}</b><ol>"
                    for paint_id in paint_list:
                        paint = self.context.models.paints_model.record_by_id(paint_id)
                        steps += f"<li>{format_paint(paint)}</li>"

                    steps += "</ol>"
                else:
                    paint = self.context.models.paints_model.record_by_id(paint_list[0])
                    steps += f"<b>{key}</b> -> {format_paint(paint)}<br>"

        return steps

    def body(self) -> str:
        """Generates the content of the report"""
        body = ""
        body += self.print_notes()
        body += self.print_steps()
        # body += self.print_usage()
        # body += self.print_components()
        return body
