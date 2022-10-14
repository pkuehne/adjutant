""" Base class for all PDF reports"""

from dataclasses import dataclass
from PyQt6 import QtGui
from PyQt6 import QtPrintSupport
from PyQt6.QtCore import QMarginsF
from PyQt6.QtSql import QSqlRecord
from PyQt6.QtWidgets import QDialog

from adjutant.context.context import Context

@dataclass
class InputValues:
    """Values that can be passed to reports"""
    colour_scheme_id: str = None
    base_id: str = None

def format_paint(paint: QSqlRecord) -> str:
    """Formats a colour"""
    paint_name = paint.value("name")
    hexvalue = paint.value("hexvalue")
    colour_box = f"<font color='{hexvalue}'>■</font>"
    return f"{colour_box} {paint_name}"


class BaseReport:
    """Base class providing utility and abstraction"""

    def __init__(self, context: Context, inputs: InputValues) -> None:
        self.title = "Unnamed Report"
        self.context = context
        self.inputs = inputs

    def style(self) -> str:
        """The style to use in the header"""
        return """
            body {
                width: 21cm;
                height: 29.7cm;
                margin: 2mm;
                }
            #title {
                text-align:center
            }
            table,
            th,
            td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th,
            td {
                padding: 15px;
                vertical-align: center;
            }
            .page-break { page-break-before: always;}
        """

    def body(self) -> str:
        """Overridable generator for the body of the report"""
        return "Empty Report"

    def document(self) -> str:
        """Generates the wrapper html for the printer"""
        return f"""
            <html>
                <head>
                    <style>
                        {self.style()}
                    </style>
                </head>
            <body>
                <h1 id="title">Adjutant {self.title}</h1><br>
                {self.body()}
            </body>
        </html>
        """

    def generate(self):
        """Generates the actual Report"""
        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageOrientation(QtGui.QPageLayout.Orientation.Portrait)
        printer.setPageMargins(QMarginsF(2, 2, 2, 2), QtGui.QPageLayout.Unit.Millimeter)
        printer.setPageSize(QtGui.QPageSize(QtGui.QPageSize.PageSizeId.A4))
        dialog = QtPrintSupport.QPrintDialog(printer)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        html = self.document()
        # print(html)

        document = QtGui.QTextDocument()
        document.setHtml(html)
        document.print(printer)
