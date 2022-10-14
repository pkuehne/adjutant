""" Window to display reports in"""

from dataclasses import dataclass
from typing import List
from PyQt6.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QFormLayout,
    QFileDialog,
    # QSizePolicy
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QGuiApplication
from adjutant.context import Context
from adjutant.reports import ColourSchemeReport, PaintingGuideReport, BaseReport
from adjutant.models.row_zero_filter_model import RowZeroFilterModel
from adjutant.reports.base_report import InputValues

PLACEHOLDER_HTML = """
<html>
    Please select a report to generate
</html>
"""


@dataclass
class Report:
    """Report"""

    title: str
    report_type: BaseReport
    input_widgets: List[QComboBox]


class ReportWindow(QDialog):
    """Dialog to see reports"""

    @dataclass
    class Widgets:
        """Widgets for the dialog"""

        close_button: QPushButton
        generate_button: QPushButton
        export_button: QPushButton
        web_view: QWebEngineView
        report_list: QComboBox
        schemes_list: QComboBox
        bases_list: QComboBox

    def __init__(self, context: Context) -> None:
        super().__init__(None)
        self.context = context

        self.widgets = self.Widgets(
            QPushButton(self.tr("Close")),
            QPushButton(self.tr("Generate")),
            QPushButton(self.tr("Export PDF")),
            QWebEngineView(),
            QComboBox(),
            QComboBox(),
            QComboBox(),
        )
        self.reports = [
            Report("Colour Scheme", ColourSchemeReport, [self.widgets.schemes_list]),
            Report("Painting Guide", PaintingGuideReport, [self.widgets.bases_list]),
        ]
        self.inputs_layout = QFormLayout()

        self.setFixedSize(QGuiApplication.primaryScreen().availableSize() * 0.5)
        self.setWindowTitle("Adjutant Reports")
        self._setup_layout()
        self._setup_widgets()
        self._setup_signals()


    def _setup_layout(self):
        """"""

        selector_layout = QFormLayout()
        selector_layout.addRow("Report", self.widgets.report_list)

        self.inputs_layout.addRow("Colour Scheme", self.widgets.schemes_list)
        self.inputs_layout.addRow("Base", self.widgets.bases_list)

        generate_layout = QVBoxLayout()
        generate_layout.addWidget(self.widgets.generate_button)

        top_layout = QHBoxLayout()
        top_layout.addLayout(selector_layout)
        top_layout.addLayout(self.inputs_layout)
        top_layout.addLayout(generate_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.widgets.export_button)
        button_layout.addStretch()
        button_layout.addWidget(self.widgets.close_button)

        central = QVBoxLayout()
        central.addLayout(top_layout)
        central.addWidget(self.widgets.web_view)
        central.addLayout(button_layout)
        self.setLayout(central)

    def _setup_widgets(self):
        """"""
        self.widgets.web_view.setHtml(PLACEHOLDER_HTML)
        for index, report in enumerate(self.reports):
            self.widgets.report_list.insertItem(index, report.title)
        filter_model = RowZeroFilterModel()
        filter_model.setSourceModel(self.context.models.colour_schemes_model)
        self.widgets.schemes_list.setModel(filter_model)
        self.widgets.schemes_list.setModelColumn(1)

        self.widgets.bases_list.setModel(self.context.models.bases_model)
        self.widgets.bases_list.setModelColumn(1)

        self.update_inputs(self.widgets.report_list.currentIndex())
        self.widgets.export_button.setEnabled(False)

    def _setup_signals(self):
        """"""
        self.widgets.close_button.pressed.connect(self.reject)
        self.widgets.generate_button.pressed.connect(self.generate_report)
        self.widgets.report_list.currentIndexChanged.connect(self.update_inputs)
        self.widgets.export_button.pressed.connect(self.export_pdf)

    def generate_report(self):
        """ Generates the selected reprot and puts it into the window """
        report = self.reports[self.widgets.report_list.currentIndex()]

        row = self.widgets.schemes_list.currentIndex()
        scheme_id = self.widgets.schemes_list.model().index(row, 0).data()
        row = self.widgets.bases_list.currentIndex()
        base_id = self.widgets.bases_list.model().index(row, 0).data()

        values = InputValues(scheme_id, base_id)
        generator = report.report_type(self.context, values)
        generator.prepare()

        self.widgets.web_view.setHtml(generator.document())
        self.widgets.export_button.setEnabled(True)

    def export_pdf(self):
        """Exports a PDF of the report """
        filename = QFileDialog.getSaveFileName(
                self, "Export data", filter=self.tr("PDF File (*.pdf)")
            )[0]
        if filename == "":
            return

        self.widgets.web_view.printToPdf(filename)

    def update_inputs(self, index):
        """ Update the input selections based on current report"""
        report = self.reports[index]
        for combo in [self.widgets.schemes_list, self.widgets.bases_list]:
            self.inputs_layout.setRowVisible(combo, False)
        for combo in report.input_widgets:
            self.inputs_layout.setRowVisible(combo, True)


    @classmethod
    def show(cls, context):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
